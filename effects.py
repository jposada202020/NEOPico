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
from colors import (
    BLACK,
    BLUE,
    RED,
    PURPLE,
    CYAN,
    ORANGE,
    ORANGEYELLOW,
    BLUE,
    GREEN,
    YELLOW,
)
from neopixel import NEOPIXEL
from functions import rgb255, hsv_to_rgb
import math
import random


def blink(
    led_object,
    color: tuple = RED,
    background_color: tuple = BLACK,
    dwell: float = 0.5,
    duration: int = 5,
) -> None:
    """
    Blink the NeoPixels.
    :param tuple color: the color to blink. Default is RED
    :param tuple background_color: the background color. Default is BLACK
    :param float dwell: time delay between each color change: default 0.5 seconds
    :param int duration: the duration in seconds. Default is 5 seconds
    :return: None
    """
    start_time = time.time()
    while time.time() - start_time < duration:
        led_object.neopixel_list = [color] * led_object.num_leds
        led_object.ShowNeoPixels(led_object.neopixel_list)
        time.sleep(dwell)
        led_object.neopixel_list = [background_color] * led_object.num_leds
        led_object.ShowNeoPixels(led_object.neopixel_list)
        time.sleep(dwell)


def chasing_color(
    led_object,
    palette: list = [RED, GREEN, BLUE],
    time_delta: float = 0.1,
    duration: int = 10,
) -> None:
    """
    Cycle through the colors in the list.
    :param tuple color: the color to chase. Default is [RED, GREEN, BLUE]
    :param float time_delta: time delay between each color change: default 0.1 seconds
    :param int duration: duration in seconds: default 10 seconds
    :return: None
    """
    rgb = 0
    i = 0
    led_object.fill_all(color=BLACK)
    start_time = time.time()
    if led_object.palette_colors is None:
        palette = [RED, GREEN, BLUE]
    else:
        buf = led_object.palette_colors
        colors_palette = []
        for _ in range(3):
            selection = choice(buf)
            colors_palette.append(selection)
            buf.remove(selection)
        palette = colors_palette

    while time.time() - start_time < duration:
        if rgb == 0:
            color = palette[0]
        elif rgb == 1:
            color = palette[1]
        else:
            color = palette[2]
        led_object.neopixel_list[i] = color
        led_object.ShowNeoPixels(led_object.neopixel_list)
        time.sleep(time_delta / 3)
        led_object.neopixel_list[i] = BLACK
        led_object.ShowNeoPixels(led_object.neopixel_list)
        rgb = (rgb + 1) % 3
        i = (i + 1) % led_object.num_leds
        time.sleep(time_delta)


def blink_rainbow(
    led_object,
    background_color=BLACK,
    dwell: float = 0.2,
    duration: int = 10,
) -> None:
    """
    Blink the NeoPixels.
    :param tuple background_color: the background color. Default is BLACK
    :param float dwell: time delay between each color change: default 0.2 seconds
    :param int duration: the duration in seconds. Default is 5 seconds
    :return: None
    """
    from rainbow import rainbow_colors

    rainbow_set = rainbow_colors

    seed = choice(range(0, 31))
    start_time = time.time()
    while time.time() - start_time < duration:
        led_object.neopixel_list = [rainbow_set[seed]] * led_object.num_leds
        led_object.ShowNeoPixels(led_object.neopixel_list)
        time.sleep(dwell)
        led_object.neopixel_list = [background_color] * led_object.num_leds
        led_object.ShowNeoPixels(led_object.neopixel_list)
        time.sleep(dwell)
        if seed < 31:
            seed = seed + 1
        else:
            seed = choice(range(0, 31))


def follow_rgb(
    led_object,
    loops: int = 3,
    color_list: any = None,
    dwell: float = 0.2,
    duration: int = 5,
) -> None:
    """
    Follow the colors Red, White, Blue.
    :param int loops: number of loops. Default is 3
    :param list color_list: list of colors. Default is None, You can pass a list of colors using
     the RGB format. For example [(255, 0, 0), (0, 255, 0), (0, 0, 255)]. Also you can define
     a palette of colors in the led object and the function will use the colors in the palette.
    :param float dwell: time delay between each color change. Default is 0.2 seconds
    :param int duration: duration in seconds. Default is 5 seconds
    :return: None
    """
    if color_list is None:
        if led_object.palette_colors is None:
            color_list = [BLACK, RED, GREEN, BLUE, YELLOW, PURPLE, CYAN, ORANGE]
        else:
            if len(led_object.palette_colors) > led_object.num_leds // 2:
                color_list = led_object.palette_colors[::2][
                    : led_object.num_leds // 2
                ]

    reference = len(color_list)

    start_time = time.time()
    while time.time() - start_time < duration:
        for i in range(led_object.num_leds * loops):
            for value in range(reference):
                led_object.neopixel_list[(i + value) % led_object.num_leds] = (
                    color_list[value]
                )
            led_object.ShowNeoPixels(led_object.neopixel_list)
            time.sleep(dwell)


