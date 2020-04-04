import sys
import moviepy.editor as mpe

video = mpe.VideoFileClip(sys.argv[1])
print('duration is', video.duration)
print('fps is ', video.fps)
frames_count = int(video.fps * video.duration)
print('frames count is', frames_count)
print('size is', video.size)