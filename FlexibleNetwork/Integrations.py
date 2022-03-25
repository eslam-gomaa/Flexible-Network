from FlexibleNetwork.integrations.rocket_chat import RocketChat_API
from FlexibleNetwork.integrations.cyberark import Cyberark_APIs_v2
from FlexibleNetwork.integrations.s3 import S3_APIs


class Integrations(
    RocketChat_API,
    Cyberark_APIs_v2,
    S3_APIs
):
    pass