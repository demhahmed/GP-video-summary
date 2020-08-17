import numpy as np
from moviepy.editor import VideoFileClip, concatenate


def cut(i, clip, fps): 
    return clip.audio.subclip(i, i + 1).to_soundarray(fps=fps)


def volume(array): 
    return np.sqrt(((1.0 * array) ** 2).mean())


def get_peak_times(path , perct):
    clip = VideoFileClip(path)
    fps = clip.audio.fps
    vol_intensities = [volume(cut(i, clip, fps)) for i in range(0, int(clip.audio.duration - 2))]
    vol_averages = np.array([sum(vol_intensities[i:i + 10]) / 10 for i in range(len(vol_intensities) - 10)])
    increments = np.diff(vol_averages)[:-1] >= 0
    decrements = np.diff(vol_averages)[1:] <= 0
    spikes_times = (increments * decrements).nonzero()[0]
    spikes_vols = vol_averages[spikes_times]
    spikes_times = spikes_times[spikes_vols > np.percentile(spikes_vols, perct)]
    return spikes_times
