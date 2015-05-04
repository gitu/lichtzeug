#!/usr/bin/python

# A more complex RGBMatrix example works with the Python Imaging Library,
# demonstrating a few graphics primitives and image loading.
# Note that PIL graphics do not have an immediate effect on the display --
# image is drawn into a separate buffer, which is then copied to the matrix
# using the SetImage() function (see examples below).
# Requires rgbmatrix.so present in the same directory.

# PIL Image module (create or load images) is explained here:
# http://effbot.org/imagingbook/image.htm
# PIL ImageDraw module (draw shapes to images) explained here:
# http://effbot.org/imagingbook/imagedraw.htm

import Image
import time
from rgbmatrix import Adafruit_RGBmatrix
import random, os

import PanicButton


button = PanicButton.PanicButton()

matrix = Adafruit_RGBmatrix(32, 1)


def display_image(image_url, seconds):
    image = Image.open(image_url)
    image.load()
    print image.info

    try:
        bg_color = (50, 50, 50)
        if image.info.get('duration'):
            duration = image.info.get('duration',1000)/1000.0
            print 'duration: ' + str(duration )

            mypalette = image.getpalette()
            total_duration = 0.0
            played_once = False
            while total_duration < seconds or not played_once:
                try:
                    image.seek(0)
                    while 1:
                        image.putpalette(mypalette)
                        new_im = Image.new('RGBA', image.size, bg_color)
                        conv_im = image.convert('RGBA')
                        new_im.paste(conv_im,conv_im)
                        matrix.SetImage(new_im.im.id, 0, 0)
                        time.sleep(duration)
                        total_duration += duration
                        image.seek(image.tell() + 1)
                except EOFError:
                    played_once = True
                    pass # end of sequence
        else:
            new_im = Image.new('RGBA', image.size, bg_color)
            conv_im = image.convert('RGBA')
            new_im.paste(conv_im,conv_im)
            matrix.SetImage(new_im.im.id, 0, 0)
            time.sleep(seconds)
    except Exception as e:
        print image_url, e
    finally:
        matrix.Clear()

def display_random_image(image_path='images'):
    random_choice = random.choice([x for x in os.listdir("%s" % image_path) if os.path.isfile(os.path.join("%s" % image_path, x))])
    print('selected: '+random_choice)
    display_image(image_path + '/' +random_choice,2)

display_image('loading-black.gif',5)

while 1:
    if button.read():
        display_random_image()
    time.sleep(.5)