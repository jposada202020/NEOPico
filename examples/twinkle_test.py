# SPDX-FileCopyrightText: Copyright (c) 2025 Jose D. Montoya
#
# SPDX-License-Identifier: MIT


from neopixel import NEOPIXEL
from machine import Pin
from palette import Palette
from effects import twinkle

# Create a NeoPixel ring with 30 pixels connected to pin 15
led_strip = NEOPIXEL(Pin(15), 30)

# Create a Twinkle animation with default palette for 4 seconds
Palette(led_strip, "BlacK_Red_Magenta_Yellow_gp")
twinkle(led_strip, 4)

# Turn off all pixels
led_strip.fill_all(color=(0, 0, 0))
