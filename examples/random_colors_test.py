# SPDX-FileCopyrightText: Copyright (c) 2025 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import palette
from neopixel import NEOPIXEL
from machine import Pin

# Create a NeoPixel strip with 30 pixels connected to pin 15
led_strip = NEOPIXEL(Pin(15), 30)

# Show the random colors for 3 seconds
led_strip.random_color(start=0, duration=3)

# Turn off all the pixels
led_strip.fill_all(color=(0, 0, 0))
