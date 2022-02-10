import pytest
from Flexible_Network.read_config import Config

config = Config()


def test_section_vault():
    """ Test case to validate that 'section_vault' returns dict """
    assert isinstance(config.section_vault(), dict)


def test_section_rocket_chat():
    """ Test case to validate that 'section_rocket_chat' returns dict """
    assert isinstance(config.section_rocket_chat(), dict)


def test_section_s3():
    """ Test case to validate that 'section_s3' returns dict """
    assert isinstance(config.section_s3(), dict)

def test_not_existed_section():
    """ Test case to validate that not existed sections raise ValueError """
    with pytest.raises(ValueError):
        config.section_vault(section_name="does_not_exist")
