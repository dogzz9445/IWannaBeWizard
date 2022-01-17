from tensorflow import keras
from tensorflow.keras.applications.inception_resnet_v2 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.callbacks import ModelCheckpoint

from concurrent import futures
import numpy as np
import logging
import math
import time

import grpc
import wizard_system_pb2
import wizard_system_pb2_grpc

def resize_image_from_bytes(pre_image, original_size: tuple, target_size: tuple):
    img = np.frombuffer(pre_image, dtype=np.float32).reshape(original_size + (3,))
    img = image.array_to_img(img)
    return img.resize(target_size) 

def predict(model, image):
    img_path = 'triangle.png'
    img = image.load_img(img_path, target_size=(299, 299))
    x = image.img_to_array(img) 
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    preds = model.predict(x).argmax(axis=1)
    # decode the results into a list of tuples (class, description, probability)
    # (one such list for each sample in the batch)
    print('Predicted:', preds)
    # print(classification_report(test_data.classes, pred))
    return preds

class WizardSystemServicer(wizard_system_pb2_grpc.WizardServiceServicer):
    
    def __init__(self):
        #self.model = keras.models.load_model('model/model_classification_20220116')
        pass
        
    def PostMagicImageRaw(self, request, context):
        context.set_code(grpc.StatusCode.OK)
        resized_image = resize_image_from_bytes(request.imageData, (request.height, request.width), (299, 299))
        return wizard_system_pb2.Magic(type=str(resized_image.height))

    def PostMagicImagePng(self, request, context):
        context.set_code(grpc.StatusCode.OK)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    wizard_system_pb2_grpc.add_WizardServiceServicer_to_server(WizardSystemServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
    