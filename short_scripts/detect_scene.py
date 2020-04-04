# USAGE
# python detect_scene.py --video batman_who_laughs_7.mp4 --output output

# import the necessary packages
import argparse
import imutils
import cv2
import os
from tqdm import trange

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", required=True, type=str,
	help="path to input video file")
ap.add_argument("-o", "--output", required=True, type=str,
	help="path to output directory to store frames")
ap.add_argument("-p", "--min-percent", type=float, default=30.0,
	help="lower boundary of percentage of motion")
ap.add_argument("-m", "--max-percent", type=float, default=30.0,
	help="upper boundary of percentage of motion")
ap.add_argument("-w", "--warmup", type=int, default=0,
	help="# of frames to use to build a reasonable background model")
args = vars(ap.parse_args())

# initialize the background subtractor
fgbg = cv2.bgsegm.createBackgroundSubtractorGMG()

# initialize a boolean used to represent whether or not a given frame
# has been captured along with two integer counters -- one to count
# the total number of frames that have been captured and another to
# count the total number of frames processed
captured = False
total = 0
frames = 0

# open a pointer to the video file initialize the width and height of
# the frame
cap = cv2.VideoCapture(args["video"])
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
cap.set(cv2.CAP_PROP_POS_FRAMES, 290 * fps)

length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
vid_writer = cv2.VideoWriter('face_recognintion.mkv', cv2.VideoWriter_fourcc(*"XVID"),
                                                fps,
                                                (width, height))
(W, H) = (None, None)

# loop over the frames of the video
p_high_value = None
for _ in trange(length):
	# grab a frame from the video
	(grabbed, frame) = cap.read()

	# if the frame is None, then we have reached the end of the
	# video file
	if frame is None:
		break

	# clone the original frame (so we can save it later), resize the
	# frame, and then apply the background subtractor
	orig = frame.copy()
	frame = imutils.resize(frame, width=600)
	mask = fgbg.apply(frame)

	# apply a series of erosions and dilations to eliminate noise
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	# if the width and height are empty, grab the spatial dimensions
	if W is None or H is None:
		(H, W) = mask.shape[:2]

	# compute the percentage of the mask that is "foreground"
	p = int((cv2.countNonZero(mask) / float(W * H)) * 100)

	# if there is less than N% of the frame as "foreground" then we
	# know that the motion has stopped and thus we should grab the
	# frame
	if p < args["min_percent"] and not captured and frames > args["warmup"]:
		# show the captured frame and update the captured bookkeeping
		# variable
		captured = True
		cv2.putText(orig, f"New Scene - {p_high_value}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
		p_high_value = None

		for i in range(30):
			vid_writer.write(orig)


	elif captured and p >= args["max_percent"]:
		if p_high_value is None:
			p_high_value = int(p)
		captured = False

	# display the frame and detect if there is a key press
	vid_writer.write(orig)

	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

	# increment the frames counter
	frames += 1

# do a bit of cleanup
cap.release()
vid_writer.release()