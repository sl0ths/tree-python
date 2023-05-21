import unittest
from os.path import join
import tree

class TestParseTree(unittest.TestCase):
    def test_parse_args_no_args(self):
        argv = ['tree.py']
        pwd = ""
        result = tree.parse_args(argv, pwd)
        flags = tree.flag()
        wanted = (flags, "")
        self.assertEqual(wanted, result)

    def test_parse_args_with_dir(self):
        argv = ['tree.py', "dir"]
        pwd = ""
        result = tree.parse_args(argv, pwd)
        flags = tree.flag()
        wanted = (flags, join(pwd, "dir"))
        self.assertEqual(wanted, result)

    def test_parse_args_gitignore(self):
        argv = ['tree.py', "--gitignore"]
        pwd = ""
        result = tree.parse_args(argv, pwd)
        flags = tree.flag(gitignore=True)
        wanted = (flags, "")
        self.assertEqual(wanted, result)

    def test_parse_args_all(self):
        argv = ['tree.py', "--all"]
        pwd = ""
        result = tree.parse_args(argv, pwd)
        flags = tree.flag(all=True)
        wanted = (flags, "")
        self.assertEqual(wanted, result)

    def test_parse_args_sortbyname(self):
        argv = ['tree.py', "--sortbyname"]
        pwd = ""
        result = tree.parse_args(argv, pwd)
        flags = tree.flag(sortbyname=True)
        wanted = (flags, "")
        self.assertEqual(wanted, result)


if __name__ == '__main__':
    unittest.main()
