#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PIL import Image

from skimage import data, filters, morphology, color, exposure
import numpy as np

THRESHOLD = 133
DISTANCE_FROM_BORDER = 2
HORIZONTAL = 0
VERTICAL = 1

FILES = ['samolot01.jpg', 'samolot07.jpg', 'samolot08.jpg', 'samolot09.jpg', 'samolot17.jpg', 'samolot10.jpg']


def join_images(image_1, image_2, direction):
    height_1, width_1 = image_1.shape[:2]
    height_2, width_2 = image_2.shape[:2]

    if direction == HORIZONTAL:
        max_height = np.max([height_1, height_2])
        target_width = width_1 + width_2
        result_image = np.zeros(shape=(max_height, target_width), dtype=np.uint8)
        result_image[:height_1, :width_1] = image_1
        result_image[:height_2, width_1:width_1 + width_2] = image_2
        return result_image

    if direction == VERTICAL:
        max_width = np.max([width_1, width_2])
        h = height_1 + height_2
        result_image = np.zeros(shape=(h, max_width), dtype=np.uint8)
        result_image[:height_1, :width_1] = image_1
        result_image[height_1:height_1 + height_2, :width_2] = image_2
        return result_image


def filter(img, r):
    h, w = img.shape[:2]
    for row in range(h):
        for value in range(w):
            if img[row][value] < r:
                img[row][value] = 0
            elif img[row][value] >= r:
                img[row][value] = 255
    return img


# noinspection PyTypeChecker
def main():
    images = [0, 0, 0, 0, 0, 0]

    for index, image in enumerate(images):
        images[index] = data.imread('source/{filename}'.format(filename=FILES[index]))

    for index, image in enumerate(images):
        images[index] = color.rgb2grey(images[index]).copy()

        images[index] = filters.gaussian(images[index], 1).copy()
        images[index] = exposure.rescale_intensity(images[index], out_range=(0, 255)).copy()
        images[index] = filter(images[index], THRESHOLD).copy()
        images[index] = filters.roberts(images[index]).copy()

        for k in range(DISTANCE_FROM_BORDER):
            images[index] = morphology.dilation(images[index])

    image = join_images(
        join_images(join_images(images[1], images[0], 0), join_images(images[DISTANCE_FROM_BORDER], images[3], 0), 1),
        join_images(images[4], images[5], 0), 1)
    Image.fromarray(image).save('output.jpg')


if __name__ == '__main__':
    main()
