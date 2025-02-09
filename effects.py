# SPDX-FileCopyrightText: Copyright (c) 2025 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

"""

`effects`
================================================================================

Create and control LED effects.

* Author: Jose D. Montoya


"""

import time
from random import choice

from neopixel import NEOPIXEL

BLACK = (0, 0, 0)

NUM_LEDS = 64
led_list = [BLACK for _ in range(NUM_LEDS)]


def segment_effect(
    led_object,
    palette_colors,
    neopixel_list,
    num_leds,
    duration: int = 5,
    segment_length: int = 3,
    values: list = None,
):
    led_list = [BLACK for _ in range(num_leds)]

    led_segments = get_led_segments(led_list, segment_length)
    assigned_segments = assign_values_to_segments(led_segments, values)
    neopixel_list = flatten_segments(assigned_segments)

    start_time = time.time()

    while time.time() - start_time < duration:
        NEOPIXEL.ShowNeoPixels(led_object, neopixel_list)
        time.sleep(0.1)


def random_color(
    led_object, neopixel_list, num_leds: int = 8, duration: int = 5
):
    """
    Random color data for testing
    :param int num_leds: number of leds. Default is 8 leds
    :param int duration: duration in seconds. Default is 5 seconds
    """

    limits = range(0, 256)

    start_time = time.time()

    while time.time() - start_time < duration:
        neopixel_list = [
            (choice(limits), choice(limits), choice(limits))
            for _ in range(num_leds)
        ]
        NEOPIXEL.ShowNeoPixels(led_object, neopixel_list)
        time.sleep(0.1)


def twinkle_effect(
    led_object, palette_colors, neopixel_list, num_leds, duration: int = 5
):
    """
    Dummy data for testing.
    :param int duration: duration in seconds. Default is 5 seconds
    """

    start_time = time.time()

    while time.time() - start_time < duration:
        neopixel_list = [choice(palette_colors) for _ in range(num_leds)]
        NEOPIXEL.ShowNeoPixels(led_object, neopixel_list)
        time.sleep(0.1)


def get_led_segments(led_list, segment_length):
    segments = []
    for i in range(0, len(led_list), segment_length):
        segments.append(led_list[i : i + segment_length])
    return segments


def assign_values_to_segments(segments, values):
    assigned_segments = []
    for i, segment in enumerate(segments):
        if i < len(values):
            assigned_segment = [values[i]] * len(segment)
        else:
            assigned_segment = [BLACK] * len(segment)  # or some default value
        assigned_segments.append(assigned_segment)
    return assigned_segments


def flatten_segments(assigned_segments):
    return [led for segment in assigned_segments for led in segment]


# Example usage
segment_length = 8
led_segments = get_led_segments(led_list, segment_length)
values = [
    (0, 0, 255),
    (0, 255, 0),
    (255, 0, 0),
    (255, 255, 0),
    (255, 0, 255),
    (0, 255, 255),
    (255, 255, 255),
    (80, 80, 80),
    (160, 160, 160),
]

assigned_segments = assign_values_to_segments(led_segments, values)
print(f"Assigned segments: {assigned_segments}")
flattened_segments = flatten_segments(assigned_segments)
