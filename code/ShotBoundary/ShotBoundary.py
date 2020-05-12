import cv2


def histogram_compare(image_1, image_2):
    frame1 = cv2.cvtColor(image_1, cv2.COLOR_BGR2RGB)
    frame2 = cv2.cvtColor(image_2, cv2.COLOR_BGR2RGB)
    # extract a 3D RGB color histogram from the image,
    # using 8 bins per channel, normalize, and update
    # the index
    hist1 = cv2.calcHist([frame1], [0, 1, 2], None, [
                         64, 64, 64], [0, 256, 0, 256, 0, 256])
    hist1 = cv2.normalize(hist1, hist1).flatten()
    hist2 = cv2.calcHist([frame2], [0, 1, 2], None, [
                         64, 64, 64], [0, 256, 0, 256, 0, 256])
    hist2 = cv2.normalize(hist2, hist2).flatten()
    return cv2.compareHist(hist1, hist2, cv2.HISTCMP_INTERSECT), 10 * cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)


def block_change(frame1, frame2):
    count = 0
    for r in range(0, frame1.shape[0], 150):
        for c in range(0, frame2.shape[1], 150):
            window1 = frame1[r:r + 150, c:c + 150]
            window2 = frame2[r:r + 150, c:c + 150]
            intersect, corr = histogram_compare(window1, window2)
            if intersect < 4 and corr < 4:
                count += 1
            elif intersect > 4 and corr < 4:
                count += 0.75
            elif intersect > 4 and corr > 4:
                count += 0.25
            elif intersect < 4 and corr > 4:
                count += 0.1
    return (count / 28 * 100)


def cut_detector(frame1, frame2):
    intersect, corr = histogram_compare(frame1, frame2)
    if intersect > 6 and corr > 5:
        return False
    return block_change(frame1, frame2) >= 30
'''
img1 = cv2.imread(
    "C:/Users\\salama\\Desktop\\GP-video-summary\\code\\ShotBoundary\\frame90.jpg")

 
img2 = cv2.imread(
    "C:/Users\\salama\\Desktop\\GP-video-summary\\code\\ShotBoundary\\frame95.jpg")
print(cut_detector(img1, img2))
'''