def wipe(
    led_object,
    color1: tuple = GREEN,
    color2: tuple = YELLOW,
    delta_time: float = 0.1,
    ccw: bool = False,
    clear: bool = False,
    duration: int = 5,
) -> None:
    """
    Wipe the NeoPixels.
    :param tuple color1: the color to wipe. Default is GREEN
    :param tuple color2: the color to wipe. Default is YELLOW
    :param float delta_time: time delay between each color change: default 0.1 seconds
    :param bool ccw: counter-clockwise or clockwise. Default is False
    :param bool clear: clear the NeoPixels after each color. Default is False
    :duration int duration: duration in seconds. Default is 5 seconds
    :return: None
    """
    led_object.fill_all(color=BLACK)
    start_time = time.time()
    while time.time() - start_time < duration:
        for i in range(led_object.num_leds):
            if ccw:
                led_object.neopixel_list[led_object.num_leds - 1 - i] = color1
            else:
                led_object.neopixel_list[i] = color1
            led_object.ShowNeoPixels(led_object.neopixel_list)
            time.sleep(delta_time)
        if clear:
            led_object.fill_all(color=BLACK)
        for i in range(led_object.num_leds):
            if ccw:
                led_object.neopixel_list[led_object.num_leds - 1 - i] = color2
            else:
                led_object.neopixel_list[i] = color2
            led_object.ShowNeoPixels(led_object.neopixel_list)
            time.sleep(delta_time)
        if clear:
            led_object.fill_all(color=BLACK)


def pacman(led_object, duration: int = 15):
    """
    PACMAN ANIMATION Adapted from https://github.com/wled-dev/WLED/pull/4536 # by BobLoeffler68
    MIT LICENSE

    :param led_object: led object
    :param neopixel_list: list of neopixel colors
    :param int num_leds: number of leds.
    :param int duration: duration in seconds. Default is 15 seconds
    """

    direction = 1
    black_dir = -1
    if led_object.num_leds > 150:
        start_blinking_ghosts = led_object.num_leds // 4
    else:
        start_blinking_ghosts = led_object.num_leds // 3

    pacman = [BLUE, 10]
    ghosts_original = [[RED, 6], [PURPLE, 4], [CYAN, 2], [ORANGE, 0]]
    ghosts = [[RED, 6], [PURPLE, 4], [CYAN, 2], [ORANGE, 0]]
    power_pellet = [ORANGEYELLOW, led_object.num_leds - 1]
    led_object.neopixel_list[power_pellet[1]] = power_pellet[0]
    NEOPIXEL.ShowNeoPixels(led_object, led_object.neopixel_list)
    ghost_timer = time.ticks_ms()
    flag = "beep"

    start_time = time.time()

    while time.time() - start_time < duration:

        delta = time.ticks_ms() - ghost_timer
        if delta > 250:
            if power_pellet[0] == ORANGEYELLOW:
                power_pellet[0] = BLACK
            else:
                power_pellet[0] = ORANGEYELLOW

            led_object.neopixel_list[power_pellet[1]] = power_pellet[0]

            ghost_timer = time.ticks_ms()

        if pacman[1] >= led_object.num_leds - 2:
            direction = direction * -1
            black_dir = black_dir * -1
            for ghost in ghosts:
                ghost[0] = BLUE

        led_object.neopixel_list[pacman[1]] = pacman[0]
        led_object.neopixel_list[pacman[1] + black_dir] = BLACK
        pacman[1] += direction

        if ghosts[3][1] <= start_blinking_ghosts and direction == -1:
            if flag == "beep":
                for i, ghost in enumerate(ghosts):
                    ghost[0] = BLACK
                flag = "bop"
            else:
                for i, ghost in enumerate(ghosts):
                    ghost[0] = ghosts_original[i][0]
                flag = "beep"

        for i, ghost in enumerate(ghosts):
            led_object.neopixel_list[ghost[1]] = ghost[0]
            led_object.neopixel_list[ghost[1] + black_dir] = BLACK
            ghost[1] += direction

        if ghosts[3][1] <= 0:
            direction = direction * -1
            black_dir = black_dir * -1
            for i, ghost in enumerate(ghosts):
                ghost[0] = ghosts_original[i][0]

        NEOPIXEL.ShowNeoPixels(led_object, led_object.neopixel_list)
        time.sleep(0.1)


