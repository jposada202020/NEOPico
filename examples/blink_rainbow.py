# SPDX-FileCopyrightText: Copyright (c) 2025 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import palette
from neopixel import NEOPIXEL
from machine import Pin
from effects import blink_rainbow
from colors import PURPLE

# Create a NeoPixel ring with 30 pixels connected to pin 15
led_strip = NEOPIXEL(Pin(15), 50)

# Define the blink colors
blink_rainbow(led_strip, background_color=PURPLE, dwell=0.1, duration=10)
blink_rainbow(led_strip, dwell=0.1, duration=10)

# Turn off all the pixels
led_strip.fill_all(color=(0, 0, 0))
