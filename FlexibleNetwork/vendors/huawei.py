class Huawei:
    def __init__(self):
        self.stderr_search_keyword = ['\^', '^%']
        self.clean_output_search_keywords = ['.*#', '.*>']
        self.backup_command = """
            screen-length 0
            display current-configuration
            undo screen-length
            """
        self.priviliged_mode_command = "super"
        self.configure_mode_command = "system-view"
        self.back_command = "quit"


# https://ipwithease.com/cisco-and-huawei-equivalent-commands/

# https://community.cisco.com/t5/other-security-subjects/shunnig-issues-error-syntax-error-from-invalid-input-at-device/td-p/172338
# https://support.huawei.com/enterprise/en/doc/EDOC1100112346/46c4f52c/interpreting-command-line-error-messages
