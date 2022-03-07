from base64 import encode
from cmath import inf
from Flexible_Network.ssh_authentication import SSH_Authentication
import time
import socket
from tabulate import tabulate
import textwrap

class SSH_connection():
    def __init__(self):
        pass

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
        
 
    def execute(self, channel, cmd):
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
        # Clean the "command" from the output & the white spaces.
        out['stdout'] = out['stdout'].replace(cmd, '').strip()

        # Need to clean the output from the last 2 lines "mgmt_sw>"

        def get_stderr(string, stderr_search_keyword='\^'):
            # Create a dictionary that has the line number as the Key & the line string as the Value.
            line_number = 0
            line_number_with_string_dct = {}

            # Split the string into lines
            string_list = string.split("\n")
            for line in string_list:
                line_number_with_string_dct[line_number] = line
                line_number  +=1
                # Search the line for syntax error
                search_syntax_error = re.findall("{}.*$".format(stderr_search_keyword), line)

                # Store the found match in a dct {line number: [matched lines as a list]}
                # Stopped here



        return out

        # Considerations (Will differ among vendors.)
        # 1. 
