import os
import shutil
import unittest
import tempfile

from src.utils.hash import encode_content

class TestHash(unittest.TestCase):
    def test_encode_content_with_empty_content_should_return_correct_hash(self):
        content = b""
        hash = encode_content(content)
        self.assertEqual(hash, "da39a3ee5e6b4b0d3255bfef95601890afd80709")

    def test_encode_content_with_non_empty_content_should_return_correct_hash(self):
        content = b"Hello, world!"
        hash = encode_content(content)
        self.assertEqual(hash, "943a702d06f34599aee1f8da8ef9f7296031d699")
