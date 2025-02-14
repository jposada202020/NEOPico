# SPDX-FileCopyrightText: Copyright (c) 2025 Jose D. Montoya
#
# SPDX-License-Identifier: MIT


from neopixel import NEOPIXEL
from machine import Pin
from effects import white_wave

# Create a NeoPixel strip with 30 pixels connected to pin 15
led_strip = NEOPIXEL(Pin(15), 30)

# Create a rainbow cycle animation for 10 seconds
white_wave(
    led_strip,
    animation_speed=0.1,
    fade_animation_speed=0.08,
    speed=0.01,
    shrinkage=0.9,
    duration=10,
)

# Turn off all the pixels
led_strip.fill_all(color=(0, 0, 0))
