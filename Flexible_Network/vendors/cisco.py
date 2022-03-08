
from tkinter import N


class Cisco:
    def __init__(self):
        self._stderr_search_keyword = '\^'
        self._clean_output_search_keyword = '.*#'
        self._backup_command = """
            terminal length 0
            show run
            term no len 0
            """


    @property
    def stderr_search_keyword(self):
        return self._stderr_search_keyword

    @stderr_search_keyword.setter
    def stderr_search_keyword(self, keyword):
        self._stderr_search_keyword = keyword

    # @stderr_search_keyword.deleter
    # def stderr_search_keyword(self):
    #     self._stderr_search_keyword = None
    ########### ############ ############
    ## To delete the attribute ##
    # del instance.stderr_search_keyword


    @property
    def clean_output_search_keyword(self):
        return self._clean_output_search_keyword
    
    @clean_output_search_keyword.setter
    def clean_output_search_keyword(self, keyword):
        self._clean_output_search_keyword = keyword

    @property
    def backup_command(self):
        return self._backup_command

    @backup_command.setter
    def backup_command(self, keyword):
        self._backup_command = keyword



# https://community.cisco.com/t5/other-security-subjects/shunnig-issues-error-syntax-error-from-invalid-input-at-device/td-p/172338
# https://support.huawei.com/enterprise/en/doc/EDOC1100112346/46c4f52c/interpreting-command-line-error-messages
