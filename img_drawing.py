from text_img import TextImg, Frame
import math


def get_text_width(text: str) -> int:
    ctr = 0
    while ctr < len(text):
        if text[ctr] == "\n":
            return ctr
        ctr += 1
    # Single line of text case
    return ctr


# Simple case
assert get_text_width(" ___ \n|   |\n|   |\n|___|") == 5


def cut_line_width(line: str, excess: int) -> str:
    if line[len(line) - 1] == "\n":
        return line[: len(line) - excess - 1] + "\n"
    else:
        return line[: len(line) - excess]


assert cut_line_width(" ___ \n", 2) == " __\n"
assert cut_line_width(" ___ ", 1) == " ___"


def cut_str_width(img_str: str, excess: int) -> str:
    img_width = get_text_width(img_str)
    new_str = ""
    cur_ind = 0
    row_end_ind = cur_ind + img_width
    while row_end_ind <= len(img_str):
        new_str += cut_line_width(img_str[cur_ind: row_end_ind], excess)
        # Move to next row
        try:
            if img_str[row_end_ind] == "\n":
                new_str += "\n"
        except IndexError:
            pass
        cur_ind = row_end_ind + 1
        row_end_ind = cur_ind + img_width
    return new_str


# Simple case
assert cut_str_width(" ___ \n|   |\n|   |\n|___|", 2) == " __\n|  \n|  \n|__"

assert cut_str_width(" ___ \n|   |\n|   |\n|___|", 1) == " ___\n|   \n|   \n|___"

assert cut_str_width(" ___ \n|   |\n|   |\n|___|", 0) == " ___ \n|   |\n|   |\n|___|"


def cut_str_height(img_str: str, excess: int) -> str:
    img_width = get_text_width(img_str)
    # Need to plus 1 because of new line char
    return img_str[: len(img_str) - excess * (img_width + 1)]


# Simple case
assert cut_str_height(" ___ \n|   |\n|   |\n|___|", 2) == " ___ \n|   |"


# Using zero indexing
def get_img_ypos(img: TextImg, background: str) -> int:
    bg_width = get_text_width(background)
    try:
        return math.floor(img.pos / bg_width)
    except ZeroDivisionError:
        return 0


assert get_img_ypos(TextImg(10, "+++\n***\n---"),
                    " ___ \n|   |\n|   |\n|___|") == 2


# Using zero-indexing
def get_img_xpos(img: TextImg, background: str, img_ypos: int) -> int:
    # Get difference between start of row and img.pos
    return img.pos - img_ypos * get_text_width(background)


assert get_img_xpos(TextImg(0, "+++\n***\n---"),
                    " ___ \n|   |\n|   |\n|___|", 0) == 0

assert get_img_xpos(TextImg(6, "+++\n***\n---"),
                    " ___ \n|   |\n|   |\n|___|", 1) == 1

assert get_img_xpos(TextImg(12, "+++\n***\n---"),
                    " ___ \n|   |\n|   |\n|___|", 2) == 2


# Cut off parts of a text img that exceeds the background
# Consumes a TextImg and background as arguments
# Returns the cut off img
def cut_off_overshoot(img: TextImg, background: str) -> str:
    bg_height = background.count('\n')
    bg_width = get_text_width(background)
    img_height = img.content.count('\n') + 1  # Accounting for first line
    img_width = get_text_width(img.content)
    # Cut height first
    cut_img = img.content
    img_ypos = get_img_ypos(img, background)
    excess_height = img_height + img_ypos - bg_height
    if excess_height > 0:
        cut_img = cut_str_height(cut_img, excess_height)
    excess_width = img_width + get_img_xpos(img, background, img_ypos) - bg_width
    if excess_width > 0:
        cut_img = cut_str_width(cut_img, excess_width)
    return cut_img


# No cut
assert cut_off_overshoot(TextImg(1, "+++\n***\n---"),
                         " ___ \n|   |\n|   |\n|___|\n") == "+++\n***\n---"

# Cut width
assert cut_off_overshoot(TextImg(3, "+++\n***\n---"),
                         " ___ \n|   |\n|   |\n|___|\n") == "++\n**\n--"

# Cut height
assert cut_off_overshoot(TextImg(10, "+++\n***\n---"),
                         " ___ \n|   |\n|   |\n|___|\n") == "+++\n***"

# Cut both
assert cut_off_overshoot(TextImg(13, "+++\n***\n---"),
                         " ___ \n|   |\n|   |\n|___|\n") == "++\n**"


# Replace the characters in a string  starting from the given index with another string
def replace_chars(org_str: str, sub_str: str, ind: int, count: int):
    if len(sub_str) < count:
        raise Exception("Less characters in substr than count")
    if len(org_str) < ind + count:
        raise Exception("Not enough chars in org str to replace")
    char_list = []
    for i in org_str:
        char_list.append(i)
    ctr = 0
    while ctr < count:
        char_list[ind + ctr] = sub_str[ctr]
        ctr += 1
    # Convert back into str
    new_str = ""
    for i in char_list:
        new_str += i
    return new_str


assert replace_chars("abcde", "ghi", 1, 2) == "aghde"


# Calculate img_index for drawing onto a background
def get_img_index(img: TextImg, background: str) -> int:
    img_ypos = get_img_ypos(img, background)
    bg_width = get_text_width(background)
    return img_ypos * (bg_width + 1) + get_img_xpos(img, background, img_ypos)


# Add option to ignore bordering whitespace chars
# Draws a given TextImg onto a background
def draw_img(img: TextImg, background: str) -> str:
    cut_img = cut_off_overshoot(img, background)
    # Get starting index
    bg_width = get_text_width(background)
    cur_ind = get_img_index(TextImg(img.pos, cut_img), background)
    img_height = cut_img.count('\n') + 1  # Accounting for first line
    img_width = get_text_width(cut_img)
    for i in range(img_height):
        # +1 for new line char
        background = replace_chars(background, cut_img[(img_width + 1) * i:], cur_ind, img_width)
        # Move to next row
        cur_ind += bg_width + 1
    return background


# Simple case
assert draw_img(TextImg(1, "+++"),
                " ___ \n|   |\n|   |\n|___|\n") == " +++ \n|   |\n|   |\n|___|\n"
assert draw_img(TextImg(1, "+++\n***\n---"),
                " ___ \n|   |\n|   |\n|___|\n") == " +++ \n|***|\n|---|\n|___|\n"

# With image cutting
assert draw_img(TextImg(13, "+++\n***\n---"),
                " ___ \n|   |\n|   |\n|___|\n") == " ___ \n|   |\n|  ++\n|__**\n"


def frame_to_str(frame: Frame) -> str:
    output_str = frame.bg
    # Deal with overlap WIP
    for key in frame.images.keys():
        output_str = draw_img(frame.images[key], output_str)
    return output_str


# Simple case
assert frame_to_str(Frame(" ___ \n|   |\n|   |\n|___|\n",
                          {'plus': TextImg(1, "+++"),
                           'minus': TextImg(6, "---")})) == " +++ \n|---|\n|   |\n|___|\n"
