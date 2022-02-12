import pytest
from read_config import Config

config = Config()

def test_set_configuration_type():
    """ Test case to validate that wrong input in 'set_configuration_type' will raise ValueError """
    with pytest.raises(ValueError):
        config.set_configuration_type(type="ANYTHING")

# def test_set_configuration_file():
#     """ Test case to validate that wrong input in 'set_configuration_file' will raise ValueError """
#     with pytest.raises(ValueError):
#         config.set_configuration_file(file="not_correct_path")

def test_section_vault():
    """ Test case to validate that 'section_vault' returns dict """
    assert isinstance(config.section_vault(), dict)


def test_section_rocket_chat():
    """ Test case to validate that 'section_rocket_chat' returns dict """
    assert isinstance(config.section_rocket_chat(), dict)


def test_section_s3():
    """ Test case to validate that 'section_s3' returns dict """
    assert isinstance(config.section_s3(), dict)

def test_not_existing_section():
    """ Test case to validate that not existed sections raise ValueError """
    with pytest.raises(ValueError):
        config.section_vault(section_name="does_not_exist")
