# SPDX-FileCopyrightText: Copyright (c) 2025 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

"""

`neopico`
================================================================================

MicroPython NeoPixel library with animations

* Author: Jose D. Montoya

Colowheel adapted from code from Kattni Rembor for Adafruit Industries
Pio from https://toptechboy.com/page/2/ Paul McWhorter
sinoussoidal data generator written by Jan Bednarik https://github.com/JanBednarik/micropython-ws2812

There are amazing libraries for NeoPixels like Adafruit_CircuitPython_NeoPixel and Adafruit_CircuitPython_LED_Animation
This is a simple library to show how to use PIO and animations with NeoPixels and to use for my own projects at home.
Only tested with a Raspberry Pi Pico and a 16 NeoPixel ring.

"""


from machine import Pin
import rp2
import time
from math import log, e, sin
from colors import BLACK, PURPLE


try:
    from typing import Tuple
except ImportError:
    pass


class NEOPIXEL:
    def __init__(self, pin: int, num_leds: int) -> None:
        """
        Initialize the NeoPixels.
        :param int pin: the pin number where the NeoPixels are connected
        :param int num_leds: the number of NeoPixels
        :return: None

        """
        # TODO verify color format

        self.pin = pin
        self.num_leds = num_leds
        self.palette_colors = None

        self.neopixel_list = []
        for i in range(num_leds):
            self.neopixel_list.append(BLACK)
        self.neopixel_list_brightness = None

        self.brightness_values = [
            0.1,
            0.2,
            0.3,
            0.4,
            0.5,
            0.6,
            0.7,
            0.8,
            0.9,
            1.0,
        ]
        y = list(self.linspace(0, 255, 10))
        self._brightnes_normalized = [
            int((e ** (log(255) / 255)) ** _) for _ in y
        ]

        self._initialize()

    @rp2.asm_pio(
        sideset_init=rp2.PIO.OUT_HIGH,
        out_shiftdir=rp2.PIO.SHIFT_LEFT,
        autopull=True,
        pull_thresh=24,
    )
    def neo_prog():
        """
        PIO program to drive NeoPixels.
        taken from https://toptechboy.com/page/2/ Paul McWhorter
        """
        wrap_target()
        label("bitloop")
        out(x, 1).side(0)
        jmp(not_x, "do_zero").side(1)
        nop().side(1)[5 - 1]
        nop().side(0)[2 - 1]
        jmp("bitloop").side(0)
        label("do_zero")
        nop().side(1)[2 - 1]
        jmp("bitloop").side(0)[6 - 1]
        wrap()

    def ShowNeoPixels(self, led_list) -> None:
        """
        each pixel is the tuple (r, g, b)
        adapted from https://toptechboy.com/page/2/ Paul McWhorter
        :param pixels: list of pixels
        :return: None
        """
        for color in led_list:
            grb = color[1] << 16 | color[0] << 8 | color[2]  # Green, Red, Blue
            self.sm.put(grb, 8)

    def _initialize(self) -> None:
        """
        Initialize the NeoPixels state machine.
        :return: None
        """
        self.sm = rp2.StateMachine(
            0,
            self.neo_prog,
            freq=8_000_000,
            sideset_base=Pin(self.pin),
        )
        self.sm.active(1)
        self.fill_all(color=PURPLE)

    def fill_all(
        self,
        duration: int = 0.1,
        time_delta: float = 0.0,
        color: tuple = (255, 0, 0),
    ) -> None:
        """
        Cycle through the rainbow colors.
        :param int duration: duration in seconds: default 5 seconds
        :param float time_delta: time delay between each color change: default 0.1 seconds
        :param tuple color: the color to fill. Default is (255, 0, 0) i.e. red
        :return: None
        """
        start_time = time.time()
        while time.time() - start_time < duration:
            # Set all pixels to the same color
            self.neopixel_list = [color] * self.num_leds
            self.ShowNeoPixels(self.neopixel_list)
            time.sleep(time_delta)

    def sequence(
        self, colors: list, delta_time: int = 0.1, duration: int = 5
    ) -> None:
        """
        Cycle through the colors in the list.
        :param list colors: list of colors
        :param float delta_time: time delay between each color change: default 0.1 seconds
        :param int duration: duration in seconds. Default is 5 seconds
        :return: None
        """
        start_time = time.time()
        while time.time() - start_time < duration:
            for color in colors:
                self.neopixel_list = [color] * self.num_leds
                self.ShowNeoPixels(self.neopixel_list)
                time.sleep(delta_time)

    def fill_custom(
        self, color_list: list, dwell: float = 0.5, duration: int = 5
    ) -> None:
        """
        Fill the NeoPixels with custom colors.
        :param list color_list: list of colors
        :param int duration: duration in seconds. Default is 5 seconds
        :return: None
        """
        start_time = time.time()
        while time.time() - start_time < duration:
            for i in range(self.num_leds):
                self.neopixel_list[i] = color_list[i]
            self.ShowNeoPixels(self.neopixel_list)
            time.sleep(dwell)

    def brightness(self, brightness: float = 1.0) -> None:
        """
        Set the brightness of the NeoPixels.
        :param float brightness: the brightness value. Default is 1.0
        :return: None
        :raises ValueError: if the brightness value is not in the list of valid values
        """
        if brightness not in self.brightness_values:
            raise ValueError(
                "Brightness must be one of 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0"
            )

        a = self.brightness_values.index(brightness)
        normalized_brightness = self._brightnes_normalized[a] / 255.0
        new_neopixel_list = [
            (
                int(r * normalized_brightness),
                int(g * normalized_brightness),
                int(b * normalized_brightness),
            )
            for (r, g, b) in self.neopixel_list
        ]
        self.ShowNeoPixels(new_neopixel_list)

    @staticmethod
    def linspace(start: int, stop: int, n: int):
        """
        Creates a linearspace
        :param int start: start number
        :param int stop: end number
        :param int n: Step number
        """
        if n == 1:
            yield stop
            return
        delta = (stop - start) / (n - 1)
        for i in range(n):
            yield start + delta * i

    def segment_animated(
        self,
        segment_length: int,
        values: list,
        duration: int = 5,
        animation: str = "fade",
    ):
        """
        Get led segments
        :param int segment_length: the segment length
        :param list values: the values
        :param int duration: duration in seconds. Default is 5 seconds
        :return: the segments
        """

        from effects import segment_animated_effect

        segment_animated_effect(
            self,
            self.neopixel_list,
            self.num_leds,
            duration,
            segment_length,
            values,
            animation,
        )

    def segment(self, segment_length: int, values: list, duration: int = 5):
        """
        Get led segments
        :param int segment_length: the segment length
        :param list values: the values
        :param int duration: duration in seconds. Default is 5 seconds
        :return: the segments
        """

        from effects import segment_effect

        segment_effect(
            self,
            self.neopixel_list,
            self.num_leds,
            duration,
            segment_length,
            values,
        )