def rainbow_cycle(
    led_object,
    time_delta: float = 0.1,
    duration: int = 5,
) -> None:
    """
    Cycle through the rainbow colors.
    :param float time_delta: time delay between each color change: default 0.1 seconds
    :param int duration: duration in seconds: default 5 seconds
    :return: None
    """

    from rainbow import rainbow_colors

    rainbow_set = rainbow_colors

    start_time = time.time()
    while time.time() - start_time < duration:
        rainbow_set = rainbow_set[-1:] + rainbow_set[:-1]
        for i in range(led_object.num_leds):
            led_object.neopixel_list[i] = rainbow_set[i]
        NEOPIXEL.ShowNeoPixels(led_object, led_object.neopixel_list)
        time.sleep(time_delta)


def random_color(
    led_object,
    start: int = 0,
    delta_time: float = 0.1,
    duration: int = 5,
):
    """
    Random color effect. This function will set random colors to the leds.
    :param int num_leds: number of leds.
    :param int start: start index. Default is 0
    :param float delta_time: time delay between each color change: default 0.1 seconds
    :param int duration: duration in seconds. Default is 5 seconds
    """

    limits = range(0, 256)

    start_time = time.time()
    while time.time() - start_time < duration:

        for i in range(start, led_object.num_leds):
            led_object.neopixel_list[i] = (
                choice(limits),
                choice(limits),
                choice(limits),
            )
        NEOPIXEL.ShowNeoPixels(led_object, led_object.neopixel_list)
        time.sleep(delta_time)


def twinkle(led_object, delta_time: float = 0.1, duration: int = 5):
    """
    Twinke effect. This function will set random colors to the leds.
    :param led_object: led object
    :param float delta_time: time delay between each color change: default 0.1 seconds
    :param int duration: duration in seconds. Default is 5 seconds
    """
    if led_object.palette_colors is None:
        led_object.palette_colors = [
            RED,
            GREEN,
            BLUE,
            YELLOW,
            PURPLE,
            CYAN,
            ORANGE,
        ]

    start_time = time.time()

    while time.time() - start_time < duration:
        neopixel_list = [
            choice(led_object.palette_colors)
            for _ in range(led_object.num_leds)
        ]
        NEOPIXEL.ShowNeoPixels(led_object, neopixel_list)
        time.sleep(delta_time)


def get_led_segments(led_list, segment_length) -> list:
    segments = []
    for i in range(0, len(led_list), segment_length):
        segments.append(led_list[i : i + segment_length])
    return segments


def assign_values_to_segments(segments, values) -> list:

    assigned_segments = []
    for i, segment in enumerate(segments):
        if i < len(values):
            assigned_segment = [values[i]] * len(segment)
        else:
            assigned_segment = [BLACK] * len(segment)  # or some default value
        assigned_segments.append(assigned_segment)
    return assigned_segments


def flatten_segments(assigned_segments) -> list:
    return [led for segment in assigned_segments for led in segment]


def rainbow_sine(
    led_object,
    shrinkage: float = 0.1,
    animation_speed: float = 0.05,
    speed: float = 0.05,
    saturation: float = 1.0,
    value: float = 1.0,
    duration: int = 5,
):
    """
    Rainbow sine wave effect.
    :param led_object: led object
    :param float shrinkage: shrinkage value. Default is 0.1. This value will control the
        size of the color segments. The bigger the number the smaller the segments will be
    :param float animation_speed: animation speed. Default is 0.05. This value will control
        the speed of the animation
    :param float speed: speed of the animation. Default is 0.05 seconds. This value will control
        how often the animation is updated. You can fin tune animation increase and speed to get the
        desired effect
    :param float saturation: saturation value. Default is 1.0
    :param float value: value. Default is 1.0
    :param int duration: duration in seconds. Default is 5 seconds
    """
    animation = 0
    start_time = time.time()
    while time.time() - start_time < duration:
        for i in range(led_object.num_leds):
            hue = math.sin(animation + (i + 1) * shrinkage)
            hue = (hue + 1) / 2
            color = rgb255(hsv_to_rgb(hue, saturation, value))
            led_object.neopixel_list[i] = color

        NEOPIXEL.ShowNeoPixels(led_object, led_object.neopixel_list)
        animation += animation_speed
        time.sleep(speed)


