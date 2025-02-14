# SPDX-FileCopyrightText: Copyright (c) 2025 Jose D. Montoya
#
# SPDX-License-Identifier: MIT


from neopixel import NEOPIXEL
from machine import Pin
from effects import lerp_phase

# Create a NeoPixel strip with 30 pixels connected to pin 15
led_strip = NEOPIXEL(Pin(15), 30)

# Create a rainbow cycle animation for 35 seconds
lerp_phase(
    led_strip,
    animation_increase=0.05,
    speed=0.1,
    shrinkage=1,
    phase_increase=15,
    duration=35,
)

# Turn off all the pixels
led_strip.fill_all(color=(0, 0, 0))
