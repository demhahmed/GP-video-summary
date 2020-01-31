import cv2

#reading a video
cap = cv2.VideoCapture('test.mp4')

if cap.isOpened() == False:
    print('err reading video')

#getting video width, height and FPS
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) 
FPS = int(cap.get(cv2.CAP_PROP_FPS))

#initializing a video writer object
out = cv2.VideoWriter('outpy.mp4',cv2.VideoWriter_fourcc('m','p','4','v'), 10, (width,height))
if out.isOpened() == False:
    print('err open video to write')

#video division ratio
delta = int(width/3)
while cap.isOpened():
    #reading a frame
    ret, frame  = cap.read()

    #converting the middle pannel into gray
    panel_middle = frame[0:height,delta:2*delta]
    gray = cv2.cvtColor(panel_middle, cv2.COLOR_BGR2GRAY)
    gray = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)   

    #getting edges of right pannel using canny edge detector
    panel_right = frame[0:height,2*delta:]
    panel_right = cv2.Canny(panel_right, 100 , 200)
    panel_right = cv2.cvtColor(panel_right, cv2.COLOR_GRAY2BGR)

    #copying the pannels to the original video
    frame[0:height,delta:2*delta] = gray
    frame[0:height,2*delta:] = panel_right


    #writing the output video frame by frame
    out.write(frame)

    #displaying the video frame by frame
    if ret == True:
        cv2.imshow('frame', frame)
    
        if cv2.waitKey(25) == ord('q'):
            break

    else: 
        break

#closing all windows
cap.release()
out.release()
cv2.destroyAllWindows() 