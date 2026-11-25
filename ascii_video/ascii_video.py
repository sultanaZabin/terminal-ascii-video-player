import cv2
import time
import os
import shutil

# to start this program: open the terminal
# install opencv: py -m pip install opencv-python
# then to start type in [ py ascii_video.py ], make sure you're in the right directory
# and to end it just click ctrl + c
video_file = "symphony.mp4"     # put the video u want in the same folder as the one this .py file is in

# Knobs: you can tune any of these parameters
resolution = 250                    # bigger number = more detail
fps = 10                            # frames per second (increase this and u'll get a smoother video, but it might take long to load)
squish = 0.40                       # terminal letters are ~2x taller than wide, this fixes it
color_pop = 1.8                     # color boost (1 = real colors, 2 = super vivid)
dark_cutoff = 60                    # ranger is (0 - 255), any thing thats darker than the number u choose will become an empty charachter
                                    # play with it see what best fits ur video
char_set = " .:-=+*#%@"             # from dark (.) to bright (@)

def get_size(vid_w, vid_h):
    # fit the video inside the terminal so nothing wraps around
    term = shutil.get_terminal_size((resolution, 50))
    cols = min(resolution, term.columns - 1)
    rows = int(cols * vid_h / vid_w * squish)
    if rows > term.lines - 1:
        rows = term.lines - 1
        cols = int(rows * vid_w / vid_h / squish)
    return cols, rows


def frame_to_ascii(img, cols, rows):
    small = cv2.resize(img, (cols, rows), interpolation=cv2.INTER_AREA)
    pixels = small.tolist()          
    lines = []
    for row in pixels:
        bits = []
        for b, g, r in row:
            light = 0.299 * r + 0.587 * g + 0.114 * b
            if light < dark_cutoff:
                bits.append(" ")
                continue
            ch = char_set[int(light / 256 * len(char_set))]
            # make colors brighter so thin charachters have color too
            boost = min(color_pop, 255 / max(r, g, b, 1))
            r = int(r * boost)
            g = int(g * boost)
            b = int(b * boost)
            bits.append("\033[38;2;" + str(r) + ";" + str(g) + ";" + str(b) + "m" + ch)
        lines.append("".join(bits) + "\033[0m")
    return "\n".join(lines)


def load_frames():
    vid = cv2.VideoCapture(video_file)
    if not vid.isOpened():
        print("couldn't open", video_file, "- is it in the same folder as this file?")
        raise SystemExit

    real_fps = vid.get(cv2.CAP_PROP_FPS) or 30
    step = real_fps / fps              # for example if real_fps = 60, then 60/10 = 6, take every sixth frame
    frames = []
    count = 0
    next_keep = 0.0
    cols = rows = None

    while True:
        ok, img = vid.read()
        if not ok:
            break
        if count >= next_keep:
            if cols is None:
                h, w = img.shape[:2]
                cols, rows = get_size(w, h)
            frames.append(frame_to_ascii(img, cols, rows))
            next_keep += step
            print("\rmaking frames... " + str(len(frames)), end="", flush=True)
        count += 1

    vid.release()
    return frames


if __name__ == "__main__":
    frames = load_frames()
    if not frames:
        print("\nno frames found :(")
        raise SystemExit

    os.system("cls" if os.name == "nt" else "clear")
    print("\033[?25l", end="")          
    wait = 1 / fps
    try:
        while True:                      
            for f in frames:
                start = time.time()
                print("\033[H" + f, end="", flush=True)
                nap = wait - (time.time() - start)
                if nap > 0:
                    time.sleep(nap)
    except KeyboardInterrupt:
        print("\033[?25h\033[0m")
