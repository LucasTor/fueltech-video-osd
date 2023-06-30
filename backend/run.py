from moviepy.editor import *
from moviepy.video import *
from moviepy.video.tools.drawing import *
import csv

def round_to_closest(x, base=50):
    x = float(x)
    base = int(base)
    return base * round(x/base)

def generate_tach(data_points):
    tach_clip = ImageClip('overlay-tach.png').set_duration(len(data_points) / 25)

    pointers_cache = {}
    pointer_frames = []
    pointer = ImageClip("overlay-pointer.png").set_duration(1/25)
    for x in data_points:
        position = str(round_to_closest(x))
        if not pointers_cache.get(position):
            pointers_cache[position] = pointer.rotate((-round_to_closest(x) / 33.3) + 36, expand=False)

        frame = pointers_cache[position]
        pointer_frames.append(frame)

    pointer_clip = CompositeVideoClip([concatenate_videoclips(pointer_frames, method="compose")])

    text_cache = {}
    text_frames = []
    for x in data_points:
        position = str(round_to_closest(x))
        if not text_cache.get(position):
            text_cache[position] = TextClip(position, font='Patopian-1986', fontsize = 75, color = 'black').set_duration(1/25).set_position(("center","center")).margin(top=300, opacity=0)

        frame = text_cache[position]
        text_frames.append(frame)

    text_clip = CompositeVideoClip([concatenate_videoclips(text_frames, method="compose")]).set_position(('center', 'center'))
    clip = CompositeVideoClip([tach_clip, pointer_clip, text_clip])

    return clip


def generate_lambda(data_points):
    wideband_clip = ImageClip('overlay-wideband.png').set_duration(len(data_points) / 25)

    text_cache = {}
    text_frames = []
    for x in data_points:
        position = f"{float(x):.2f}"
        if not text_cache.get(position):
            text_cache[position] = TextClip(position, font='Patopian-1986', fontsize = 90, color = 'red').set_duration(1/25).set_position(("center","center")).margin(top=15, left=12, opacity=0)

        frame = text_cache[position]
        text_frames.append(frame)

    text_clip = CompositeVideoClip([concatenate_videoclips(text_frames, method="compose")]).set_position(('center', 'center'))

    clip = CompositeVideoClip([wideband_clip, text_clip])

    return clip

with open('log_fueltech.csv', 'r') as csv_file:
    reader = csv.reader(csv_file)
    list = [*reader]
    list.pop(0)

    bg = ImageClip('overlay-bg.png').set_duration(len(list) / 25).set_pos(("center","center"))

    tachometer = generate_tach([x[1] for x in list]).set_position(('center', 'center'))
    wideband = generate_lambda([x[4] for x in list]).set_position((300, 500))

    clip = CompositeVideoClip([bg, tachometer, wideband])

    clip.write_videofile("test.mp4", fps=25)

    # bar = [
    #     ImageClip("overlay-bg.png").set_start((1/25) * idx).set_duration(1/25).set_pos((540,1000)).resize((50, int(float(x[1]) / 20) or 1))
    #     for (idx, x) in enumerate(list)
    # ]