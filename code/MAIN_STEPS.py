
import time
from UTL.classes import shot_types, event_types
from ProcessingSteps.Processing_Steps import (STEP_1_shots_processing, STEP_2_resolving_double_logos, STEP_3_audio_processing, STEP_4_processing_output_shots,
                                              STEP_5_classifying_shot_sequence, STEP_6_processing_final_output, STEP_7_file_output, STEP_8_rendering_video)
import cv2


def main():
    # CONSTANTS _________________________________________________________
    video_name = "matchnew3"
    VIDEO_PATH = "{0}{1}{2}".format(
        'C:/Users\\salama\\Desktop\\', video_name, '.mp4')
    cap = cv2.VideoCapture(VIDEO_PATH)
    if cap.isOpened() == False:
        print('err reading video')
        return

    SHOT_TYPES = shot_types()
    EVENT_TYPES = event_types()

    t1 = time.time()

    # shots processing _____________________________________________________
    shots = STEP_1_shots_processing(cap, SHOT_TYPES)

    # resolving double logos _____________________________________________
    STEP_2_resolving_double_logos(shots, SHOT_TYPES)

    # audio processing _________________________________________________
    # Detecing if shot contains high volume ____________________________
    STEP_3_audio_processing(shots, VIDEO_PATH)

    # processing output shots __________________________________________________
    # main shots depending on replay and other shots depending on high volume
    output_video_shots_1, output_video_shots_2 = STEP_4_processing_output_shots(
        shots, SHOT_TYPES)

    # classifying shots Sequence _____________________________________________
    shots_classes = STEP_5_classifying_shot_sequence(
        output_video_shots_1, output_video_shots_2, SHOT_TYPES, EVENT_TYPES)
    # Final output ______________________________________________________________
    output_video_shots, final_video = STEP_6_processing_final_output(
        output_video_shots_1, output_video_shots_2, shots_classes)

    t2 = time.time()

    # write outputs to file ________________________________________________
    STEP_7_file_output(shots_classes, EVENT_TYPES, video_name,
                       shots, output_video_shots, output_video_shots_2, t1, t2)

    # rendering video  _______________________________________________________
    # STEP_8_rendering_video(final_video,VIDEO_PATH)


main()
