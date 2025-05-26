import os
import shutil
import unittest
import tempfile

from src.utils.hash import hash_file

class TestHash(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.temp_dir)

        self.file_path = os.path.join(self.temp_dir, "test_file.txt")
        with open(self.file_path, "w"):
            pass

    def tearDown(self):
        os.chdir(self.original_dir)
        shutil.rmtree(self.temp_dir)

    def test_hash_file_with_empty_file_should_return_correct_hash(self):
        hash = hash_file(self.file_path)
        self.assertEqual(hash, "da39a3ee5e6b4b0d3255bfef95601890afd80709")

    def test_hash_file_with_non_empty_file_should_return_correct_hash(self):
        with open(self.file_path, "w") as f:
            f.write("Hello, world!")

        hash = hash_file(self.file_path)
        self.assertEqual(hash, "943a702d06f34599aee1f8da8ef9f7296031d699")