from collections import defaultdict
from numpy.random import RandomState

from hypnopyze.scales import *

# special pattern elements

SILENCE = -256
S = SILENCE


# Returns true, if the note represents silence.
def is_silence(note):
    return not (0 <= note <= MAX_NOTE)


# Returns true, if the index represents silence in a scale walk.
def is_silence_walk(index):
    return index == SILENCE


# Returns true, if the note represents silence in a list of directions.
def is_silence_directions(index):
    return not STAY <= index <= NEXT_DOWN


# directions for generating patterns using scales
# see Pattern.walk_from_these_directions

STAY = 0  # play the previous note again
ROOT = 1  # play the current octave's root note
NEXT_ROOT = 2  # play the next octave's root note
PREV_ROOT = 3  # play the previous octave's root note

NEXT = 4  # play the next note
PREV = 5  # play the previous note

UP = 6  # play random in (current, NEXT_ROOT), closer to current are more likely
DOWN = 7  # play random in (ROOT, current), closer to current are more likely

ROOT_DOWN = 8  # play random in (PREV_ROOT, ROOT), closer to ROOT are more likely

PREV_UP = 9  # switch to PREV_ROOT -> UP
PREV_DOWN = 10  # switch to PREV_ROOT -> ROOT_DOWN

NEXT_UP = 11  # switch to NEXT_ROOT -> UP
NEXT_DOWN = 12  # switch to NEXT_ROOT -> ROOT_DOWN

# velocities

L = 30  # light
M = 70  # medium
H = 120  # hard
MAX_VELOCITY = 127
DEFAULT_VELOCITY = MAX_VELOCITY

# durations

DEFAULT_DURATION = 1


# A sequence of offsets within a scale / sounds to be played.
class Pattern:
    # - min_beats_per_bar - minimum compatible beats per bar
    # (minimum resolution)
    # - indices - a sequence of integers (offsets or sounds)
    # - velocity - velocity for each note
    # - duration - duration for each note
    # - real_time - if true, pattern won't be upscaled to fit the entire bar,
    # if the target has more beats per bar than min_beats_per_bar
    def __init__(self,
                 name: str,  # the pattern name
                 min_beats_per_bar: int,
                 indices: [int],
                 velocity: [int],
                 duration: [int],
                 repeatable: bool = True,
                 real_time: bool = False):

        # the pattern name
        self.name = name

        # the minimum number of beats per bar for this pattern to work
        self.min_beats_per_bar = min_beats_per_bar

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
        #
        # Example:
        # for
        # [CURRENT, UP, UP, DOWN, DOWN, NEXT_ROOT, PREV_ROOT]
        # scale_size = 5
        # one possibility would be:
        # absolute offsets: [0, 1, 3, 2, 1, 4, 0]
        # walk offsets: [0, 1, 2, -1, -1, 3, -4]

        if scale_size == 0:
            return None

        new_indices = []
        current_offset = 0

        def current_root():
            return current_offset - (current_offset % scale_size)

        def next_root():
            return current_root() + scale_size

        def prev_root():
            return current_root() - scale_size

        def rand(max_val):
            return abs(prng.binomial(2 * max_val, 0.5) - max_val)

        def rand_nonzero(max_val):
            result = 0
            while result == 0:
                result = rand(max_val)
            return result

        for i in self.indices:

            if i == PREV_UP:  # switch to PREV_ROOT -> UP
                current_offset = prev_root()
                i = UP
            elif i == PREV_DOWN:  # switch to PREV_ROOT -> ROOT_DOWN
                current_offset = prev_root()
                i = ROOT_DOWN
            elif i == NEXT_UP:  # switch to NEXT_ROOT -> UP
                current_offset = next_root()
                i = UP
            elif i == NEXT_DOWN:  # switch to NEXT_ROOT -> ROOT_DOWN
                current_offset = next_root()
                i = ROOT_DOWN

            if i == STAY:  # play the previous note again
                pass
            elif i == NEXT:  # play the next note
                current_offset += 1
            elif i == PREV:  # play the previous note
                current_offset -= 1
            elif i == UP:  # go up (staying within the same octave)

                top = next_root() - 1
                bottom = current_offset + 1
                if bottom > top:
                    return None  # can be fixed, perhaps

                off = rand_nonzero(top - bottom + 1)
                current_offset = bottom - 1 + off

            elif i == DOWN:  # go down (staying within the same octave)

                top = current_offset - 1
                bottom = current_root() + 1
                if bottom > top:
                    return None  # can be fixed, perhaps

                off = rand_nonzero(top - bottom + 1)
                current_offset = top + 1 - off

            elif i == ROOT:  # play the current root
                current_offset = current_root()
            elif i == PREV_ROOT:  # root note one octave below
                current_offset = prev_root()
            elif i == NEXT_ROOT:  # root note one octave above
                current_offset = next_root()
            elif i == ROOT_DOWN:  # play random in (PREV_ROOT, ROOT)

                top = current_root() - 1
                bottom = prev_root() + 1

                if bottom > top:
                    return None  # can be fixed, perhaps

                off = rand_nonzero(top - bottom + 1)
                current_offset = top + 1 - off

            else:
                new_indices.append(SILENCE)
                continue

            new_indices.append(current_offset)

        # convert absolute to relative offsets

        last_index = 0
        for i in range(0, len(new_indices)):
            this_index = new_indices[i]

            # ignore silence
            if is_silence_directions(this_index):
                continue

            new_indices[i] = this_index - last_index
            last_index = this_index

        return Pattern(self.name,
                       self.min_beats_per_bar,
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
                       self.min_beats_per_bar,
                       new_indices,
                       self.velocity,
                       self.duration,
                       self.repeatable,
                       self.real_time)

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


# A singleton collection of patterns, grouped by instruments.
class PatternCollection:
    __shared = defaultdict(lambda: [])

    def __init__(self):
        self.__patterns = self.__shared

    # Add some patterns
    def add_patterns(self, instrument, patterns: [Pattern]):
        self.__patterns[instrument].extend(patterns)

    # Returns all available patterns for this instrument
    def patterns(self, instrument):
        return self.__patterns[instrument]
