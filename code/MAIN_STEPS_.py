import time
from Processing.Processing import *
import cv2


def main():
    # CONSTANTS
    video_name = "Arsenal-Chelsea 1 pt2"
    VIDEO_PATH = "{0}{1}{2}".format(
        'C:/Users\\medo\\Desktop\\match_test\\', video_name, '.mp4')

    cap = cv2.VideoCapture(VIDEO_PATH)
    if cap.isOpened() == False:
        print('err reading video')
        return

    t1 = time.time()

    # shots processing
    shots = shots_processing(cap)

    # audio processing
    # Detecing if shot contains high volume
    audio_processing(shots, VIDEO_PATH)

    # processing output shots
    # main shots depending on replay and other shots depending on high volume
    output_video_shots_1, output_video_shots_2 = output_shots_processing(shots)

    # classifying shots Sequence
    shots_classes = classifying_shot_sequence(
        output_video_shots_1, output_video_shots_2)

    # Final output
    output_video_shots, final_video = final_output_processing(
        output_video_shots_1, output_video_shots_2, shots_classes)

    t2 = time.time()

    # write outputs to file
    output_to_file(shots_classes, video_name,
                   shots, output_video_shots, output_video_shots_2, t1, t2)

    # rendering video
    # rendering_sumary(final_video,VIDEO_PATH)


main()
