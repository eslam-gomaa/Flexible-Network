# if __name__ == '__main__':
#     from os import path
#     import sys
#     sys.path.append(path.join(path.dirname(__file__), '..'))

from distutils.log import info
from Flexible_Network.read_config import Config
from requests import sessions
from rocketchat_API.rocketchat import RocketChat # https://github.com/jadolg/rocketchat_API


class RocketChat_API():
    config = Config()
    config_data = config.section_rocket_chat()

    def __init__(self, username=config_data["username"], password=config_data["password"], url=config_data["url"]):
        """ Authenticate with RocketChat Server """
        self.auth_session = None
        try:
            with sessions.Session() as session:
                rocket = RocketChat(username, 
                                    password,
                                    server_url=url,
                                    session=session)
            self.auth_session = rocket
        except:
            raise ConnectionError("Failed to authenticate to RocketChat Server {} with {}".format(url, username))


    def list_members_channels(self):
        """ List members and Channels """
        return self.auth_session.channels_list().json()['channels']

    def list_all_members(self):
        """ Return a list of all users """
        lst = self.auth_session.users_list(count=0).json()
        return lst

    def channel_info(self, channel_id):
        pass

    def list_members_in_channel(self, channel_id):
        output = self.auth_session.channels_members(channel_id).json()
        members_count, members_list = output['count'], output['members']
        return members_list

    def member_info(self, member_id):
        """
        returns user info (Apply rate limiting !)
        """
        output = self.auth_session.users_info(member_id).json()
        return output

    def send_message_by_member_id(self, member_id, message):
        """ Send message to a member or Channel """
        output = self.auth_session.chat_post_message(message, channel=member_id).json()
        return output

    def return_member_id_by_name(self, member_name):
        for member in self.list_all_members()['users']:
            if member['username'] == member_name:
                    return member['_id']

    def send_message(self, member_name_lst, message):
        """
        Send a RocketChat message to a list of members
        """
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


# rocket = RocketChat_API()
# print(rocket.list_members_channels())
# print(rocket.list_members_in_channel('gS7Z8p3n7g6xJqfaB'))
# print(rocket.member_info('DDdgQBy5KJnHBo64r'))
# print(rocket.send_message('DDdgQBy5KJnHBo64r'))
# print(rocket.return_member_id_by_name('eslam.gomaa'))
# print(rocket.send_message_by_member_name('eslam.gomaa1', 'Hello World'))