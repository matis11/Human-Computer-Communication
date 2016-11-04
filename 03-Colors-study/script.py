#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division  # Division in Python 2.7

import colorsys

import matplotlib

matplotlib.use('Agg')  # So that we can render files without GUI
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np

from matplotlib import colors


def plot_color_gradients(gradients, names):
    # For pretty latex fonts (commented out, because it does not work on some machines)
    # rc('text', usetex=True)
    # rc('font', family='serif', serif=['Times'], size=10)
    rc('legend', fontsize=10)

    column_width_pt = 400  # Show in latex using \the\linewidth
    pt_per_inch = 72
    size = column_width_pt / pt_per_inch

    fig, axes = plt.subplots(nrows=len(gradients), sharex=True, figsize=(size, 0.75 * size))
    fig.subplots_adjust(top=1.00, bottom=0.05, left=0.25, right=0.95)

    for ax, gradient, name in zip(axes, gradients, names):
        # Create image with two lines and draw gradient on it
        img = np.zeros((2, 1024, 3))
        for i, v in enumerate(np.linspace(0, 1, 1024)):
            img[:, i] = gradient(v)

        im = ax.imshow(img, aspect='auto')
        im.set_extent([0, 1, 0, 1])
        ax.yaxis.set_visible(False)

        pos = list(ax.get_position().bounds)
        x_text = pos[0] - 0.25
        y_text = pos[1] + pos[3] / 2.
        fig.text(x_text, y_text, name, va='center', ha='left', fontsize=10)

    fig.savefig('my-gradients.pdf')


def hsv2rgb(h, s, v):
    # h: 0-359, s: 0-1, v: 0-1
    if s == 0:
        return v, v, v  # greyscale

    main_color = v * s
    sec_color = main_color * (1 - abs(((h / 60) % 2) - 1))
    temp = v - main_color
    sec = sec_color + temp

    if h < 60:
        return v, sec, temp  # b>g
    if h < 120:
        return sec, v, temp  # b<g
    if h < 180:
        return temp, v, sec  # g>r
    if h < 240:
        return temp, sec, v  # g<r
    if h < 300:
        return sec, temp, v  # b<r
    return v, temp, sec  # b>r


def gradient_rgb_bw(v):
    return v, v, v


def gradient_rgb_gbr(v):
    if v <= 0.5:
        return 0, 1 - (2 * v), v * 2

    return (v - 0.5) * 2, 0, 1 - ((v - 0.5) * 2)


def gradient_rgb_gbr_full(v):
    if v <= 0.25:
        return 0, 1, v * 4
    if v <= 0.50:
        return 0, 1 - (v - 0.25) * 4, 1
    if v <= 0.75:
        return (v - 0.5) * 4, 0, 1
    return 1, 0, 1 - (v - 0.75) * 4


def gradient_rgb_wb_custom(v):
    if v <= 1 / 7:
        return 1, 1 - v * 7, 1
    if v <= 2 / 7:
        return 1 - (v - 1 / 7) * 7, 0, 1
    if v <= 3 / 7:
        return 0, (v - 2 / 7) * 7, 1
    if v <= 4 / 7:
        return 0, 1, 1 - (v - 3 / 7) * 7
    if v <= 5 / 7:
        return (v - 4 / 7) * 7, 1, 0
    if v <= 6 / 7:
        return 1, 1 - (v - 5 / 7) * 7, 0

    return 1 - (v - 6 / 7) * 7, 0, 0


def gradient_hsv_bw(v):
    return hsv2rgb(0, 0, v)


def gradient_hsv_gbr(v):
    return hsv2rgb(((v * 240) + 120) % 360, 1, 1)


def gradient_hsv_unknown(v):
    # 120->0 [o]
    return hsv2rgb(120 * (1 - v), 0.5, 1)


def gradient_hsv_custom(v):
    # 240 1 1 -> 240   0 1
    if v <= 1 / 4:
        return hsv2rgb(240, 1 - 4 * v, 1)
    # 60 0 1 -> 60 1 1
    if v <= 1 / 2:
        return hsv2rgb(60, 4 * v - 1, 1)
    # 60 1 1 -> 60 0 0
    if v <= 3 / 4:
        return hsv2rgb(60, 1 - 4 * (v - 1 / 2), 1 - 4 * (v - 1 / 2))
    # 120   0 0 -> 120 1 1
    return hsv2rgb(120, (v - 3 / 4) * 4, (v - 3 / 4) * 4)


if __name__ == '__main__':
    def toname(g):
        return g.__name__.replace('gradient_', '').replace('_', '-').upper()


    gradients = (gradient_rgb_bw, gradient_rgb_gbr, gradient_rgb_gbr_full, gradient_rgb_wb_custom,
                 gradient_hsv_bw, gradient_hsv_gbr, gradient_hsv_unknown, gradient_hsv_custom)

    plot_color_gradients(gradients, [toname(g) for g in gradients])
