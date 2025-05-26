import os
import shutil
import unittest
import tempfile
import configparser

from src.utils.config import add_config, get_config, seperate_key_into_section_and_key, ConfigError
from src.utils.constants import REPO_DIR_NAME, CONFIG_FILE_NAME

class TestConfig(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()

        os.chdir(self.temp_dir)

        repo_dir_path = os.path.join(os.getcwd(), REPO_DIR_NAME)
        os.makedirs(repo_dir_path, exist_ok=True)

        config_file_path = os.path.join(repo_dir_path, CONFIG_FILE_NAME)
        with open(config_file_path, "w"):
            pass
        
    def tearDown(self):
        os.chdir(self.original_dir)
        shutil.rmtree(self.temp_dir)
        
    def test_seperate_key_into_section_and_key_with_no_section_should_raise_error(self):
        with self.assertRaises(ConfigError) as context:
            seperate_key_into_section_and_key("email")
            self.assertEqual(str(context.exception), "key does not contain a section: email")

    def test_write_with_section_should_add_config(self):
        add_config("user.name", "Sean")
        config_file_path = os.path.join(os.getcwd(), REPO_DIR_NAME, CONFIG_FILE_NAME)

        config = configparser.ConfigParser()
        config.read(config_file_path)
        
        self.assertEqual(config["user"]["name"], "Sean")

    def test_write_with_existing_section_should_add_config(self):
        add_config("user.name", "Sean")
        add_config("user.email", "sean@example.com")
        config_file_path = os.path.join(os.getcwd(), REPO_DIR_NAME, CONFIG_FILE_NAME)

        config = configparser.ConfigParser()
        config.read(config_file_path)

        self.assertEqual(config["user"]["name"], "Sean")
        self.assertEqual(config["user"]["email"], "sean@example.com")

    def test_seperate_key_into_section_and_key_with_multiple_section_separators(self):
        section, key = seperate_key_into_section_and_key("user.name.preferred.first")
        self.assertEqual(section, "user 'name.preferred'")

    def test_write_with_no_config_file_should_raise_error(self):
        config_file_path = os.path.join(os.getcwd(), REPO_DIR_NAME, CONFIG_FILE_NAME)
        os.remove(config_file_path)

        with self.assertRaises(ConfigError) as context:
            add_config("user.name", "Sean")
            self.assertEqual(str(context.exception), "No configurations have been set, repository may not have been initialized")

    def test_get_config_with_key_containing_invalid_section_should_raise_error(self):
        with self.assertRaises(ConfigError) as context:
            get_config("core.repositoryformatversion")
            self.assertEqual(str(context.exception), "Configuration not found")

if __name__ == "__main__":
    unittest.main()