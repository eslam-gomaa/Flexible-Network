
# enhance authenticate method

from FlexibleNetwork.Flexible_Network import Terminal_Task
task = Terminal_Task()

auth = task.authenticate('works', 'orange', 'cisco', 1113)

print(auth.connection_report_table)

print("hosts total", auth.hosts_total)
print("hosts connected", auth.hosts_connected)
print("hosts failed", auth.hosts_failed)
print("hosts total number", auth.hosts_total_number)
print("hosts connected number", auth.hosts_connected_number)
print("hosts failed number", auth.hosts_failed_number)

# Only 1 host connected
for host in auth.hosts_connected:
    test = task.execute(host, 'sho ip int br')
    print("host", test.host)
    print("command", test.cmd)
    print("exit_code", test.exit_code)
    print("stderr", test.stderr)
    print("stdout", test.stdout)

