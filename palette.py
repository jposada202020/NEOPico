# SPDX-FileCopyrightText: Copyright (c) 2025 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

"""

`palette`
================================================================================

Palette generator for NeoPixel LED strips.


* Author: Jose D. Montoya

"""


import random

try:
    from typing import Tuple
except ImportError:
    pass


class HarmonyType:
    COMPLEMENTARY = "complementary"


def hsv_to_rgb(
    hue: float, sat: float, val: float
) -> Tuple[float, float, float]:
    """Converts HSV to RGB values

    :param float hue: The hue of the color to convert
    :param float sat: The saturation of the color to convert
    :param float val: The value (or brightness) of the color to convert
    :return: RGB values
    :rtype: Tuple[float, float, float]
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


def interpolate_color(
    start_color: list, end_color: list, factor: int
) -> list[int, int, int]:
    """Interpolate between two colors
    :param list start_color: First color in RGB format
    :param list end_color: Second color in RGB format
    :param int factor: Factor to interpolate between colors
    :return: Interpolated color in RGB format
    :rtype: list
    """
    return [
        int(start_color[i] + (end_color[i] - start_color[i]) * factor)
        for i in range(3)
    ]


def interpolate_color_p(
    color1: list, color2: list, factor: int
) -> list[int, int, int]:
    """Interpolate between two colors
    :param list color1: First color in RGB format
    :param list color2: Second color in RGB format
    :param int factor: Factor to interpolate between colors
    :return: Interpolated color in RGB format
    :rtype: list
    """
    r = int(color1[0] + (color2[0] - color1[0]) * factor)
    g = int(color1[1] + (color2[1] - color1[1]) * factor)
    b = int(color1[2] + (color2[2] - color1[2]) * factor)
    return [r, g, b]


def blend_colors(colors: list, num_steps: int = 8) -> list:
    """Create a smooth blend between colors
    :param list colors: List of colors to blend
    :param int num_steps: Number of steps to blend. Default is 8
    :return: List of blended colors
    :rtype: list
    """
    num_colors = len(colors)
    num_steps = num_steps
    segment_length = num_steps // (num_colors - 1)

    blended = [[0 for _ in range(3)] for _ in range(num_steps)]
    print(blended)

    for i in range(num_colors - 1):
        start_color = colors[i].to_rgb()
        end_color = colors[i + 1].to_rgb()

        for j in range(segment_length):
            factor = j / segment_length
            blended_color = interpolate_color(start_color, end_color, factor)
            start_idx = i * segment_length
            blended[start_idx + j] = blended_color

    return blended


def generate_base_color(
    temperature: str = "neutral",
) -> Tuple[float, float, float]:
    """Generate a base color with given temperature preference
    :param str temperature: Temperature preference. Options are "warm", "cool", or "neutral". Default is "neutral"
    :return: Base color in HSV format
    :rtype: Tuple[float, float, float]
    """
    if temperature == "warm":
        h = random.uniform(0.95, 0.15)  # Red to Yellow
    elif temperature == "cool":
        h = random.uniform(0.45, 0.65)  # Green to Blue
    else:
        h = random.random()

    s = random.uniform(0.6, 0.9)  # Medium to high saturation
    v = random.uniform(0.7, 0.9)  # Medium to high value

    return h, s, v


def clip(value: float, min_value: float, max_value: float) -> float:
    """Clips a value between a minimum and maximum value
    :param float value: Value to clip
    :param float min_value: Minimum value
    :param float max_value: Maximum value
    :return: Clipped value
    :rtype: float
    """
    return max(min(value, max_value), min_value)


def adjust_color(
    color: Tuple[float, float, float],
    hue_shift: float = 0.0,
    sat_adjust: float = 0.0,
    val_adjust: float = 0.0,
) -> Tuple[float, float, float]:
    """Adjust a color's HSV values
    :param Tuple[float, float, float] color: Color to adjust
    :param float hue_shift: Hue shift value. Default is 0.0
    :param float sat_adjust: Saturation adjustment value. Default is 0.0
    :param float val_adjust: Value adjustment value. Default is 0.0
    :return: Adjusted color in HSV format
    :rtype: Tuple[float, float, float]
    """
    h, s, v = color

    """Adjust a color's HSV values"""
    new_h = (h + hue_shift) % 1.0
    new_s = clip(s + sat_adjust, 0, 1)
    new_v = clip(v + val_adjust, 0, 1)

    return new_h, new_s, new_v


