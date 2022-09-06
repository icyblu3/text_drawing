class TextImg:
    def __init__(self, pos: int, content: str, right=0, down=0):
        self.pos = pos
        self.content = content
        self.right = right
        self.down = down


# Contains a list of images
class Frame:
    def __init__(self, bg: str, images: dict[str, TextImg]):
        self.bg = bg
        self.images = images
