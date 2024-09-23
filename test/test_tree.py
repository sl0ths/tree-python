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

    def test_parse_args_multiple_scenarios(self):
        """
        Test multiple parse args scenarios
        """
        test_cases = [
            ("no_args", ['tree.py'], "", tree.Flag(), ""),
            ("with_dir", ['tree.py', "dir"], "", tree.Flag(), "dir"),
            ("gitignore", ['tree.py', "--gitignore"], "", tree.Flag(gitignore=True), ""),
            ("all", ['tree.py', "--all"], "", tree.Flag(all=True), ""),
            ("sortbyname", ['tree.py', "--sortbyname"], "", tree.Flag(sortbyname=True), ""),
            ("sortbyname_reverse", ['tree.py', '-r'], "", tree.Flag(sortbyname=True, reverse=True), ""),
            ("files_only", ['tree.py', '-fo'], "", tree.Flag(files_only=True), ""),
            ("dirs_only", ['tree.py', '-do'], "", tree.Flag(dirs_only=True), ""),
            ("depth", ['tree.py', '-L1'], "", tree.Flag(depth=1), ""),
        ]

        for name, argv, pwd, expected_flags, expected_dir in test_cases:
            with self.subTest(name=name):
                result = tree.parse_args(argv, pwd)
                wanted = (expected_flags, join(pwd, expected_dir) if expected_dir else "")
                self.assertEqual(wanted, result)

if __name__ == '__main__':
    unittest.main()
