import cv2
import numpy as np

img = cv2.imread("../images/lol.jpeg", 0)
cv2.imshow('g',img)
cv2.waitKey(0)