def generate_harmony(
    base_color: Tuple[float, float, float],
    harmony_type: HarmonyType,
    num_colors: int = 5,
):
    """Generate a color harmony based on the specified type
    :param Tuple[float, float, float] base_color: Base color in HSV format
    :param HarmonyType harmony_type: Type of harmony to generate
    :param int num_colors: Number of colors in the harmony. Default is 5
    :return: List of colors in the harmony
    :rtype: list
    """
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
) -> list:
    """Generate a complete color palette with analysis
    :param str temperature: Temperature preference. Options are "warm", "cool", or "neutral". Default is "neutral
    :param HarmonyType harmony_type: Type of harmony to generate. Default is HarmonyType.COMPLEMENTARY
    :param int num_colors: Number of colors in the palette. Default is 5
    :param int seeding: Random seed value. Default is 42
    :return: List of colors in the palette
    :rtype: list
    """
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


def generate_color_palette(
    base_color: list, stretch: int, num_colors: int = 12
) -> list:
    """Generate a color palette based on a base color
    :param list base_color: Base color in RGB format
    :param int stretch: Stretch factor for the color palette
    :param int num_colors: Number of colors in the palette. Default is 12
    :return: List of colors in the palette
    :rtype: list
    """
    palette = []
    base_r, base_g, base_b = base_color

    for i in range(num_colors):
        r = (base_r + (i * stretch) % 256) % 256
        g = (base_g + ((i * stretch) // 2) % 256) % 256
        b = (base_b + ((i * stretch) // 3) % 256) % 256
        palette.append((r, g, b))

    return palette


def generate_pastel_palette(
    base_color: list, stretch: int, num_colors=12
) -> list:
    """Generate a pastel color palette based on a base color
    :param list base_color: Base color in RGB format
    :param int stretch: Stretch factor for the color palette
    :param int num_colors: Number of colors in the palette. Default is 12
    :return: List of pastel colors in the palette
    :rtype: list
    """
    palette = []
    base_r, base_g, base_b = base_color

    for i in range(num_colors):
        r = (base_r + i * stretch) % 256
        g = (base_g + i * stretch) % 256
        b = (base_b + i * stretch) % 256

        # Mix with white to create pastel colors
        r = (r + 255) // 2
        g = (g + 255) // 2
        b = (b + 255) // 2

        palette.append((r, g, b))

    return palette


def generate_three_color_palette(
    color1: Tuple[int, int, int],
    color2: Tuple[int, int, int],
    color3: Tuple[int, int, int],
    num_colors: int = 16,
) -> list:
    """Generate a three-color palette
    :param Tuple[int, int, int] color1: First color in RGB format
    :param Tuple[int, int, int] color2: Second color in RGB format
    :param Tuple[int, int, int] color3: Third color in RGB format
    :param int num_colors: Number of colors in the palette. Default is 16
    :return: List of colors in the palette
    :rtype: list
    """
    palette = []
    segment_size = num_colors // 2

    # Interpolate between color1 and color2
    for i in range(segment_size):
        factor = i / segment_size
        palette.append(interpolate_color_p(color1, color2, factor))

    # Interpolate between color2 and color3
    for i in range(segment_size):
        factor = i / segment_size
        palette.append(interpolate_color_p(color2, color3, factor))

    return palette


def generate_three_color_pastel_palette(
    color1: Tuple[int, int, int],
    color2: Tuple[int, int, int],
    color3: Tuple[int, int, int],
    num_colors: int = 16,
) -> list:
    """Generate a pastel three-color palette
    :param Tuple[int, int, int] color1: First color in RGB format
    :param Tuple[int, int, int] color2: Second color in RGB format
    :param Tuple[int, int, int] color3: Third color in RGB format
    :param int num_colors: Number of colors in the palette. Default is 16
    :return: List of pastel colors in the palette
    :rtype: list
    """
    palette = generate_three_color_palette(color1, color2, color3, num_colors)

    # Mix each color with white to create pastel colors
    for color in palette:
        color[0] = (color[0] + 255) // 2
        color[1] = (color[1] + 255) // 2
        color[2] = (color[2] + 255) // 2

    return palette


if __name__ == "__main__":
    colors = generate_palette(seeding=42)

    # Blend the colors and create a list of 16 colors
    blended = blend_colors(colors, 8)
