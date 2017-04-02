from numpy.random import RandomState
from hypnopyze.scales.walker import *
from hypnopyze.scales.directions import directions_to_walk
from math import ceil

# special pattern elements

SILENCE = -256
S = SILENCE


# Returns true, if the note represents silence.
def is_silence(note):
    return not (0 <= note <= MAX_NOTE)


# Returns true, if the index represents silence in a scale walk.
def is_silence_walk(index):
    return index == SILENCE


# velocities

L = 30  # light
M = 70  # medium
H = 120  # hard
MAX_VELOCITY = 127
DEFAULT_VELOCITY = MAX_VELOCITY

# durations

DEFAULT_DURATION = 1


# A sequence of indices:
#  - directions for building a scale walk, or
#  - a scale walk: offsets within a scale, or
#  - sounds to be played (usable for MIDI output)/
class Pattern:
    # - bars - how many bars the pattern represents
    # - indices - a sequence of integers (directions/offsets/sounds)
    # - velocity - velocity for each note
    # - duration - duration for each note
    # - real_time - if true, pattern won't be upscaled to fit the entire bar,
    # if the target has more beats per bar than min_beats_per_bar
    def __init__(self,
                 name: str,  # the pattern name
                 bars: int,
                 indices: [int],
                 velocity: [int],
                 duration: [int],
                 repeatable: bool = True,
                 real_time: bool = False):

        # the pattern name
        self.name = name

        # the bar count
        self.bars = bars

        # is the pattern repeatable at compatible time scales?
        self.repeatable = repeatable

        # should the pattern be scaled to fit a bar (False),
        # or played at the target tempo?
        self.real_time = real_time

        # integer indices (offsets or MIDI notes).
        self.__indices = tuple(indices)

        # velocity for each index (sound)
        self.__velocity = tuple(velocity)

        len_indices = len(self.__indices)

        if len(self.__velocity) != len_indices:
            self.__velocity = tuple(len_indices * [DEFAULT_VELOCITY])

        # duration for each index (sound)
        self.__duration = tuple(duration)

        if len(self.__duration) != len_indices:
            self.__duration = tuple(len_indices * [DEFAULT_DURATION])

    # Treats the indices as general directions for a walk, and
    # returns a pattern that uses offsets within a scale, for this scale
    # size.
    # May produce different results each time, as it uses a PRNG.
    # Returns None if the directions are invalid for a scale of this size,
    # or the imperfect algorithm failed (for now).
    def walk_from_these_directions(self, scale_size: int, prng: RandomState):

        new_indices = directions_to_walk(self.indices, scale_size, prng)

        return Pattern(self.name,
                       self.bars,
                       new_indices,
                       self.velocity,
                       self.duration,
                       self.repeatable,
                       self.real_time)

    # Returns the pattern using sounds, by walking a scale with the scale
    # walker.
    def sound_pattern_from_this_walk(self, scale_walker: ScaleWalker):

        new_indices = []
        for i in self.indices:

            # ignore silence
            if is_silence_walk(i):
                new_indices.append(i)
                continue

            scale_walker.walk(i)
            new_indices.append(scale_walker.current.midi_note)

        return Pattern(self.name,
                       self.bars,
                       new_indices,
                       self.velocity,
                       self.duration,
                       self.repeatable,
                       self.real_time)

    # If this is a sound pattern, returns the same pattern,
    # but octave-shifted.
    def octave_shifted(self, shift: int):

        new_indices = []
        for i in self.indices:

            # ignore silence
            if is_silence_walk(i):
                new_indices.append(i)
                continue

            new_indices.append(shift * BASE_NOTE_COUNT + i)

        return Pattern(self.name,
                       self.bars,
                       new_indices,
                       self.velocity,
                       self.duration,
                       self.repeatable,
                       self.real_time)

    # Returns the minimum compatible beats per bar (minimum resolution)
    @property
    def min_beats_per_bar(self):
        return int(ceil(self.beats / self.bars))

    # Returns the length of the pattern in beats.
    @property
    def beats(self) -> int:
        return len(self.__indices)

    # Returns the integer indices (offsets or MIDI notes).
    @property
    def indices(self):
        return self.__indices

    # Returns a velocity for each index.
    @property
    def velocity(self):
        return self.__velocity

    # Returns a duration for each index.
    @property
    def duration(self):
        return self.__duration

    # Returns zip(indices, velocity, duration)
    @property
    def ivd(self):
        return zip(self.__indices, self.__velocity, self.__duration)

    # Checks if the pattern is valid.
    @property
    def good(self):
        return self.beats > 0

    def __bool__(self):
        return self.good

    def __hash__(self):
        return hash(self.indices)
