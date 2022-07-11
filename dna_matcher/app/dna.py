"""Module for dna analysis related class and functions."""

import Levenshtein as lv
import pygame.draw as draw


class DNA:
    """DNA class."""

    def __init__(self, screen, x_boundaries, file: str):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        # ex. 67, 548
        self.genome = DNA.get_genome(file)
        self.colour_map = {
            "G": (73, 52, 235),
            "A": (52, 235, 52),
            "T": (147, 52, 235),
            "C": (208, 235, 52)
        }
        if self.genome is None:
            raise ValueError(f"{file} is not a DNA sample.")

        # TODO: Calculate how many balls, their y distance from each other
        self.x_boundaries = x_boundaries
        self.middle_point = sum(x_boundaries) // 2
        self.y_boundaries = (40, 590)
        self.circles = []
        self.lines = []
        y_row = self.y_boundaries[0]

        for i in range(20):
            circle_pair = []
            line_par_points = []

            circle_pair.append([self.x_boundaries[0], y_row])
            circle_pair.append([self.x_boundaries[1], y_row])

            line_par_points.append([self.x_boundaries[0], y_row])
            line_par_points.append([self.x_boundaries[1], y_row])

            self.circles.append(circle_pair)
            self.lines.append(line_par_points)

            y_row += 25
    
    def draw(self):
        for circle_pair, line_points, code in zip(self.circles, self.lines, self.genome):
            draw.line(self.screen, self.colour_map.get(code), line_points[0], line_points[1], width=3)
            draw.circle(self.screen, (255, 255, 255), circle_pair[0], 10)
            draw.circle(self.screen, (255, 255, 255), circle_pair[1], 10)
    
    def update(self):
        # TODO: synchronised movement
        # speed = 10
        # for circle_pair, line_points in zip(self.circles, self.lines):
        #     circle_pair[0][0] += speed
        #     circle_pair[1][0] += speed

        #     for circle
        pass

    @staticmethod
    def get_genome(filename: str) -> str:
        if ".moura" not in filename:
            return None
        with open(filename, "r") as dna_sample:
            return dna_sample.read()[:20]

    @staticmethod
    def match(sample1, sample2) -> float:
        return lv.ratio(sample1.genome, sample2.genome)
