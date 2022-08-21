
class Cisco:
    def __init__(self):
        # If needed check that error messgaes list
        # https://www.cisco.com/c/en/us/td/docs/security/ips/7-2/command/reference/cmdref72/crError.pdf
        self.stderr_search_keyword = ['\^', '^%', 'Translating.*(255.255.255.255)']
        self.clean_output_search_keywords = ['.*#', '.*>']
        self.backup_command = """
            terminal length 0
            show run
            term no len 0
            """
        self.priviliged_mode_command = "enable"
        self.configure_mode_command = "configure terminal"
        self.back_command = "exit"
        



# https://community.cisco.com/t5/other-security-subjects/shunnig-issues-error-syntax-error-from-invalid-input-at-device/td-p/172338
# https://support.huawei.com/enterprise/en/doc/EDOC1100112346/46c4f52c/interpreting-command-line-error-messages
