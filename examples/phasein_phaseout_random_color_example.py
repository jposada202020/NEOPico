# SPDX-FileCopyrightText: Copyright (c) 2025 Jose D. Montoya
#
# SPDX-License-Identifier: MIT


from neopixel import NEOPIXEL
from machine import Pin
from effects import fadein_fadeout_random_color
from colors import BLUE, RED

# Create a NeoPixel strip with 30 pixels connected to pin 15
led_strip = NEOPIXEL(Pin(15), 30)

# led_strip.palette_colors = [BLUE, RED]

# Create a rainbow cycle animation for 10 seconds
fadein_fadeout_random_color(
    led_strip, fade_increment=0.03, speed=0.1, duration=180
)

# Turn off all the pixels
led_strip.fill_all(color=(0, 0, 0))
