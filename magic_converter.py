from tensorflow.keras.preprocessing import image
import numpy as np

# get shape type from int result
class MagicConveter:

    def resize_image_from_bytes(pre_image, original_size: tuple, target_size: tuple):
        img = np.frombuffer(pre_image, dtype=np.byte).reshape(original_size + (3,))
        img = image.array_to_img(img)
        return img.resize(target_size) 

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
