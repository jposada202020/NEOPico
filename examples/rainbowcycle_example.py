# SPDX-FileCopyrightText: Copyright (c) 2025 Jose D. Montoya
#
# SPDX-License-Identifier: MIT


from neopixel import NEOPIXEL
from machine import Pin

# Create a NeoPixel strip with 8 pixels connected to pin 15
led_strip = NEOPIXEL(Pin(15), 8)

# Create a rainbow cycle animation for 10 seconds
led_strip.rainbow_sine(duration=20)

# Turn off all the pixels
led_strip.fill_all(color=(0, 0, 0))
