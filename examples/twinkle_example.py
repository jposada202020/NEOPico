# SPDX-FileCopyrightText: Copyright (c) 2025 Jose D. Montoya
#
# SPDX-License-Identifier: MIT


from neopixel import NEOPIXEL
from machine import Pin
from palette import Palette

# Create a NeoPixel strip with 30 pixels connected to pin 15
led_strip = NEOPIXEL(Pin(15), 30)

# Define a palette with three pastel colors
colors = [(90, 180, 27), (111, 123, 154), (231, 45, 120)]
Palette(led_strip, "three_colors_pastel", base_color=colors)

# Create a Twinkle animation with the three pastel colors for 15 seconds
led_strip.twinkle(15)

# Turn off all the pixels
led_strip.fill_all(color=(0, 0, 0))
