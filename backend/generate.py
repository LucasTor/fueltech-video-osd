from moviepy.editor import *
from moviepy.video import *
from moviepy.video.tools.drawing import *
from moviepy.video.fx.all import *
from moviepy.video.io.VideoFileClip import *
import csv
import moviepy

for i in range (0, 360):
    pointer = ImageClip("pointer.png").set_duration(1/25)
    moviepy.video.io.VideoFileClip.VideoFileClip.save_frame(pointer.rotate(-i, expand=False), f'./assets/pointers/pointer-{i}.png')