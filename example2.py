
# enhance authenticate method

from FlexibleNetwork.Flexible_Network import Terminal_Task
task = Terminal_Task()

auth = task.authenticate('works', 'orange', 'cisco', 1113)

test = task.execute_raw('90.84.41.239', 'sho ip int br1')
print(test)
print(test.host)
print(test.cmd)
print(test.exit_code)
print(test.stderr)
print(test.stdout)