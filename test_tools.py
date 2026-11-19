import os
import tempfile
import unittest
from tools import read_file, write_file, list_files


class TestTools(unittest.TestCase):
    def test_outside_project_denied(self):
        self.assertIn("Access denied", read_file(".." + os.sep + "x.txt"))
        self.assertIn("Access denied", write_file(".." + os.sep + "x.txt", "no"))
        self.assertIn("Access denied", list_files(".."))

    def test_write_then_read(self):
        with tempfile.TemporaryDirectory(dir=".") as d:
            path = os.path.join(d, "sub", "a.txt")
            self.assertIn("Successfully", write_file(path, "hello"))
            self.assertEqual(read_file(path), "hello")

    def test_read_missing_file(self):
        self.assertIn("ERROR", read_file("does_not_exist.txt"))

    def test_list_files_skips_hidden(self):
        with tempfile.TemporaryDirectory(dir=".") as d:
            write_file(os.path.join(d, "a.txt"), "x")
            write_file(os.path.join(d, ".hidden"), "x")
            result = list_files(d)
            self.assertIn("a.txt", result)
            self.assertNotIn(".hidden", result)


if __name__ == "__main__":
    unittest.main()
