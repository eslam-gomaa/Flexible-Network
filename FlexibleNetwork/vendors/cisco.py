
class Cisco:
    def __init__(self):
        # If needed check that error messgaes list
        # https://www.cisco.com/c/en/us/td/docs/security/ips/7-2/command/reference/cmdref72/crError.pdf
        self._stderr_search_keyword = ['\^', '^%', 'Translating.*(255.255.255.255)']
        self._clean_output_search_keywords = ['.*#', '.*>']
        self._backup_command = """
            terminal length 0
            show run
            term no len 0
            """
        self.backup_command_config_mode = """
            do terminal length 0
            do show run
            do term no len 0
            """
        self.priviliged_mode_command = "enable"


    @property
    def stderr_search_keyword(self):
        return self._stderr_search_keyword

    @stderr_search_keyword.setter
    def stderr_search_keyword(self, keyword):
        self._stderr_search_keyword = keyword

    @property
    def clean_output_search_keywords(self):
        return self._clean_output_search_keywords
    
    @clean_output_search_keywords.setter
    def clean_output_search_keywords(self, keyword):
        self._clean_output_search_keywords = keyword

    @property
    def backup_command(self):
        return self._backup_command

    @backup_command.setter
    def backup_command(self, keyword):
        self._stderr_search_keyword = keyword



# https://community.cisco.com/t5/other-security-subjects/shunnig-issues-error-syntax-error-from-invalid-input-at-device/td-p/172338
# https://support.huawei.com/enterprise/en/doc/EDOC1100112346/46c4f52c/interpreting-command-line-error-messages
