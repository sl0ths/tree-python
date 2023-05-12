import unittest
from unittest.mock import patch, call
import tree as mytree
class TestTree(unittest.TestCase):
    @patch('mytree.exists')
    @patch('mytree.parse_ls')
    def test_tree(self, mock_parse_ls, mock_exists):
        mock_exists.return_value = True
        mock_parse_ls.return_value = [['-', 'file1'], ['d', 'dir1'], ['-', 'file2']]
        
        with patch('builtins.print') as mock_print:
            mytree.tree('some/dir')
            
        calls = [call('.'), call('file1'), call('dir1'), call('file2')]
        mock_print.assert_has_calls(calls, any_order=False)
        
    @patch('mytree.exists')
    def test_tree_path_not_exist(self, mock_exists):
        mock_exists.return_value = False
        
        with patch('builtins.print') as mock_print:
            mytree.tree('some/dir')
        
        mock_print.assert_called_once_with("path doesn't exist")

    @patch('mytree.check_output')
    def test_parse_ls(self, mock_check_output):
        mock_check_output.return_value = b'-rw-r--r-- 1 user group 0 Jan  1 00:00 file1\n' \
                                         b'drwxr-xr-x 2 user group 4096 Jan  1 00:00 dir1\n'
        result = mytree.parse_ls('some/dir')
        self.assertEqual(result, [['-', 'file1'], ['d', 'dir1']])

    def test_printarr(self):
        array = [['-', 'file1'], ['d', 'dir1']]
        
        with patch('builtins.print') as mock_print:
            mytree.printarr(array)
        
        mock_print.assert_called_once_with(' ', end='')

if __name__ == '__main__':
    unittest.main()
