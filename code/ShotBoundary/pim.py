import numpy as np
import pims
V = pims.video('filename.avi')
im = V[100]
im = np.array(im)


@pims.pipeline
def grayscale(vid):
    return np.array(vid)[..., 0].astype('float')/255  # float grayscale


gray = grayscale(vid)
