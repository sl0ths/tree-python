#!/usr/bin/python3
"""
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
    Ahmed Merimi
    Benlmoaujoud Mohamed
    Yassine Ibrahimi
    Abdellah Ouaggane
    Mouslim Mouden
    Adam El Berdai
"""
from os.path import exists, join
from os import walk, getcwd
from sys import argv
from dataclasses import dataclass


V_PIPE = '│'
MID_NODE = '├'
FINAL_NODE = '└'
H_PIPE = '──'


@dataclass
class Flag:
    """
    Flag dataclass to hold the values of arguments 
    passed by the user
    """
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
        """
        Sets all values once given
        whatever is passed in kwargs
        """
        for key, value in kwargs.items():
            object.__setattr__(self, key, value)

    def __setattr__(self, *args):
        """
        Disables setting attributes via
        item.prop = val or item['prop'] = val
        """
        raise TypeError(
            'Immutable objects cannot have properties set after init')

    def __delattr__(self, *args):
        """
        Disables deleting properties
        """
        raise TypeError('Immutable objects cannot have properties deleted')


# returns a 2d list of the form [[{is it a directory?}, name],...]
def parse_ls(pwd, flag):
    """
    parse list
    """
    ls_arr = []
    dirs = []
    files = []

    for (_, dirnames, filenames) in walk(pwd):
        # TODO gitignore
        if not flag.files_only:
            dirs = [[False, dir] for dir in dirnames
                    if flag.all or not dir.startswith('.')]

        # TODO gitignore
        if not flag.dirs_only:
            files = [[True, file] for file in filenames
                     if flag.all or not file.startswith('.')]
        # breaks the walk from yeilding other directory contents...
        # we might actually use this to make the whole tool
        break

    if flag.filesfirst:
        ls_arr.extend(files)
        ls_arr.extend(dirs)
    else:
        ls_arr.extend(dirs)
        ls_arr.extend(files)

    return ls_arr


def printarr(array):
    """
    print array
    """
    for i in array:
        for j in i:
            print(j, end='')
    print(" ", end='')


def tree(pwd, flags: Flag):
    """
    tree
    """
    if flags.help:
        # basic help prinitng here
        print_help()
        return
    print('.')

    def _tree(pwd, arr, depth):
        """
        _tree
        """
        if not exists(pwd):
            print("path doesn't exist")
            return

        ls_arr = parse_ls(pwd, flags)
        if flags.sortbyname:
            # sort list by name
            if flags.reverse:
                ls_arr = sorted(ls_arr, key=lambda x: x[1], reverse=True)
            else:
                ls_arr = sorted(ls_arr, key=lambda x: x[1])

        lslen = len(ls_arr)
        arr += [[MID_NODE, H_PIPE]]

        depth += 1

        for i in range(lslen):
            if i >= lslen-1:
                arr[-1][0] = FINAL_NODE
            if ls_arr[i][0]:  # is it a file?
                printarr(arr)
                print(ls_arr[i][1])
            else:
                printarr(arr)
                print(ls_arr[i][1])
                if flags.depth == 0 or depth < flags.depth:
                    if i < lslen-1:
                        _tree(pwd + '/' + ls_arr[i][1],
                              arr[:-1] + [[V_PIPE, "   "]], depth)
                    else:
                        _tree(pwd + '/' + ls_arr[i][1],
                              arr[:-1] + [[" ", "   "]], depth)
    _tree(pwd, [], depth=0)


def parse_args(argv_list: list, pwd: str):
    """
    parse args
    """
    all_arg, gitignore, help_arg, sortbyname = False, False, False, False
    reverse, files_only, dirs_only, filesfirst = False, False, False, False
    depth = 0
    is_pwd_set = False
    if len(argv_list) <= 1:
        pass
    else:
        for arg in argv_list[1:]:
            if arg.startswith('-'):
                arg = arg[1:]
                if arg in ('a', '-all'):
                    all_arg = True
                elif arg in ('h', '-help'):
                    help_arg = True
                elif arg in ('gitignore', '-gitignore'):
                    gitignore = True
                elif arg in ('sn', '-sortbyname'):
                    sortbyname = True
                elif arg in ('r', '-reverse'):
                    reverse = True
                elif arg in ('fo', '-filesonly'):
                    files_only = True
                elif arg in ('do', '-dirsonly'):
                    dirs_only = True
                # this has to be used like this: tree -L5 with the number
                # directly next to the arg no space
                elif arg.startswith('L'):
                    depth = int(arg[1:])
                else:
                    help_arg = True
            else:
                if not is_pwd_set:
                    pwd = join(pwd, arg)
                    is_pwd_set = True
    flags = Flag(all=all_arg, gitignore=gitignore, sortbyname=sortbyname,
                 help=help_arg, reverse=reverse, files_only=files_only,
                 dirs_only=dirs_only, depth=depth, filesfirst=filesfirst)
    return (flags, pwd)


def print_help():
    """
    print help
    """
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
    Ahmed Merimi
    Benlmoaujoud Mohamed
    Yassine Ibrahimi
    Abdellah Ouaggane
    Mouslim Mouden
    Adam El Berdai
""")


if __name__ == "__main__":
    cwd = getcwd()
    (arg_flags, cwd) = parse_args(argv, cwd)

    tree(cwd, arg_flags)
