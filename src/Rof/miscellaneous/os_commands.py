
import os

Windows={'cp' : 'copy',
         'rm': 'del',
         'mkdir' : 'mkdir'}

Linux={'cp': 'cp',
       'rm': 'rm',
       'mkdir': 'mkdir'}


def unzip_windows(input, output, zip_path,option):
    string = '{} {} -y {} -o{}'.format(zip_path, option,input, output)
    os.system(string)


def unzip_linux(input, output, zip_path,*option):
    string = '{} {} -d {}'.format(zip_path, input, output)
    os.system(string)


def rmDir_windows(name):
    string = 'rmdir /s /q {}'.format(name)
    os.system(string)


def rmDir_linux(name):
    string = 'rm -r {}'.format(name)
    os.system(string)


def rmFile_windows(name):
    string = 'del /s /q {}'.format(name)
    os.system(string)


def rmFile_linux(name):
    string = 'rm {}'.format(name)
    os.system(string)