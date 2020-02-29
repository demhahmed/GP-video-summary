
from FrameBlocks import block_Change
from HistogramCompare import histogramCompare


def cutDetector(frame1, frame2):
    intersect, corr = histogramCompare(frame1, frame2)

    if intersect > 6 and corr > 5:
        return False

    #frame_blocks_1 = getFrameBlocks(frame1, frame1.shape[0], frame1.shape[1])
    #frame_blocks_2 = getFrameBlocks(frame2, frame1.shape[0], frame1.shape[1])

    if block_Change(frame1, frame2) >= 30:
        return True
    return False
