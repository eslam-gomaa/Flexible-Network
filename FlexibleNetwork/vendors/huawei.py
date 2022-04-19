class Huawei:
    def __init__(self):
        self._stderr_search_keyword = ['\^', '^%']
        self._clean_output_search_keywords = ['.*#', '.*>']
        self._backup_command = """
            screen-length 0
            display current-configuration
            undo screen-length
            """


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
