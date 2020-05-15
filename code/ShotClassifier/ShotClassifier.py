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

    def __get_majority(self, frames):
        histogram = {}
        for frame in frames:
            frame_class = self.__get_image_class(frame)
            if histogram.get(frame_class):
                histogram[frame_class] += 1
            else:
                histogram[frame_class] = 1
        max_type = ''
        max_type_freq = 0
        for key, val in histogram.items():
            if val == max_type_freq and max_type == 'logo':
                continue
            if val >= max_type_freq:
                max_type_freq = val
                max_type = key
        return max_type


    def get_shot_class(self, frames):
        total_majority = self.__get_majority(frames)
        if len(frames) < 20:
            return total_majority
        if total_majority != 'logo':
            begin_majority = self.__get_majority(frames[:5])
            end_majority = self.__get_majority(frames[-5:])
            if begin_majority == 'logo':
                total_majority = f'logo+{total_majority}'
            if end_majority == 'logo':
                total_majority = f'{total_majority}+logo'
            if begin_majority == "logo" and end_majority == "logo":
                total_majority = total_majority[4:]
            return total_majority
        else:
            return 'logo'
'''
im1 = cv2.imread("C:/Users\\salama\\Desktop\\GP-video-summary\\code\\ShotClassifier\\frame2970.jpg")
im2 = cv2.imread("C:/Users\\salama\\Desktop\\GP-video-summary\\code\\ShotClassifier\\frame2975.jpg")

im3 = cv2.imread("C:/Users\\salama\\Desktop\\GP-video-summary\\code\\ShotClassifier\\frame2980.jpg")

im4 = cv2.imread("C:/Users\\salama\\Desktop\\GP-video-summary\\code\\ShotClassifier\\frame2985.jpg")

frames = [im1,im2,im3,im4]

print(ShotClassifier(model_type=1).get_shot_class(frames))
'''