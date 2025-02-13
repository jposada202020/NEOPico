# SPDX-FileCopyrightText: Copyright (c) 2025 Jose D. Montoya
#
# SPDX-License-Identifier: MIT


from neopixel import NEOPIXEL
from machine import Pin
from effects import wave_back_and_forth

# Create a NeoPixel strip with 30 pixels connected to pin 15
led_strip = NEOPIXEL(Pin(15), 30)

# Create a rainbow cycle animation for 15 seconds
wave_back_and_forth(led_strip, duration=15)

# Turn off all the pixels
led_strip.fill_all(color=(0, 0, 0))
