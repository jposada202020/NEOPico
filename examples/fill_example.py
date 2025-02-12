# SPDX-FileCopyrightText: Copyright (c) 2025 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import palette
from neopixel import NEOPIXEL
from machine import Pin

# Create a NeoPixel ring with 30 pixels connected to pin 15
ring = NEOPIXEL(Pin(15), 30)

# Define the colors to include in the segment
ring.fill_all(color=(0, 255, 80))

# Turn off all the pixels
ring.fill_all(color=(0, 0, 0))
