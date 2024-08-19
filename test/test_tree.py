import unittest
from os.path import join
import tree
from parameterized import parameterized

class TestParseTree(unittest.TestCase):
    @parameterized.expand([
        ("no_args", ['tree.py'], "", tree.Flag(), ""),
        ("with_dir", ['tree.py', "dir"], "", tree.Flag(), "dir"),
        ("gitignore", ['tree.py', "--gitignore"], "", tree.Flag(gitignore=True), ""),
        ("all", ['tree.py', "--all"], "", tree.Flag(all=True), ""),
        ("sortbyname", ['tree.py', "--sortbyname"], "", tree.Flag(sortbyname=True), ""),
        ("sortbyname_reverse", ['tree.py', '-r'], "", tree.Flag(sortbyname=True, reverse=True), ""),
        ("files_only", ['tree.py', '-fo'], "", tree.Flag(files_only=True), ""),
        ("dirs_only", ['tree.py', '-do'], "", tree.Flag(dirs_only=True), ""),
        ("depth", ['tree.py', '-L1'], "", tree.Flag(depth=1), ""),
    ])
    def test_parse_args(self, name, argv, pwd, expected_flags, expected_dir):
        result = tree.parse_args(argv, pwd)
        wanted = (expected_flags, join(pwd, expected_dir) if expected_dir else "")
        self.assertEqual(wanted, result)

if __name__ == '__main__':
    unittest.main()
