from io import BytesIO

from PIL import Image


class UnsupportedFormat(Exception):
    pass


class Converter(object):

    def __init__(self, stream):
        stream.seek(0)
        self.stream = stream
        try:
            self.image = Image.open(stream)
        except IOError:
            raise UnsupportedFormat()
        self.format = self.image.format.lower()

    def to_format(self, fmt):
        fmt = fmt.lower()
        if self.format == fmt:
            # leave the object as is
            out = self.stream
        else:
            # Lot of options can be specified for format conversions
            # that's why we keep converters independently of each other
            # by coding methods like
            # Convertor.from_jpeg_to_png
            # Convertor.from_png_to_jpeg
            method_name = 'from_{}_to_{}'.format(self.format, fmt)
            method = getattr(self, method_name, None)
            if not method:
                raise UnsupportedFormat()
            out = method()
        out.seek(0)
        return out

    def from_jpeg_to_png(self):
        out = BytesIO()
        self.image.save(out, "png")
        return out

    def from_png_to_jpeg(self):
        out = BytesIO()
        rgb_img = self.image.convert('RGB')
        rgb_img.save(out, "jpeg")
        return out

    # ToDo: Code plenty of supported Pillow conversions