def white_wave(
    led_object,
    animation_speed: float = 0.08,
    fade_animation_speed: float = 0.08,
    speed: float = 0.01,
    shrinkage: float = 0.3,
    duration: int = 5,
):
    """
    White wave effect.
    :param led_object: led object
    :param float animation_speed: animation speed. Default is 0.08. This value will control the
        speed of the animation
    :param float fade_animation_speed: fade animation speed. Default is 0.08. This value will control
        the speed of the fade animation
    :param float speed: speed of the animation. Default is 0.01 seconds. This value will control
        how often the animation is updated. You can fin tune animation increase and speed to get the
        desired effect
    :param float shrinkage: shrinkage value. Default is 0.3. This value will control the
        size of the segments. The bigger the number the smaller the segments will be
    :param int duration: duration in seconds. Default is 5 seconds
    """
    animation = 0
    fade_animation = 0

    start_time = time.time()
    while time.time() - start_time < duration:
        # Calculate fade effect using sine wave
        fade_effect = (math.sin(fade_animation) + 1) / 2
        # Set global brightness based on fade effect
        led_object.brightness = fade_effect
        for i in range(led_object.num_leds):
            brightness = math.sin(animation + i * shrinkage)
            brightness = (brightness + 1) / 2
            color = rgb255(hsv_to_rgb(0.0, 0.0, brightness))

            led_object.neopixel_list[i] = color

        NEOPIXEL.ShowNeoPixels(led_object, led_object.neopixel_list)
        # Increment animation variables
        animation += animation_speed
        fade_animation += fade_animation_speed
        # Small delay to control the speed of the animation
        time.sleep(speed)


def white_wave_color(
    led_object,
    animation_speed: float = 0.08,
    fade_animation_speed: float = 0.08,
    frequency: float = 0.003,
    speed: float = 0.1,
    duration: int = 5,
):
    """
    White wave effect.
    :param led_object: led object
    :param float animation_speed: animation speed. Default is 0.08. This value will control the
        speed of the animation
    :param float fade_animation_speed: fade animation speed. Default is 0.08. This value will control
        the speed of the fade animation
    :param float frequency: frequency value. Default is 0.003. This value will control the
        frequency of the wave
    :param float speed: speed of the animation. Default is 0.1 seconds. This value will control
        how often the animation is updated. You can fin tune animation increase and speed to get the
        desired effect
    :param int duration: duration in seconds. Default is 5 seconds
    """

    animation = 0
    fade_animation = 0
    shrinkage = 0
    freq = 0
    expand = 0

    start_time = time.time()
    while time.time() - start_time < duration:

        shrinkage = math.sin(freq)
        shrinkage = (shrinkage + 1) / 2

        expand = math.cos(freq)
        expand = (expand + 1) / 2

        for i in range(led_object.num_leds):
            # Calculate brightness for each LED using sine wave
            saturation = math.sin(animation + i * shrinkage)
            saturation = (saturation + 1) / 2
            saturation = int(saturation * 255)

            brightness = math.sin(animation + i * expand)
            brightness = (brightness + 1) / 2
            brightness = int(brightness * 255)

            led_object.neopixel_list[i] = (
                saturation,
                int(saturation / (brightness + 1)),
                brightness,
            )

        NEOPIXEL.ShowNeoPixels(led_object, led_object.neopixel_list)
        # Increment animation variables
        animation += animation_speed
        fade_animation += fade_animation_speed
        freq += frequency

        # Small delay to control the speed of the animation
        time.sleep(speed)


def linear_interpolation(
    led_object,
    shrinkage: float = 0.5,
    animation_increase: int = 0.1,
    speed: float = 0.01,
    duration: int = 5,
):
    """
    Linear interpolation effect. For this animation if you want to use a palette. The palette must
    be set in the led object. The palette must be a list of tuples with RGB values. The function will
    select two random colors from the palette and will interpolate between them.
    :param led_object: led object
    :param float shrinkage: shrinkage value. Default is 0.5. This value will control the
     size of the color segments. The bigger the number the smaller the segments will be
    :param float animation_increase: animation increase value. Default is 0.1. This value wil
        control the speed of the animation
    :param float speed: speed of the animation. Default is 0.01 seconds. This value will control
     how often the animation is updated. You can fin tune animation increase and speed to get the
        desired effect
    :param int duration: duration in seconds. Default is 5 seconds
    """
    from functions import lerp8by8

    animation = 0

    if led_object.palette_colors is None:
        color1 = (255, 0, 0)
        color2 = (0, 0, 255)
    else:
        color1 = choice(led_object.palette_colors)
        color2 = choice(led_object.palette_colors)

    start_time = time.time()
    while time.time() - start_time < duration:

        for i in range(led_object.num_leds):

            interpolation = math.sin(animation + i * shrinkage)
            interpolation = (interpolation + 1) / 2
            interpolation *= 255

            r = lerp8by8(color1[0], color2[0], int(interpolation))
            g = lerp8by8(color1[1], color2[1], int(interpolation))
            b = lerp8by8(color1[2], color2[2], int(interpolation))

            led_object.neopixel_list[i] = (r, g, b)

        NEOPIXEL.ShowNeoPixels(led_object, led_object.neopixel_list)

        animation += animation_increase

        time.sleep(speed)


