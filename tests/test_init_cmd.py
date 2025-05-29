import os
import shutil
import tempfile
import unittest

from unittest import mock

from src.utils.constants import *
from src.commands.init_cmd import init_cmd

class TestInitCmd(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.temp_dir)
        
    def tearDown(self):
        os.chdir(self.original_dir)
        shutil.rmtree(self.temp_dir)

    def test_init_cmd_with_relative_path_creates_repo_in_current_dir(self):
        init_cmd()
        repo_path = os.path.join(self.temp_dir, REPO_DIR_NAME)
        self.assertTrue(os.path.isdir(repo_path))

    def test_init_cmd_with_absolute_path_creates_repo_in_given_dir(self):
        init_cmd("test")
        repo_path = os.path.join(self.temp_dir, "test", REPO_DIR_NAME)
        self.assertTrue(os.path.isdir(repo_path))

    def test_init_cmd_with_relative_path_creates_objects_dir(self):
        init_cmd()
        repo_path = os.path.join(self.temp_dir, REPO_DIR_NAME)
        objects_path = os.path.join(repo_path, OBJECTS_DIR_NAME)
        self.assertTrue(os.path.isdir(objects_path))

    def test_init_cmd_with_relative_path_creates_objects_dir_subdirs(self):
        init_cmd()
        repo_path = os.path.join(self.temp_dir, REPO_DIR_NAME)
        objects_path = os.path.join(repo_path, OBJECTS_DIR_NAME)
        for subdir in OBJECTS_DIR_SUBDIRS:
            self.assertTrue(os.path.isdir(os.path.join(objects_path, subdir)))


if __name__ == "__main__":
    unittest.main()