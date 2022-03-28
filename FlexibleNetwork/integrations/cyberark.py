import requests
import json
from urllib3.exceptions import InsecureRequestWarning
from FlexibleNetwork.Flexible_Network import Config


requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
# https://stackoverflow.com/a/41041028
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'

class Cyberark_APIs_v2:

    def __init__(self):
        """
        Authenticate with the Cyberark server
        """
        config = Config()
        config_data = config.section_cyberark()
        self.cyberark_url = config_data['url']
        self.concurrent_session = bool(config_data['concurrent_session'])
        self.username = config_data['username']
        self.password = config_data['password']
        self.authentication_method = config_data['authentication_method']
        self.allowed_authentication_methods = ['LDAP', 'CyberArk']
        self.cyberark_session_token = None
        self.verify_ssl = bool(config_data['verify_ssl'])
        # It's important to have one session object for all the suXbsequent requests 
        # (Because it keeps the cookies sent by the Cyberark sever at authentication and resend them at subsequent requests)
        # That is important if there is a Load balancer on top (which uses the cookies for session persistence [Direct to the same client to the same server] ) 
        self.session = requests.Session()

    def authenticate(self):
        """
        Returns the session token
        """
        url = f"{self.cyberark_url}/PasswordVault/API/auth/LDAP/Logon"
        try:
            
            self.session.verify = self.verify_ssl
            req = self.session.post(url, data={"username": self.username,
                                        "password": self.password,
                                        "concurrentSession": self.concurrent_session})

            if req.status_code == int(200):
                self.cyberark_session_token = req.text.strip('\"') # Remove " from the start and end.
                # print(req.cookies)
                return req.text.strip('\"')
            else:
                print(f"Cyberark Authentication Failed \n> {req.text}")
                raise SystemExit(f"ERROR -- Failed Request to {url} , {req.status_code} , {req.reason})")
        except requests.exceptions.RequestException as e:
            print(f"ERROR -- Cyberark Authentication Failed \n")
            raise SystemExit(f"> {e}")

    def authenticate_raw(self):
        """
        Returns the session token
        """
        url = f"{self.cyberark_url}/PasswordVault/API/auth/LDAP/Logon"
        try:
            
            self.session.verify = self.verify_ssl
            req = self.session.post(url, data={"username": self.username,
                                        "password": self.password,
                                        "concurrentSession": self.concurrent_session})

            if req.status_code == int(200):
                return {"success": True, 'fail_reason': ''}
            else:
                return {"success": False, 'fail_reason': f"Cyberark Authentication Failed \n> {req.text} \n> Failed Request to {url} , {req.status_code} , {req.reason})"}
        except requests.exceptions.RequestException as e:
            return {"success": False, 'fail_reason': str(e)}


    def logoff(self):
        """
        Returns the session token
        """
        url = f"{self.cyberark_url}/PasswordVault/API/Auth/Logoff"
        try:
            self.session.verify = self.verify_ssl
            headers = {"Authorization": self.cyberark_session_token}
            req = self.session.post(url, headers=headers)

            if req.status_code == int(200):
                return 'success'
            else:
                print(req.text)
                raise SystemExit(f"ERROR -- Failed Request to {url} , {req.status_code} , {req.reason})")
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)


    def get_all_safes(self):
        """
        Returns all the safes
        """
        if self.cyberark_session_token is None:
            self.authenticate()
        url = f"{self.cyberark_url}/PasswordVault/api/Safes"
        try:
            self.session.verify = self.verify_ssl
            headers = {"Authorization": self.cyberark_session_token}
            req = self.session.get(url, headers=headers)

            if req.status_code == int(200):
                response_data = json.loads(req.text)
                return response_data.get('Safes')
            else:
                print(req.text)
                raise SystemExit(f"ERROR -- Failed Request to {url} , {req.status_code} , {req.reason})")
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)


    def get_account_details(self, account_id):
        """
        Returns the account details
        INPUT: the account ID
        """
        if self.cyberark_session_token is None:
            self.authenticate()
        url = f"{self.cyberark_url}/PasswordVault/api/Accounts/{account_id}"
        try:
            self.session.verify = self.verify_ssl
            headers = {"Authorization": self.cyberark_session_token}
            req = self.session.get(url, headers=headers)

            if req.status_code == int(200):
                response_data = json.loads(req.text)
                return response_data
            else:
                print(req.text)
                raise SystemExit(f"ERROR -- Failed Request to {url} , {req.status_code} , {req.reason})")
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

    def search_accounts(self, search=None, safe=None):
        """
        This method returns a list of all the accounts in the Vault.
        INPUT
            1. search_keyword (Optional)
            2. safe_name      (Optional)
        https://docs.cyberark.com/Product-Doc/OnlineHelp/PrivCloud/Latest/en/Content/SDK/GetAccounts.htm?tocpath=Developers%7CREST%20APIs%7CAccounts%7C_____1
        """
        if self.cyberark_session_token is None:
            self.authenticate()
        url = f"{self.cyberark_url}/PasswordVault/api/Accounts"
        filter_sign = '?'
        if search is not None:
            url = url + "?search={}".format(search)
            filter_sign = '&'
        if safe is not None:
            url = url + f"{filter_sign}filter=safeName eq {safe}"
        try:
            self.session.verify = self.verify_ssl
            headers = {"Authorization": self.cyberark_session_token}
            req = self.session.get(url, headers=headers)

            if req.status_code == int(200):
                response_data = json.loads(req.text)
                return response_data.get('value')
            else:
                print(req.text)
                raise SystemExit(f"ERROR -- Failed Request to {url} , {req.status_code} , {req.reason})")
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

    def get_account_password(self, account_id):
        """
        This method enables users to retrieve the password or SSH key of an existing account that is identified by its Account ID.
        INPUT: The account ID
        https://docs.cyberark.com/Product-Doc/OnlineHelp/PrivCloud/Latest/en/Content/WebServices/GetPasswordValueV10.htm?tocpath=Developers%7CREST%20APIs%7CAccounts%7CAccount%20actions%7C_____3
        """
        self.authenticate()
        if self.cyberark_session_token is None:
            self.authenticate()
        url = f"{self.cyberark_url}/PasswordVault/api/Accounts/{account_id}/Password/Retrieve"
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
        try:
            self.session.verify = self.verify_ssl
            # token = 'MDhkM2Y3ZTItNGI0NC00NjIyLWJjZTMtZTI5MzVhM2IyOTg3O0QxN0ZCMUIwQzg1MzI1MTU7MDAwMDAwMDI5NTFFQzQ5OUQ3M0NGMTcxNUE0NzkwNTgzOEU1MEM4N0IwQTk3QjhGQzdGQzY5RkI3ODkwMDA3Njk2NUFENERDMDAwMDAwMDA7'
            headers = {"Authorization": self.cyberark_session_token}
            
            data = {"Reason": "NoReason",
                    "TicketingSystemName": "Jira",
                    "TicketId": "12345",
                    "Version": "0", # Set the version to 0 to get the current password
                    "ActionType": "copy",
                    "IsUse": "false",
                    "Machine":  "10.72.18.65",
                    "Content-Type": "application/json"
                    }
            req = self.session.post(url, headers=headers, data=data)

            if req.status_code == int(200):
                response_data = json.loads(req.text)
                return response_data
            else:
                print(req.text)
                raise SystemExit(f"ERROR -- Failed Request to {url} , {req.status_code} , {req.reason})")
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
    
    def update_account_password(self, account_id, new_password):
        """
        This method enables users to set account credentials and change them in the Vault.
        This will not affect credentials on the target device.
        INPUT: 
            1. The account ID    
            2. The new password
        Notes
        1. Digits are never placed as the first or last character of the password, regardless of the password policy or specifications.
        2. If the specified password contains leading and/or trailing white spaces, they will automatically be removed.
        https://docs.cyberark.com/Product-Doc/OnlineHelp/PrivCloud/Latest/en/Content/WebServices/ChangeCredentialsInVault.htm?tocpath=Developers%7CREST%20APIs%7CAccounts%7CAccount%20actions%7C_____10
        """
        if self.cyberark_session_token is None:
            self.authenticate()
        url = f"{self.cyberark_url}/PasswordVault/api/Accounts/{account_id}/Password/Update"
        try:
            self.session.verify = self.verify_ssl
            headers = {"Authorization": self.cyberark_session_token}
            
            data = {"NewCredentials": new_password}
            req = self.session.post(url, headers=headers, data=data)

            if req.status_code == int(200):
                response_data = json.loads(req.text)
                return response_data
            else:
                print(req.text)
                raise SystemExit(f"ERROR -- Failed Request to {url} , {req.status_code} , {req.reason})")
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

    def delete_account(self, account_id):
        """
        This method deletes a specific account in the Vault.
        INPUT: the account ID
        https://docs.cyberark.com/Product-Doc/OnlineHelp/PrivCloud/Latest/en/Content/WebServices/Delete%20Account.htm?TocPath=Developers%7CREST%20APIs%7CAccounts%7C_____8
        """
        if self.cyberark_session_token is None:
            self.authenticate()
        url = f"{self.cyberark_url}/PasswordVault/api/Accounts/{account_id}"
        try:
            self.session.verify = self.verify_ssl
            headers = {"Authorization": self.cyberark_session_token}
            req = self.session.delete(url, headers=headers)

            if req.status_code == int(204):
                return "success"
            elif req.status_code == int(404):
                print(f"WARNING -- Account [ {account_id} ] NOT found")
            else:
                print(req.text)
                raise SystemExit(f"ERROR -- Failed Request to {url} , {req.status_code} , {req.reason})")
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

    def add_account(self, name, address, userName, safeName, secretType, secret, platformId, platformAccountProperties={}):
        """
        This method deletes a specific account in the Vault.
        https://docs.cyberark.com/Product-Doc/OnlineHelp/PrivCloud/Latest/en/Content/WebServices/Delete%20Account.htm?TocPath=Developers%7CREST%20APIs%7CAccounts%7C_____8
        """
        if self.cyberark_session_token is None:
            self.authenticate()
        url = f"{self.cyberark_url}/PasswordVault/api/Accounts"
        try:
            self.session.verify = self.verify_ssl
            headers = {"Authorization": self.cyberark_session_token}
            data = {"name": name,
                    "address": address,
                    "userName": userName,
                    "platformId": platformId,
                    "secretType": secretType,
                    "safeName": safeName,
                    "secret":  secret,
                    "secretManagement": {
                        "automaticManagementEnabled": True,
                        "manualManagementReason": "NoReason"},
                    "platformAccountProperties": platformAccountProperties,
                    "Content-Type": "application/json"
                    }
            req = self.session.post(url, headers=headers, data=data)
            if req.status_code == int(201):
                response_data = json.loads(req.text)
                return response_data
            elif req.status_code == int(409):
                print(f"WARNING -- Account [ {name} ] Already exists")
            else:
                print(req.text)
                raise SystemExit(f"ERROR -- Failed Request to {url} , {req.status_code} , {req.reason})")
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)