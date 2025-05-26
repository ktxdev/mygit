import os
import shutil
import unittest
import tempfile

from src.objects.blob import write_blob, read_blob

class TestBlob(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.temp_dir)

    def tearDown(self):
        os.chdir(self.original_dir)
        shutil.rmtree(self.temp_dir)

    def test_write_blob_with_file_path_should_write_file_to_objects_dir(self):
        file_path = os.path.join(self.temp_dir, "test_file.txt")
        with open(file_path, "w") as f:
            f.write("Hello, world!")

        sha1_hex = write_blob(file_path)
        self.assertEqual(sha1_hex, "943a702d06f34599aee1f8da8ef9f7296031d699")

    def test_write_blob_with_content_string_should_write_content_to_objects_dir(self):
        content = "Hello, world!"
        sha1_hex = write_blob(content)
        self.assertEqual(sha1_hex, "943a702d06f34599aee1f8da8ef9f7296031d699")

    def test_write_blob_with_content_bytes_should_write_content_to_objects_dir(self):
        content = b"Hello, world!"
        sha1_hex = write_blob(content)
        self.assertEqual(sha1_hex, "943a702d06f34599aee1f8da8ef9f7296031d699")
    
    def test_read_blob_with_sha1_hex_should_return_content(self):
        content = "Hello, world!"
        sha1_hex = write_blob(content)
        read_content = read_blob(sha1_hex)
        self.assertEqual(read_content, content)

