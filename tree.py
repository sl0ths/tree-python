#!/usr/bin/python3
from subprocess import check_output


pwd = str(check_output('pwd'))[2:-3]

v_pipe = '│'
mid_node = '├'
final_node = '└'
h_pipe = '──'


# returns a 2d list of the form [[file/dir, name],...]
def parse_ls(pwd):
    buffer = str(check_output(["ls", "-l", pwd]))[2:-3].split('\\n')[1:]
    ls = []
    for i in buffer:
        ls1 = i[0]
        # TODO this supposes no space in the names
        ls2 = i.split(' ')[-1]
        ls += [[ls1, ls2]]
    return ls


def printarr(array):
    for i in array:
        for j in i:
            print(j, end='')
    print(" ", end='')


def tree(pwd=pwd, arr=[]):
    ls = parse_ls(pwd)
    lslen = len(ls)
    arr += [[mid_node, h_pipe]]

    for i in range(lslen):
        if i >= lslen-1:
            arr[-1][0] = final_node
        if ls[i][0] == '-':
            printarr(arr)
            print(ls[i][1])
        elif ls[i][0] == 'd':
            printarr(arr)
            print(ls[i][1])
            if i < lslen-1:
                tree(pwd + '/' + ls[i][1], arr[:-1] + [[v_pipe, '   ']])
            else:
                tree(pwd + '/' + ls[i][1], arr[:-1] + [[" ", '   ']])


print('.')

if __name__ == "__main__":
    tree()
