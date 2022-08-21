import paramiko
import time
import socket
from datetime import datetime, timezone
import rich
import threading
from rich.progress import SpinnerColumn, Progress, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn, TimeElapsedColumn
from rich.live import Live
import tabulate
import textwrap
import re

tabulate.tabulate.WIDE_CHARS_MODE = False


class SSH_Authentication():

    hosts_dct = {
        "hosts": {},
        "total": {}
    }

    def __init__(self, debug=False):
        # self.devices_dct = {}
        # self.connected_devices_dct = {}
        self.vendor = None # should be updated in the exec method.

        self.connection_failed_devices_number = 0
        self.connected_devices_number = 0

        self.debug = debug

        self.hosts_dct = {
            "hosts": {},
            "total": {}
        }

        self.threads = []

    def authenticate_hosts(self, hosts, group_name, user, password, privileged_mode_password="", port=22, terminal_print=False, timeout=5, max_tries=3, debug=False):
        """
        Authenticate list of hosts (network devices)
            - The authentication is done In Prarallel using Threading
            - Prints a progress bar
            - Prints a report table at the end
        INPUT:
            1. hosts (list / dct) List of hosts to authenticate
            2. group_name (str) group name to print
            3. user (str)
            4. password (str)
            5. port (int)
            6. terminal_print (bool) whether to print output to the terminal or not.
            7. timeout (int) SSH timeout
            8. max_tries (int) How many times to try to authenticatoin (in case the host fails the authenticate)
        """
        try:

            if len(hosts) < 1:
                print("INFO -- no hosts to authenticate")
                exit(1)

            time_start = datetime.now()
            # Start a thread for each host
            for host in hosts:
                thread  = threading.Thread(target=self.connect, args=(host, user, password, privileged_mode_password, port, timeout, max_tries))
                thread.daemon = True
                self.threads.append(thread)
                thread.start()

            if terminal_print:
                # print("> Authenticating selected devices")
                
                # Progress for updating Rates bar
                authentication_progress = Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    BarColumn(),
                    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                    TextColumn("{task.fields[status]}"),
                )

                task_authentication_progress = authentication_progress.add_task(
                    description=f"[bold]Authenticating Group: [ {group_name} ]",
                    status=f"[ 0 / {len(hosts)} ] ",
                    total=len(hosts)
                    )

            with Live(authentication_progress, auto_refresh=True, screen=False):

                if self.debug:
                    rich.print(f"DEBUG: start of authentication")
                    rich.print(self.hosts_dct)

                while self.hosts_dct['total']['n_tasks_finished'] <= len(host):
                    time_end = datetime.now()
                    time_taken = time_end - time_start
                    # Update progress bar
                    authentication_progress.update(task_id=task_authentication_progress, completed=self.hosts_dct['total']['n_tasks_finished'], status=f" HOSTS: [ {self.hosts_dct['total']['n_tasks_finished']} / {len(hosts)} ]   TIMEOUT: [ {time_taken.seconds} / {2 + (max_tries * timeout)} sec ] ")
                    if self.hosts_dct['total']['n_tasks_finished'] == len(hosts):
                        if self.debug:
                            rich.print(f"DEBUG: end of authentication")
                            rich.print(self.hosts_dct)
                        break
                    time.sleep(1)

            SSH_Authentication.hosts_dct = self.hosts_dct
            return self.hosts_dct
        except (KeyboardInterrupt) as e:
            rich.print("[bright_green]OK !")
            exit(1)

    def is_channel_closed(self, channel):
        """
        Check if the [pre opened] channel is closed  (True if closed, False if active)
        INPUT:
            1. channel (object) The ssh channel object
        """
        # Check if the channel is None (means not opened before)
        if channel is None:
            return True

        # Check if explicitly the channel is closed
        if channel.closed:
            return True

        try:
            channel.send("\n")
            time.sleep(0.1)
            if not channel.recv_ready():
                return True
            transport = channel.get_transport()
            if not transport.is_active():
                return True
            if channel is None:
                # return True
                rich.print(f"ERROR -- The channel was NOT opened before !\n > Need to handle this.")
                exit(1)
        except (paramiko.SSHException, socket.error) as e:
            rich.print(f"ERROR -- Something went wrong !\n> [bright_red]{e}[/bright_red]")
            exit(1)
        
                
        return False

    def reconnect(self, host):
        """
        Re-authenticate a network device (that was already authenticated)
        """
        rich.print(f"\n🟡 Closed Socket detected @{host}\n   [grey42]Trying to reconnect ...")

        time_start = datetime.now()
        # Try to re-connect and get a new dct for the host
        new_host_dct = self.connect(host, self.hosts_dct['hosts'][host]['user'], self.hosts_dct['hosts'][host]['password'], self.hosts_dct['hosts'][host]['privileged_mode_password'], self.hosts_dct['hosts'][host]['port'], self.hosts_dct['hosts'][host]['timeout'], self.hosts_dct['hosts'][host]['tries'])
        # Update the host dct
        self.hosts_dct['hosts'][host] = new_host_dct

        time_end = datetime.now()
        time_taken = time_end - time_start

        if self.hosts_dct['hosts'][host]['is_connected']:
            self.hosts_dct['hosts'][host]['is_reconnected'] = True
            self.hosts_dct['hosts'][host]['reconnection_time'] = datetime.now((timezone.utc)).strftime("%Y-%m-%d %H:%M:%S")
            self.hosts_dct['hosts'][host]['privileged_mode'] = False

        if new_host_dct['task_finished']:
            if new_host_dct['is_reconnected']:
                rich.print(f"🟢 Reconnected successfully to {host}")
                print(self.connection_report_Table({host: self.hosts_dct['hosts'][host]}))
                print("INFO -- Entering privileged mode")
            else:
                rich.print(f"🔴 FAILED to reconnect to {host}")
                # In case I want to print a table
                print(self.connection_report_Table({host: self.hosts_dct['hosts'][host]}))
                # rich.print("print markdown here.")

            if self.debug:
                rich.print(f"\nDEBUG: Reconneting host: {host} [underline]result:")
                rich.print(self.hosts_dct['hosts'][host])



    def connect(self, host, user, password, privileged_mode_password="", port=22, timeout=5, max_tries=3, allow_agent=True):
        """
        Authenticate a network device
        """

        # Creaet a nested dct for the host
        self.hosts_dct['hosts'][host] = {
            "host": host,
            "user": user,
            "password": password,
            "privileged_mode_password": privileged_mode_password,
            "port": port,
            "timeout": timeout,
            "max_tries": max_tries,

            # Will be updated during authentication
            "fail_reason": "",
            "ssh": None,
            "channel": None,
            "is_connected": False,
            # "time_to_connect_seconds": 0,
            "time_taken": 0,
            "tries": 1,
            "task_finished": False,

            "is_reconnected": False,
            "connection_time": "",
            "reconnection_time": "",
            'privileged_mode': False
        }

        # Flag to track how many hosts finished
        self.hosts_dct['total']['n_tasks_finished'] = 0
        self.hosts_dct['total']['n_hosts_total'] = 0
        self.hosts_dct['total']['n_hosts_connected'] = 0
        self.hosts_dct['total']['n_hosts_failed'] = 0
        
        # Note time to calculate time taken at the end
        time_start = datetime.now()

        while  (self.hosts_dct['hosts'][host]['tries'] <= max_tries):
            try:
                # Create an ssh client
                self.hosts_dct['hosts'][host]['ssh'] = paramiko.SSHClient()
                
                self.hosts_dct['hosts'][host]['ssh'].set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.hosts_dct['hosts'][host]['ssh'].connect(host, port, user, password, timeout=timeout,
                                    allow_agent=allow_agent, look_for_keys=False)
                self.hosts_dct['hosts'][host]['channel'] = self.hosts_dct['hosts'][host]['ssh'].invoke_shell()

                self.hosts_dct['hosts'][host]['is_connected'] = True
                self.hosts_dct['hosts'][host]['fail_reason'] = ""

                output = self.hosts_dct['hosts'][host]['channel'].recv(9999)
                self.hosts_dct['hosts'][host]['channel'].send_ready()
                time.sleep(1)
                self.hosts_dct['hosts'][host]['task_finished'] = True
                break
            except paramiko.AuthenticationException as e:
                self.hosts_dct['hosts'][host]['is_connected'] = False
                self.hosts_dct['hosts'][host]['fail_reason'] = f"Authentication failed >> {e}"
                self.hosts_dct['hosts'][host]['task_finished'] = True
                break
            except socket.gaierror as e:
                self.hosts_dct['hosts'][host]['is_connected'] = False
                self.hosts_dct['hosts'][host]['fail_reason'] = "Could NOT resolve hostname {} Name or service not known >> {}".format(host, e)
                self.hosts_dct['hosts'][host]['task_finished'] = True
                break
            except (ConnectionResetError, paramiko.ssh_exception.SSHException) as e:
                self.hosts_dct['hosts'][host]['is_connected'] = False
                self.hosts_dct['hosts'][host]['fail_reason'] = f"Connection reset by peer >> {host, e}"
                # Do NOT work as expected
                # https://github.com/napalm-automation/napalm/issues/963
                # Raises Exceptions when setting the port to 111
                self.hosts_dct['hosts'][host]['task_finished'] = True
                break
            except (paramiko.ssh_exception.NoValidConnectionsError, paramiko.SSHException, socket.error)  as e:
                self.hosts_dct['hosts'][host]['is_connected'] = False
                time.sleep(0.4)
                self.hosts_dct['hosts'][host]['fail_reason'] = "NOT able to establish an ssh connection with {} on port {} >> {}".format(host, port, e)
                if self.hosts_dct['hosts'][host]['tries'] == max_tries:
                    self.hosts_dct['hosts'][host]['task_finished'] = True
                    break
            self.hosts_dct['hosts'][host]['tries'] += 1
        
        time_end = datetime.now()
        time_taken = time_end - time_start
        self.hosts_dct['hosts'][host]['time_taken'] = time_taken.seconds

        if self.hosts_dct['hosts'][host]['task_finished']:
            self.hosts_dct['total']['n_tasks_finished'] +=1
            self.hosts_dct['total']['n_hosts_total'] +=1
        if self.hosts_dct['hosts'][host]['is_connected']:
            self.hosts_dct['total']['n_hosts_connected'] +=1
            self.hosts_dct['hosts'][host]['connection_time'] = datetime.now((timezone.utc)).strftime("%Y-%m-%d %H:%M:%S")
        else:
            self.hosts_dct['total']['n_hosts_failed'] +=1

        return self.hosts_dct['hosts'][host]

    def close(self, host, terminal_print=True):
        """
        Close the SSH connection with a network device
        INPUT:
            1. host_dct (dct) the host dictionary that contains host details
            2. terminal_print (bool) whether to print INFO to the terminal
        """
        if self.hosts_dct['hosts'][host]['is_connected']:
            self.hosts_dct['hosts'][host]['ssh'].close()
            self.hosts_dct['hosts'][host]['is_connected'] = False
            if terminal_print:
                rich.print(f"INFO -- connection closed with {host}")

    def close_channel(self, host):
        """
        Close the SSH Channel with a network device (For Testing.)
        INPUT:
            1. host_dct (dct) the host dictionary that contains host details
        """
        if self.hosts_dct['hosts'][host]['is_connected']:
            self.hosts_dct['hosts'][host]['channel'].close()
            self.hosts_dct['hosts'][host]['is_connected'] = False


    def ask_for_confirmation(self, msg="Confirm before running the following command", cmd=""):
        try:
            options = ['yes', 'no']
            decision = None
            while decision not in options:
                confirm = input(
                "\nWARNING -- {}: \n".format(msg)
                + "\n"
                + cmd  + "\n"
                + "\nyes || no \n\n"
                + "yes: Run & continue\n"
                + "no:  Abort\n"
                + "YOUR Decision: ")
                if confirm == 'yes':
                    print("> Ok .. Let\'s continue ...\n")
                    break
                elif confirm == 'no':
                    print("> See you \n")
                    exit(1)
        except (KeyboardInterrupt):
            rich.print("\n[bright_green]OK !")
            exit(1)

    def connection_report_Table(self, dct={}, terminal_print=False, ask_when_hosts_fail=False):
        """
        Takes an dict generated from the "authenticate_devices" Method
        And prints them in a an organized table
        """
        table = [['Host', 'Connection Status', 'N of tries', 'Max Retries', 'Time taken in seconds', 'Fail Reason']]
        for host, info in dct.items():
            
            if info['is_connected']:
                connection_status = "🟢 connected"
            else:
                connection_status = "🔴 Fail to connect"
            fail_reason = "\n".join(textwrap.wrap(info['fail_reason'], width=32, replace_whitespace=False))
            
            row = [host, connection_status, info['tries'], info['max_tries'], info['time_taken'], fail_reason]
            table.append(row)
        out = tabulate.tabulate(table, headers='firstrow', tablefmt='grid', showindex=False)

        if terminal_print:
            print()
            rich.print("[bold green on black]# Connection Report")
            print(out)
            if (self.hosts_dct['total']['n_hosts_failed'] ==  self.hosts_dct['total']['n_hosts_total']):
                rich.print("\n[bold]INFO -- No need to continue; All hosts of the group failed to authenticate\n")
                exit(1)
            if (ask_when_hosts_fail) and (self.hosts_dct['total']['n_hosts_failed'] > 0) :
                self.ask_for_confirmation(msg=f"Failed to connect to {self.hosts_dct['total']['n_hosts_failed']} devices, Please confirm to continue")
            print()

        return tabulate.tabulate(table, headers='firstrow', tablefmt='grid', showindex=False)

    # def reconnect_if_socket_closed(self, host_dct):
    #     """
    #     Method to detect if the ssh connection is close, and if so will try to re-connect.
    #     INPUT:
    #         1. host_dct -> (dct) the authentication information of a host 
    #     """
    #     # Flag to watch if a connection reconnect was needed (closed connection detected.)
    #     self.needed = False
    #     # Flag to watch if the connection of the host was re-connected.
    #     self.reconnected = False
    #     def reconnect():
    #         """
    #         A function to try to reconnect a closed ssh connection
    #         - Will be triggered if a closed socket is detected.
    #         """
    #         print(f"\n> 🟡 Closed Socket detected {host_dct['host']}\n> Trying to reconnect ...")

    #         print()
    #         # Re-authenticate the host
    #         # reauth = self.authenticate(hosts=[host_dct], user=self.user, password=self.password, port=self.port, terminal_print=True)
    #         reauth = self.connect(host=host_dct['host'], user=host_dct['user'], password=host_dct['password'], port=host_dct['port'])
    #         print(reauth)
    #         # If the host was re-connected successfully.
    #         if reauth[host_dct['host']]['is_connected']:
    #             # Update the channel & ssh client objects of the host (So that the channel will be used for further commands execution.)
    #             host_dct['channel']  = reauth[host_dct['host']]['channel']
    #             host_dct['ssh']  = reauth[host_dct['host']]['ssh']
    #             print(f"> 🟢 Reconnected successfully to @{host_dct['host']}")
    #             self.reconnected = True
    #             # rich.print(reauth)
    #         else:
    #             print(f"> 🔴 FAILED to reconnect to @{host_dct['host']}")
    #             self.reconnected = False
    #     try:
    #         transport = host_dct['ssh'].get_transport()
    #         if host_dct['channel'] is not None:
    #             # Send a new line on the ssh channel as a test
    #             host_dct['channel'].send("\n")
    #             # We need to wait a bit after sending the test new line.
    #             time.sleep(0.1)
    #             # Check if the channel has something to get receive. (If no then there is a problem and we need to reconnect
    #             # [because we already sent a test new line & that should return something.])
                
    #             if not host_dct['channel'].recv_ready():
    #                 reconnect()
    #                 self.needed = True
    #             # Reconnect if the transport is not active
    #             elif not transport.is_active():
    #                 reconnect()
    #                 self.needed = True
    #             # Reconnect if the channel is not closed
    #             elif host_dct['channel'].closed:
    #                 reconnect()
    #                 self.needed = True
    #         # If the channel is None that means that the device was failed to authenticate the first time !
    #         # But anyway, if the user decided to loop over all the devices (including the ones that didn't connect)
    #         # We'll try to connect again.
    #         elif host_dct['channel'] is None:
    #             reconnect()
    #             self.needed = True
    #             # If the authentication is successful, the channel & ssh objects will be updated otherwise, the channel object will remain None.
    #         return {'needed': self.needed, 'reconnected': self.reconnected}

    #     except (paramiko.SSHException) as e:
    #         print(13)
    #     except socket.error  as e:
    #         rich.print(f"ERROR -- Something went wrong !\n> [bright_red]{e}[/bright_red]")
    #         exit(1)
        
 
    def exec(self, host, cmd, vendor, reconnect_closed_socket=True):
        """
        Excutes a command on a remove network device
        INPUT:
            1. host -> (string) host IP address 
            2. reconnect_closed_socket -> (bool) If to try to reconnect closed sockets. (Default: True)
        
        Returns a dictionary:
        {
            "stdout": "The output of the command",
            "stderr": "The error (Syntax error are detected.)",
            "exit_code":  0 --> the command run successfully,  1 --> an error occurred
        }
        - does NOT print to the terminal
        """
        self.vendor = vendor

        def get_stderr(string, stderr_search_keyword=self.vendor.stderr_search_keyword):
            """
            - A Function to search the output of command for syntax errors
            - Returns a list of lines (Starts with the command has the error including the error location)
            """
            # Convert the stdout to list
            string_lst = string.replace("\r", '').strip().split("\n")
            # Loop through the indexes of the list
            # If the search is found in one of the lines, then we know the line number that contains the error keyword
            # And since the the command should be directly in the line before the error keyword,
            # we'll return the list starting from the index -1 till the end of the list.
            for str_to_search in stderr_search_keyword:
                for i in range(len(string_lst)):
                    search = re.findall("{}.*$".format(str_to_search), string_lst[i])
                    if search:
                        return string_lst[i-1:]
            return []

        out = {}
        # Clean the command & turn it to a list (splitted with new lines.)
        out['cmd'] = cmd.replace("\r", '').split("\n")
        
        # Clean the empty lines
        out['cmd'] = [i for i in out['cmd'] if i]
        out['stdout'] = []
        out['stderr'] = []
        out['exit_code'] = 0
        
        if reconnect_closed_socket:
            if self.is_channel_closed(self.hosts_dct['hosts'][host]['channel']):
                self.reconnect(host)

        # If the socket is closed try to reconnect.
        # if reconnect_closed_socket:
        #     result = self.reconnect_if_socket_closed(host_dct)
        #     # If tried to re-connect & failed -> return -1
        #     if (result['needed']) and (not result['reconnected']):
        #         out['exit_code'] = -1
        #         out['stderr'] = ["Socket is closed > Failed to reconnect."]
        #         return out
        #     elif host_dct['channel'] is None:
        #         out['exit_code'] = -1
        #         out['stderr'] = ["Socket is closed > The host was NOT connected > The second authentication attempt was Failed"]
        #         return out         
    
        # Run the command
        try:
            # Probably channel will be None in case "Connection reset by peer" (host sent a RST packet " indicates an immediate dropping of the connection")
            # https://stackoverflow.com/a/1434506
            channel = self.hosts_dct['hosts'][host]['channel']
            if channel is None:
                err = {
                    "cmd": [cmd],
                    "stdout": [""],
                    "stderr": [self.hosts_dct['hosts'][host]['fail_reason']],
                    "exit_code": -1
                }
                return err
            
            channel.send(cmd + '\n' + '\n')
            # Important to set wait time, if not set it might not be able to read full output.
            time.sleep(0.5)
        
            # Get the output of the command
            if channel.recv_ready():
                out['stdout'] = channel.recv(9999).decode("utf-8")
            else:
                out['stdout'] = ""

            # Preserve of the original stdout (Before cleaning)
            stdout_original = out['stdout']
            # Clean the "command" from the output & the white spaces.
            out['stdout'] = out['stdout'].replace(cmd.strip(), '')
            # Clean the stdout from unneeded lines.
            for keyword in self.vendor.clean_output_search_keywords:
                out['stdout'] = re.sub(keyword, '', out['stdout'])

            # Get the stderr
            out['stderr'] = get_stderr(stdout_original)
            # out['exit_code'] = 0
            if len(out['stderr']) > 0:
                # Get the exit_code based on the stderr
                out['exit_code'] = 1
                # Remove empty lines in stdout
                out['stderr'] = [i for i in out['stderr'] if i]

            # convert the stdout to a list of lines
            out['stdout'] = out['stdout'].replace("\r", '').split("\n")
            # Remove empty lines in stdout
            if len(out['stdout']) > 0:
                out['stdout'] = [i for i in out['stdout'] if i]

        # If the connection is interrupted during execution
        except (socket.error)  as e:
            out['stderr'] = [str(e)]
            out['exit_code'] = -1
            
        return out

    # def backup_config(self, host):
    #     """
    #     Take a backup of the device configurations
    #     """
    #     out = self.exec(host, self.vendor.backup_command, self.vendor)
    #     return out