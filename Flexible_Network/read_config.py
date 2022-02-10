import configparser
# https://docs.python.org/3/library/configparser.html
import os
# pip3 install configparser

class Config():
    def __init__(self):
        self.configuration_file = "/home/orange/work_dir/Flexible-Network/Flexible_Network/flexible_network.cfg"
        if not os.path.isfile(self.configuration_file):
            raise Exception("[ ERROR ] -- Configuration file '{}' is NOT found".format(self.configuration_file))


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
            raise Exception("ERROR .. Accessing the section '{}'".format(section_name))

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
        except:
            raise Exception("ERROR .. Accessing the section '{}'".format(section_name))


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
            raise Exception("ERROR .. Accessing the section '{}'".format(section_name))