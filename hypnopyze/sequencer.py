import random
from math import ceil
from hypnopyze.patterns import *
from hypnopyze.notes import *


# For creating sequences of notes.
class Sequencer:

    # Constructs from:
    # - beats_per_bar - how many beats in a bar (maximum pattern resolution)
    # - time_step - each beat will take time_step MIDI beats
    # - max_velocity_offset - randomly perturbs the base velocities by +- this
    def __init__(self, beats_per_bar, time_step: int = 1,
                 perturb_velocity_cap: int = 0):
        self.__channel = 0
        self.__beats_per_bar = beats_per_bar
        self.__time_step = time_step if time_step > 0 else 1
        self.__perturb_velocity_cap = perturb_velocity_cap
        self.__notes = []
        self.__t = 0
        self.__relative = False
        self.__relative_to = 0

    # Moves the next bar's position to another time point.
    def set_time(self, time):
        self.__t = time if time >= 0 else 0

    # Returns the current time.
    def time(self):
        return self.__t

    # Sets a different MIDI channel. This will take effect
    # starting from the next bar.
    def set_channel(self, channel: int):
        self.__channel = channel

    # Sets the next pattern's indices to be treated as relative to this note.
    # def set_relative(self, note: Note):
    #    self.__relative = True
    #    self.__relative_to = note.midi_note()

    # Returns true, if the pattern is compatible
    def compatible(self, pattern: Pattern):
        # if bad pattern
        if not pattern:
            return False

        # if pattern resolution is too high
        if self.__beats_per_bar < pattern.min_beats_per_bar():
            return False

        # should be fine
        return True

    # If compatible, returns how much the pattern will be scaled up.
    #
    # Example 1:
    # e.g. beats_per_bar = 16
    #      pattern.min_beats_per_bar() = 4
    #
    # time_scale = beats_per_bar // p.mbpb = 4
    #
    # can be be repeated, as beats_per_bar % p.mbpb == 0
    #
    # Example 2:
    # e.g. beats_per_bar = 20
    #      pattern.min_beats_per_bar() = 3
    #
    # time_scale = beats_per_bar // p.mbpb = 6
    #
    # shouldn't be repeated, as beats_per_bar % p.mbpb != 0
    def time_scale(self, pattern: Pattern) -> int:
        return self.__beats_per_bar // pattern.min_beats_per_bar()

    # Returns true, if the pattern can be looped at this time scale,
    # see time_scale().
    def repeatable(self, pattern: Pattern) -> bool:
        return pattern.repeatable() and self.__beats_per_bar % \
                                        pattern.min_beats_per_bar() == 0

    # If compatible, returns the number of bars a pattern will take up.
    def bar_count(self, pattern: Pattern) -> int:
        return int(ceil(self.time_scale(pattern) * pattern.beats() /
                        self.__beats_per_bar))

    # Append the pattern, if it's compatible
    def append(self, pattern: Pattern) -> bool:
        if not self.compatible(pattern):
            print("Pattern is not compatible")
            return False

        time_scale = self.time_scale(pattern)
        bar_count = self.bar_count(pattern)
        perturb_range = range(-self.__perturb_velocity_cap,
                              self.__perturb_velocity_cap)
        p = pattern
        t = self.__t
        full_step = self.__time_step * time_scale
        for (index, velocity, duration)\
                in zip(p.indices(), p.velocity(), p.duration()):

            # ignore silence
            if is_silence(index):
                t += full_step  # update the time
                continue

            # convert to absolute note index if necessary
            # if self.__relative:
            #    index += self.__relative_to

            # perturb the velocity if required
            if perturb_range:
                velocity += random.choice(perturb_range)
                velocity = max(0, min(velocity, MAX_VELOCITY))

            # correct the duration given scale
            duration *= full_step

            # append the note
            print(self.__notes)
            self.__notes.append([[t, index, velocity, duration],
                                 self.__channel])

            # update the time
            t += full_step

        self.__t += self.__beats_per_bar * bar_count * self.__time_step

        return True

    # Returns the generated notes.
    def notes(self):
        return self.__notes
