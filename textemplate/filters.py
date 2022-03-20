# SPDX-FileCopyrightText: 2022 Daniel Laidig <daniel@laidig.info>
#
# SPDX-License-Identifier: MIT
import copy

import numpy as np


def shuffled(items, seed=None, prefixHead=None, prefixTail=None):
    if seed is not None:
        r = np.random.RandomState(seed)
    else:
        r = np.random

    itemsCopy = copy.copy(items)
    r.shuffle(itemsCopy)

    # optional: move some items that start with a specific string to the head or tail of the list
    if prefixHead is not None or prefixTail is not None:
        head = []
        regular = []
        tail = []
        for item in itemsCopy:
            if prefixHead is not None and item.startswith(prefixHead):
                head.append(item)
            elif prefixTail is not None and item.startswith(prefixTail):
                tail.append(item)
            else:
                regular.append(item)
        itemsCopy = head + regular + tail

    return itemsCopy


def shuffledAnswerLetters(seed=None, skip='i', similar='ou,ha,bd,mn,dt,pb,cz,pq,qg'):
    letters = [chr(i) for i in range(ord('a'), ord('z')+1) if chr(i) not in skip]
    shuffledLetters = shuffled(letters, seed=seed)

    pairs = similar.split(',')
    assert all([len(p) == 2 for p in pairs])
    keep = []
    keptPairs = []
    move = []
    for letter in shuffledLetters:
        moved = False
        for pair in keptPairs:
            if letter in pair:
                move.append(letter)
                moved = True
                break
        if moved:
            continue
        for pair in pairs:
            if letter in pair:
                keptPairs.append(pair)
        keep.append(letter)

    output = keep + move
    assert len(output) == len(letters)
    assert set(output) == set(letters)
    return output


def precision(value, decimals=3):
    return ('{0:.' + str(int(decimals)) + 'f}').format(round(value, decimals))


def nodotzero(res):
    ires = int(res)
    if res == ires:
        return f'{ires:d}'
    else:
        return np.format_float_positional(res)


def _interpolate_hsv(d, min_, max_):
    saturation = 100
    value = 50
    hue_range = (0, 110)

    d = int(round(d))

    if d <= min_:
        hue = hue_range[1] / 360
    elif d >= max_:
        hue = hue_range[0]
    else:
        hue_values = sorted(np.arange(*hue_range, int(hue_range[1] / max_)), reverse=True)
        hue = hue_values[d] / 360

    return hue, saturation/100, value/100


def _rgb2hex(color):
    r = int(round(color[0] * 255))
    g = int(round(color[1] * 255))
    b = int(round(color[2] * 255))
    return f'{r:02X}{g:02X}{b:02X}'


def green2red(value, green=0, red=1):
    import colorsys

    hsv_color = _interpolate_hsv(value, green, red)
    rgb_color = colorsys.hsv_to_rgb(*hsv_color)
    color = _rgb2hex(rgb_color)

    return str(color)


def debug(text):
    print(text)
    return ''

