import cv2
import numpy as np
from math import sqrt
import argparse
 

parser = argparse.ArgumentParser()
parser.add_argument('-i', dest='img_path', required=True)
args = parser.parse_args()

windowName = 'MouseCallback'
img = cv2.imread(args.img_path)
cv2.namedWindow(windowName)

 
def CallBackFunc(event, x, y, flags, param):

	if event == cv2.EVENT_MBUTTONDOWN:
		cv2.putText(img, f'{x}, {y}', (x, y), cv2.FONT_HERSHEY_SIMPLEX,
		0.65, (0, 255, 0), 2)

cv2.setMouseCallback(windowName, CallBackFunc)
 
 
def main():
	while (True):
		cv2.imshow(windowName, img)
		if cv2.waitKey(20) == 27:
			break
 
	cv2.destroyAllWindows()
 
 
if __name__ == "__main__":
	main()