from read_config import Config
from requests import sessions
from rocketchat_API.rocketchat import RocketChat
# https://github.com/jadolg/rocketchat_API

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
        for member in self.list_members_channels():
            try:
                if member['u']['username'] == member_name:
                    return member['u']['_id']
            except:
                if not member['_id'] == 'GENERAL':
                    return None

    def send_message_by_member_name(self, member_name, message):
        id = self.return_member_id_by_name(member_name)
        if id is not None:
           return self.send_message_by_member_id(id, message)


rocket = RocketChat_API()
# print(rocket.list_members_channels())
# print(rocket.list_members_in_channel('gS7Z8p3n7g6xJqfaB'))
# print(rocket.member_info('DDdgQBy5KJnHBo64r'))
# print(rocket.send_message('DDdgQBy5KJnHBo64r'))
# print(rocket.return_member_id_by_name('eslam.gomaa'))
print(rocket.send_message_by_member_name('eslam.gomaa', 'Hello World'))


# python3.6 Flexible_Network/RocketChat.py
