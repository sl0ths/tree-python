#!/usr/bin/python3
from os.path import exists, join
from os import walk, getcwd
from subprocess import check_output
from sys import argv
from dataclasses import dataclass


v_pipe = '│'
mid_node = '├'
final_node = '└'
h_pipe = '──'


@dataclass
class flag:
    all: bool = False
    gitignore: bool = False
    sortbyname: bool = False
    reverse: bool = False
    help: bool = False
    dirs_only: bool = False
    files_only: bool = False
    filesfirst: bool = False
    depth: int = 0

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
        raise TypeError(
            'Immutable objects cannot have properties set after init')

    def __delattr__(self, *args):
        """Disables deleting properties"""
        raise TypeError('Immutable objects cannot have properties deleted')


# returns a 2d list of the form [[{is it a directory?}, name],...]
def parse_ls(pwd, flag):
    ls = []
    dirs = []
    files = []

    for (_, dirnames, filenames) in walk(pwd):
        # TODO gitignore
        if not flag.files_only:
            dirs = [[False, dir] for dir in dirnames
                    if flag.all or not dir.__str__().startswith('.')]

        # TODO gitignore
        if not flag.dirs_only:
            files = [[True, file] for file in filenames
                     if flag.all or not file.__str__().startswith('.')]
        # breaks the walk from yeilding other directory contents...
        # we might actually use this to make the whole tool
        break

    if flag.filesfirst:
        ls.extend(files)
        ls.extend(dirs)
    else:
        ls.extend(dirs)
        ls.extend(files)

    return ls


def printarr(array):
    for i in array:
        for j in i:
            print(j, end='')
    print(" ", end='')


def tree(pwd, flags: flag):
    if flags.help:
        # basic help prinitng here
        print_help()
        return
    print('.')

    def _tree(pwd, arr, depth):
        if not exists(pwd):
            print("path doesn't exist")
            return

        ls = parse_ls(pwd, flags)
        if flags.sortbyname:
            # sort list by name
            if flags.reverse:
                ls = sorted(ls, key=lambda x: x[1], reverse=True)
            else:
                ls = sorted(ls, key=lambda x: x[1])

        lslen = len(ls)
        arr += [[mid_node, h_pipe]]

        depth += 1

        for i in range(lslen):
            if i >= lslen-1:
                arr[-1][0] = final_node
            if ls[i][0]:  # is it a file?
                printarr(arr)
                print(ls[i][1])
            else:
                printarr(arr)
                print(ls[i][1])
                if flags.depth == 0 or depth < flags.depth:
                    if i < lslen-1:
                        _tree(pwd + '/' + ls[i][1],
                              arr[:-1] + [[v_pipe, "   "]], depth)
                    else:
                        _tree(pwd + '/' + ls[i][1],
                              arr[:-1] + [[" ", "   "]], depth)
    _tree(pwd, [], depth=0)


def parse_args(argv: list, pwd: str):
    all, gitignore, help, sortbyname, reverse, files_only, dirs_only, filesfirst = False, False, False, False, False, False, False, False
    depth = 0
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
                elif arg == 'do' or arg == '-dirsonly':
                    dirs_only = True
                # this has to be used like this: tree -L5 with the number directly next to the arg no space
                elif arg.startswith('L'):
                    depth = int(arg[1:])
                else:
                    help = True
            else:
                if not is_pwd_set:
                    pwd = join(pwd, arg)
                    is_pwd_set = True
    flags = flag(all=all, gitignore=gitignore, sortbyname=sortbyname,
                 help=help, reverse=reverse, files_only=files_only,
                 dirs_only=dirs_only, depth=depth, filesfirst=filesfirst)
    return (flags, pwd)


def print_help():
    print(r"""

  _____      ____     U _____ u U _____ u
 |_ " _|  U |  _"\ u  \| ___"|/ \| ___"|/
   | |     \| |_) |/   |  _|"    |  _|"
  /| |\     |  _ <     | |___    | |___
 u |_|U     |_| \_\    |_____|   |_____|
 _// \\_    //   \\_   <<   >>   <<   >>
(__) (__)  (__)  (__) (__) (__) (__) (__) .py

A tree(1) clone written in Python.

Usage: tree.py [options] [directory]

Options:
  -a,  --all                Include hidden files
  -gitignore                Exclude files listed in .gitignore.
  -sn, --sortbyname         Sort files by name.
  -r,  --reverse            Sort files by name in reverse.
  -fo, --filesonly          Only show files.
  -do, --dirsonly           Only show directories
  -L                        Max depth the directory tree reaches.
  -h,  --help               Show this help message and exit.

  All Rights Reserved
  If you have any questions, or you need help please contact the developers:
    
    
    
    
    
    
""")


if __name__ == "__main__":
    pwd = getcwd()
    (flags, pwd) = parse_args(argv, pwd)

    tree(pwd, flags)
