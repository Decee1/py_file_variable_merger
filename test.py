import importlib
import os
import sys


def load_config(cfg_path, module_name="module"):
    """
    Load the config file and merge the config file in cfg_path and the mage config
    if cfg_path is None it first tries to check if there is a valid file in the path, if not it returns

    :param cfg_path: Os path to config file
    :returns: loaded module
    """

    if cfg_path is not None and not os.path.exists(cfg_path):
        raise FileNotFoundError(f"No valid config file in path {cfg_path}")

    if cfg_path is None:
        cfg_path = r"./config.py"

    # If no file is here
    if not os.path.exists(cfg_path):
        return
    else:

        spec = importlib.util.spec_from_file_location(module_name, os.path.abspath(cfg_path))
        foo = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = foo
        spec.loader.exec_module(foo)

        # res = [item for item in dir(foo) if not item.startswith("__")]

        return foo


def merge_config(user_config, config):
    """
    Merges the 2 config files together
    ``user_config´´ is merged into ``config´´.
    For non-sequencing types the variables are overwritten directly
    For sequencing types the variable is updated with the new data.
    for mapping type if the key already exist it will overwrite the value, else it will be updated into the dict

    :param user_config: Loaded config Module, load using :py:meth:`~Queue.Queue.load_config`
    :param config: Loaded config Module, load using :py:meth:`~Queue.Queue.load_config`
    :returns: module path to config
    """

    # Load keys from the user config and make a dict containing all variabels
    # { VAR_NAME: VAR_VALUE .. }
    keys = {key: value for key, value in user_config.__dict__.items() if not key.startswith('__') and not callable(key)}

    # Loop though all keys from user config so they can be merged with old config
    for key in keys:
        key_type = type(keys[key])

        # If the variable exist in both config, and is a dict, list or tuple
        if getattr(config, key, None) and isinstance(keys[key], (list, tuple, dict)):
            # If sequence type
            if key_type in (list, tuple):
                old_data = getattr(config, key)
                new_data = getattr(user_config, key)
                new_data += old_data

            # If mapping type
            elif isinstance(keys[key], dict):
                # If dict exist
                old_data = getattr(config, key)
                new_data = getattr(user_config, key)
                old_data.update(new_data)
                new_data = old_data

        else:
            # This is non-sequence types and therefore can be overwritten directly or
            # If if a dict, list or tuple does not exist in config already
            new_data = keys[key]

        # Overwrite data in config with data from user config
        setattr(config, key, new_data)

    return config


if __name__ == "__main__":

    config = load_config("./config.py")
    user_config = load_config("./config2.py")

    config = merge_config(user_config, config)

    keys = {key: value for key, value in config.__dict__.items() if not key.startswith('__') and not callable(key)}
    print(keys)