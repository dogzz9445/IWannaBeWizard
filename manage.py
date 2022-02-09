import os
import sys
from os import listdir
from os.path import isfile, join
import argparse
import logging

from tensorflow.keras.preprocessing import image as KerasImage
import numpy as np

from wizard import *

class WizardManager:
    # GRPC server for shape classification 
    # Server responses convert shpae image to string 
    # 1. Train data : python manage.py train
    # 2. Run server : python manage.py runserver
    
    def __init__(self):
        self.argument_parser = argparse.ArgumentParser()
        self.argument_parser.add_argument('migrateprotobuf', help='Migrate protobuf for communication between this shape classifier and client uses', action='store_true')
        self.argument_parser.add_argument('runserver', help='Run the WizardServer, it classifies shapes and accepts requests', action='store_true')
        self.argument_parser.add_argument('train', help='Train data and build model', action='store_true')
        self.argument_parser.add_argument('testmodel', help='Test Model', action='store_true')
        
        self.model_path = './model/model_classification.model'
        self.train_data_path = './train_data/'
        self.test_data_path = './test_data/'
                
    def execute(self, argv):
        if len(argv) <= 1 or argv[1] == '-h' or argv[1] == '--help':
            parser.print_help()
            return
        
        if len(argv) > 2:
            self.model_path = argv[2]
        
        # ------------
        # For development
        # ------------ 
        if argv[1] == 'migrateprotobuf':
            self.migrate_protobuf()
        elif argv[1] == 'testmodel':
            self.test_model()
            
        # ------------
        # For service
        # ------------ 
        elif argv[1] == 'runserver':
            self.run_server()
        elif argv[1] == 'train':
            self.train()
        else:
            self.argument_parser.print_help()


    # --------------------------------
    #
    # Public
    #
    # --------------------------------

    def migrate_protobuf(self):
        # python -m grpc_tools.protoc -I=./proto/ --python_out=./wizard/proto/ --grpc_python_out=./wizard/proto/ ./proto/wizard_system.proto
        pass
    
    def test_model(self):
        classifier = MagicClassifier(self.model_path)
        filenames = self.all_filename_from(self.test_data_path)
        for filename in filenames:
            loaded_image = self.load_image(self.test_data_path + filename)
            shape = classifier.predict(loaded_image)
            magic = MagicConverter.get_shape_type(shape)

    def train(self):
        builder = MagicModelBuilder(self.train_data_path)
        builder.load_data()
        builder.make_model()
        builder.fit_model()
        builder.test_model()
        builder.save_model(self.model_path)
    
    def run_server(self):
        server = WizardServer(self.model_path)
        loggin.basicConfig()
        server.run()

    # --------------------------------
    #
    # Public
    #
    # --------------------------------
    def all_filename_from(self, directory: str):
        return [f for f in listdir(directory) if isfile(join(directory, f))]
    
    def load_image(self, filename: str):
        img = KerasImage.load_img(filename, target_size=(300, 300))
        arr_img = KerasImage.img_to_array(img)
        return arr_img.astype(np.byte).tobytes()

def main():
    manager = WizardManager()
    manager.execute(sys.argv)

if __name__ == '__main__':
    main()