def lerp_phase(
    led_object,
    animation_increase: int = 0.1,
    speed: float = 0.01,
    shrinkage: float = 0.2,
    phase_increase: float = 1.5,
    duration: int = 5,
):
    """
    Linear interpolation effect. For this animation if you want to use a palette. The palette must
    be set in the led object. The palette must be a list of tuples with RGB values. The function will
    select two random colors from the palette and will interpolate between them.
    :param led_object: led object
    :param float shrinkage: shrinkage value. Default is 0.5. This value will control the
     size of the color segments. The bigger the number the smaller the segments will be
    :param float animation_increase: animation increase value. Default is 0.1. This value wil
        control the speed of the animation
    :param float speed: speed of the animation. Default is 0.01 seconds. This value will control
     how often the animation is updated. You can fin tune animation increase and speed to get the
        desired effect
    :param float phase_increase: phase increase value. Default is 1.5. This value will control the
        speed of the phase. The bigger the number the faster the phase will change, this will be reflect
        in how the interpolation from one color to the other will change
    :param int duration: duration in seconds. Default is 5 seconds
    """
    from functions import lerp8by8

    animation = 0

    if led_object.palette_colors is None:
        color1 = (255, 0, 0)
        color2 = (0, 0, 255)
    else:
        color1 = choice(led_object.palette_colors)
        color2 = choice(led_object.palette_colors)

    start_time = time.time()
    while time.time() - start_time < duration:

        for i in range(led_object.num_leds):

            interpolation = math.sin(i * shrinkage)
            interpolation *= 127

            phase = math.sin(animation * phase_increase)

            interpolation *= phase
            interpolation += 127

            r = lerp8by8(color1[0], color2[0], int(interpolation))
            g = lerp8by8(color1[1], color2[1], int(interpolation))
            b = lerp8by8(color1[2], color2[2], int(interpolation))

            led_object.neopixel_list[i] = (r, g, b)

        NEOPIXEL.ShowNeoPixels(led_object, led_object.neopixel_list)

        animation += animation_increase

        time.sleep(speed)


def fadein_fadeout_random_color(
    led_object, fade_increment: float = 0.03, speed=0.1, duration: int = 5
):
    """
    White wave effect.
    :param led_object: led object
    :param float fade: fade value. Default is 0.03. You can play with the value
     For lower values the transition between colors will be smoother. For higher
     values the transition will be more abrupt. However this will depend on the
     animation speed paramer
    :param float speed: speed of the animation. Default is 0.1 seconds.
    :param int duration: duration in seconds. Default is 5 seconds
    """

    colorlist = [
        random.randint(0, 256),
        random.randint(0, 256),
        random.randint(0, 256),
    ]
    color_index = random.randint(0, len(colorlist) - 1)

    fade = 0
    start_time = time.time()
    while time.time() - start_time < duration:

        for i in range(led_object.num_leds):

            brightness = math.sin(fade + math.pi)
            brightness = (brightness + 1) / 2
            brightness = int(brightness * 255)
            colorlist[color_index] = brightness

            led_object.neopixel_list[i] = (
                colorlist[0],
                colorlist[1],
                colorlist[2],
            )

        NEOPIXEL.ShowNeoPixels(led_object, led_object.neopixel_list)

        if fade >= 2 * math.pi:
            fade = 0
            colorlist = [
                random.randint(0, 256),
                random.randint(0, 256),
                random.randint(0, 256),
            ]
            color_index = random.randint(0, len(colorlist) - 1)

        # Increment animation variables
        fade += fade_increment

        # Small delay to control the speed of the animation
        time.sleep(speed)


