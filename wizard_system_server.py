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

def get_feature(feature_db, point):
    """Returns Feature at given location or None."""
    for feature in feature_db:
        if feature.location == point:
            return feature
    return None


def get_distance(start, end):
    """Distance between two points."""
    coord_factor = 10000000.0
    lat_1 = start.latitude / coord_factor
    lat_2 = end.latitude / coord_factor
    lon_1 = start.longitude / coord_factor
    lon_2 = end.longitude / coord_factor
    lat_rad_1 = math.radians(lat_1)
    lat_rad_2 = math.radians(lat_2)
    delta_lat_rad = math.radians(lat_2 - lat_1)
    delta_lon_rad = math.radians(lon_2 - lon_1)

    # Formula is based on http://mathforum.org/library/drmath/view/51879.html
    a = (pow(math.sin(delta_lat_rad / 2), 2) +
         (math.cos(lat_rad_1) * math.cos(lat_rad_2) *
          pow(math.sin(delta_lon_rad / 2), 2)))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    R = 6371000
    # metres
    return R * c

class WizardSystemServicer(wizard_system_pb2_grpc.WizardServiceServicer):
    
    def __init__(self):
        self.model = keras.models.load_model('model/model_classification_20220116')
        

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    wizard_system_pb2_grpc.add_WizardServiceServicer_to_server(WizardSystemServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
    