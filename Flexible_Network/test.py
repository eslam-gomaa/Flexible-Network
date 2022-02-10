import hvac
import os
from read_config import Config

config = Config()
# config.configuration_file = "/etc/flexible_network/flexible_network.cfg"

print(config.section_vault())
print(config.section_rocket_chat())
print(config.section_s3())

exit(2)












TMP="""
export VAULT_ADDR='http://192.168.122.71:8200'
export VAULT_TOKEN='s.A3lrrmOgvVSZjDkJ9s99SXAO'
"""



def init_server():
    client = hvac.Client(
        url=os.environ['VAULT_ADDR'],
        token=os.environ['VAULT_TOKEN']
        )

    print(client.is_authenticated())

    client.secrets.kv.v2.create_or_update_secret(mount_point='kv', path='kv/hello2', secret=dict(foo="bar"))
    read_response = client.secrets.kv.v2.read_secret_version(mount_point='kv', path="kv/hello2")
    print(read_response)



init_server()



