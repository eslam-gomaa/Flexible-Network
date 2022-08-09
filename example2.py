
# enhance authenticate method

from tokenize import group
from FlexibleNetwork.Flexible_Network import Terminal_Task
from FlexibleNetwork.Vendors import Cisco

task = Terminal_Task()
task.vendor = Cisco()

auth = task.authenticate(groups='pa3', user='orange', password='cisco', privileged_mode_password='cisco', port=1113)

# print(auth.connection_report_table)

# print("hosts total", auth.hosts_total)
# print("hosts connected", auth.hosts_connected)
# print("hosts failed", auth.hosts_failed)
# print("hosts total number", auth.hosts_total_number)
# print("hosts connected number", auth.hosts_connected_number)
# print("hosts failed number", auth.hosts_failed_number)

# Only 1 host connected
for host in auth.hosts_connected:

    # task.execute_raw(host, "enable\n" + "cisco")
    # task.execute(host, """
    # conf t
    # do sh ip int br
    # """)
    # task.execute(host, "do sho ip int br")
    
    backup = task.take_config_backup(host, "Test", privileged_mode_password='cisco', target='local')

    task.execute(host, "sho ip int br")
    task.execute(host, "show vlan br")
    task.execute(host, "show version")

    # print(backup.exit_code)
    # print(backup.stdout)
    # print(backup.stderr)
    # print(backup.location)
    # print(backup.id)


    # test = task.execute(host, 'sho ip int br')
    # print("host", test.host)
    # print("command", test.cmd)
    # print("exit_code", test.exit_code)
    # print("stderr", test.stderr)
    # print("stdout", test.stdout)
    

# search_backup = task.get_config_backup('d3dee1e4-f1cf-4736-b300-120252c5c602')

# print("exit_code", search_backup.exit_code)
# print("stdout", search_backup.stdout)
# print("stderr", search_backup.stderr)
# print("text", search_backup.text)
