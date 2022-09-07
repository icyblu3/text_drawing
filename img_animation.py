from text_img import TextImg, Frame
from img_drawing import get_img_index, get_img_ypos, get_text_width, frame_to_str
from time import sleep
import os
from ascii_images import duck_left, duck_right
import math
from typing import Tuple


# Returns a tuple, first value is new pos and 2nd value is new direction
def get_sideways_motion(frame: Frame, img_name: str) -> Tuple[int, int]:
    img = frame.images[img_name]
    # Case where no space for sideways_motion
    if get_text_width(img.content) == get_text_width(frame.bg):
        return img.pos, 0
    # Moving right and colliding
    if img.right == 1 and frame.bg[get_img_index(img, frame.bg) +
                                   img.right + get_text_width(img.content) - 1] == "\n":
        return img.pos - img.right, -img.right
    # Moving left and colliding
    elif img.right == -1 and frame.bg[get_img_index(img, frame.bg) + img.right] == "\n":
        return img.pos - img.right, -img.right
    else:
        return img.pos + img.right, img.right


# Simple case
assert get_sideways_motion(
    Frame("012\n345\n678\n", {'plus': TextImg(1, "+", right=1)}), 'plus') == (2, 1)

# Left movement
assert get_sideways_motion(
    Frame("012\n345\n678\n", {'plus': TextImg(1, "+", right=-1)}), 'plus') == (0, -1)

# Collision
assert get_sideways_motion(
    Frame("012\n345\n678\n", {'plus': TextImg(2, "+", right=1)}), 'plus') == (1, -1)
assert get_sideways_motion(
    Frame("012\n345\n678\n", {'plus': TextImg(3, "+", right=-1)}), 'plus') == (4, 1)

# Wide img
assert get_sideways_motion(
    Frame("012\n345\n678\n", {'plus': TextImg(1, "++", right=1)}), 'plus') == (0, -1)

# No space for sideways motion
assert get_sideways_motion(
    Frame("0\n", {'plus': TextImg(0, "+", right=-1)}), 'plus') == (0, 0)


# Returns a tuple, first value is new pos and 2nd value is new direction
def get_topdown_motion(frame: Frame, img_name: str) -> Tuple[int, int]:
    img = frame.images[img_name]
    # Account for no space for topdown_motion
    if frame.bg.count("\n") == img.content.count("\n") + 1:
        return img.pos, 0
    img_ypos = get_img_ypos(img, frame.bg)
    img_height = img.content.count('\n') + 1  # Accounting for first line
    bg_height = frame.bg.count('\n')
    bg_width = get_text_width(frame.bg)
    # Hitting border
    if img_ypos + img.down < 0 or img_ypos + img.down + img_height >= bg_height:
        return img.pos - img.down * bg_width, -img.down
    else:
        return img.pos + img.down * bg_width, img.down


# Simple case
assert get_topdown_motion(
    Frame("012\n345\n678\n", {'plus': TextImg(1, "+", down=1)}), 'plus') == (4, 1)

# Collision
assert get_topdown_motion(
    Frame("012\n345\n678\n", {'plus': TextImg(7, "+", down=1)}), 'plus') == (4, -1)

# Tall img
assert get_topdown_motion(
    Frame("012\n345\n678\n", {'plus': TextImg(4, "+\n+", down=1)}), 'plus') == (1, -1)

# No space for topdown_motion
assert get_topdown_motion(
    Frame("0\n", {'plus': TextImg(0, "+", down=1)}), 'plus') == (0, 0)


# For dir:
# 1: Movement in that direction
# 0: no movement in that direction
# -1: movement in opp direction
def update_img_pos(frame: Frame, img_name: str):
    # Move sideways first
    new_pos, new_side_dir = get_sideways_motion(frame, img_name)
    # Update values
    frame.images[img_name].pos = new_pos
    frame.images[img_name].right = new_side_dir
    # Move topdown
    new_pos, new_updown_dir = get_topdown_motion(frame, img_name)
    # Update values
    frame.images[img_name].pos = new_pos
    frame.images[img_name].down = new_updown_dir


# Changes the duck TextImg based on direction duck is heading toward
def change_duck(frame: Frame, img_name: str):
    duck_img = frame.images[img_name]
    if duck_img.right == 1:
        duck_img.content = duck_right
    elif duck_img.right == -1:
        duck_img.content = duck_left


# Shift the imgs within a frame according to their direction
def animate_frame(frame: Frame, interval: float, duration: int, duck=False):
    clear_console = 'clear' if os.name == 'posix' else 'CLS'
    num_frames = math.floor(duration / interval)
    frame_strs = []
    # Generate all text to be output
    for i in range(num_frames):
        frame_strs.append(frame_to_str(frame))
        for img_name in frame.images.keys():
            update_img_pos(frame, img_name)
            if duck:
                change_duck(frame, 'duck', )

    # Output text frame by frame
    for frame_str in frame_strs:
        os.system(clear_console)
        print(frame_str)
        sleep(interval)
