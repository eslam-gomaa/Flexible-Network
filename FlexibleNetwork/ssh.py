from FlexibleNetwork.ssh_authentication import SSH_Authentication
import time
from tabulate import tabulate
import textwrap
import re
import socket
from FlexibleNetwork.vendors.cisco import Cisco


class SSH_connection():
    def __init__(self):
        self.devices_dct = {}
        self.connected_devices_dct = {}
        self.connected_devices_number = 0
        self.connection_failed_devices_number = 0
        self._vendor = Cisco()

    @property
    def vendor(self):
        return self._vendor
    
    @vendor.setter
    def vendor(self, vendor):
        self._vendor = vendor


    def authenticate(self, hosts=[], user='orange', password='cisco', port='1113', terminal_print=False):
        """
        Autenticates a List of devices and returns a dictionary of dictionaries,
        * The key of each nested dict is the host IP and the value is the connection & authentication information.
        # Modified copy of .. (for terminal printing.)
        """
        try:
            if terminal_print:
                print()
                print("> Authenticating selected devices")         
            
            self.user = user
            self.password = password
            self.port = port
            out = {}
            self.authentication = SSH_Authentication()
            cnt = 0
            for host in hosts:
                connection = self.authentication.connect(host, user, password, port)
                if connection['is_connected']:
                    self.connected_devices_number +=1
                else:
                    self.connection_failed_devices_number  +=1
                out[host] = connection
                cnt +=1
                if terminal_print:
                    print("   {}  [ {} / {} ]          Connected [ {} ]     Failed [ {} ]    ".format(host, cnt , len(hosts), self.connected_devices_number, self.connection_failed_devices_number), end="\r")
            # print("                                                                                              ", end='\r')
            print()
            self.devices_dct = out
            for host in self.devices_dct:
                if self.devices_dct[host]['is_connected']:
                    self.connected_devices_dct[host] = self.devices_dct[host]
            return out
        except KeyboardInterrupt:
            print()
            print("> Stopped.  See you \n")
            exit(1)

    def close(self, authenticated_hosts_dct):
        """
        Close the SSH connection for a list of hosts
        Time Complexity -> O(n)
        """
        for host in authenticated_hosts_dct:
            ssh = authenticated_hosts_dct[host]['ssh']
            data = {}
            data['success'] = 'False'
            if authenticated_hosts_dct[host]['is_connected']:
                ssh.close()
                data['success'] = 'True'
            return data


    def ask_for_confirmation(self, msg="Confirm before running the following command", cmd=""):
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



    def connection_report_Table(self, dct={}, terminal_print=False, ask_when_hosts_fail=False):
        """
        Takes an dict generated from the "authenticate_devices" Method
        And prints them in a an organized table
        """
        table = [['Host', 'Connection Status', 'Comment', 'N of tries', 'Max Retries', 'Time tring in seconds', 'Fail Reason']]
        tabulate.WIDE_CHARS_MODE = False
        for host, info in dct.items():
            
            if info['is_connected']:
                connection_status = "🟢"
                comment = "connected"
            else:
                connection_status = "🔴"
                comment = "Fail to connect"
            fail_reason = "\n".join(textwrap.wrap(info['Fail_Reason'], width=22, replace_whitespace=False))
            
            row = [host, connection_status, comment, info['tries'], info['max_tries'], info['time_to_connect_seconds'], fail_reason]
            table.append(row)
        out = tabulate(table, headers='firstrow', tablefmt='grid', showindex=False)
        if terminal_print:
            print()
            print("> Connection Report   ")
            print(out)
            if (ask_when_hosts_fail and self.connection_failed_devices_number > 0) :
                self.ask_for_confirmation(msg="Failed to connect to some devices, Please confirm to continue")
            print()

        return tabulate(table, headers='firstrow', tablefmt='grid', showindex=False)

    
    def connection_report_to_csv(self, dct={}):
        """
        Takes an dict generated from the "authenticate_devices" Method
        And prints them in a an organized table
        """
        table = [['Host', 'Connection Status', 'Comment', 'N of tries', 'Max Retries', 'Time tring in seconds', 'Fail Reason']]
        tabulate.WIDE_CHARS_MODE = False
        for host, info in dct.items():
            
            if info['is_connected']:
                connection_status = "🟢"
                comment = "connected"
            else:
                connection_status = "🔴"
                comment = "Fail to connect"
            fail_reason = "\n".join(textwrap.wrap(info['Fail_Reason'], width=22, replace_whitespace=False))
            
            row = [host, connection_status, comment, info['tries'], info['max_tries'], info['time_to_connect_seconds'], fail_reason]
            table.append(row)
        output_data = tabulate(table, headers='firstrow', tablefmt='tsv', showindex=False)
        # Need to Figure out how to write these these data to a csv or Excel file. 
        
 
    def exec(self, channel, cmd):
        """
        - Excutes a command on a remove network device
        - Returns a dictionary:
        {
            "stdout": "The output of the command",
            "stderr": "The error (Syntax error are detected.)",
            "exit_code":  0 --> the command run successfully,  1 --> an error occurred
        }
        - does NOT print to the terminal
        """

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
        # What was I replacing !??
        out['cmd'] = cmd.replace("\r", '').split("\n")
        out['cmd'] = [i for i in out['cmd'] if i]
        out['stdout'] = []
        out['stderr'] = []
        out['exit_code'] = -1

        ## Thinking: How to reconnect if the socket is closed.
        # try:
        #     channel.send("")
        # except (socket.error)  as e:
        #     pass
    
        # Run the command
        try:
            channel.send(cmd + '\n' + '\n')
            # Important to set wait time, if not set it might not be able to read full output.
            time.sleep(0.5)
        
            # Get the output of the command
            out['stdout'] = channel.recv(9999).decode("utf-8")
            # Preserve of the original stdout (Before cleaning)
            stdout_original = out['stdout']
            # Clean the "command" from the output & the white spaces.
            out['stdout'] = out['stdout'].replace(cmd.strip(), '')
            # Clean the stdout from unneeded lines.
            for keyword in self.vendor.clean_output_search_keywords:
                out['stdout'] = re.sub(keyword, '', out['stdout'])

            # Get the stderr
            out['stderr'] = get_stderr(stdout_original)
            out['exit_code'] = 0
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

        return out

    def backup_config(self, channel, comment, target):
        """
        Take a backup of the device configurations
        """
        out = self.exec(channel, self.vendor.backup_command)
        return out
