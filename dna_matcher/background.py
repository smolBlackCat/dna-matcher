"""Module dedicated for putting backgrounds on scenes."""

import random

import pygame.sprite as sprite
import pygame.surface as surface


class BaseBackground:
    """Base for background class."""

    def __init__(self, screen):
        """Initialises the object."""

        self.screen = screen
        self.screen_rect = screen.get_rect()

    def draw(self):
        """It draws the background."""

        pass

    def update(self):
        """It updates the background state."""

        pass


class ColourChangingBackground(BaseBackground):
    """A class that represents a Surface that changes its colour
    all the time.
    """

    def __init__(self, screen):
        super().__init__(screen)
        self.bg = surface.Surface(screen.get_size())
        self.colour = {
            "r": [random.randint(0, 255), 1],
            "g": [random.randint(0, 255), 1],
            "b": [random.randint(0, 255), 1]
        }

    def draw(self):
        r = self.colour["r"][0]
        g = self.colour["g"][0]
        b = self.colour["b"][0]
        self.screen.fill((r, g, b))

    def update(self):
        for key, colour_stats in self.colour.items():
            if colour_stats[0] >= 255:
                self.colour[key][1] = -1
            elif colour_stats[0] <= 0:
                self.colour[key][1] = 1

            self.colour[key][0] += self.colour[key][1]
