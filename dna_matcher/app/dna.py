"""Module for dna analysis related class and functions."""

import Levenshtein as lv


class DNA:
    """DNA class."""

    def __init__(self, file: str):
        self.genome = DNA.get_genome(file)
        if self.genome is None:
            raise ValueError(f"{file} is not a DNA sample.")

    @staticmethod
    def get_genome(filename: str) -> str:
        if ".moura" not in filename:
            return None
        with open(filename, "r") as dna_sample:
            return dna_sample.read()
    
    @staticmethod
    def match(sample1: DNA, sample2: DNA) -> float:
        return lv.ratio(sample1.genome, sample2.genome)
