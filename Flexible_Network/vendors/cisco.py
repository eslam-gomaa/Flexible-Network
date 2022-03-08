class Cisco:
    def __init(self):
        pass

    def stderr_search_keyword(self):
        return '\^'

    def clean_output_search_keyword(self):
        return '.*#'

    def backup_command(self):
        return """
        terminal length 0
        show run
        term no len 0
        """


# https://community.cisco.com/t5/other-security-subjects/shunnig-issues-error-syntax-error-from-invalid-input-at-device/td-p/172338
# https://support.huawei.com/enterprise/en/doc/EDOC1100112346/46c4f52c/interpreting-command-line-error-messages