def fadein_fadeout_fragmented(
    led_object,
    fragments: int = 3,
    fade_increment: float = 0.08,
    speed=0.01,
    duration: int = 5,
):
    """
    White wave effect.
    :param led_object: led object
    :param int fragments: number of fragments. Default is 3
    :param float fade: fade value. Default is 0.03. You can play with the value
     For lower values the transition between colors will be smoother. For higher
     values the transition will be more abrupt. However this will depend on the
     animation speed paramer
    :param float speed: speed of the animation. Default is 0.1 seconds.
    :param int duration: duration in seconds. Default is 5 seconds
    """

    fade = 0
    fragment_size = led_object.num_leds // fragments

    fragment = 0
    colorlist = [
        random.randint(0, 256),
        random.randint(0, 256),
        random.randint(0, 256),
    ]
    color_index = random.randint(0, len(colorlist) - 1)

    start_time = time.time()
    while time.time() - start_time < duration:

        for i in range(
            fragment * fragment_size, fragment_size * (fragment + 1)
        ):

            brightness = math.cos(fade + math.pi)
            brightness = (brightness + 1) / 2
            brightness = int(brightness * 255)
            colorlist[color_index] = brightness

            led_object.neopixel_list[i] = (
                colorlist[0],
                colorlist[1],
                colorlist[2],
            )

        NEOPIXEL.ShowNeoPixels(led_object, led_object.neopixel_list)

        if fade >= 2 * math.pi:
            fade = 0
            colorlist = [
                random.randint(0, 256),
                random.randint(0, 256),
                random.randint(0, 256),
            ]
            color_index = random.randint(0, len(colorlist) - 1)
            fragment = fragment + 1
            fragment = fragment % fragments

        # Increment animation variables
        fade += fade_increment

        # Small delay to control the speed of the animation
        time.sleep(speed)


