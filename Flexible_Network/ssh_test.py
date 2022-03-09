# from site import venv
from Flexible_Network.ssh_authentication import SSH_Authentication
import time
from tabulate import tabulate
import textwrap
import re


class SSH_connection():
    def __init__(self):
        # self.supported_vendors = ['cisco', 'huawei']
        # if vendor not in supported_vendors:
        #     print("[ ERROR ] Only supported vendors are {}".format(supported_vendors))

        self._vendor = None

    @property
    def vendor(self):
        return self._vendor
    
    @vendor.setter
    def vendor(self, vendor):
        self._vendor = vendor

    def authenticate(self, hosts=[], user='orange', password='cisco', port='1113'):
        """
        Autenticates a List of devices and returns a dictionary of dictionaries,
        * The key of each nested dict is the host IP and the value is the connection & authentication information.
        """
        out = {}
        self.authentication = SSH_Authentication()
        for host in hosts:
            connection = self.authentication.connect(host, user, password, port)
            out[host] = connection
        return out

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



    def connection_report_Table(self, dct={}):
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
        """

        def get_stderr(string, stderr_search_keyword=self.vendor.stderr_search_keyword):
            """
            - A Function to search the output of command for syntax errors
            - Returns a list of lines (Starts with the command has the error including the error location)
            """
            # Convert the stdout to list
            string_lst = string.split("\n")
            # Loop through the indexes of the list
            # If the search is found in one of the lines, then we know the line number that contains the error keyword
            # And since the the command should be directly in the line before the error keyword,
            # we'll returnthe list starting from the index -1 till the end of the list.
            for i in range(len(string_lst)):
                search = re.findall("{}.*$".format(stderr_search_keyword), string_lst[i])
                if search:
                    return string_lst[i-1:]
            return []

        out = {}
        # Run the command
        channel.send(cmd + '\n' + '\n')
        # Important to set wait time, if not set it might not be able to read full output.
        time.sleep(0.5)
        # What was I replacing !??
        out['cmd'] = cmd.replace("\r", '').split("\n")
        # Get the output of the command
        out['stdout'] = channel.recv(9999).decode("utf-8")
        # Preserve of the original stdout (Before cleaning)
        stdout_original = out['stdout']
        out['stderr'] = get_stderr(stdout_original)
        out['exit_code'] = 0
        if len(out['stderr']) > 0:
            out['exit_code'] = 1
        if len(out['stderr']) < 0:
            out['stderr'] = ""
        out['stderr'] = "\n".join(out['stderr']).strip()
        # Clean the "command" from the output & the white spaces.
        out['stdout'] = out['stdout'].replace(cmd, '').strip()
        # Get the exit_code based on the stderr


        # Need to clean the output from the last 2 lines "mgmt_sw>"
        
        # Considerations (Will differ among vendors.)
        # 1. 

        return out

    def execute(self, channel, cmd, print='default', ask_for_confirmation=False):
        """
        - Excutes a command on a remove network device
        - Print [ default, json ]
        - Ask for confirmation before executing the command on the remote device.
        - Returns a dictionary:
        {
            "stdout": "The output of the command",
            "stderr": "The error (Syntax error are detected.)",
            "exit_code":  0 --> the command run successfully,  1 --> an error occurred
        }
        """
        pass

    def backup_config(self, channel, comment, target='local'):
        """
        Take a backup of the device configurations
        Options: 'local' or 's3'
        """
        return self.vendor.backup_command
        
    
