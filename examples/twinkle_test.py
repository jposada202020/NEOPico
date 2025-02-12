# SPDX-FileCopyrightText: Copyright (c) 2025 Jose D. Montoya
#
# SPDX-License-Identifier: MIT


from neopixel import NEOPIXEL
from machine import Pin


led_strip = NEOPIXEL(Pin(15), 30)
colors = (80, 0, 80)
led_strip.define_palette("one_color", colors=colors)

# Create a Twinkle animation with the three pastel colors
led_strip.twinkle(4)
led_strip.fill_all(color=(0, 0, 0))
