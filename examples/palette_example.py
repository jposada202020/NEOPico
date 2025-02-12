# SPDX-FileCopyrightText: Copyright (c) 2025 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import palette
from neopixel import NEOPIXEL
from machine import Pin
from palette import Palette

# Create a NeoPixel ring with 30 pixels connected to pin 15
led_strip = NEOPIXEL(Pin(15), 30)


Palette(led_strip, "harmony1")
blended_complementary = palette.blend_colors(led_strip.palette_colors, 30)
led_strip.fill_custom(blended_complementary)
led_strip.fill_all(color=(0, 0, 0))

Palette(led_strip, "harmony2")
blended_complementary = palette.blend_colors(led_strip.palette_colors, 30)
led_strip.fill_custom(blended_complementary)
led_strip.fill_all(color=(0, 0, 0))

