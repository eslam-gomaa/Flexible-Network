
# enhance authenticate method

from FlexibleNetwork.Flexible_Network import Terminal_Task
task = Terminal_Task()

auth = task.authenticate('works', 'orange', 'cisco', 1113)

# test = task.execute('90.84.41.239', 'sho ip int brfqfsfd', exit_on_fail=False)
# print(test)
# print(test.host)
# print(test.cmd)
# print(test.exit_code)
# print(test.stderr)
# print(test.stdout)

task.execute_from_file(host='90.84.41.239', file='commands.txt')

