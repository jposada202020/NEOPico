# SPDX-FileCopyrightText: Copyright (c) 2025 Jose D. Montoya
#
# SPDX-License-Identifier: MIT


from neopixel import NEOPIXEL
from machine import Pin
from effects import linear_interpolation
from palette import Palette
from colors import RED, WHITE

# Create a NeoPixel strip with 30 pixels connected to pin 15
led_strip = NEOPIXEL(Pin(15), 30)

""" Different methods to select the palette to use"""
# Palette(led_strip, palette_name="harmony4")
# led_strip.palette_colors = [(255,0,0), (0,0,255)]
led_strip.palette_colors = [RED, WHITE]

# Create a rainbow cycle animation for 35 seconds
linear_interpolation(
    led_strip, shrinkage=0.5, animation_increase=0.2, speed=0.1, duration=35
)


# Turn off all the pixels
led_strip.fill_all(color=(0, 0, 0))
