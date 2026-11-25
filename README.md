# ascii video player

turn any video into colored ascii art and play it right in ur terminal

every frame gets shrunk down, each pixel becomes a character based on how bright it is (` .:-=+*#%@`), and then it gets painted with the pixel's real color (boosted a bit so it pops)

---

## what it does

- plays any video opencv can open (`.mp4`, `.mov`, `.avi`, ...)
- full 24-bit color using ansi escape codes
- fits the video inside ur terminal so nothing wraps around
- fixes the tall letters problem so the video doesn't look stretched
- loops forever until u stop it
- has a few knobs u can play with to change the look

---

## what u need

- python 3
- opencv

```bash
py -m pip install opencv-python
```

(on mac / linux use `python3 -m pip install opencv-python`)

---

## how to run it

1. put the video u want in the same folder as `ascii_video.py`
2. open `ascii_video.py` and change the file name to ur video:
   ```python
   video_file = "symphony.mp4"
   ```
3. open the terminal, make sure ur in the right directory, then type:
   ```bash
   py ascii_video.py
   ```
   (or `python3 ascii_video.py` on mac / linux)
4. wait for it to finish `making frames...` and enjoy
5. to end it just click **ctrl + c**

> **tip:** make ur terminal full screen and zoom out (ctrl + minus) before u run it. smaller font = more room = way more detail

---

## knobs

u can tune any of these, they're at the top of `ascii_video.py`:

| knob | default | what it does |
|------|---------|--------------|
| `resolution` | `250` | bigger number = more detail (it still can't go wider than ur terminal) |
| `fps` | `10` | frames per second. increase it and u'll get a smoother video, but it might take long to load |
| `squish` | `0.40` | terminal letters are ~2x taller than wide, this fixes it |
| `color_pop` | `1.8` | color boost. `1` = real colors, `2` = super vivid |
| `dark_cutoff` | `60` | range is (0 - 255), anything thats darker than the number u choose becomes an empty character. play with it and see what fits ur video best |
| `char_set` | `" .:-=+*#%@"` | the characters it uses, from dark to bright. u can swap in ur own |

---

## how it works

1. **load:** opencv reads the video and only keeps every nth frame. for example if the video is 60 fps and u want 10, then 60/10 = 6, so it takes every sixth frame
2. **resize:** each frame gets shrunk to fit the terminal
3. **brightness:** the brightness of each pixel is calculated with `0.299·R + 0.587·G + 0.114·B`
4. **pick a character:** that brightness picks a character from `char_set`
5. **color it:** the character gets wrapped in an ansi color code `\033[38;2;R;G;Bm`
6. **play:** all the frames are made first, then they get drawn one after the other by moving the cursor back to the top (`\033[H`) instead of clearing the screen, so it doesn't flicker

---

## notes

- **colors not showing or u see weird symbols?** use a terminal that supports 24-bit color like windows terminal, the vs code terminal, or any modern mac / linux terminal. the old windows `cmd` might not work well
- **long videos** take a while to load and use a lot of memory, since every frame gets made before it starts playing. lower the `fps` or `resolution`, or just use a shorter clip
- **don't resize the terminal while it's playing**, it'll mess up the picture because the size is only picked once at the start
