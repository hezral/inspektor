# Requires pydub (with ffmpeg) and Pillow
#
# Usage: python waveform.py <audio_file>

import sys

from pydub import AudioSegment
from PIL import Image, ImageDraw

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GdkPixbuf, GLib

class Waveform(object):
    """
    Credits: https://gist.github.com/mixxorz/abb8a2f22adbdb6d387f
    Minor modifications on shape and colors by hezral@gmail.com
    Credits: https://gist.github.com/mozbugbox/10cd35b2872628246140
    Added function image2pixbuf
    """

    bar_count = 107
    db_ceiling = 60

    def __init__(self, filename):
        self.filename = filename

        audio_file = AudioSegment.from_file(
            self.filename, self.filename.split('.')[-1])

        self.peaks = self._calculate_peaks(audio_file)

    def _calculate_peaks(self, audio_file):
        """ Returns a list of audio level peaks """
        chunk_length = len(audio_file) / self.bar_count

        loudness_of_chunks = [
            audio_file[i * chunk_length: (i + 1) * chunk_length].rms
            for i in range(self.bar_count)]

        max_rms = max(loudness_of_chunks) * 1.00

        return [int((loudness / max_rms) * self.db_ceiling)
                for loudness in loudness_of_chunks]

    def _get_bar_image(self, size, fill):
        """ Returns an image of a bar. """
        width, height = size
        bar = Image.new('RGBA', size, fill)

        end = Image.new('RGBA', (width, 2), fill)
        draw = ImageDraw.Draw(end)
        # draw.point([(0, 0), (3, 0)], fill='#c1c1c1')
        # draw.point([(0, 1), (3, 1), (1, 0), (2, 0)], fill='#555555')

        bar.paste(end, (0, 0))
        bar.paste(end.rotate(180), (0, height - 2))
        return bar

    def _generate_waveform_image(self):
        """ Returns the full waveform image """
        im = Image.new('RGBA', (840, 128), (255, 255, 255, 0))
        for index, value in enumerate(self.peaks, start=0):
            column = index * 8 + 2
            upper_endpoint = 64 - value

            im.paste(self._get_bar_image((4, value * 2), '#5E5EF4'),
                     (column, upper_endpoint))

        return im

    def save(self, outfile):
        """ Save the waveform as an image """
        png_filename = self.filename.replace(self.filename.split('.')[-1], 'png')
        png_filename = outfile
        with open(png_filename, 'wb') as imfile:
            self._generate_waveform_image().save(imfile, 'PNG')

    def image2pixbuf(self):
        """Convert Pillow image to GdkPixbuf"""
        im = self._generate_waveform_image()
        data = im.tobytes()
        w, h = im.size
        data = GLib.Bytes.new(data)
        pix = GdkPixbuf.Pixbuf.new_from_bytes(data, GdkPixbuf.Colorspace.RGB,
                False, 8, w, h, w * 3)
        return pix

# if __name__ == '__main__':
#     filename = sys.argv[1]

#     waveform = Waveform(filename)
#     waveform.save()
