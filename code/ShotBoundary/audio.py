import numpy as np  # for numerical operations
from moviepy.editor import VideoFileClip, concatenate


def cut(i, clip, fps): return clip.audio.subclip(i, i+1).to_soundarray(fps=fps)


def volume(array): return np.sqrt(((1.0*array)**2).mean())


def getPeakTimes(path):
    clip = VideoFileClip(path)

    fps = clip.audio.fps
    volumes = [volume(cut(i, clip, fps))
               for i in range(0, int(clip.audio.duration-2))]
    averaged_volumes = np.array([sum(volumes[i:i+10])/10
                                 for i in range(len(volumes)-10)])

    increases = np.diff(averaged_volumes)[:-1] >= 0
    decreases = np.diff(averaged_volumes)[1:] <= 0
    peaks_times = (increases * decreases).nonzero()[0]
    peaks_vols = averaged_volumes[peaks_times]
    peaks_times = peaks_times[peaks_vols > np.percentile(peaks_vols, 90)]

    return peaks_times
