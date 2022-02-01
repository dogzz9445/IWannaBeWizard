import os
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('runserver', help='train data', action='store_true')
parser.add_argument('train', help='train data', action='store_true')
parser.add_argument('test', help='train data', action='store_true')

def runserver():
    pass

def train():
    pass

def test():
    pass

def execute_from_command_line(argv):
    if len(argv) <= 1 or argv[1] == '-h' or argv[1] == '--help':
        parser.print_help()
        return
    
    if argv[1] == 'runserver':
        runserver()
        return
    elif argv[1] == 'train':
        train()
        return
    elif argv[1] == 'test':
        test()
        return
    
    parser.print_help()

def main():
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()

