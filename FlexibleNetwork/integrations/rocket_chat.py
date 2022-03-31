
from requests import sessions
from rocketchat_API.rocketchat import RocketChat # https://github.com/jadolg/rocketchat_API
from rocketchat_API.APIExceptions import RocketExceptions
from FlexibleNetwork.Flexible_Network import Config
import requests


class RocketChat_API():

    def __init__(self):
        """ Authenticate with RocketChat Server """
        self.auth_session = None

    def auth_raw(self):
        """ Authenticate with RocketChat Server [ Without Exception handeling ] """
        config = Config()
        config_data = config.section_rocket_chat()
        try:
            with sessions.Session() as session:
                rocket = RocketChat(config_data["username"], 
                                    config_data["password"],
                                    server_url=config_data["url"],
                                    session=session)
            self.auth_session = rocket
            return {'success': True, 'fail_reason': ''} 
        except (RocketExceptions.RocketAuthenticationException, 
                RocketExceptions.RocketConnectionException,
                RocketExceptions.RocketMissingParamException,):
            # The RocketChat exceptions doesn't return messages, so I'll assume that it's an authentication issue.
            # (Since all other connection issues are raised via requests exceptoins)
            return {'success': False, 'fail_reason': 'Authentication Failed'}
        except (requests.exceptions.RequestException, requests.exceptions.MissingSchema) as e :
            return {'success': False, 'fail_reason': str(e)}



    def authenticate(self):
        """ Authenticate with RocketChat Server """
        try:
            self.auth_raw()
        except:
            raise SystemExit("ERROR -- Failed to authenticate RocketChat")

    def list_channels(self):
        if self.auth_session is None:
            self.authenticate()
        """ Returns a list of all channels """
        return self.auth_session.channels_list().json()['channels']

    def list_all_members(self):
        """ Return a list of all users """
        if self.auth_session is None:
            self.authenticate()
        lst = self.auth_session.users_list(count=0).json()
        return lst

    def channel_info(self, channel_id):
        pass

    def list_members_in_channel(self, channel_id):
        if self.auth_session is None:
            self.authenticate()
        output = self.auth_session.channels_members(channel_id).json()
        members_count, members_list = output['count'], output['members']
        return members_list

    def member_info(self, member_id):
        """
        returns user info (Apply rate limiting in my case !)
        """
        if self.auth_session is None:
            self.authenticate()
        output = self.auth_session.users_info(member_id).json()
        return output

    def send_message_by_member_id(self, member_id, message):
        """ 
        Send message to a member or Channel 
        """
        if self.auth_session is None:
            self.authenticate()
        output = self.auth_session.chat_post_message(message, channel=member_id).json()
        return output

    def return_member_id_by_name(self, member_name):
        """
        Search for the id of the user using the name
        """
        if self.auth_session is None:
            self.authenticate()
        for member in self.list_all_members()['users']:
            if member['username'] == member_name:
                    return member['_id']

    def send_message(self, member_name_lst, message):
        """
        Send a RocketChat message to a list of members
        INPUT:
            1. member_name_lst -> (List of strings)  users to send messages to.
            2. message -> (String)  Message to send
        """
        if not isinstance(member_name_lst, list):
            print("ERROR -- RocketChat method 'send_message' takes a List of users\n> You've provided: '{}' which is a {}".format(member_name_lst, type(member_name_lst)))
            exit(1)
        if self.auth_session is None:
            self.authenticate()
        out = {}
        for member_name in member_name_lst:
            id = self.return_member_id_by_name(member_name)
            member_out = {}
            member_out['success'] = None
            member_out['fail_reason'] = None
            if id is not None:
                msg = self.send_message_by_member_id(id, message)
                member_out['success'] = True
            else:
                member_out['success'] = False
                member_out['fail_reason'] = "Can NOT find the username"
            out[member_name] = member_out
        return out

    def send_as_attachment(self):
        if self.auth_session is None:
            self.authenticate()
        pass