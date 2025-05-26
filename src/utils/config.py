import os
import configparser

from src.utils.constants import REPO_DIR_NAME, CONFIG_FILE_NAME

class ConfigError(Exception):
    pass

def add_config(key: str, value: str) -> None:
    key_parts = key.split('.')

    if len(key_parts) < 2:
        raise ConfigError(f"key does not contain a section: {key}")
    
    section = f"{key_parts[0]} '{'.'.join(key_parts[1: len(key_parts) - 1])}'".replace("''", "").strip()
    key = key_parts[len(key_parts) - 1]
    
    config_file_path = os.path.join(os.getcwd(), REPO_DIR_NAME, CONFIG_FILE_NAME)

    if not os.path.exists(config_file_path):
        raise ConfigError(f"No configurations have been set, repository may not have been initialized")

    config_parser = configparser.ConfigParser()
    config_parser.read(config_file_path)

    if section not in config_parser.sections():
        config_parser[section] = {}

    config_parser[section][key] = value

    with open(config_file_path, "w") as configfile:
        config_parser.write(configfile)
