import argparse
import sys
from PIL import Image
import cv2
import glob
import jetson.inference
import jetson.utils
import os, sys
path = "/home/smartpark/Pictures/data/Full/result/{}.jpg"
scalePercent = 50
for bb, file in enumerata(glob.glob(path)):
    print(file)
    a = cv2.imread(file)
    print(a)
    img, width, height = jetson.utils.loadImageRGBA(file)
    net = jetson.inference.detectNet("ssd-inception-v2", threshold=0.5)
    detections = net.Detect(img, width, height, overlays = 'box, labels, conf')
    file_out = r'/home/smartpark/Pictures/data/Full/result/{}.jpg'
    if file_out is not None:
        jetson.utils.saveImageRGBA(file_out.format(bb), img, width, height)
        k = cv2.waitKey(500)
        cv2.destroyAllWindows