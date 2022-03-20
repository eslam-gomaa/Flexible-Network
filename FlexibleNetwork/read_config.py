# https://docs.python.org/3/library/configparser.html
import configparser
import os
from FlexibleNetwork.Flexible_Network import ReadCliOptions
# from flexible_network.read_cli_options import ReadCliOptions


class Config():
    def __init__(self):
        self.config_type = "FILE" # FILE || ENV
        # Default configuration file path
        self.configuration_file = "/etc/flexible_network/flexible_network.cfg"
        # Update the configuration file path if given as a cli option.
        if ReadCliOptions.config_file is not None:
            self.configuration_file = ReadCliOptions.config_file
        # Validate that the configuration file exists
        if self.config_type == "FILE":
            if not os.path.isfile(self.configuration_file):
                print("\nERROR -- Configuration file '{}' is NOT found".format(self.configuration_file))
                exit(1)
        # Maybe need to check if the config file is valid before start parsing it.

    def section_general(self, section_name='general'):
        try:
            config = configparser.ConfigParser(comment_prefixes=('#',';'), inline_comment_prefixes=('#',';'))
            config.read(self.configuration_file)
            # section = dict(config.items(section_name))
            info = {}
            info['default_vendor'] = config.get(section_name, 'default_vendor').strip('"')
            info['default_inventory'] = config.get(section_name, 'default_inventory').strip('"')
            return info
        except configparser.NoOptionError as e:
            print("ERROR -- Accessing the section '{}'\n> {}".format(section_name, e))
            exit(1)
            # raise ValueError("ERROR -- Accessing the section '{}'".format(section_name))

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
        except configparser.NoOptionError as e:
            print("ERROR -- Accessing the section '{}'\n> {}".format(section_name, e))
            exit(1)
            # raise ValueError("ERROR -- Accessing the section '{}'".format(section_name))

    def section_rocket_chat(self, section_name='rocket_chat'):
        try:
            config = configparser.ConfigParser(comment_prefixes=('#',';'), inline_comment_prefixes=('#',';'))
            config.read(self.configuration_file)
            # section = dict(config.items(section_name))
            info = {}
            info['url'] = config.get(section_name, 'url').strip('"')
            info['username'] = config.get(section_name, 'username').strip('"')
            info['password'] = config.get(section_name, 'password').strip('"')
            return info
        except configparser.NoOptionError as e:
            print("ERROR -- Accessing the section '{}'\n> {}".format(section_name, e))
            exit(1)
            # raise ValueError("ERROR -- Accessing the section '{}'".format(section_name))


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
        except configparser.NoOptionError as e:
            print("ERROR -- Accessing the section '{}'\n> {}".format(section_name, e))
            exit(1)
            # raise ValueError("ERROR -- Accessing the section '{}'".format(section_name))

    


