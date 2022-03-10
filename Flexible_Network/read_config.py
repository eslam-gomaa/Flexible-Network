# https://docs.python.org/3/library/configparser.html
import configparser
import os

class ReadCliOptions:
    task_name = None

    def __init(self):
        self.task_name

class Config():

    def __init__(self):
        self.config_type = "FILE" # FILE || ENV
        # self.configuration_file = "/home/orange/work_dir/Flexible-Network/user/flexible_network.cfg" # Path to configuration file
        self.configuration_file = "user/flexible_network.cfg" # Path to configuration file

    def set_configuration_type(self, type):
        self.config_type = type
        if self.config_type not in ["FILE", "ENV"]:
            raise ValueError("configuration_type supported options are: {}".format(["FILE", "ENV"]))

    def Check_configuration_file(self, file):
        if self.config_type == "File":
            if not os.path.isfile(file):
                raise ValueError("ERROR -- Configuration file '{}' is NOT found".format(file))
     
    def set_configuration_file(self, file):
        self.configuration_file = file
        self.Check_configuration_file(file)

    def section_vault(self, section_name='vault'):
        try:
    
            config = configparser.ConfigParser(comment_prefixes=('#',';'), inline_comment_prefixes=('#',';'))
            config.read(self.configuration_file)
            # section = dict(config.items(section_name))
            info = {}
            info['url'] = config.get(section_name, 'url').strip('"')
            info['token'] = config.get(section_name, 'token').strip('"')
            info['engine'] = config.get(section_name, 'engine').strip('"')
            return info
        except:
            raise ValueError("ERROR -- Accessing the section '{}'".format(section_name))

    def section_rocket_chat(self, section_name='rocket_chat'):
        if self.config_type == 'FILE':
            self.Check_configuration_file(self.configuration_file)
        try:
            config = configparser.ConfigParser(comment_prefixes=('#',';'), inline_comment_prefixes=('#',';'))
            config.read(self.configuration_file)
            # section = dict(config.items(section_name))
            info = {}
            info['url'] = config.get(section_name, 'url').strip('"')
            info['username'] = config.get(section_name, 'username').strip('"')
            info['password'] = config.get(section_name, 'password').strip('"')
            return info
        except:
            raise ValueError("ERROR -- Accessing the section '{}'".format(section_name))


    def section_s3(self, section_name='s3'):
        try:
            config = configparser.ConfigParser(comment_prefixes=('#',';'), inline_comment_prefixes=('#',';'))
            config.read(self.configuration_file)
            # section = dict(config.items(section_name))
            info = {}
            info['url'] = config.get(section_name, 'url').strip('"')
            info['ak'] = config.get(section_name, 'ak').strip('"')
            info['sk'] = config.get(section_name, 'sk').strip('"')
            info['bucket'] = config.get(section_name, 'bucket').strip('"')
            return info
        except:
            raise ValueError("ERROR -- Accessing the section '{}'".format(section_name))

    


