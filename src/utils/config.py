import os
import configparser

from utils.constants import REPO_DIR_NAME, CONFIG_FILE_NAME

class ConfigError(Exception):
    pass

def seperate_key_into_section_and_key(key: str) -> tuple[str, str]:
    key_parts = key.split('.')
    if len(key_parts) < 2:
        raise ConfigError(f"key does not contain a section: {key}")
    
    section = f"{key_parts[0]} '{'.'.join(key_parts[1: len(key_parts) - 1])}'".replace("''", "").strip()
    key = key_parts[len(key_parts) - 1]

    return section, key

def add_config(key: str, value: str) -> None:
    section, key = seperate_key_into_section_and_key(key)
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

def get_config(key: str) -> str:
    section, key = seperate_key_into_section_and_key(key)
    config_file_path = os.path.join(os.getcwd(), REPO_DIR_NAME, CONFIG_FILE_NAME)

    if not os.path.exists(config_file_path):
        raise ConfigError(f"No configurations have been set, repository may not have been initialized")

    config_parser = configparser.ConfigParser()
    config_parser.read(config_file_path)

    if section not in config_parser.sections():
        raise ConfigError(f"Configuration not found")
    
    return config_parser[section][key]