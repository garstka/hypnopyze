from collections import defaultdict
from hypnopyze.patterns.pattern import Pattern
from typing import List


# A collection of patterns, grouped by instruments.
class PatternCollection:
    def __init__(self):
        self.__patterns = defaultdict(lambda: [])

    # Add some patterns
    def add_patterns(self, instrument, patterns: List[Pattern]):
        self.__patterns[instrument].extend(patterns)

    # Returns all available patterns for this instrument
    def patterns(self, instrument):
        return self.__patterns[instrument]

    # Removes all patterns
    def clear(self):
        self.__patterns.clear()
