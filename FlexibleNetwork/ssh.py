from FlexibleNetwork.ssh_authentication import SSH_Authentication
import time
from tabulate import tabulate
import textwrap
import re
import socket
import threading
import rich

class SSH_connection(SSH_Authentication):
    def __init__(self):
        super().__init__()

        self.devices_dct = {}
        self.connected_devices_dct = {}
        self.vendor = None # should be updated in the exec method.


    # def authenticate_2(self, hosts, user, password, port, terminal_print=False, parallel=True, n_parallel_connections=10):
    #     """
    #     Testing. Threading.
    #     """
    #     try:
    #         if terminal_print:
    #             print("> Authenticating selected devices")
            
    #         self.connection_failed_devices_number = 0
    #         self.connected_devices_number = 0
    #         self.user = user
    #         self.password = password
    #         self.port = port
    #         # out = {}

    #         # self.authentication = SSH_Authentication()


    #         threads = []
    #         rich.print(hosts)
    #         for host in hosts:
    #             print(host)
    #             thread  = threading.Thread(target=self.connect, args=(host, user, password, port))
    #             thread.daemon = True
    #             threads.append(thread)

    #             # thread.start()

            
    #             # connection = self.authentication.connect(host, user, password, port)
    #             # if connection['is_connected']:
    #             #     self.connected_devices_number +=1
    #             # else:
    #             #     self.connection_failed_devices_number  +=1
    #             # out[host] = connection
    #             # cnt +=1
    #             # if terminal_print:
    #             #     print("testing..")


    #     except:
    #         pass



    # def authenticate(self, hosts, user, password, port, terminal_print=False):
    #     """
    #     Autenticates a List of devices and returns a dictionary of dictionaries,
    #     * The key of each nested dict is the host IP and the value is the connection & authentication information.
    #     # Modified copy of .. (for terminal printing.)
    #     """
    #     try:
    #         if terminal_print:
    #             print("> Authenticating selected devices")

    #         self.connection_failed_devices_number = 0
    #         self.connected_devices_number = 0
    #         self.user = user
    #         self.password = password
    #         self.port = port
    #         out = {}
    #         self.authentication = SSH_Authentication()
    #         cnt = 0
    #         for host in hosts:
    #             connection = self.authentication.connect(host, user, password, port)
    #             if connection['is_connected']:
    #                 self.connected_devices_number +=1
    #             else:
    #                 self.connection_failed_devices_number  +=1
    #             out[host] = connection
    #             cnt +=1
    #             if terminal_print:
    #                 print("   {}  [ {} / {} ]          Connected [ {} ]     Failed [ {} ]    ".format(host, cnt , len(hosts), self.connected_devices_number, self.connection_failed_devices_number), end="\r")
    #         # print("                                                                                              ", end='\r')
    #         print()
    #         self.devices_dct = out
    #         for host in self.devices_dct:
    #             if self.devices_dct[host]['is_connected']:
    #                 self.connected_devices_dct[host] = self.devices_dct[host]
    #         return out
    #     except KeyboardInterrupt:
    #         print()
    #         print("> Stopped.  See you \n")
    #         exit(1)

    # def authenticate_concurrent(self, hosts, user, password, port, terminal_print=True):
    #     """
    #     Autenticates a List of devices and returns a dictionary of dictionaries,
    #     * The key of each nested dict is the host IP and the value is the connection & authentication information.
    #     # Modified copy of .. (for terminal printing.)
    #     """
    #     try:
    #         if terminal_print:
    #             print("> Authenticating selected devices")

    #         self.connection_failed_devices_number = 0
    #         self.connected_devices_number = 0
    #         self.user = user
    #         self.password = password
    #         self.port = port

    #         out = {}
    #         self.authentication = SSH_Authentication()
    #         cnt = 0
            
    #         with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    #             host_feature_dct = {}

    #             # for host in hosts:
    #             #     connection = executor.map(self.authentication.connect, host, user, password, port, timeout=5)
    #             #     print(host, connection)
    #             #     host_feature_dct[host] = connection
                
    #             # for host, future in host_feature_dct.items():
    #             #     print(str(future))

    #             for host in hosts:
    #                 connection = executor.submit(self.authentication.connect, host, user, password, port)
    #                 time.sleep(2)
    #                 print(f"> Starting parallel ssh clients:  [ {host} ]", end="\r")
    #                 # results.append(connection)
    #                 host_feature_dct[host] = connection

    #             for host, future in zip(host_feature_dct.keys(), concurrent.futures.as_completed(host_feature_dct.values())):
    #                 if future.result()['is_connected']:
    #                     self.connected_devices_number +=1
    #                 else:
    #                     self.connection_failed_devices_number  +=1
    #                 out[host] = future.result()
    #                 cnt +=1
    #                 if terminal_print:
    #                     print("   {}  [ {} / {} ]          Connected [ {} ]     Failed [ {} ]    ".format(host, cnt , len(hosts), self.connected_devices_number, self.connection_failed_devices_number), end="\r")



    #             # for host, future in host_feature_dct.items():
    #             #     if future.result()['is_connected']:
    #             #         self.connected_devices_number +=1
    #             #     else:
    #             #         self.connection_failed_devices_number  +=1
    #             #     out[host] = future.result()
    #             #     cnt +=1
    #             #     if terminal_print:
    #             #         print("   {}  [ {} / {} ]          Connected [ {} ]     Failed [ {} ]    ".format(host, cnt , len(hosts), self.connected_devices_number, self.connection_failed_devices_number), end="\r")


    #             # for f, host in zip(concurrent.futures.as_completed(results), hosts):
    #             #     if f.result()['is_connected']:
    #             #         self.connected_devices_number +=1
    #             #     else:
    #             #         self.connection_failed_devices_number  +=1
    #             #     out[host] = f.result()
    #             #     cnt +=1
    #             #     if terminal_print:
    #             #         print("   {}  [ {} / {} ]          Connected [ {} ]     Failed [ {} ]    ".format(host, cnt , len(hosts), self.connected_devices_number, self.connection_failed_devices_number), end="\r")

    #             # print("                                                                                              ", end='\r')
    #         print()
    #         self.devices_dct = out
    #         for host in self.devices_dct:
    #             if self.devices_dct[host]['is_connected']:
    #                 self.connected_devices_dct[host] = self.devices_dct[host]
    #         return out
    #     except KeyboardInterrupt:
    #         print()
    #         print("> Stopped.  See you \n")
    #         exit(1)

    # def close(self, authenticated_hosts_dct):
    #     """
    #     Close the SSH connection for a list of hosts
    #     Time Complexity -> O(n)
    #     """
    #     for host in authenticated_hosts_dct:
    #         ssh = authenticated_hosts_dct[host]['ssh']
    #         data = {}
    #         data['success'] = 'False'
    #         if authenticated_hosts_dct[host]['is_connected']:
    #             ssh.close()
    #             data['success'] = 'True'
    #         return data


    # def ask_for_confirmation(self, msg="Confirm before running the following command", cmd=""):
    #     options = ['yes', 'no']
    #     decision = None
    #     while decision not in options:
    #         confirm = input(
    #         "\nWARNING -- {}: \n".format(msg)
    #         + "\n"
    #         + cmd  + "\n"
    #         + "\nyes || no \n\n"
    #         + "yes: Run & continue\n"
    #         + "no:  Abort\n"
    #         + "YOUR Decision: ")
    #         if confirm == 'yes':
    #             print("> Ok .. Let\'s continue ...\n")
    #             break
    #         elif confirm == 'no':
    #             print("> See you \n")
    #             exit(1)


    # def connection_report_Table(self, dct={}, terminal_print=False, ask_when_hosts_fail=False):
    #     """
    #     Takes an dict generated from the "authenticate_devices" Method
    #     And prints them in a an organized table
    #     """
    #     table = [['Host', 'Connection Status', 'N of tries', 'Max Retries', 'Time tring in seconds', 'Fail Reason']]
    #     tabulate.WIDE_CHARS_MODE = False
    #     for host, info in dct.items():
            
    #         if info['is_connected']:
    #             connection_status = "🟢 connected"
    #         else:
    #             connection_status = "🔴 Fail to connect"
    #         fail_reason = "\n".join(textwrap.wrap(info['fail_reason'], width=32, replace_whitespace=False))
            
    #         row = [host, connection_status, info['tries'], info['max_tries'], info['time_taken'], fail_reason]
    #         table.append(row)
    #     out = tabulate(table, headers='firstrow', tablefmt='grid', showindex=False)
    #     if terminal_print:
    #         print()
    #         rich.print("[bold green on black]# Connection Report")
    #         print(out)
    #         if (ask_when_hosts_fail and self.connection_failed_devices_number > 0) :
    #             self.ask_for_confirmation(msg="Failed to connect to some devices, Please confirm to continue")
    #         print()

    #     return tabulate(table, headers='firstrow', tablefmt='grid', showindex=False)

    
    # def connection_report_to_csv(self, dct={}):
    #     """
    #     Takes an dict generated from the "authenticate_devices" Method
    #     And prints them in a an organized table
    #     """
    #     table = [['Host', 'Connection Status', 'Comment', 'N of tries', 'Max Retries', 'Time taken in seconds', 'Fail Reason']]
    #     tabulate.WIDE_CHARS_MODE = False
    #     for host, info in dct.items():
            
    #         if info['is_connected']:
    #             connection_status = "🟢"
    #             comment = "connected"
    #         else:
    #             connection_status = "🔴"
    #             comment = "Fail to connect"
    #         fail_reason = "\n".join(textwrap.wrap(info['fail_reason'], width=22, replace_whitespace=False))
            
    #         row = [host, connection_status, comment, info['tries'], info['max_tries'], info['time_taken'], fail_reason]
    #         table.append(row)
    #     output_data = tabulate(table, headers='firstrow', tablefmt='tsv', showindex=False)
    #     # Need to Figure out how to write these these data to a csv or Excel file. 

    def reconnect_if_socket_closed(self, host_dct):
        """
        Method to detect if the ssh connection is close, and if so will try to re-connect.
        INPUT:
            1. host_dct -> (dct) the authentication information of a host 
        """
        # Flag to watch if a connection reconnect was needed (closed connection detected.)
        self.needed = False
        # Flag to watch if the connection of the host was re-connected.
        self.reconnected = False
        def reconnect():
            """
            A function to try to reconnect a closed ssh connection
            - Will be triggered if a closed socket is detected.
            """
            print(f"\n> 🟡 Closed Socket detected @{host_dct['host']}\n> Trying to reconnect ...")

            print()

            # rich.print(SSH_Authentication.hosts_dct['hosts'][host_dct['host']])
            # exit(1)

            # Re-authenticate the host
            reauth = self.authenticate(hosts=[host_dct['host']], user=self.user, password=self.password, port=self.port, terminal_print=True)
            # If the host was re-connected successfully.
            if reauth[host_dct['host']]['is_connected']:
                # Update the channel & ssh client objects of the host (So that the channel will be used for further commands execution.)
                host_dct['channel']  = reauth[host_dct['host']]['channel']
                host_dct['ssh']  = reauth[host_dct['host']]['ssh']
                print(f"> 🟢 Reconnected successfully to @{host_dct['host']}")
                self.reconnected = True
            else:
                print(f"> 🔴 FAILED to reconnect to @{host_dct['host']}")
                self.reconnected = False
        try:
            transport = host_dct['ssh'].get_transport()
            if host_dct['channel'] is not None:
                # Send a new line on the ssh channel as a test
                host_dct['channel'].send("\n")
                # We need to wait a bit after sending the test new line.
                time.sleep(0.1)
                # Check if the channel has something to get receive. (If no then there is a problem and we need to reconnect
                # [because we already sent a test new line & that should return something.])
                
                if not host_dct['channel'].recv_ready():
                    reconnect()
                    self.needed = True
                # Reconnect if the transport is not active
                elif not transport.is_active():
                    reconnect()
                    self.needed = True
                # Reconnect if the channel is not closed
                elif host_dct['channel'].closed:
                    reconnect()
                    self.needed = True
            # If the channel is None that means that the device was failed to authenticate the first time !
            # But anyway, if the user decided to loop over all the devices (including the ones that didn't connect)
            # We'll try to connect again.
            elif host_dct['channel'] is None:
                reconnect()
                self.needed = True
                # If the authentication is successful, the channel & ssh objects will be updated otherwise, the channel object will remain None.
            return {'needed': self.needed, 'reconnected': self.reconnected}
        except socket.error  as e:
            print(f"ERROR -- Something went wrong !\n> {e}")
            exit(1)
        
 
    def exec(self, host_dct, cmd, vendor, reconnect_closed_socket=True):
        """
        Excutes a command on a remove network device
        INPUT:
            1. host_dct -> (dct) the authentication information of a host 
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

        # If the socket is closed try to reconnect.
        print(self.is_channel_closed(host_dct))
        if reconnect_closed_socket:
            result = self.reconnect_if_socket_closed(host_dct)
            # If tried to re-connect & failed -> return -1
            if (result['needed']) and (not result['reconnected']):
                out['exit_code'] = -1
                out['stderr'] = ["Socket is closed > Failed to reconnect."]
                return out
            elif host_dct['channel'] is None:
                out['exit_code'] = -1
                out['stderr'] = ["Socket is closed > The host was NOT connected > The second authentication attempt was Failed"]
                return out         
    
        # Run the command
        try:
            channel = host_dct['channel']
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

    def backup_config(self, host_dct):
        """
        Take a backup of the device configurations
        """
        out = self.exec(host_dct, self.vendor.backup_command, self.vendor)
        return out