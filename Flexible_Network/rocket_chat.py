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
            raise ConnectionError("Failed to authenticate to RocketChat Server {} with {}".format(config_data["url"], config_data["username"]))


    def list_accounts(self):
        return self.auth_session.channels_list().json()

    def send_message(self):
        """ Send message to a member or Channel """
        pass




rocket = RocketChat_API()
print(rocket.list_accounts())

