import unittest
import os
import shutil
import tempfile

from src.commands.status_cmd import status_cmd

class TestStatusCmd(unittest.TestCase):

    def test_status_cmd_with_empty_repo_should_return_empty_list(self):
        file_paths = status_cmd()

if __name__ == "__main__":
    unittest.main()