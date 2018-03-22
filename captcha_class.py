__author__ = 'tian'
__author__ = 'tian'

import random
import os

from PIL import Image
from PIL import ImageFilter
from PIL import ImageFont
from PIL.ImageDraw import Draw
from PIL.ImageFont import truetype

try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO

# DATA_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data')
# DEFAULT_FONTS = [os.path.join(DATA_DIR, 'DroidSansMono.ttf')]
#DEFAULT_FONTS = '/Users/tian/Downloads/open-sans/OpenSans-Italic.ttf'
table = []
for i in range(256):
    table.append(i * 1.97)


class _Captcha(object):
    def generate(self, chars, format='png'):
        """Generate an Image Captcha of the given characters.
        :param chars: text to be generated.
        :param format: image file format
        """
        im = self.generate_image(chars)
        out = BytesIO()
        im.save(out, format=format)
        out.seek(0)
        return out

    def write(self, chars, output, format='png'):
        """Generate and write an image CAPTCHA data to the output.
        :param chars: text to be generated.
        :param output: output destination.
        :param format: image file format
        """
        im = self.generate_image(chars)
        return im.save(output, format=format)

    def random_color(self,start, end, opacity=None):
        red = random.randint(start, end)
        green = random.randint(start, end)
        blue = random.randint(start, end)
        if opacity is None:
            return (red, green, blue)
        return (red, green, blue, opacity)


class ImageCaptcha(_Captcha):
    def __init__(self, width=80, height=23, fonts=None,font_size=None):
        self._width = width
        self._height = height
        self._font_size = font_size or (23,26,28)
        self._fonts = fonts




    @staticmethod
    def create_noise_dots(image, color, width=3, number=5):
        draw = Draw(image)
        w, h = image.size
        while number:
            x1 = random.randint(0, w)
            y1 = random.randint(0, h)
            draw.line(((x1, y1), (x1 - 1, y1 - 1)), fill=color, width=width)
            number -= 1
        return image

    @staticmethod
    def create_noise_curve(image, color):
        w, h = image.size
        x1 = random.randint(0, int(w / 5))
        x2 = random.randint(w - int(w / 5), w)
        y1 = random.randint(int(h / 5), h - int(h / 5))
        y2 = random.randint(y1, h - int(h / 5))
        points = [x1, y1, x2, y2]
        end = random.randint(160, 200)
        start = random.randint(0, 20)
        Draw(image).arc(points, start, end, fill=color)
        return image

    def create_captcha_image(self, chars, color, background):
        image = Image.new('RGB', (self._width, self._height), background)
        draw = Draw(image)

        def _draw_character(c):
            font = ImageFont.truetype('OpenSans-Italic.ttf',23)
            w, h = draw.textsize(c, font=font)

            dx = random.randint(0, 4)
            dy = random.randint(0, 6)
            im = Image.new('RGBA', (w + dx, h + dy))
            Draw(im).text((dx, dy), c, font=font, fill=color)

            # rotate
            im = im.crop(im.getbbox())
            im = im.rotate(random.uniform(-30, 30), Image.BILINEAR, expand=1)

            # warp
            dx = w * random.uniform(0.1, 0.3)
            dy = h * random.uniform(0.2, 0.3)
            x1 = int(random.uniform(-dx, dx))
            y1 = int(random.uniform(-dy, dy))
            x2 = int(random.uniform(-dx, dx))
            y2 = int(random.uniform(-dy, dy))
            w2 = w + abs(x1) + abs(x2)
            h2 = h + abs(y1) + abs(y2)
            data = (
                x1, y1,
                -x1, h2 - y2,
                w2 + x2, h2 + y2,
                w2 - x2, -y1,
            )
            im = im.resize((w2, h2))
            im = im.transform((w, h), Image.QUAD, data)
            return im

        images = []
        for c in chars:
            images.append(_draw_character(c))

        text_width = sum([im.size[0] for im in images])

        width = max(text_width, self._width)
        image = image.resize((width, self._height))

        average = int(text_width / len(chars))
        rand = int(0.25 * average)
        offset = int(average * 0.1)

        for im in images:
            w, h = im.size
            mask = im.convert('L').point(table)
            image.paste(im, (offset, int((self._height - h) / 2)), mask)
            offset = offset + w + random.randint(-rand, 0)

        if width > self._width:
            image = image.resize((self._width, self._height))

        return image

    def generate_image(self, chars):
        """Generate the image of the given characters.
        :param chars: text to be generated.
        """
        background = self.random_color(238, 255)
        color = self.random_color(10, 200, random.randint(220, 255))
        im = self.create_captcha_image(chars, color, background)
        self.create_noise_dots(im, color)
        self.create_noise_curve(im, color)
        im = im.filter(ImageFilter.SMOOTH)
        return im

# def random_captcha_text(char_set=number + alphabet + ALPHABET, captcha_size=5):
#     captcha_text = []
#     for i in range(captcha_size):
#         c = random.choice(char_set)
#         captcha_text.append(c)
#     return captcha_text
#
#
#
#
#
#
#
#
#
# def gen_captcha_text_and_image():
#     image = ImageCaptcha(width=80,height=23,font_sizes=(23,26,28))
#
#
#     captcha_text = random_captcha_text()
#     captcha_text = ''.join(captcha_text)
#
#
#
#
#
#
#
#
#     captcha = image.generate(captcha_text)
#     image.write(captcha_text, captcha_text + '.jpg')  # 写到文件
#
#
#     captcha_image = Image.open(captcha)
#
#     captcha_image = np.array(captcha_image)
#     #print(captcha_image)
#     # captcha_image = np.array(captcha)
#     #
#     # print(captcha_image)
#     return captcha_text, captcha_image
#
#
# if __name__ == '__main__':
#
#     text, image = gen_captcha_text_and_image()
#
#     f = plt.figure()
#
#     plt.imshow(image)
#
#     plt.show()
