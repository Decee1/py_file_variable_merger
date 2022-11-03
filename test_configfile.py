import os
import pytest

from mage.mage import load_config, merge_config

# Tests in here is for general testing of mage

def module_to_dict(module):
    """
    Convert a imported module into a dict
    """
    res = [item for item in dir(module) if not item.startswith("__")]
    return res


def create_config(path, custom_text=""):
    """
    Create a config file used under testing
    Config file is created in path
    """

    # This is a lazy way to make a easy-to-edit file
    # Does not look very pretty but it sees the newlines and taps correctly
    # If custom_text is specified, it will add that to the docstring
    def config_file():
        """
typeExcludeRegex = [
    'random_data',                 # random data
]

baseTypes = {
    'random_type': 'D',
}
"""

    f = open(path, "w")
    f.write(config_file.__doc__ + custom_text)
    f.close()


def test_config_load():
    """
    Test that the config can be loaded correctly
    """

    filepath = "./config.py"

    create_config(filepath)

    module = load_config(filepath)
    res = module_to_dict(module)

    assert "baseTypes" in res
    assert "typeExcludeRegex" in res


def test_config_load_none():
    """
    Test that the config is not loaded when config is None
    """
    # Generate a config file
    filepath = "./config.py"
    create_config(filepath)

    module = load_config(None)
    res = module_to_dict(module)

    assert "baseTypes" in res
    assert "typeExcludeRegex" in res


def test_config_load_invalid_path():
    """
    Test that the config can throw error if path is incorrect
    It is expected to raise FileNotFoundError
    """
    with pytest.raises(FileNotFoundError):
        load_config("./config")

    with pytest.raises(FileNotFoundError):
        load_config("./configpath/")


def test_config_load_no_path_config_local():
    """
    Test that when there is no valid config file it does not load anything
    """
    res = load_config(None)

    assert res is None


def test_config_merge():
    """
    Test that 2 configs can merge together
    """

    filepath = "./config.py"
    create_config(filepath, custom_text="\nSecretVariable = True\n")

    user_config = load_config(None)

    from mage import config

    new_config = merge_config(user_config=user_config, config=config)

    res = module_to_dict(new_config)

    assert "SecretVariable" in res

    assert "typeExcludeRegex" in res


def test_mage_config_load():
    """
    Test that mage can load config properly
    It checks for the variable SecretVariable in config
    """

    filepath = "./config.py"
    create_config(filepath, custom_text="\nSecretVariable = True\n")

    user_config = load_config(None)

    from mage import config

    new_config = merge_config(user_config=user_config, config=config)
    config.overwrite_config(new_config)

    assert hasattr(config, "SecretVariable"),  ""


def setUp():
    print("Setup")
    if os.path.exists("./config.py"):
        os.remove("./config.py")


def tearDown():
    print("Teardown")
    pass


@pytest.fixture(autouse=True)
def resource():
    setUp()
    yield "resource"
    tearDown()
