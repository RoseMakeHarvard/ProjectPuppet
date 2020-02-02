import numpy as np
import cv2
import time
import pipeline

xRes = 1920
yRes = 1080
cap = cv2.VideoCapture('http://10.253.64.129:8080/video')
g = pipeline.GripPipeline()

while (True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    g.process(frame)
    # redBand, greenBand, blueBand = cv2.split(frame)
    # cv2.threshold(redBand, 200, 255, cv2.THRESH_TOZERO_INV, redBand)
    # cv2.threshold(blueBand, 0, 0, cv2.THRESH_TOZERO, blueBand)
    # cv2.threshold(blueBand, 0, 0, cv2.THRESH_TOZERO, greenBand)

    # newFrame = cv2.merge([redBand,greenBand,blueBand])
    # Display the resulting frame
    # cv2.imshow('frame', newFrame)
    rect = cv2.boundingRect(g.find_contours_1_output[1])
    print(rect)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
