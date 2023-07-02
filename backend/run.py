from moviepy.editor import *
from moviepy.video import *
from moviepy.video.tools.drawing import *
from moviepy.video.fx.all import *
import csv
import moviepy

pointers_cache = {}
pointer = ImageClip("pointer.png").set_duration(1/25)

def round_to_closest(x, base=50):
    x = float(x)
    base = int(base)
    return base * round(x/base)

def generate_tach(data_points):
    tach_clip = ImageClip('tachometer-bg.png').set_duration(len(data_points) / 25)

    pointer_frames = []
    for x in data_points:
        position = str(int((-round_to_closest(x) / 33.3) - 60))
        if not pointers_cache.get(position):
            pointers_cache[position] = pointer.rotate(int(position), expand=False)

        frame = pointers_cache[position]
        pointer_frames.append(frame)

    pointer_clip = concatenate_videoclips(pointer_frames)

    text_cache = {}
    text_frames = []
    for x in data_points:
        position = str(round_to_closest(x))
        if not text_cache.get(position):
            text_cache[position] = TextClip(position, font='Patopian-1986', fontsize = 75, color = 'black').set_duration(1/25).set_position(("center","center")).margin(top=300, opacity=0)

        frame = text_cache[position]
        text_frames.append(frame)

    text_clip = concatenate_videoclips(text_frames).set_position(('center', 'center'))
    clip = CompositeVideoClip([tach_clip, pointer_clip, text_clip])

    return clip

def generate_speed(data_points):
    speed_clip = ImageClip('speedometer-bg.png').set_duration(len(data_points) / 25)

    pointer_frames = []
    for x in data_points:
        position = str(int((-round_to_closest(x, 1) / 1.1) - 55))
        if not pointers_cache.get(position):
            pointers_cache[position] = pointer.rotate(int(position), expand=False)

        frame = pointers_cache[position]
        pointer_frames.append(frame)

    pointer_clip = concatenate_videoclips(pointer_frames)

    text_cache = {}
    text_frames = []
    for x in data_points:
        position = str(round_to_closest(x, 1))
        if not text_cache.get(position):
            text_cache[position] = TextClip(position, font='Patopian-1986', fontsize = 75, color = 'black').set_duration(1/25).set_position(("center","center")).margin(top=300, opacity=0)

        frame = text_cache[position]
        text_frames.append(frame)

    text_clip = concatenate_videoclips(text_frames).set_position(('center', 'center'))
    clip = CompositeVideoClip([speed_clip, pointer_clip, text_clip])

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

    text_clip = concatenate_videoclips(text_frames).set_position(('center', 'center'))

    clip = CompositeVideoClip([wideband_clip, text_clip])

    return clip

def generate_2step(data_points):
    image_2step = ImageClip('2step.png').set_duration(1 / 25)

    on = image_2step
    off = moviepy.video.fx.all.blackwhite(image_2step)

    frames = []
    for x in data_points:
        frame = on if x == 'ON' else off
        frames.append(frame)

    return concatenate_videoclips(frames).set_position(('center', 'center'))

def generate_thing(gauges):
    with open('log_fueltech_2.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)
        list = [*reader]
        list.pop(0)

        bg = ImageClip('overlay-bg.png').set_duration(len(list) / 25).set_pos(("center","center"))
        clip = CompositeVideoClip([bg])

        for gauge in gauges:
            posX = gauge['x']
            posY = gauge['y']
            scale = gauge['scale']
            id = gauge['id']
            gauge = None

            match id:
                case 'tachometer':
                    gauge = generate_tach([x[1] for x in list]).set_position((posX, posY)).resize(scale)

                case 'speedometer':
                    gauge = generate_speed([x[6] for x in list]).set_position((posX, posY)).resize(scale)

                case 'twostep':
                    gauge = generate_2step([x[5] for x in list]).set_position((posX, posY)).resize(scale)

                case 'lambda':
                    gauge = generate_lambda([x[4] for x in list]).set_position((posX, posY)).resize(scale)

            if gauge:
                clip = CompositeVideoClip([clip, gauge])

        clip.write_videofile("test.mp4", fps=25)
