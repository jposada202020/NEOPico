# SPDX-FileCopyrightText: Copyright (c) 2025 Jose D. Montoya
#
# SPDX-License-Identifier: MIT


from neopixel import NEOPIXEL
from machine import Pin
from effects import shrink_and_grow_multiple_moving

# Create a NeoPixel strip with 30 pixels connected to pin 15
led_strip = NEOPIXEL(Pin(15), 30)

# Create a rainbow cycle animation for 15 seconds
shrink_and_grow_multiple_moving(
    led_strip,
    fragment_amount=4,
    midpoint_increase=0.15,
    move_increase=0.15,
    speed=0.01,
    duration=35,
)

# Turn off all the pixels
led_strip.fill_all(color=(0, 0, 0))
