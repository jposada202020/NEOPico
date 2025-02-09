# SPDX-FileCopyrightText: Copyright (c) 2025 Jose D. Montoya, DJDevon
#
# SPDX-License-Identifier: MIT

import palette
from neopixel import NEOPIXEL
from machine import Pin

# Create a NeoPixel ring with 8 pixels connected to pin 15
ring = NEOPIXEL(Pin(15), 8)

# Define the colors to include in the segment
ring.fill_all(color=(0, 255, 80))

# Turn off all the pixels
ring.fill_all(color=(0, 0, 0))
