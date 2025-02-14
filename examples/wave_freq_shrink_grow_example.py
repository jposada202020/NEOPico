# SPDX-FileCopyrightText: Copyright (c) 2025 Jose D. Montoya
#
# SPDX-License-Identifier: MIT


from neopixel import NEOPIXEL
from machine import Pin
from effects import wave_freq_shrink_and_grow

# Create a NeoPixel strip with 30 pixels connected to pin 15
led_strip = NEOPIXEL(Pin(15), 30)

# Create a rainbow cycle animation for 15 seconds
wave_freq_shrink_and_grow(
    led_strip, move_increase=0.1, freq_increase=0.3, speed=0.1, duration=55
)

# Turn off all the pixels
led_strip.fill_all(color=(0, 0, 0))
