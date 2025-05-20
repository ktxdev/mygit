import os
import shutil
import tempfile
import unittest

from unittest import mock

from src.commands.init_cmd import init_cmd, REPO_DIR_NAME, HEAD_FILE_NAME, CONFIG_FILE_NAME, OBJECTS_DIR_NAME, REFS_DIR_NAME

class TestInitCmd(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.temp_dir)
        
    def tearDown(self):
        os.chdir(self.original_dir)
        shutil.rmtree(self.temp_dir)
        
    def test_init_cmd_creates_repo_dir_structure(self):
        init_cmd()
        repo_path = os.path.join(self.temp_dir, REPO_DIR_NAME)

        # Check if .mygit directory exists
        self.assertTrue(os.path.isdir(repo_path))

        # Check if HEAD and config files exist
        self.assertTrue(os.path.isfile(os.path.join(repo_path, HEAD_FILE_NAME)))
        self.assertTrue(os.path.isfile(os.path.join(repo_path, CONFIG_FILE_NAME)))

        # Check if objects and refs directories exist
        self.assertTrue(os.path.isdir(os.path.join(repo_path, OBJECTS_DIR_NAME)))
        self.assertTrue(os.path.isdir(os.path.join(repo_path, REFS_DIR_NAME)))

    def test_init_cmd_prints_message(self):
        with mock.patch('builtins.print') as mock_print:
            init_cmd()
            repo_path = os.path.realpath(os.path.join(self.temp_dir, REPO_DIR_NAME))
            mock_print.assert_called_with(f"Initialized empty mygit repository in {repo_path}")


if __name__ == "__main__":
    unittest.main()