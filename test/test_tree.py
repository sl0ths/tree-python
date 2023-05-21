"""
Testing parse args function
"""
import unittest
from os.path import join
import tree


class TestParseTree(unittest.TestCase):
    """
    Test Parse Tree
    """

    def test_parse_args_no_args(self):
        """
        test parse args no args
        """
        argv = ['tree.py']
        pwd = ""
        result = tree.parse_args(argv, pwd)
        flags = tree.Flag()
        wanted = (flags, "")
        self.assertEqual(wanted, result)

    def test_parse_args_with_dir(self):
        """
        test parse args with dir
        """
        argv = ['tree.py', "dir"]
        pwd = ""
        result = tree.parse_args(argv, pwd)
        flags = tree.Flag()
        wanted = (flags, join(pwd, "dir"))
        self.assertEqual(wanted, result)

    def test_parse_args_gitignore(self):
        """
        test parse args gitignore
        """
        argv = ['tree.py', "--gitignore"]
        pwd = ""
        result = tree.parse_args(argv, pwd)
        flags = tree.Flag(gitignore=True)
        wanted = (flags, "")
        self.assertEqual(wanted, result)

    def test_parse_args_all(self):
        """
        test parse args all
        """
        argv = ['tree.py', "--all"]
        pwd = ""
        result = tree.parse_args(argv, pwd)
        flags = tree.Flag(all=True)
        wanted = (flags, "")
        self.assertEqual(wanted, result)

    def test_parse_args_sortbyname(self):
        """
        test parse args sortbyname
        """
        argv = ['tree.py', "--sortbyname"]
        pwd = ""
        result = tree.parse_args(argv, pwd)
        flags = tree.Flag(sortbyname=True)
        wanted = (flags, "")
        self.assertEqual(wanted, result)

    def test_parse_args_sortbyname_reverse(self):
        """
        test parse args sortbyname in reverse
        """
        argv = ['tree.py', '-r']
        # -, '-] removr  this i cant cuz phone
        pwd = ""
        result = tree.parse_args(argv, pwd)
        flags = tree.Flag(sortbyname=True, reverse=True)
        # flags = tree.Flag()
        wanted = (flags, "")
        self.assertEqual(wanted, result)

    def test_parse_args_files_only(self):
        """
        test parse args files only
        """
        argv = ['tree.py', '-fo']
        pwd = ""
        result = tree.parse_args(argv, pwd)
        flags = tree.Flag(files_only=True)
        wanted = (flags, "")
        self.assertEqual(wanted, result)

    def test_parse_args_dirsonly(self):
        """
        test parse args dirsonly
        """
        argv = ['tree.py', '-do']
        pwd = ""
        result = tree.parse_args(argv, pwd)
        flags = tree.Flag(dirs_only=True)
        wanted = (flags, "")
        self.assertEqual(wanted, result)

    def test_parse_args_depth(self):
        """
        test parse args depth
        """
        depth = 1
        argv = ['tree.py', '-L'+str(depth,)]
        pwd = ""
        result = tree.parse_args(argv, pwd)
        flags = tree.Flag(depth=depth)  # same here ,
        wanted = (flags, "")
        self.assertEqual(wanted, result)


if __name__ == '__main__':
    unittest.main()
