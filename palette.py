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
from math import cos, pi
from palettes import BlacK_Blue_Magenta_White_gp
from effects import rgb255, hsv_to_rgb

try:
    from typing import Tuple
except ImportError:
    pass


class HarmonyType:
    COMPLEMENTARY = "complementary"
    TRIADIC = "triadic"
    ANALOGOUS = "analogous"
    TETRADIC = "tetradic"


class Palette:
    def __init__(self, led_object, palette_name=None, base_color=None):
        self.led_object = led_object
        self.palette_name = palette_name
        self.default_color_number = self.led_object.num_leds
        self.seed = None
        self.stretch = None
        self.base_color = None
        self._harmony_type = None
        self.base_color = base_color
        self.define_palette()

    def define_palette(
        self,
        seed: int = 1999,
        stretch: int = 350,
    ):
        """
        Define a palette based in different algorithms. Be aware that some palettes require a specific number of colors.
        Also not all options are available for all palettes. Reading the function documentation is recommended.
        :param int seed: the seed value. Default is 1999
        :param tuple base_color: the base color. Default is (90, 180, 27)
        :param int stretch: the stretch value. Default is 350
        :return: None
        """
        self.seed = seed
        self.stretch = stretch

        if self.palette_name == "harmony1":
            self._harmony_type = HarmonyType.COMPLEMENTARY
            self.create_harmony_palette()
        elif self.palette_name == "harmony2":
            self._harmony_type = HarmonyType.ANALOGOUS
            self.create_harmony_palette()
        elif self.palette_name == "harmony3":
            self._harmony_type = HarmonyType.TRIADIC
            self.create_harmony_palette()
        elif self.palette_name == "harmony4":
            self._harmony_type = HarmonyType.TETRADIC
            self.create_harmony_palette()

        elif self.palette_name == "one_color":
            if isinstance(self.base_color, list):
                raise ValueError("Color list must have only one color")
            self.led_object.palette_colors = self.generate_color_palette()

        elif self.palette_name == "one_color_pastel":
            if isinstance(self.base_color, list):
                raise ValueError("Color list must have only one color")

            self.palette_colors = self.generate_pastel_palette(
                self.base_color, self.stretch, self.default_color_number
            )
        elif self.palette_name == "three_colors":
            if isinstance(self.base_color, tuple):
                raise ValueError("Color list must have three colors")

            self.led_object.palette_colors = self.generate_three_color_palette()

        elif self.palette_name == "three_colors_pastel":
            if isinstance(self.base_color, tuple):
                raise ValueError("Color list must have three colors")

            self.led_object.palette_colors = (
                self.generate_three_color_pastel_palette()
            )

        elif self.palette_name == "BlacK_Red_Magenta_Yellow_gp":
            self.led_object.palette_colors = BlacK_Blue_Magenta_White_gp

        else:
            a = (0.5, 0.5, 0.4)  # base color
            b = (0.4, 0.5, 0.5)  # amplitude
            c = (1.0, 1.0, 1.0)  # frequency
            d = (0.0, 0.33, 0.67)  # phase
            self.led_object.palette_colors = self.palette_cos(0.7, a, b, c, d)

    def create_harmony_palette(self):
        palette_data = self.generate_palette(
            temperature="neutral",
        )
        self.led_object.palette_colors = blend_colors(
            palette_data, self.default_color_number
        )

    def generate_palette(
        self,
        temperature: str = "neutral",
    ) -> list:
        """Generate a complete color palette with analysis
        :param str temperature: Temperature preference. Options are "warm", "cool", or "neutral". Default is "neutral
        :return: List of colors in the palette
        :rtype: list
        """
        random.seed(self.seed)
        """Generate a complete color palette with analysis"""
        base_color = self.generate_base_color(temperature)

        colors = self.generate_harmony(
            base_color, self._harmony_type, self.default_color_number
        )
        colors_rgb = []

        for color in colors:
            rgb = hsv_to_rgb(*color)

            colors_rgb.append(
                (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))
            )

        return colors_rgb

    def generate_harmony(
        self,
        base_color: Tuple[float, float, float],
        harmony_type: HarmonyType,
        num_colors: int = 5,
    ):
        """Generate a color harmony based on the specified type
        :param Tuple[float, float, float] base_color: Base color in HSV format
        :param int num_colors: Number of colors in the harmony. Default is 5
        :return: List of colors in the harmony
        :rtype: list
        """
        colors = [base_color]

        if harmony_type == HarmonyType.COMPLEMENTARY:
            complementary = self.adjust_color(base_color, hue_shift=0.5)
            colors.append(complementary)

        if harmony_type == HarmonyType.TRIADIC:
            colors.extend(
                [
                    self.adjust_color(base_color, hue_shift=1 / 3),
                    self.adjust_color(base_color, hue_shift=2 / 3),
                ]
            )

        if harmony_type == HarmonyType.ANALOGOUS:
            for i in range(1, num_colors):
                shift = 0.05 * i
                colors.append(self.adjust_color(base_color, hue_shift=shift))

        if harmony_type == HarmonyType.TETRADIC:
            colors.extend(
                [
                    self.adjust_color(base_color, hue_shift=0.25),
                    self.adjust_color(base_color, hue_shift=0.5),
                    self.adjust_color(base_color, hue_shift=0.75),
                ]
            )

        return colors

    def generate_base_color(
        self,
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

    def adjust_color(
        self,
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
        new_s = self.clip(s + sat_adjust, 0, 1)
        new_v = self.clip(v + val_adjust, 0, 1)

        return new_h, new_s, new_v

    def clip(self, value: float, min_value: float, max_value: float) -> float:
        """Clips a value between a minimum and maximum value
        :param float value: Value to clip
        :param float min_value: Minimum value
        :param float max_value: Maximum value
        :return: Clipped value
        :rtype: float
        """
        return max(min(value, max_value), min_value)

    def generate_color_palette(self) -> list:
        """Generate a color palette based on a base color
        :return: List of colors in the palette
        :rtype: list
        """
        palette = []
        base_r, base_g, base_b = self.base_color

        for i in range(self.default_color_number):
            r = (base_r + (i * self.stretch) % 256) % 256
            g = (base_g + ((i * self.stretch) // 2) % 256) % 256
            b = (base_b + ((i * self.stretch) // 3) % 256) % 256
            palette.append((r, g, b))

        return palette

    def generate_pastel_palette(self) -> list:
        """Generate a pastel color palette based on a base color
        :return: List of pastel colors in the palette
        :rtype: list
        """
        palette = []
        base_r, base_g, base_b = self.base_color

        for i in range(self.default_color_number):
            r = (base_r + i * self.stretch) % 256
            g = (base_g + i * self.stretch) % 256
            b = (base_b + i * self.stretch) % 256

            # Mix with white to create pastel colors
            r = (r + 255) // 2
            g = (g + 255) // 2
            b = (b + 255) // 2

            palette.append((r, g, b))

        return palette

    def generate_three_color_palette(self) -> list:
        """Generate a three-color palette
        :return: List of colors in the palette
        :rtype: list
        """
        palette = []
        segment_size = self.default_color_number // 2

        # Interpolate between color1 and color2
        for i in range(segment_size):
            factor = i / segment_size
            palette.append(
                interpolate_color_p(
                    self.base_color[0], self.base_color[1], factor
                )
            )

        # Interpolate between color2 and color3
        for i in range(segment_size):
            factor = i / segment_size
            palette.append(
                interpolate_color_p(
                    self.base_color[1], self.base_color[2], factor
                )
            )

        return palette

    def generate_three_color_pastel_palette(
        self,
    ) -> list:
        """Generate a pastel three-color palette
        :return: List of pastel colors in the palette
        :rtype: list
        """
        palette = self.generate_three_color_palette()

        # Mix each color with white to create pastel colors
        for color in palette:
            color[0] = (color[0] + 255) // 2
            color[1] = (color[1] + 255) // 2
            color[2] = (color[2] + 255) // 2

        return palette


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

    for i in range(num_colors - 1):
        start_color = colors[i]
        end_color = colors[i + 1]

        for j in range(segment_length):
            factor = j / segment_length
            blended_color = interpolate_color(start_color, end_color, factor)
            start_idx = i * segment_length
            blended[start_idx + j] = blended_color

    return blended


if __name__ == "__main__":
    pass
