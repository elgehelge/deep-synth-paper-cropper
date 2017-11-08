import random
import numpy

from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color


class CornerImageGenerator:

    def __init__(self, image_width, image_height):
        self.image_width = image_width
        self.image_height = image_height

    def random_coord(self):
        return random.randint(0, self.image_width-1), random.randint(0, self.image_height-1)

    @staticmethod
    def translate_coord(coord, translation):
        return coord[0]+translation[0], coord[1]+translation[1]

    def generate(self):
        with Image(width=self.image_width, height=self.image_height, background=Color('black')) as image:
            with Drawing() as draw:
                draw.fill_color = Color('white')
                visible_corner = self.random_coord()
                corners = [
                    self.translate_coord(self.random_coord(), (-self.image_width, 0)),  # bottom left
                    visible_corner,  # bottom right (visible)
                    self.translate_coord(self.random_coord(), (0, -self.image_height)),  # top right
                    self.translate_coord(self.random_coord(), (-self.image_width, -self.image_height)),  # top left
                ]
                draw.polygon(corners)
                draw(image)
                # image.save(filename='draw_test.gif')
                numpy_image = numpy.fromstring(image.make_blob("gray"), numpy.uint8).reshape(image.height, image.width)
                return numpy_image, visible_corner

    def generator(self):
        while True:
            yield self.generate()
