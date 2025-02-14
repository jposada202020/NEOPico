# SPDX-FileCopyrightText: Copyright (c) 2025 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import palette
from neopixel import NEOPIXEL
from machine import Pin
from effects import segments

# Create a NeoPixel strip with 30 pixels connected to pin 15
led_strip = NEOPIXEL(Pin(15), 30)

# Define the colors to include in the segment
values = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (80, 0, 80)]

# show the segment of colors. The segment is 2 pixels long
segments(led_strip, segment_length=5, values=values)

# Turn off all the pixels
led_strip.fill_all(color=(0, 0, 0))
