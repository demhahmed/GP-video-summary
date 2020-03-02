import cv2
import numpy as np

grass_color = (100, 150, 50)
grass_threshold = 20

goalpost_color = (220, 220, 220)
goalpost_threshold = 5

horizontal_threshold = 10
vertical_threshold = 10

def magnitude(x1, y1, x2, y2):
    return np.sqrt((x2-x1)**2.0 + (y2-y1)**2.0)

def angle(x1,y1,x2,y2):
    if x2 == x1: return 0
    return np.arctan((y2-y1)/(x2-x1))

def rt_degrees(rt):
    return np.array([[r, np.rad2deg(t)] for r, t in rt])

def find_lines(edges, threshold=65, minLineLength=40, maxLineGap=10):
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold, minLineLength=minLineLength, maxLineGap=maxLineGap)
    if lines is None: return []
    lines = [(magnitude(*line[0]), angle(*line[0])) for line in lines]
    return lines

def color_space(img, target_color):
	#luv = cv2.cvtColor(img, cv2.COLOR_RGB2Luv)
    R1, G1, B1 = img[:,:,0], img[:,:,1], img[:,:,2]
    R2, G2, B2 = target_color
    rmean = ((R1 + R2) / 2).astype('int')
    rsquare = np.square(R1 - R2)
    gsquare = np.square(G1 - G2)
    bsquare = np.square(B1 - B2)
    result = (((512+rmean)*rsquare)>>8) + 4*gsquare + (((767-rmean)*bsquare)>>8)
    result = result.astype('float')
    result -= np.min(result)
    result /= np.max(result)
    result *= 255
    result = result.astype('int')
    return result

def detect_goalpost(img):
    grass = color_space(img, grass_color) < grass_threshold
    img[grass] = [0,0,0]
    
    goalpost = color_space(img, goalpost_color) < goalpost_threshold
    img_goalpost = goalpost.astype(bool).astype('uint8') * 255

    img_goalpost = cv2.medianBlur(img_goalpost, 5)
    kernel = np.ones((7,7))
    img_goalpost = cv2.morphologyEx(img_goalpost, cv2.MORPH_CLOSE, kernel)
    
    density = np.mean(img_goalpost)/255

    if density < 0.3:
        lines = find_lines(img_goalpost)
        lines = rt_degrees(lines)
    else:
        return False 

    if len(lines) == 0:
        return False

    f2 = 0
    # an image has a goalpost if two perpendicular lines with 0 degrees and 90 degrees intersect
    horizontal_line = len(lines[(abs(lines[:,1]) < horizontal_threshold)]) > 0
    for line in lines:
        if abs(abs(line[1]) - 90) < vertical_threshold:
            f2 += 1
    print(f2)        
    if f2 > 0:
        vertical_line = True
    else:
        vertical_line = False    
    return horizontal_line and vertical_line

images = ['im_6.jpg','im_10.jpg','im_1.jpg','im_2.jpg','im_4.jpg','im_7.jpg','im_8.jpg']
for img in images:
    print(detect_goalpost(cv2.imread(img).astype('int')))