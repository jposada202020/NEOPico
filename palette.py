# SPDX-FileCopyrightText: Copyright (c) 2025 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

"""

`palette`
================================================================================

Palette generator for NeoPixel LED strips. Adapted from https://github.com/gddickinson/colour-palette


* Author: Jose D. Montoya

"""


import random

try:
    from typing import Tuple
except ImportError:
    pass


class HarmonyType:
    COMPLEMENTARY = "complementary"


class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def to_rgb(self):
        return [self.r, self.g, self.b]


def hsv_to_rgb(
    hue: float, sat: float, val: float
) -> Tuple[float, float, float]:
    """Converts HSV to RGB values

    :param float hue: The hue of the color to convert
    :param float sat: The saturation of the color to convert
    :param float val: The value (or brightness) of the color to convert
    """
    if sat == 0.0:
        return val, val, val
    i = int(hue * 6.0)  # assume int() truncates!
    hue1 = (hue * 6.0) - i
    chroma1 = val * (1.0 - sat)
    chroma2 = val * (1.0 - sat * hue1)
    chroma3 = val * (1.0 - sat * (1.0 - hue1))
    i = i % 6
    if i == 0:
        return val, chroma3, chroma1
    if i == 1:
        return chroma2, val, chroma1
    if i == 2:
        return chroma1, val, chroma3
    if i == 3:
        return chroma1, chroma2, val
    if i == 4:
        return chroma3, chroma1, val
    if i == 5:
        return val, chroma1, chroma2


def interpolate_color(start_color, end_color, factor):
    return [
        int(start_color[i] + (end_color[i] - start_color[i]) * factor)
        for i in range(3)
    ]


def blend_colors(colors, num_steps=8):
    num_colors = len(colors)
    num_steps = num_steps
    segment_length = num_steps // (num_colors - 1)

    blended = [[0 for _ in range(3)] for _ in range(num_steps)]

    for i in range(num_colors - 1):
        start_color = colors[i].to_rgb()
        end_color = colors[i + 1].to_rgb()

        for j in range(segment_length):
            factor = j / segment_length
            blended_color = interpolate_color(start_color, end_color, factor)
            start_idx = i * segment_length
            blended[start_idx + j] = blended_color

    return blended


def generate_base_color(temperature: str = "neutral"):
    """Generate a base color with given temperature preference"""
    if temperature == "warm":
        h = random.uniform(0.95, 0.15)  # Red to Yellow
    elif temperature == "cool":
        h = random.uniform(0.45, 0.65)  # Green to Blue
    else:
        h = random.random()

    s = random.uniform(0.6, 0.9)  # Medium to high saturation
    v = random.uniform(0.7, 0.9)  # Medium to high value

    return h, s, v


def clip(value, min_value, max_value):
    return max(min(value, max_value), min_value)


def adjust_color(
    color,
    hue_shift: float = 0.0,
    sat_adjust: float = 0.0,
    val_adjust: float = 0.0,
):
    h, s, v = color

    """Adjust a color's HSV values"""
    new_h = (h + hue_shift) % 1.0
    new_s = clip(s + sat_adjust, 0, 1)
    new_v = clip(v + val_adjust, 0, 1)

    return new_h, new_s, new_v


def generate_harmony(
    base_color,
    harmony_type: HarmonyType,
    num_colors: int = 5,
):
    """Generate a color harmony based on the specified type"""
    colors = [base_color]

    if harmony_type == HarmonyType.COMPLEMENTARY:
        complementary = adjust_color(base_color, hue_shift=0.5)
        colors.append(complementary)

    return colors


def generate_palette(
    temperature: str = "neutral",
    harmony_type: HarmonyType = HarmonyType.COMPLEMENTARY,
    num_colors: int = 5,
    seeding=42,
):
    random.seed(seeding)
    """Generate a complete color palette with analysis"""
    base_color = generate_base_color(temperature)

    colors = generate_harmony(base_color, harmony_type, num_colors)
    colors_rgb = []

    for color in colors:
        rgb = hsv_to_rgb(*color)

        colors_rgb.append(
            Color(int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))
        )

    return colors_rgb


if __name__ == "__main__":
    colors = generate_palette(seeding=42)

    # Blend the colors and create a list of 16 colors
    blended = blend_colors(colors, 8)
