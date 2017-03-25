from collections import defaultdict
from hypnopyze.scales import ScaleWalker
from hypnopyze.notes import *

# special pattern elements

SILENCE = -256
S = SILENCE


# Returns true, if the note represents silence.
def is_silence(note):
    return not (0 <= note <= MAX_NOTE)

# velocities

L = 30
M = 70
H = 120
MAX_VELOCITY = 127
DEFAULT_VELOCITY = MAX_VELOCITY


# A sequence of offsets within a scale / sounds to be played.
class Pattern:

    # - name - the pattern name
    # - beats_per_bar - minimum compatible beats per bar (minimum resolution)
    # - pattern - a sequence of integers (offsets or sounds)
    # - velocity - base sound velocity
    # - duration - each sound duration
    def __init__(self, name: str, min_beats_per_bar: int,
                 indices: [int], velocity: [int],
                 duration: [int], repeatable: bool = True):
        self.__name = name
        self.__min_beats_per_bar = min_beats_per_bar
        self.__indices = indices
        self.__repeatable = repeatable

        pattern_len = len(indices)
        if len(velocity) == pattern_len:
            self.__velocity = velocity
        else:
            self.__velocity = pattern_len * [DEFAULT_VELOCITY]

        if len(duration) == pattern_len:
            self.__duration = duration
        else:
            self.__duration = pattern_len * [1]

    # Returns the exact same pattern, but using sounds (as opposed
    # to indices  within a scale), by using the scale walker.
    def sound_pattern_from_this_walk(self, scale_walker: ScaleWalker):
        new_indices = []
        for i in self.__indices:
            if is_silence(i):
                new_indices.append(i)
                continue
            scale_walker.walk(i)
            new_indices.append(scale_walker.current().midi_note())

        return Pattern(self.__name, self.__min_beats_per_bar, new_indices,
                       self.__velocity, self.__duration)

    # Returns the length of the pattern in beats.
    def beats(self):
        return len(self.__indices)

    # Returns the minimum number of beats per bar.
    def min_beats_per_bar(self):
        return self.__min_beats_per_bar

    # Returns the indices.
    def indices(self):
        return self.__indices

    # Returns the velocity for each sound.
    def velocity(self):
        return self.__velocity

    # Returns the velocity for each sound.
    def duration(self):
        return self.__duration

    # Returns the pattern name.
    def name(self):
        return self.__name

    # Is the pattern repeatable at its original time scale.
    def repeatable(self):
        return self.__repeatable

    # Checks if valid
    def __bool__(self):
        return self.beats() > 0

    def __hash__(self):
        return self.__indices.__hash__()


# A collection of patterns, grouped by instruments.
class PatternCollection:

    def __init__(self):
        self.__patterns = defaultdict(lambda: set())

    # Add some patterns
    def add_patterns(self, instrument: str, patterns: [Pattern]):
        self.__patterns[instrument].update(*patterns)

    # Returns all available patterns for this instrument
    def patterns(self, instrument: str):
        return self.__patterns[instrument]
