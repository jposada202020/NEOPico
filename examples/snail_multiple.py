# SPDX-FileCopyrightText: Copyright (c) 2025 Jose D. Montoya
#
# SPDX-License-Identifier: MIT


from neopixel import NEOPIXEL
from machine import Pin
from effects import snail_multiple

# Create a NeoPixel strip with 30 pixels connected to pin 15
led_strip = NEOPIXEL(Pin(15), 30)

# Create a rainbow cycle animation for 15 seconds
snail_multiple(
    led_strip,
    fragment_amount=2,
    snail_minimum_size=4,
    is_shrinking=True,
    snailbegin=0,
    snailend=4,
    speed=0.05,
    duration=205,
)

# Turn off all the pixels
led_strip.fill_all(color=(0, 0, 0))
