# SPDX-FileCopyrightText: Copyright (c) 2025 Jose D. Montoya
#
# SPDX-License-Identifier: MIT


from neopixel import NEOPIXEL
from machine import Pin

# Create a NeoPixel strip with 8 pixels connected to pin 15
led_strip = NEOPIXEL(Pin(15), 8)

# Define a palette with three pastel colors
colors = [(90, 180, 27), (111, 123, 154), (231, 45, 120)]
led_strip.define_palette("three_colors_pastel", colors=colors)

# Create a Twinkle animation with the three pastel colors for 15 seconds
led_strip.twinkle(15)

# Turn off all the pixels
led_strip.fill_all(color=(0, 0, 0))
