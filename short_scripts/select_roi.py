import cv2
import argparse
 

parser = argparse.ArgumentParser()
parser.add_argument('-i', dest='img_path', required=True)
args = parser.parse_args()

img = cv2.imread(args.img_path)

fromCenter = False
ROI = cv2.selectROIs('Select ROIs', img, fromCenter)

print(ROI)


cv2.waitKey(0)
cv2.destroyAllWindows()