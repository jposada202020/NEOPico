# SPDX-FileCopyrightText: Copyright (c) 2025 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import palette
from neopixel import NEOPIXEL
from machine import Pin
from palette import Palette

# Create a NeoPixel ring with 30 pixels connected to pin 15
led_strip = NEOPIXEL(Pin(15), 50)

Palette(led_strip, "harmony1")

# Do the simulation again with a defined palette
led_strip.chasing_color(duration=5)

# Turn off all the pixels
led_strip.fill_all(color=(0, 0, 0))
