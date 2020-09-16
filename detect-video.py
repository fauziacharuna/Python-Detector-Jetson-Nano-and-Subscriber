import cv2
import numpy as np
import jetson.inference
import jetson.utils

net = jetson.inference.detectNet("ssd-inception-v2", threshold=0.5)
vid = cv2.VideoCapture('/home/smartpark/Videos/videodetection/yabis_avi/0053.avi')
width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*'H264')
writerX = cv2.VideoWriter('/home/smartpark/Videos/videodetection/yabis_avi/result/53.mp4', fourcc, 30.0, (width, height))
while display.IsOpen():
    ret, frame = vid.read()
    frame_rgba = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA).astype(np.float32)
    print('RGBA shape', frame_rgba.shape)
    img = jetson.utils.cudaFromNumpy(frame_rgba)
    detections = net.Detect(img, width, height)
    display.RenderOnce(img, width, height)
    display.setTitle("Object detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
    conversion1 = jetson.utils.cudaToNumpy(img,width,height,4)
    conversion2 = cv2.cvtColor(conversion1, cv2.COLOR_BGR2RGBA).astype(np.uint8)
    conversion3 = cv2.cvtColor(conversion2, cv2.COLOR_BGR2RGBA)
    if ret == True:
            writerX.write(conversion3)
vid.release()
writerX.release()
cv2.destroyAllWindows()
