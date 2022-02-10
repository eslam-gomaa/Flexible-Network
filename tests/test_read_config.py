import pytest
from Flexible_Network.read_config import Config

config = Config()

def test_section_vault():
    """ Test case to validate that 'section_vault' returns dict """
    assert isinstance(config.section_vault(), dict)




