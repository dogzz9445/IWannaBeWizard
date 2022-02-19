from tensorflow.keras.preprocessing import image as KerasImage
from PIL import Image
import io
import numpy as np
import base64

# get shape type from int result
class MagicImage:

    def resize_image_from_bytes(pre_image, original_size: tuple, target_size: tuple):
        img = np.frombuffer(pre_image, dtype=np.byte).reshape(original_size + (3,))
        img = KerasImage.array_to_img(img)
        return img.resize(target_size) 

    def resize_image_from_png(pre_image, target_size: tuple):
        img = Image.open(io.BytesIO(pre_image))
        return img.resize(target_size)

    def load_image(filename: str, target_size: tuple):
        img = KerasImage.load_img(filename, target_size=target_size)
        img = KerasImage.array_to_img(img)
        return img

    def get_shape_type(shape):
        if shape == 0:
            return 'circle'
        elif shape == 1:
            return 'square'
        elif shape == 2:
            return 'star'
        elif shape == 3:
            return 'triangle'
        elif shape == 4:
            return 'lightning'

        return 'None'
