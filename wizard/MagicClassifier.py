from PIL import Image
from tensorflow import keras
from tensorflow.keras.applications.inception_resnet_v2 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.callbacks import ModelCheckpoint

import numpy as np

class MagicClassifier:
    image_size_for_predict = (299, 299)
    
    def __init__(self, model_path: str):
        if not model_path:
            self.model = keras.models.load_model('model/model_classification')
        else:
            self.model = keras.models.load_model(model_path)

    def predict(self, img: Image):
        if img.size != MagicClassifier.image_size_for_predict:
            img.resize(MagicClassifier.image_size_for_predict)
            
        isValidate = False
        preds = self.model.predict(preprocess_input(np.expand_dims(img, axis=0)))
        for pred in preds[0]:
            if pred > 0.5:
                isValidate = True
        if isValidate is False:
            return -1
        preds = preds.argmax(axis=1)
        if preds == None:
            return -1
        return preds[0]
