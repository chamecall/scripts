import cv2

class VideoReader:
    def __init__(self, video_file_name):
        self.cap = cv2.VideoCapture(video_file_name)
        self.frames_no = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        width  = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.size = (width, height)

    def rewind(self, frame_no):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)

    def read(self):
        return self.cap.read()

    def release(self):
        if self.cap:
            self.cap.release()
