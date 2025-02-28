# SPDX-FileCopyrightText: Copyright (c) 2025 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import palette
from neopixel import NEOPIXEL
from machine import Pin
from colors import BLUE, PURPLE
from effects import wipe

# Create a NeoPixel ring with 30 pixels connected to pin 15
led_strip = NEOPIXEL(Pin(15), 30)

# Define the blink colors
wipe(
    led_strip,
    color1=PURPLE,
    color2=BLUE,
    delta_time=0.2,
    clear=True,
    duration=15,
)

# Turn off all the pixels
led_strip.fill_all(color=(0, 0, 0))
