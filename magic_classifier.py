from tensorflow import keras
from tensorflow.keras.applications.inception_resnet_v2 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.callbacks import ModelCheckpoint

import numpy as np

class MagicClassifier:

    # model_path 
    def __init__(self, model_path: str):
        if model_path is None:
            self.model = keras.models.load_model('model/model_classification')
        else:
            self.model = keras.models.load_model(model_path)

    # image must be a bytes array
    def predict(self, image):
        # TODO:
        # check the validation of image
        # image would be 299x299 bytes array

        image = np.expand_dims(image, axis=0)
        image = preprocess_input(image)

        isValidate = False
        preds = self.model.predict(image)
        for pred in preds[0]:
            if pred > 0.5:
                isValidate = True
        if isValidate is False:
            return -1
        preds = preds.argmax(axis=1)
        print('Predicted:', preds)
        if preds == None:
            return -1
        return preds[0]
