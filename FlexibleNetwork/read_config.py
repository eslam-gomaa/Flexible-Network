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
            # info['default_vendor'] = config.get(section_name, 'default_vendor').strip('"')
            info['default_inventory'] = config.get(section_name, 'default_inventory').strip('"')
            return info
        except configparser.NoOptionError as e:
            raise SystemExit("ERROR -- Accessing the section '{}'\n> {}".format(section_name, e))

    def section_cyberark(self, section_name='cyberark'):
        try:
            config = configparser.ConfigParser(comment_prefixes=('#',';'), inline_comment_prefixes=('#',';'))
            config.read(self.configuration_file)
            # section = dict(config.items(section_name))
            info = {}
            info['url'] = config.get(section_name, 'url').strip('"')
            info['username'] = config.get(section_name, 'username').strip('"')
            info['password'] = config.get(section_name, 'password').strip('"')
            info['verify_ssl'] = config.get(section_name, 'verify_ssl').strip('"')
            info['concurrent_session'] = config.get(section_name, 'concurrent_session').strip('"')
            info['authentication_method'] = config.get(section_name, 'authentication_method').strip('"')
            return info
        except configparser.NoOptionError as e:
            raise SystemExit("ERROR -- Accessing the section '{}'\n> {}".format(section_name, e))

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
            raise SystemExit("ERROR -- Accessing the section '{}'\n> {}".format(section_name, e))

    def section_s3(self, section_name='s3'):
        try:
            config = configparser.ConfigParser(comment_prefixes=('#',';'), inline_comment_prefixes=('#',';'))
            config.read(self.configuration_file)
            # section = dict(config.items(section_name))
            info = {}
            info['endpoint'] = config.get(section_name, 'endpoint').strip('"').strip("'")
            info['ak'] = config.get(section_name, 'ak').strip('"').strip("'")
            info['sk'] = config.get(section_name, 'sk').strip('"').strip("'")
            info['region'] = config.get(section_name, 'region').strip('"').strip("'")
            info['bucket'] = config.get(section_name, 'bucket').strip('"').strip("'")
            info['create_bucket'] = config.get(section_name, 'create_bucket').strip('"').strip("'")
            return info
        except configparser.NoOptionError as e:
            raise SystemExit("ERROR -- Accessing the section '{}'\n> {}".format(section_name, e))

    


