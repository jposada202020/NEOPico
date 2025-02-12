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
import palette
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

    def rainbow_cycle(self, time_delta: float = 0.1, duration: int = 5) -> None:
        """
        Cycle through the rainbow colors.
        :param float time_delta: time delay between each color change: default 0.1 seconds
        :param int duration: duration in seconds: default 5 seconds
        :return: None
        """
        from effects import rainbow_cycle_effect

        rainbow_cycle_effect(
            self,
            self.neopixel_list,
            self.num_leds,
            time_delta,
            duration,
        )

    def chasing_color(
        self,
        palette: list = [(255, 0, 0), (0, 255, 0), (0, 0, 255)],
        time_delta: float = 0.1,
        duration: int = 10,
    ) -> None:
        """
        Cycle through the colors in the list.
        :param tuple color: the color to chase. Default is [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        :param float time_delta: time delay between each color change: default 0.1 seconds
        :param int duration: duration in seconds: default 10 seconds
        :return: None
        """
        rgb = 0
        i = 0
        self.fill_all(color=BLACK)
        start_time = time.time()
        if self.palette_colors is None:
            palette = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        else:
            buf = self.palette_colors
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
            self.neopixel_list[i] = color
            self.ShowNeoPixels(self.neopixel_list)
            time.sleep(time_delta / 3)
            self.neopixel_list[i] = BLACK
            self.ShowNeoPixels(self.neopixel_list)
            rgb = (rgb + 1) % 3
            i = (i + 1) % self.num_leds
            time.sleep(time_delta)

    def fill_all(
        self,
        duration: int = 0.1,
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
        dwell: float = 0.5,
        duration: int = 5,
    ) -> None:
        """
        Blink the NeoPixels.
        :param tuple color: the color to blink. Default is (255, 0, 0) i.e. red
        :param tuple background_color: the background color. Default is (0, 0, 0) i.e. black
        :param float dwell: time delay between each color change: default 0.5 seconds
        :param int duration: the duration in seconds. Default is 5 seconds
        :return: None
        """
        start_time = time.time()
        while time.time() - start_time < duration:
            self.neopixel_list = [color] * self.num_leds
            self.ShowNeoPixels(self.neopixel_list)
            time.sleep(dwell)
            self.neopixel_list = [background_color] * self.num_leds
            self.ShowNeoPixels(self.neopixel_list)
            time.sleep(dwell)

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

    def follow_rgb(
        self,
        loops: int = 3,
        color_list: any = None,
        dwell: float = 0.2,
        duration: int = 5,
    ) -> None:
        """
        Follow the colors Red, White, Blue.
        :param int loops: number of loops. Default is 3
        :param list color_list: list of colors. Default is None
        :param float dwell: time delay between each color change. Default is 0.2 seconds
        :param int duration: duration in seconds. Default is 5 seconds
        :return: None
        """
        if color_list is None:
            color_list = [(0, 0, 0), (255, 0, 0), (127, 255, 127), (0, 0, 255)]
        reference = len(color_list)

        start_time = time.time()
        while time.time() - start_time < duration:
            for i in range(self.num_leds * loops):
                for value in range(reference):
                    self.neopixel_list[(i + value) % self.num_leds] = (
                        color_list[value]
                    )
                self.ShowNeoPixels(self.neopixel_list)
                time.sleep(dwell)

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
        self.fill_all(color=BLACK)
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

    def random_color(self, start=0, duration: int = 5):
        """
        Random color data for testing
        :param int start: start number. Default is 0
        :param int duration: duration in seconds. Default is 5 seconds
        """

        from effects import random_color

        random_color(
            self,
            self.neopixel_list,
            start,
            self.num_leds,
            duration,
        )

    def pacman(self, duration: int = 5):
        """
        Dummy data for testing.
        :param int duration: duration in seconds. Default is 5 seconds
        """
        from effects import pacman_effect

        pacman_effect(
            self,
            self.neopixel_list,
            self.num_leds,
            duration,
        )

    def rainbow_sine(self, duration: int = 5):
        """
        Rainbow sine data to display
        :param int duration: duration in seconds. Default is 5 seconds
        """
        from effects import rainbow_sine_effect

        rainbow_sine_effect(
            self,
            self.neopixel_list,
            self.num_leds,
            duration,
        )

    def twinkle(self, duration: int = 5):
        """
        Dummy data for testing.
        :param int duration: duration in seconds. Default is 5 seconds
        """
        from effects import twinkle_effect

        twinkle_effect(
            self,
            self.palette_colors,
            self.neopixel_list,
            self.num_leds,
            duration,
        )

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

    def white_wave(self, duration: int = 5):
        """
        White wave animation
        :param int duration: duration in seconds. Default is 5 seconds
        """
        from effects import white_wave_effect

        white_wave_effect(
            self,
            self.neopixel_list,
            self.num_leds,
            duration,
        )

    def white_wave_color(self, duration: int = 5):
        """
        White wave color effect
        :param int duration: duration in seconds. Default is 5 seconds
        """
        from effects import white_wave_color_effect

        white_wave_color_effect(
            self,
            self.neopixel_list,
            self.num_leds,
            duration,
        )

    def linear_interpolation(self, duration: int = 5):
        """
        Linear interpolation effect
        :param int duration: duration in seconds. Default is 5 seconds
        """
        from effects import lerp_effect

        lerp_effect(
            self,
            self.neopixel_list,
            self.num_leds,
            duration,
        )

    def linear_phase_interpolation(self, duration: int = 5):
        """
        Linear phase interpolation effect
        :param int duration: duration in seconds. Default is 5 seconds
        """
        from effects import lerp_phase_effect

        lerp_phase_effect(
            self,
            self.neopixel_list,
            self.num_leds,
            duration,
        )

    def fadein_fadeout_random_color(self, duration: int = 5):
        """
        Fade in fade out effect
        :param int duration: duration in seconds. Default is 5 seconds
        """
        from effects import fadein_fadeout_random_color_effect

        fadein_fadeout_random_color_effect(
            self,
            self.neopixel_list,
            self.num_leds,
            duration,
        )

    def fadein_fadeout_fragmented(self, duration: int = 5):
        """
        Fade in fade out fragmented effect
        :param int duration: duration in seconds. Default is 5 seconds
        """
        from effects import fadein_fadeout_fragmented_effect

        fadein_fadeout_fragmented_effect(
            self,
            self.neopixel_list,
            self.num_leds,
            duration,
        )

    def fifo_fragmented_phase(self, duration: int = 5):
        """
        FIFO fragmented effect
        :param int duration: duration in seconds. Default is 5 seconds
        """
        from effects import fifo_fragmented_phase_effect

        fifo_fragmented_phase_effect(
            self,
            self.neopixel_list,
            self.num_leds,
            duration,
        )

    def wave_freq_shrink_and_grow(self, duration: int = 5):
        """
        Wave frequency shrink and grow effect
        :param int duration: duration in seconds. Default is 5 seconds
        """
        from effects import wave_freq_shrink_and_grow_effect

        wave_freq_shrink_and_grow_effect(
            self,
            self.neopixel_list,
            self.num_leds,
            duration,
        )


if __name__ == "__main__":
    ring = NEOPIXEL(Pin(15), 8)
    ring.define_palette()
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
