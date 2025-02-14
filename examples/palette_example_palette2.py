# SPDX-FileCopyrightText: Copyright (c) 2025 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

from palette import Palette, blend_colors
import time
from neopixel import NEOPIXEL
from machine import Pin

# Create a NeoPixel ring with 30 pixels connected to pin 15
led_strip = NEOPIXEL(Pin(15), 30)

# Define the colors to include in the palette
color1 = (90, 180, 27)  # Example color 1
color2 = (111, 123, 154)  # Example color 2
color3 = (231, 45, 120)  # Example color 3
base_color = (128, 0, 0)  # Example base color
stretch = 350  # Example stretch factor

Palette(led_strip, "three_colors", base_color=[color1, color2, color3])
blended_complementary = blend_colors(led_strip.palette_colors, 30)
led_strip.fill_custom(blended_complementary)
led_strip.fill_all(color=(0, 0, 0))

Palette(led_strip, "one_color", base_color=base_color)
blended_complementary = blend_colors(led_strip.palette_colors, 30)
led_strip.fill_custom(blended_complementary)
led_strip.fill_all(color=(0, 0, 0))
