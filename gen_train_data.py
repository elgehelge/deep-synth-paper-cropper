import random
import numpy

from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color


class CornerImageGenerator:

    def __init__(self, image_width, image_height, allow_outside_distance):
        self.image_width = image_width
        self.image_height = image_height
        self.outside_limit = allow_outside_distance

    def random_coord(self, allow_outside=False):
        if allow_outside:
            extra = self.outside_limit
        else:
            extra = 0
        return \
            random.randint(0 - extra, self.image_width - 1 + extra), \
            random.randint(0 - extra, self.image_height - 1 + extra)

    @staticmethod
    def translate_coord(coord, translation):
        return coord[0]+translation[0], coord[1]+translation[1]

    def generate(self):
        with Image(width=self.image_width, height=self.image_height, background=Color('black')) as image:
            with Drawing() as draw:
                draw.fill_color = Color('white')
                corner_of_interest = self.random_coord(allow_outside=True)
                corners = [
                    self.translate_coord(self.random_coord(), (-self.image_width, 0)),  # bottom left (not visible)
                    corner_of_interest,  # bottom right (possibly visible)
                    self.translate_coord(self.random_coord(), (0, -self.image_height)),  # top right (not visible)
                    self.translate_coord(self.random_coord(), (-self.image_width, -self.image_height)),  # top left (not
                    # visible)
                ]
                draw.polygon(corners)
                draw(image)
                numpy_image = numpy.fromstring(image.make_blob("gray"), numpy.uint8).reshape(image.height, image.width)
                return numpy_image, corner_of_interest

    def generator(self):
        while True:
            yield self.generate()
