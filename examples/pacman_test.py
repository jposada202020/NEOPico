# SPDX-FileCopyrightText: Copyright (c) 2025 Jose D. Montoya
#
# SPDX-License-Identifier: MIT


from neopixel import NEOPIXEL
from machine import Pin
from effects import pacman

# Create a NeoPixel strip with 50 pixels connected to pin 15
led_strip = NEOPIXEL(Pin(15), 50)

# Fill the strip with black (0, 0, 0) to start
led_strip.fill_all(color=(0, 0, 0))

# Pacman animation
pacman(led_strip, 30)
