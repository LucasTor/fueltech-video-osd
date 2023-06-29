from moviepy.editor import *
from moviepy.video import *
from moviepy.video.tools.drawing import *
import csv

def round_to_closest(x, base=50):
    return base * round(x/base)

pointers_cache = {}
rpm_text_cache = {}

with open('log_fueltech.csv', 'r') as csv_file:
    reader = csv.reader(csv_file)
    list = [*reader]
    list.pop(0)

    bg = ImageClip('overlay-bg.png').set_duration(len(list) / 25).set_pos(("center","center"))
    tach = ImageClip('overlay-tach.png').set_duration(len(list) / 25).set_pos(("center","center"))

    clip = CompositeVideoClip([tach])

    del tach

    pointer_frames = []
    pointer = ImageClip("overlay-pointer.png").set_duration(1/25).set_pos(("center","center"))
    for x in list:
        position = str(int(round_to_closest(int(x[1]))))
        if not pointers_cache.get(position):
            pointers_cache[position] = pointer.rotate((-int(round_to_closest(int(x[1]))) / 33.3) + 36, expand=False)

        frame = pointers_cache[position]
        pointer_frames.append(frame)

    pointer_clip = CompositeVideoClip([concatenate_videoclips(pointer_frames, method="compose")]).set_position(('left', 'top'))

    text_frames = []
    for x in list:
        position = str(int(round_to_closest(int(x[1]))))
        if not rpm_text_cache.get(position):
            rpm_text_cache[position] = TextClip(position, fontsize = 75, color = 'black').set_duration(1/25).set_position(("center","center")).margin(top=300, opacity=0)

        frame = rpm_text_cache[position]
        text_frames.append(frame)

    text_clip = CompositeVideoClip([concatenate_videoclips(text_frames, method="compose")]).set_position(('center', 'center'))
    clip = CompositeVideoClip([clip, pointer_clip, text_clip])
    clip = clip.set_position(('center', 'center'))

    clip = CompositeVideoClip([bg, clip])

    print('rpm done')

    clip.write_videofile("test.mp4", fps=25)
    exit()

    del frames

    # clip = VideoFileClip("test.mp4")
    frames = [
        TextClip(x[1], fontsize = 75, color = 'black').set_start((1/25) * idx).set_duration(1/25).set_pos(("center","center")).margin(top=300, opacity=0)
        for (idx, x) in enumerate(list)
    ]
    clip = CompositeVideoClip([clip, *frames])
    # clip.write_videofile("test.mp4", fps=25)
    print('rpm text done')

    del frames

    # clip = VideoFileClip("test.mp4")
    frames = [
        TextClip(f"Lambda: {x[4]}", fontsize = 50, color = 'black').set_start((1/25) * idx).set_duration(1/25).set_pos(("center","center")).margin(top=600, opacity=0)
        for (idx, x) in enumerate(list)
    ]
    clip = CompositeVideoClip([clip, *frames])
    # clip.write_videofile("test.mp4", fps=25)
    print('lambda done')

    del frames

    # clip = VideoFileClip("test.mp4")
    frames = [
        TextClip(f"TPS: {x[2]}%", fontsize = 50, color = 'black').set_start((1/25) * idx).set_duration(1/25).set_pos(("center","center")).margin(top=725, opacity=0)
        for (idx, x) in enumerate(list)
    ]

    clip = CompositeVideoClip([clip, *frames])

    print('tps done')

    clip.write_videofile("test.mp4", fps=25)

    # bar = [
    #     ImageClip("overlay-bg.png").set_start((1/25) * idx).set_duration(1/25).set_pos((540,1000)).resize((50, int(float(x[1]) / 20) or 1))
    #     for (idx, x) in enumerate(list)
    # ]