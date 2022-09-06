from img_drawing import get_text_width, draw_img
from text_img import TextImg, Frame
from img_animation import animate_frame
from random import randint, randrange
import ascii_images
# Working with purely one line of text
# /n chars are used to delineate new lines


def generate_background(width: int, height: int) -> str:
    out_str = ""
    for i in range(height):
        out_str += (width * ' ') + '\n'
    return out_str


# Simple case
assert generate_background(3, 2) == "   \n   \n"


def ascii_img_from_file(filename: str) -> str:
    f = open(filename, "r")
    str_list = []
    for line in f.readlines():
        str_list.append(line)
    # Find the longest string in list
    len_lim = 0
    for f_str in str_list:
        if len_lim < len(f_str):
            len_lim = len(f_str)
    pad_str_list = []
    for f_str in str_list:
        # Pad strings with whitespace accordingly
        pad_str = f_str.removesuffix('\n')
        if "\n" in f_str:
            pad_str += (len_lim - len(f_str)) * " " + "\n"
        else:
            pad_str += (len_lim - len(f_str) - 1) * " "
        pad_str_list.append(pad_str)
    # Merge into one str
    out_str = ""
    for pad_str in pad_str_list:
        out_str += pad_str
    return out_str

def snowglobe_generator(num: int, background: str) -> dict[str, TextImg]:
    # characters = "~!@#$%^&*()_+`-={}|[]\\:\";\'<>?,./"
    characters = ".oO0@#%&+~:|/\\"
    max_pos = get_text_width(background) * background.count('\n') - 1
    output_dict = dict()
    for i in range(num):
        # Randomly pick a position
        pos = randint(0, max_pos)
        # Randomly generate content
        content = characters[randint(0, len(characters) - 1)]
        # Randomly pick a direction
        right = randrange(-1, 2, step=2)
        down = randrange(-1, 2, step=2)
        # Generate TextImg in output_dict
        output_dict[f"{content}{i}"] = TextImg(pos, content, right, down)
    return output_dict


if __name__ == '__main__':
    """
    # Animated duck
    bg = generate_background(15, 8)
    duck = TextImg(0, ascii_images.duck_right, right=1, down=1)
    animate_frame(Frame(bg, {'duck': duck}), 0.5, 10, duck=True)
    """
    # Animated snowglobe
    bg = generate_background(50, 25)
    bg = draw_img(TextImg(860, ascii_images.snowman), bg)
    animate_frame(Frame(bg, snowglobe_generator(70, bg)), 0.25, 10)
    