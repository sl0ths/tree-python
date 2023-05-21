#!/usr/bin/python3
from os.path import exists, join
from os import walk
from subprocess import check_output
from sys import argv


v_pipe = '│'
mid_node = '├'
final_node = '└'
h_pipe = '──'


class flag:
    all = False
    gitignore = False
    sortbyname = False
    help = False
    directories_only = False
    files_only = False

    def __init__(self, **kwargs):
        """Sets all values once given
        whatever is passed in kwargs
        """
        for k, v in kwargs.items():
            object.__setattr__(self, k, v)

    def __setattr__(self, *args):
        """Disables setting attributes via
        item.prop = val or item['prop'] = val
        """
        raise TypeError('Immutable objects cannot have properties set after init')

    def __delattr__(self, *args):
        """Disables deleting properties"""
        raise TypeError('Immutable objects cannot have properties deleted')


# returns a 2d list of the form [[{is it a directory?}, name],...]
def parse_ls(pwd, flag):
    ls = []

    for (_, dirnames, filenames) in walk(pwd):
        # TODO gitignore
        if not flag.files_only:
            ls.extend([[False, dir] for dir in dirnames
                       if flag.all or not dir.__str__().startswith('.')])
          # TODO gitignore
        if not flag.directories_only:
            ls.extend([[True, file] for file in filenames
                       if flag.all or not file.__str__().startswith('.')])
        # breaks the walk from yeilding other directory contents...
        # we might actually use this to make the whole tool
        break

    return ls


def printarr(array):
    for i in array:
        for j in i:
            print(j, end='')
    print(" ", end='')


def tree(pwd, flags: flag):
    if flags.help:
         # basic help prinitng here
         print(r"""

                                         
                                         
                                        
    #                                    
   ##                                    
   ##                                    
 ######## ###  /###     /##       /##    
########   ###/ #### / / ###     / ###   
   ##       ##   ###/ /   ###   /   ###  
   ##       ##       ##    ### ##    ### 
   ##       ##       ########  ########  
   ##       ##       #######   #######   
   ##       ##       ##        ##        
   ##       ##       ####    / ####    / 
   ##       ###       ######/   ######/  
    ##       ###       #####     #####   
                                         
                                         
                                         
          """)
         return
    print('.')
    def _tree(pwd, arr):
        if not exists(pwd):
            print("path doesn't exist")
            return
        ls = parse_ls(pwd, flags)
        if flags.sortbyname:
             # sort list by name
             ls = sorted(ls, key=lambda x: x[1])
        lslen = len(ls)
        arr += [[mid_node, h_pipe]]

        for i in range(lslen):
            if i >= lslen-1:
                arr[-1][0] = final_node
            if ls[i][0]:  # is it a file?
                printarr(arr)
                print(ls[i][1])
            else:
                printarr(arr)
                print(ls[i][1])
                if i < lslen-1:
                    _tree(pwd + '/' + ls[i][1], arr[:-1] + [[v_pipe, "   "]])
                else:
                    _tree(pwd + '/' + ls[i][1], arr[:-1] + [[" ", "   "]])
    _tree(pwd, [])


def parse_args(argv: list, pwd: str):
    all, gitignore, help, sortbyname, reverse, files_only, directories_only = False, False, False, False, False, False, False
    is_pwd_set = False
    if len(argv) <= 1:
        pass
    else:
        for arg in argv[1:]:
            if arg.startswith('-'):
                arg = arg[1:]
                if arg == 'a' or arg == '-all':
                    all = True
                elif arg == 'h' or arg == '-help':
                    help = True
                elif arg == 'gitignore' or arg == '-gitignore':
                    gitignore = True
                elif arg == 'sn' or arg == '-sortbyname':
                    sortbyname = True
                elif arg == 'r' or arg == '-reverse':
                    reverse = True
                elif arg == 'fo' or arg == '-filesonly':
                    files_only = True
                elif arg == 'do' or arg == '-directoriesonly':
                    directories_only = True
                else:
                    help = True
            else:
                if not is_pwd_set:
                    pwd = join(pwd, arg)
                    is_pwd_set = True
    flags = flag(all=all, gitignore=gitignore, sortbyname=sortbyname, help=help, reverse=reverse, files_only=files_only, directories_only=directories_only)
    return (flags, pwd)


if __name__ == "__main__":
    pwd = str(check_output('pwd'))[2:-3]
    (flags, pwd) = parse_args(argv, pwd)

    tree(pwd, flags)
