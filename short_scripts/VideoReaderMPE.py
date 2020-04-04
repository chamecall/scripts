import cv2
import moviepy.editor as mpe
import numpy as np


class VideoReader:
    def __init__(self, video_file_name):
        self.cap = cv2.VideoCapture(video_file_name)
        # self.cap.set(cv2.CAP_PROP_POS_FRAMES, 4950)
        video = mpe.VideoFileClip(video_file_name)
        self.length = video.reader.nframes
        self.fps = video.fps
        self.width, self.height = video.size
        self.one_frame_duration = video.duration / self.length * 1000

        self.frames = video.iter_frames()
        self.cur_frame_num = 0
        self.cur_frame = None

    def get_cur_timestamp(self):
        return self.cur_frame_num * self.one_frame_duration

    def get_cur_frame(self):
        return self.cur_frame

    def get_next_frame(self):
        # read, frame = self.cap.read()
        self.cur_frame_num += 1
        frame = next(self.frames)
        self.cur_frame = np.copy(frame[:, :, ::-1])
        return self.get_cur_frame()

    def close(self):
        if self.cap:
            self.cap.release()
