import cv2
from VideoReaderCV2 import VideoReader

class VideoWriter:
	def __init__(self, out_name, reader: VideoReader):
		self.reader = reader
		fourcc = cv2.VideoWriter_fourcc(*"mp4v")
		print(out_name)
		self.writer = cv2.VideoWriter(out_name, fourcc, self.reader.fps, self.reader.size)

	def write(self, frame):
		self.writer.write(frame)


	def release(self):
		if self.writer:
			self.writer.release()