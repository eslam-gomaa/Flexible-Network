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
                    'log_format' : {
                    'type': 'string',
                    'required': False,
                    'default': 'markdown',
                    'allowed': ['txt', 'markdown']
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
                                            'type': 'dict',
                                            'required': False,
                                            'default': {},
                                            'schema' : {
                                                "value": {
                                                    'type': 'string',
                                                    'required': False,
                                                    'default': ""
                                                    
                                                },
                                                "value_from_env": {
                                                    'type': 'dict',
                                                    'required': False,
                                                    'default': {},
                                                    'schema': {
                                                        "key": {
                                                            'type': 'string',
                                                            'required': True,
                                                            'default': ""
                                                        }
                                                    }
                                                }                                               
                                            }
                                        },
                                        'password': {
                                            'type': 'dict',
                                            'required': False,
                                            'default': {},
                                            'schema' : {
                                                "value": {
                                                    'type': 'string',
                                                    'required': False,
                                                    'default': ""
                                                    
                                                },
                                                "value_from_env": {
                                                    'type': 'dict',
                                                    'required': False,
                                                    'default': {},
                                                    'schema': {
                                                        "key": {
                                                            'type': 'string',
                                                            'required': True,
                                                            'default': ""
                                                        }
                                                    }
                                                }                                               
                                            }
                                        },
                                        'privileged_mode_password': {
                                            'type': 'dict',
                                            'required': False,
                                            'default': {},
                                            'schema' : {
                                                "value": {
                                                    'type': 'string',
                                                    'required': False,
                                                    'default': ""
                                                    
                                                },
                                                "value_from_env": {
                                                    'type': 'dict',
                                                    'required': False,
                                                    'default': {},
                                                    'schema': {
                                                        "key": {
                                                            'type': 'string',
                                                            'required': True,
                                                            'default': ""
                                                        }
                                                    }
                                                }                                               
                                            }
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
                                            'default': {},
                                            'schema' : {
                                                'key': {
                                                    'type': 'string',
                                                    'required': False,
                                                    'default': ""
                                                }
                                            }
                                        }
                                    }
                                },
                                'configBackup': {
                                    'type': 'dict',
                                    'required': False,
                                    'default': {},
                                    'schema': {
                                        'comment': {
                                            'type': 'string',
                                            'required': True,
                                            'default': ""
                                        },
                                        'exit_on_fail': {
                                            'type': 'boolean',
                                            'required': False,
                                            'default': True
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
            with open(self.yaml_file, "r") as f:
                doc = yaml.safe_load_all(f)
                return list(doc)
        except (yaml.YAMLError, ) as e:
            rich.print(f"[bold]ERROR -- Error while parsing YAML file: [underline]{self.yaml_file}")
            if hasattr(e, 'problem_mark'):
                if e.context != None:
                    rich.print (str(e.problem_mark) + '\n  ' + str(e.problem) + ' ' + str(e.context) + '\n[yellow]Please correct the YAML file and retry.')
                    exit(1)
                else:
                    rich.print (str(e.problem_mark) + '\n  ' + str(e.problem) + '\n[yellow]Please correct the YAML file and retry.')
                    exit(1)
            else:
                print ("ERROR -- Something went wrong while parsing yaml file")
                
