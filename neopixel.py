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
from random import choice

try:
    from typing import Tuple
except ImportError:
    pass

BLACK = (0, 0, 0)


class NEOPIXEL:
    def __init__(self, pin: int, num_leds: int) -> None:
        """
        Initialize the NeoPixels.
        :param int pin: the pin number where the NeoPixels are connected
        :param int num_leds: the number of NeoPixels
        :return: None

        """
        self.pin = pin
        self.num_leds = num_leds

        self.rainbow = [
            (126, 1, 0),
            (114, 13, 0),
            (102, 25, 0),
            (90, 37, 0),
            (78, 49, 0),
            (66, 61, 0),
            (54, 73, 0),
            (42, 85, 0),
            (30, 97, 0),
            (18, 109, 0),
            (6, 121, 0),
            (0, 122, 5),
            (0, 110, 17),
            (0, 98, 29),
            (0, 86, 41),
            (0, 74, 53),
            (0, 62, 65),
            (0, 50, 77),
            (0, 38, 89),
            (0, 26, 101),
            (0, 14, 113),
            (0, 2, 125),
            (9, 0, 118),
            (21, 0, 106),
            (33, 0, 94),
            (45, 0, 82),
            (57, 0, 70),
            (69, 0, 58),
            (81, 0, 46),
            (93, 0, 34),
            (105, 0, 22),
            (117, 0, 10),
        ]

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

    def rainbow_cycle(self, time_delta: float = 0.1, duration: int = 5) -> None:
        """
        Cycle through the rainbow colors.
        :param float time_delta: time delay between each color change: default 0.1 seconds
        :param int duration: duration in seconds: default 5 seconds
        :return: None
        """
        start_time = time.time()
        while time.time() - start_time < duration:
            self.rainbow = self.rainbow[-1:] + self.rainbow[:-1]
            for i in range(16):
                self.neopixel_list[i] = self.rainbow[i]
            self.ShowNeoPixels(self.neopixel_list)
            time.sleep(time_delta)

    def chasing_color(
        self,
        color: tuple = (255, 0, 0),
        time_delta: float = 0.1,
        duration: int = 10,
    ) -> None:
        """
        Cycle through the colors in the list.
        :param tuple color: the color to chase. Default is (255, 0, 0) i.e. red
        :param float time_delta: time delay between each color change: default 0.1 seconds
        :param int duration: duration in seconds: default 10 seconds
        :return: None
        """
        rgb = 0
        i = 0
        start_time = time.time()
        while time.time() - start_time < duration:
            self.neopixel_list[i] = color
            self.ShowNeoPixels(self.neopixel_list)
            time.sleep(time_delta)
            self.neopixel_list[i] = (0, 0, 0)
            self.ShowNeoPixels(self.neopixel_list)
            rgb = (rgb + 1) % 3
            i = (i + 1) % self.num_leds

    def fill_all(
        self,
        duration: int = 5,
        time_delta: float = 0.1,
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

    def blink(
        self,
        color: tuple = (255, 0, 0),
        background_color: Tuple[int, int, int] = (0, 0, 0),
        duration: int = 5,
    ) -> None:
        """
        Blink the NeoPixels.
        :param tuple color: the color to blink. Default is (255, 0, 0) i.e. red
        :param tuple background_color: the background color. Default is (0, 0, 0) i.e. black
        :param int duration: the duration in seconds. Default is 5 seconds
        :return: None
        """
        start_time = time.time()
        while time.time() - start_time < duration:
            self.neopixel_list = [color] * self.num_leds
            self.ShowNeoPixels(self.neopixel_list)
            time.sleep(0.5)
            self.neopixel_list = [background_color] * self.num_leds
            self.ShowNeoPixels(self.neopixel_list)
            time.sleep(0.5)

    def blink_rainbow(
        self,
        background_color: Tuple[int, int, int] = (0, 0, 0),
        duration: int = 10,
        dwell: float = 0.2,
    ) -> None:
        """
        Blink the NeoPixels.
        :param tuple background_color: the background color. Default is (0, 0, 0) i.e. black
        :param int duration: the duration in seconds. Default is 5 seconds
        :param float dwell: time delay between each color change: default 0.2 seconds
        :return: None
        """
        seed = choice(range(0, 31))
        start_time = time.time()
        while time.time() - start_time < duration:
            self.neopixel_list = [self.rainbow[seed]] * self.num_leds
            self.ShowNeoPixels(self.neopixel_list)
            time.sleep(dwell)
            self.neopixel_list = [background_color] * self.num_leds
            self.ShowNeoPixels(self.neopixel_list)
            time.sleep(dwell)
            if seed < 31:
                seed = seed + 1
            else:
                seed = 0

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

    def follow_rgb(self, loops: int = 3, color_list: any = None) -> None:
        """
        Follow the colors Red, White, Blue.
        :param int loops: number of loops. Default is 3
        :param list color_list: list of colors. Default is None
        :return: None
        """
        if color_list is None:
            color_list = [(0, 0, 0), (255, 0, 0), (127, 255, 127), (0, 0, 255)]
        reference = len(color_list)

        for i in range(self.num_leds * loops):
            for value in range(reference):
                self.neopixel_list[(i + value) % self.num_leds] = color_list[
                    value
                ]
            self.ShowNeoPixels(self.neopixel_list)
            time.sleep(0.2)

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

    def wipe(
        self,
        color1: tuple = (0, 255, 0),
        color2: tuple = (255, 255, 0),
        delta_time: float = 0.1,
        ccw: bool = False,
        duration: int = 5,
    ) -> None:
        """
        Wipe the NeoPixels.
        :param tuple color1: the color to wipe. Default is (0, 255, 0) i.e. green
        :param tuple color2: the color to wipe. Default is (255, 255, 0) i.e. yellow
        :param float delta_time: time delay between each color change: default 0.1 seconds
        :param bool ccw: counter-clockwise or clockwise. Default is False
        :duration int duration: duration in seconds. Default is 5 seconds
        :return: None
        """
        start_time = time.time()
        while time.time() - start_time < duration:
            for i in range(self.num_leds):
                if ccw:
                    self.neopixel_list[self.num_leds - 1 - i] = color1
                else:
                    self.neopixel_list[i] = color1
                self.ShowNeoPixels(self.neopixel_list)
                time.sleep(delta_time)
            for i in range(self.num_leds):
                if ccw:
                    self.neopixel_list[self.num_leds - 1 - i] = color2
                else:
                    self.neopixel_list[i] = color2
                self.ShowNeoPixels(self.neopixel_list)
                time.sleep(delta_time)

    def data_dummy(self):
        """
        Dummy data for testing.
        """

        data = [BLACK for i in range(self.num_leds)]
        step = 0
        while True:
            red = int((1 + sin(step * 0.1324)) * 127)
            green = int((1 + sin(step * 0.1654)) * 127)
            blue = int((1 + sin(step * 0.1)) * 127)
            data[step % self.num_leds] = (red, green, blue)
            yield data
            step += 1

    def sinousoidal(self, dwell=0.5, duration: int = 5):
        """
        Sinousoidal data for testing
        :param float dwell: time delay between each color change. Default is 0.5 seconds
        :param int duration: duration in seconds. Default is 5 seconds
        """
        start_time = time.time()
        while time.time() - start_time < duration:
            for data in self.data_dummy():
                self.ShowNeoPixels(data)
                time.sleep(dwell)


if __name__ == "__main__":
    ring = NEOPIXEL(Pin(15), 16)

    ring.chasing_color()
    ring.fill_all(color=(0, 255, 0))
    ring.blink_rainbow(background_color=(0, 255, 0))
    ring.wipe(color1=(0, 255, 0))
    ring.sequence([(255, 0, 0), (0, 255, 0), (0, 0, 255)])
    ring.fill_all(color=(0, 0, 0))
    ring.fill_all(color=(0, 255, 0))
    for i in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
        ring.brightness(brightness=i)
        time.sleep(1)
    ring.follow_rgb()
    ring.fill_all(color=(0, 0, 0))
    ring.sinousoidal()
