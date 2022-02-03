import os
import sys
import argparse
import logging

from wizard import *

parser = argparse.ArgumentParser()
parser.add_argument('migrateprotobuf', help='train data', action='store_true')
parser.add_argument('runserver', help='train data', action='store_true')
parser.add_argument('train', help='train data', action='store_true')
parser.add_argument('test', help='train data', action='store_true')

def migrateprotobuf():
    pass

def runserver(model_path: str):
    server = WizardServer(model_path)
    logging.basicConfig()
    server.run()
    return

def train(model_path: str):
    builder = MagicModelBuilder('./train_data')
    builder.load_data()
    builder.make_model()
    builder.fit_model()
    builder.test_model()
    builder.save_model(model_path)
    return

def test(model_path: str):
    classifier = MagicClassifier(model_path)
    classifier.predict()
    pass

def execute_from_command_line(argv):
    if len(argv) <= 1 or argv[1] == '-h' or argv[1] == '--help':
        parser.print_help()
        return
    
    model_path = str()
    if len(argv) > 2:
        model_path = argv[2]

    if argv[1] == 'migrate':
        migrateprotobuf()
        return
    elif argv[1] == 'runserver':
        runserver(model_path)
        return
    elif argv[1] == 'train':
        train(model_path)
        return
    elif argv[1] == 'test':
        test(model_path)
        return
    
    parser.print_help()

def main():
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()

