from FlexibleNetwork.Flexible_Network import Terminal_Task
task = Terminal_Task()

# python3 example.py -n test -i user/hosts -c user/flexible_network.cfg --authenticate-group cisco_switches  --user orange --password cisco --port 1114

# python3 example.py -n test -i user/hosts -c user/flexible_network.cfg --authenticate-group pa3  --user orange --password cisco --port 1114


# for host in task.devices_dct.values():
#     task.execute(host, "sh version")
# rich.print(task.devices_dct)


# For each host in the group execute the listed commands
# task.execute_on_group(group='pa3', cmd=[
#                                         "show vlan br",
#                                         "show ip int br"
#                                         ])


# task.sub_task(name="Testing", group='pa3', cmds=[
#     {
#         "command": "show ip int br", 
#         "tag": "123df",
#     },
#     {
#         "command": "show vlan br", 
#         "when": {"tag": "123df", "exit_code": 1, 'operator': 'is'}
#     },
#     {
#         "command": "show vlan br", 
#     }
# ])



import yaml
import rich
import cerberus

class YamlParser:
    def __init__(self, yaml_file):
        self.yaml_file = yaml_file
        self.validated_documents = []

    def validate_yaml(self, print_msg=False):
        schema_dct = {
            "Task": {
                'type': 'dict',
                'required': True,
                'schema': {
                    'name': {
                        "type": "string",
                        'required': True,
                    },
                    'subTask': {
                        'type': 'list',
                        'required': True,
                        'schema': {
                            'type': 'dict',
                            'schema': {
                                'name': {
                                    'type': 'string',
                                    'required': True
                                },
                                'vendor': {
                                    'type': 'string',
                                    'required': False,
                                    'default': 'cisco',
                                    'allowed': ['cisco', 'huawei']

                                },
                                'label': {
                                    'type': 'string',
                                    'required': False,
                                    'default': ""
                                },
                                'parallel': {
                                    'type': 'boolean',
                                    'required': False,
                                    'default': False
                                },
                                'authenticate': {
                                    'type': 'dict',
                                    'schema': {
                                        'group': {
                                            'type': 'string',
                                            'required': False,
                                            'default': ''
                                        },
                                        'host': {
                                            'type': 'string',
                                            'required': False,
                                            'default': ''
                                        },
                                        'port': {
                                            'type': 'integer',
                                            'required': False,
                                            'default': 22
                                        },
                                        'username': {
                                            'type': 'string',
                                            'required': True
                                        },
                                        'password': {
                                            'type': 'string',
                                            'required': False,
                                            'default': ''
                                        },
                                        'reconnect': {
                                            'type': 'boolean',
                                            'required': False,
                                            'default': True
                                        },
                                        'password_from_sm': {
                                            'type': 'dict',
                                            'required': False,
                                            'schema' : {
                                                'secretManager': {
                                                    'type': 'string',
                                                    'required': True,
                                                    'allowed': ['cyberark', 'vault']
                                                },
                                                'key': {
                                                    'type': 'string',
                                                    'required': True
                                                }
                                            }
                                        },
                                        'password_from_env': {
                                            'type': 'dict',
                                            'required': False,
                                            'schema' : {
                                                'key': {
                                                    'type': 'string',
                                                    'required': True
                                                }
                                            }
                                        }
                                    }
                                },
                                'configBackup': {
                                    'type': 'dict',
                                    'required': False,
                                    'schema': {
                                        'comment': {
                                            'type': 'string',
                                            'required': True,
                                        },
                                        'after_commands': {
                                            'type': 'boolean',
                                            'required': False,
                                            'default': False
                                        },
                                        'target': {
                                            'type': 'string',
                                            'required': False,
                                            'default': 'local',
                                            'allowed': ['local', 's3']
                                        },
                                        'onlyOn': {
                                            'type': 'list',
                                            'required': False,
                                            'default': []
                                        },
                                        'skip': {
                                            'type': 'list',
                                            'required': False,
                                            'default': []
                                        }
                                    }
                                },
                                'commands': {
                                    'type': 'list',
                                    'required': True,
                                    'schema': {
                                        'type': 'dict',
                                        'schema': {
                                            'command': {
                                                'type': 'string',
                                                'required': True
                                            },
                                            'tag': {
                                                'type': 'string',
                                                'required': False,
                                                'default': ''
                                            },
                                            'exit_on_fail': {
                                                'type': 'boolean',
                                                'required': False,
                                                'default': True
                                            },
                                            'ask_for_confirmation': {
                                                'type': 'boolean',
                                                'required': False,
                                                'default': False
                                            },
                                            'onlyOn': {
                                                'type': 'list',
                                                'required': False,
                                                'default': []
                                            },
                                            'skip': {
                                                'type': 'list',
                                                'required': False,
                                                'default': []
                                            },
                                            'when': {
                                                'type': 'dict',
                                                'required': False,
                                                'default': {},
                                                'schema': {
                                                    'tag': {
                                                        'type': 'string',
                                                        'required': False,
                                                        'default': ''
                                                    },
                                                    'operator': {
                                                        'type': 'string',
                                                        'required': False,
                                                        'allowed': ['is', 'is_not'],
                                                        'default': 'is'
                                                    },
                                                    'exit_code': {
                                                        'type': 'integer',
                                                        'required': False,
                                                        'default': 100 # indication of non-user-input 
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        try:
            # Get the parsed YAML (dct)
            parsed_yaml = self.parse_yaml()
            # Validating each doc in the YAML file seperately
            for doc in parsed_yaml:
                v = cerberus.Validator(schema_dct)
                v.validate(doc, schema_dct)
                # If validation errors found, print them.
                if v.errors:
                    rich.print(f"[bold]ERROR --  Found the following erros while validating the YAML file '{self.yaml_file}'")
                    rich.print("\t -> Please fix the following:")
                    rich.print(v.errors)
                    exit(1)
                if print_msg:
                    rich.print(f"{self.yaml_file} Validated, [bold green]Seems OK !")
                    exit(0)
                else:
                    self.validated_documents.append(v.document)
            return self.validated_documents
        except (cerberus.schema.SchemaError) as e:
            rich.print(f"[bold]ERROR -- YAML Validation Failed[/bold]\n> {e}")

    def parse_yaml(self):
        try:
            with open("test.yaml", "r") as f:
                doc = yaml.safe_load_all(f)
                return list(doc)
        except (yaml.YAMLError, ) as e:
            rich.print(f"[bold]ERROR -- Error while parsing YAML file: [underline]{self.yaml_file}")
            if hasattr(e, 'problem_mark'):
                if e.context != None:
                    print (str(e.problem_mark) + '\n  ' + str(e.problem) + ' ' + str(e.context) + '\n[yellow]Please correct data and retry.')
                    exit(1)
                else:
                    rich.print (str(e.problem_mark) + '\n  ' + str(e.problem) + '\n[yellow]Please correct data and retry.')
                    exit(1)
            else:
                print ("ERROR -- Something went wrong while parsing yaml file")


y = YamlParser('test.yaml')

validated_docs = y.validate_yaml(print_msg=False)
for doc in validated_docs:
    rich.print(doc)
    rich.print(f"TASK: {doc.get('Task').get('name')}")
    for subtask in doc.get('Task').get('subTask'):
        # print(subtask.get('name'))
        task.sub_task(name=subtask.get('name'), group=subtask.get('authenticate').get('group'), username=subtask.get('authenticate').get('username'), password=subtask.get('authenticate').get('password'), port=subtask.get('authenticate').get('port'), cmds=subtask.get('commands'), reconnect=subtask.get('authenticate').get('reconnect'))

# parsed_dct = y.parse_yaml()
# rich.print(parsed_dct)


# [
#             {
#                 "command": "show ip int br", 
#                 "tag": "123df",
#             },
#             {
#                 "command": "show vlan br", 
#                 "when": {"tag": "123df", "exit_code": 1, 'operator': 'is'}
#             },
#             {
#                 "command": "show vlan br", 
#             }
#         ]