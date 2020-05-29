
import time
from UTL.classes import shot_types, event_types
from ProcessingSteps.Processing_Steps import (STEP_1_shots_processing, STEP_2_resolving_double_logos, STEP_3_audio_processing, STEP_4_processing_output_shots,
                                              STEP_5_classifying_shot_sequence, STEP_6_processing_final_output, STEP_7_file_output, STEP_8_rendering_video)
import cv2


def main(VIDEO_PATH, video_name, output_file_name, summary_id, coefficient):
    cap = cv2.VideoCapture(VIDEO_PATH)
    if cap.isOpened() == False:
        print('err reading video')
        return

    SHOT_TYPES = shot_types()
    EVENT_TYPES = event_types()

    t1 = time.time()

    # shots processing _____________________________________________________
    shots = STEP_1_shots_processing(cap, SHOT_TYPES, summary_id, coefficient)

    # resolving double logos _____________________________________________
    STEP_2_resolving_double_logos(shots, SHOT_TYPES)

    # audio processing _________________________________________________
    # Detecing if shot contains high volume ____________________________
    STEP_3_audio_processing(shots, VIDEO_PATH, summary_id)

    # processing output shots __________________________________________________
    # main shots depending on replay and other shots depending on high volume
    output_video_shots_1, output_video_shots_2 = STEP_4_processing_output_shots(
        shots, SHOT_TYPES, summary_id)

    # classifying shots Sequence _____________________________________________
    shots_classes = STEP_5_classifying_shot_sequence(
        output_video_shots_1, output_video_shots_2, SHOT_TYPES, EVENT_TYPES, summary_id)
    # Final output ______________________________________________________________
    output_video_shots, final_video = STEP_6_processing_final_output(
        output_video_shots_1, output_video_shots_2, shots_classes, SHOT_TYPES)

    t2 = time.time()

    # write outputs to file ________________________________________________
    STEP_7_file_output(shots_classes, EVENT_TYPES, video_name,
                       shots, output_video_shots, output_video_shots_2, t1, t2, summary_id)

    # rendering video  _______________________________________________________
    STEP_8_rendering_video(final_video, VIDEO_PATH, output_file_name, summary_id)