def fifo_fragmented_phase(
    led_object,
    fragment_amount: int = 2,
    fade_speed: float = 0.03,
    speed: float = 0.01,
    duration: int = 5,
):
    """
    White wave effect.
    :param led_object: led object
    :param int fragment_amount: number of fragments. Default is 2
    :param float fade_speed: fade value. Default is 0.03. You can play with the value
        For lower values the transition between colors will be smoother. For higher
        values the transition will be more abrupt. However this will depend on the
        animation speed paramer
    :param float speed: speed of the animation. Default is 0.1 seconds.
    :param int duration: duration in seconds. Default is 5 seconds
    """

    fade = 0

    fragment_size = math.floor(led_object.num_leds / fragment_amount)

    # Start time
    start_time = time.time()
    while time.time() - start_time < duration:

        for i in range(fragment_amount):

            brightness = math.cos(fade + (math.pi // 2 * i))
            brightness = (brightness + 1) / 2
            brightness = int(brightness * 255)

            # Set color for each LED
            begin = i * fragment_size
            end = min(fragment_size * (i + 1), led_object.num_leds)
            for j in range(begin, end):
                led_object.neopixel_list[j] = 0, 0, brightness

        fade += fade_speed

        if fade >= 20:
            fade = 0
            if fragment_amount >= 8:
                fragment_amount = 1
            fragment_amount *= 2
            fragment_size = math.ceil(led_object.num_leds / fragment_amount)

            led_object.fill_all(color=BLACK)

        # Increment animation variables
        NEOPIXEL.ShowNeoPixels(led_object, led_object.neopixel_list)

        # Small delay to control the speed of the animation
        time.sleep(speed)


def wave_freq_shrink_and_grow(
    led_object,
    move_increase: float = 0.2,
    freq_increase: float = 0.003,
    speed: float = 0.01,
    duration: int = 5,
):
    """
    White wave effect.
    :param led_object: led object
    :param float move_increase: move increase value. Default is 0.2. This value will control the
        speed of the move
    :param float freq_increase: frequency increase value. Default is 0.003. This value will control
        the frequency of the wave
    :param float speed: speed of the animation. Default is 0.01 seconds. This value will control
        how often the animation is updated. You can fin tune animation increase and speed to get the
        desired effect
    :param int duration: duration in seconds. Default is 5 seconds
    """

    move = 0
    freq = 0

    start_time = time.time()
    while time.time() - start_time < duration:
        shrinkage = math.sin(freq)
        shrinkage = (shrinkage + 1) / 2

        for i in range(led_object.num_leds):
            saturation = math.sin(move + i * shrinkage)
            saturation = (saturation + 1) / 2
            saturation = int(saturation * 255)

            led_object.neopixel_list[i] = 80, saturation, 80

        NEOPIXEL.ShowNeoPixels(led_object, led_object.neopixel_list)

        move += move_increase
        freq -= freq_increase

        # Small delay to control the speed of the animation
        time.sleep(speed)


def wave_freq_shrink_and_grow_centered(
    led_object,
    move_increase: float = 0.2,
    frequency: float = 0.003,
    speed: float = 0.01,
    duration: int = 5,
):
    """
    Wave effect with frequency and shrinkage centered.
    :param led_object: led object
    :param float move_increase: move increase value. Default is 0.2. This value will control the
        speed of the move
    :param float frequency: frequency value. Default is 0.003. This value will control the
        frequency of the wave
    :param float speed: speed of the animation. Default is 0.01 seconds. This value will control
        how often the animation is updated. You can fin tune animation increase and speed to get the
        desired effect
    :param int duration: duration in seconds. Default is 5 seconds
    """

    move = 0
    freq = 0

    start_time = time.time()
    while time.time() - start_time < duration:
        shrinkage = math.sin(freq)
        shrinkage = (shrinkage + 1) / 2

        midpoint = led_object.num_leds // 2

        for i in range(midpoint):

            saturation = math.cos(move + i * shrinkage)
            saturation = (saturation + 1) / 2
            saturation = int(saturation * 255)

            led_object.neopixel_list[midpoint + i] = 25, saturation, 80
            led_object.neopixel_list[midpoint - i] = 80, saturation, 25

        NEOPIXEL.ShowNeoPixels(led_object, led_object.neopixel_list)

        move += move_increase
        freq += frequency

        time.sleep(speed)


def wave_back_and_forth(
    led_object,
    move_increase: float = 0.06,
    speed: float = 0.01,
    duration: int = 5,
):
    """
    White wave effect.
    :param led_object: led object
    :param float move_increase: move increase value. Default is 0.06. This value will control the
        speed of the move
    :param float speed: speed of the animation. Default is 0.01 seconds. This value will control
        how often the animation is updated. You can fin tune animation increase and speed to get the
        desired effect
    :param int duration: duration in seconds. Default is 5 seconds
    """

    move = 0
    hue = 0

    start_time = time.time()
    while time.time() - start_time < duration:

        for i in range(led_object.num_leds):
            hue = int(hue + math.sin(move) * led_object.num_leds)

            brigthness = i + math.sin(move) * 20
            brigthness = math.sin(brigthness)
            brigthness = (brigthness + 1) / 2
            brigthness = int(brigthness * 255)

            led_object.neopixel_list[i] = hue, 80, brigthness

        NEOPIXEL.ShowNeoPixels(led_object, led_object.neopixel_list)

        move += move_increase

        time.sleep(speed)


def shrink_and_grow(led_object, duration: int = 5):
    """
    White wave effect.
    :param led_object: led object
    :param int duration: duration in seconds. Default is 5 seconds
    """

    move = 0
    midpoint = led_object.num_leds // 2
    spread = midpoint * ((math.sin(move) + 1) / 2)
    step = math.pi / spread

    # Start time
    start_time = time.time()
    while time.time() - start_time < duration:

        for i in range(int(spread)):
            brigthness = math.cos(i + move * step)
            brigthness = (brigthness + 1) / 2
            brigthness = int(brigthness * 255)

            led_object.neopixel_list[midpoint + i] = 60, 60, brigthness
            led_object.neopixel_list[midpoint - i] = 60, 60, brigthness

        NEOPIXEL.ShowNeoPixels(led_object, led_object.neopixel_list)

        move += 0.05

        # Small delay to control the speed of the animation
        time.sleep(0.01)
        if move >= 2 * math.pi:
            move = 0


def shrink_and_grow_multiple(
    led_object,
    fragment_amount: int = 4,
    move_increase: float = 0.08,
    speed: float = 0.01,
    duration: int = 5,
):
    """
    White wave effect.
    :param led_object: led object
    :param int fragment_amount: number of fragments. Default is 4
    :param float move_increase: move increase value. Default is 0.08. This value will control the
        speed of the move
    :param float speed: speed of the animation. Default is 0.01 seconds. This value will control
        how often the animation is updated. You can fin tune animation increase and speed to get the
        desired effect
    :param int duration: duration in seconds. Default is 5 seconds
    """

    move = 0

    fragment_size = led_object.num_leds // fragment_amount
    fragment_midpoint = fragment_size // 2

    spread = fragment_midpoint * ((math.sin(move) + 1) / 2)
    step = math.pi / spread
    led_object.fill_all(color=(BLACK))

    start_time = time.time()
    while time.time() - start_time < duration:

        for fragment in range(fragment_amount):
            pos = fragment * fragment_size
            midpoint = pos + fragment_midpoint

            for i in range(int(spread)):
                brigthness = math.cos(i + move * step * math.pi)
                brigthness = (brigthness + 1) / 2
                brigthness = int(brigthness * 255)

                led_object.neopixel_list[midpoint + i] = 25, brigthness, 80
                led_object.neopixel_list[midpoint - i] = 80, brigthness, 25

        NEOPIXEL.ShowNeoPixels(led_object, led_object.neopixel_list)

        move += move_increase

        # Small delay to control the speed of the animation
        time.sleep(speed)
        if move >= 2 * math.pi:
            move = 0
            pos = 0


def shrink_and_grow_multiple_moving(
    led_object,
    fragment_amount: int = 4,
    midpoint_increase: float = 0.05,
    move_increase: float = 0.05,
    speed: float = 0.01,
    duration: int = 5,
):
    """
    White wave effect.
    :param led_object: led object
    :param int fragment_amount: number of fragments. Default is 4
    :param float midpoint_increase: midpoint increase value. Default is 0.05. This value will control the
        speed of the move
    :param float move_increase: move increase value. Default is 0.05. This value will control the
        speed of the move
    :param float speed: speed of the animation. Default is 0.01 seconds. This value will control
        how often the animation is updated. You can fin tune animation increase and speed to get the
        desired effect
    :param int duration: duration in seconds. Default is 5 seconds
    """

    move = 0

    midpoint = [0] * fragment_amount

    leds = [(0, 0, 0)] * led_object.num_leds
    fragment_size = led_object.num_leds // fragment_amount
    fragment_midpoint = fragment_size // 2

    for fragment in range(fragment_amount):
        pos = fragment * fragment_size
        midpoint[fragment] = fragment_midpoint + (fragment * fragment_size)

    spread = fragment_midpoint * ((math.sin(move) + 1) / 2)
    step = math.pi / spread

    start_time = time.time()
    while time.time() - start_time < duration:

        for fragment in range(fragment_amount):
            midpoint[fragment] += midpoint_increase

            if midpoint[fragment] > led_object.num_leds:
                midpoint[fragment] = 0

            pos = midpoint[fragment]

            for i in range(int(spread) + 1):

                brightness = math.cos(i + step)
                brightness = (brightness + 1) / 2
                brightness = int(brightness * 255)

                leds[int((pos + i) % led_object.num_leds)] = 110, 32, brightness

                if pos - i < 0:
                    leds[int(pos + led_object.num_leds - i)] = (
                        80,
                        80,
                        brightness,
                    )
                else:
                    leds[int(pos - i)] = 128, 54, brightness

        NEOPIXEL.ShowNeoPixels(led_object, leds)

        move += move_increase

        # Small delay to control the speed of the animation
        time.sleep(speed)


def snail(
    led_object,
    fragment_amount: int = 8,
    snail_minimum_size: int = 6,
    is_shrinking: bool = False,
    snailbegin: int = 0,
    snailend: int = 2,
    speed: float = 0.01,
    duration: int = 5,
):
    """
    White wave effect.
    :param led_object: led object
    :param int fragment_amount: number of fragments. Default is 8
    :param int duration: duration in seconds. Default is 5 seconds
    """

    fragment_size = led_object.num_leds // fragment_amount

    leds = [BLACK] * led_object.num_leds

    start_time = time.time()
    while time.time() - start_time < duration:
        snail_size = 0

        if snailend >= snailbegin:
            snail_size = snailend - snailbegin
        else:
            snail_size = led_object.num_leds - snailbegin + snailend

        spread = snail_size
        step = 2 * math.pi / spread

        for i in range(spread):
            brightness = math.cos(math.pi + (i * step))
            brightness = (brightness + 1) / 2
            brightness = int(brightness * 255)

            index = int((snailbegin + i) % led_object.num_leds)
            leds[index] = 215, 128, brightness

        NEOPIXEL.ShowNeoPixels(led_object, leds)
        time.sleep(speed)

        if not is_shrinking:
            snailend += 0.08
            if snailend >= led_object.num_leds:
                snailend = 0
            if snail_size > fragment_size:
                is_shrinking = True
        else:
            snailbegin += 0.08
            if snailbegin >= led_object.num_leds:
                snailbegin = 0
            if snail_size < snail_minimum_size:
                is_shrinking = False


def segments(
    led_object,
    segment_length: int = 3,
    values: list = None,
    speed: float = 0.1,
    duration: int = 5,
):
    """
    Segment effect. This function will set values to segments of the led strip.
    :param led_object: led object
    :param int segment_length: segment length. Default is 3
    :param list values: list of values. Default is None
    :param float speed: speed of the animation. Default is 0.1 seconds
    :param int duration: duration in seconds. Default is 5 seconds
    """

    led_list = [BLACK for _ in range(led_object.num_leds)]

    led_segments = get_led_segments(led_list, segment_length)
    assigned_segments = assign_values_to_segments(led_segments, values)
    led_object.neopixel_list = flatten_segments(assigned_segments)

    start_time = time.time()
    while time.time() - start_time < duration:
        NEOPIXEL.ShowNeoPixels(led_object, led_object.neopixel_list)
        time.sleep(speed)
