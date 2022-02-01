from tensorflow.keras.preprocessing import image
import numpy as np
import base64

# get shape type from int result
class MagicConverter:

    def resize_image_from_bytes(pre_image, original_size: tuple, target_size: tuple):
        img = np.frombuffer(pre_image, dtype=np.byte).reshape(original_size + (3,))
        img = image.array_to_img(img)
        return img.resize(target_size) 

    def resize_image_from_png(pre_image, original_size: tuple, target_size: tuple):
        img = np.frombuffer(pre_image, )
        picture_bytes = base64.b64encode(pre_image)
        return picture_bytes

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
