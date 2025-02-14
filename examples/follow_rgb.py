# SPDX-FileCopyrightText: Copyright (c) 2025 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import palette
from neopixel import NEOPIXEL
from machine import Pin
from palette import Palette
from effects import follow_rgb

# Create a NeoPixel ring with 30 pixels connected to pin 15
led_strip = NEOPIXEL(Pin(15), 30)

Palette(led_strip, "harmony3")

# Define the blink colors
follow_rgb(led_strip)

# Turn off all the pixels
led_strip.fill_all(color=(0, 0, 0))
