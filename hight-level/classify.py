# import the necessary packages
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import numpy as np
import cv2
from os.path import dirname, realpath, join


class ShotClassifier:
    def __init__(self, model_type=1):
        self.__classes = ['logo', 'medium', 'close-out', 'close', 'wide']
        if model_type == 1:
            self.__model = load_model(
                join(dirname(realpath(__file__)), 'moamen.model'))
        else:
            self.__model = load_model(
                join(dirname(realpath(__file__)), 'maher.model'))

    def __get_image_class(self, img):
        """ expected rgb image """
        image = img.copy()
        # pre-process the image for classification
        image = cv2.resize(image, (64, 64))
        image = image.astype('float') / 255.0
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)
        # classify the input image
        idx = np.argmax(self.__model.predict(image))
        return self.__classes[idx]

    def get_shot_class(self, frames):
        histogram = {}
        for frame_type in self.__classes:
            histogram[frame_type] = 0
        for frame in frames:
            frame_class = self.__get_image_class(frame)
            histogram[frame_class] += 1
        # special case
        if (histogram['logo'] / len(frames)) * 100 >= 10:
            # majority is logo.
            print("major is logo")
            return 'logo'
        max_type = ''
        max_type_freq = 0
        for key, val in histogram.items():
            if val >= max_type_freq:
                max_type_freq = val
                max_type = key
        print(f"major is {max_type}")
        return max_type
