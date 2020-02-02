import ffmpeg
import numpy as np
import tensorflow as tf

from transnet import TransNetParams, TransNet
from transnet_utils import draw_video_with_predictions, scenes_from_predictions


# initialize the network
params = TransNetParams()
params.CHECKPOINT_PATH = "./model/transnet_model-F16_L3_S2_D256"

net = TransNet(params)

# export video into numpy array using ffmpeg
video_stream, err = (
    ffmpeg
    .input('BigBuckBunny.mp4')
    .output('pipe:', format='rawvideo', pix_fmt='rgb24', s='{}x{}'.format(params.INPUT_WIDTH, params.INPUT_HEIGHT))
    .run(capture_stdout=True)
)

video = np.frombuffer(video_stream, np.uint8).reshape(
    [-1, params.INPUT_HEIGHT, params.INPUT_WIDTH, 3])

predictions = net.predict_video(video)


# For ilustration purposes, we show only 200 frames starting with frame number 8000.
draw_video_with_predictions(
    video[8000:8200], predictions[8000:8200], threshold=0.1)


scenes = scenes_from_predictions(predictions, threshold=0.1)
