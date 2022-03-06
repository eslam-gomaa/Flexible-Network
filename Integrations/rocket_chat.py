# if __name__ == '__main__':
#     from os import path
#     import sys
#     sys.path.append(path.join(path.dirname(__file__), '..'))

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

    def send_message(self, member_name, message):
        id = self.return_member_id_by_name(member_name)
        info = {}
        info['success'] = None
        # info['output'] = None
        info['fail_reason'] = None
        if id is not None:
            try:
                msg = self.send_message_by_member_id(id, message)
                info['success'] = True
                # info['output'] = msg
            except:
                pass
        else:
            info['success'] = False
            info['fail_reason'] = "Can NOT find the username"
        return info


# rocket = RocketChat_API()
# print(rocket.list_members_channels())
# print(rocket.list_members_in_channel('gS7Z8p3n7g6xJqfaB'))
# print(rocket.member_info('DDdgQBy5KJnHBo64r'))
# print(rocket.send_message('DDdgQBy5KJnHBo64r'))
# print(rocket.return_member_id_by_name('eslam.gomaa'))
# print(rocket.send_message_by_member_name('eslam.gomaa1', 'Hello World'))



# python3.6 Integrations/rocket_chat.py