from FlexibleNetwork.Flexible_Network import Config
from FlexibleNetwork.Flexible_Network import ReadCliOptions
import os
import configparser

class Inventory():
    # Define 'inventory_file' as a class level attribute, so that I can update it from the cli class 
    # Need to specify the default value in the configuration file

    def __init__(self):
        # Check the input is file
        if ReadCliOptions.inventory_file is None:
            pass
            config = Config()
            config_data = config.section_general()
            self.inventory_file = config_data['default_inventory']
        else:
            self.inventory_file = ReadCliOptions.inventory_file

        # Check that the inventory file is an actual file
        if not os.path.isfile(self.inventory_file):
                print("ERROR -- Inventory file '{}' is NOT found".format(self.inventory_file))
                exit(1)

        self.inventory = None

    def read_inventory(self):
        """ 
        Read the hosts into groups 
        Returns list of dicts (each dict is a list of hosts)
        """
        try:
            config = configparser.ConfigParser(comment_prefixes=('#',';'), inline_comment_prefixes=('#',';'), allow_no_value=True, strict=False)
            config.read(self.inventory_file)
            # List of sections
            sections = config.sections()
            out = {}
            all = {}
            for section in sections:
                # get the values of each section (key, pair)
                out[section] = dict(config.items(section))
                # Add the section to the all dict
                all = dict(all, **out[section])
            # the 'all' section has all the hosts from all the groups.
            out['all'] = all
            # self.inventory = out
            return out
        except configparser.NoOptionError as e:
            print("ERROR -- Accessing the group in the inventory \n> {}".format, e)
            exit(1)

        
    def get_section(self, section):
        try:
            sections = self.read_inventory()
            if section in sections:
                return sections[section]
            else:
                return None
        except:
            print("ERROR -- could NOT read section [ {} ] !".format(section))
            exit(1)
