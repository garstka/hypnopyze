from math import ceil

from hypnopyze.patterns import *
import numpy as np


# For creating sequences of notes.
class Sequencer:
    # - beats_per_bar - how many beats in a bar (maximum pattern resolution)
    # - time_step - each beat will take time_step MIDI beats
    # - perturb_velocity_cap - randomly perturbs the base velocities by +- this
    def __init__(self,
                 beats_per_bar: int,
                 time_step: int = 1,
                 perturb_velocity_cap: int = 0):

        # The midi channel to use. Any change takes effect from the next bar.
        self.channel = 0

        # How many beats in a bar to allow (maximum pattern resolution)
        self.beats_per_bar = beats_per_bar

        # How much to randomly perturb velocities
        self.perturb_velocity_cap = perturb_velocity_cap

        # MIDI beats per one time step
        self.__time_step = time_step if time_step > 0 else 1

        # The output notes
        self.__notes = []

        # Current time
        self.__t = 0

    # Returns the current time point.
    @property
    def time(self):
        return self.__t

    # Sets the current time point.
    @time.setter
    def time(self, value):
        self.__t = value if value >= 0 else 0

    # Returns the generated notes.
    @property
    def notes(self):
        return self.__notes

    # Returns true, if the pattern is compatible
    def compatible(self, pattern: Pattern):
        # if bad pattern
        if not pattern:
            return False

        # if pattern resolution is too high
        if self.beats_per_bar < pattern.min_beats_per_bar:
            return False

        # should be fine
        return True

    # If compatible, returns how much the pattern will be scaled up.
    #
    # Example 1:
    # e.g. beats_per_bar = 16
    #      pattern.min_beats_per_bar = 4
    #
    # time_scale = beats_per_bar // p.mbpb = 4
    #
    # also, can be be repeated, as beats_per_bar % p.mbpb == 0
    #
    # Example 2:
    # e.g. beats_per_bar = 20
    #      pattern.min_beats_per_bar = 3
    #
    # time_scale = beats_per_bar // p.mbpb = 6
    #
    # shouldn't be repeated, as beats_per_bar % p.mbpb != 0
    def time_scale(self, pattern: Pattern) -> int:
        return self.beats_per_bar // pattern.min_beats_per_bar

    # Returns true, if the pattern can be looped at this time scale,
    # see time_scale().
    def repeatable(self, pattern: Pattern) -> bool:
        return pattern.repeatable \
               and self.beats_per_bar % pattern.min_beats_per_bar == 0

    # If compatible, returns the number of bars the pattern will take up.
    def bar_count(self, pattern: Pattern) -> int:
        return int(ceil(self.time_scale(pattern) * pattern.beats
                        / self.beats_per_bar))

    # Appends the pattern at the current time point, if it's compatible.
    def append(self, pattern: Pattern) -> bool:

        if not self.compatible(pattern):
            print("Pattern is not compatible")
            return False

        time_scale = self.time_scale(pattern)
        bar_count = self.bar_count(pattern)
        perturb_range = list(range(-abs(self.perturb_velocity_cap),
                                   abs(self.perturb_velocity_cap)))
        perturb_range_len = len(perturb_range)
        p = pattern
        t = self.__t
        full_step = self.__time_step * time_scale
        for (index, velocity, duration) in p.ivd:

            # ignore silence
            if is_silence(index):
                t += full_step  # update the time
                continue

            # perturb the velocity if required
            if perturb_range:
                velocity += perturb_range[
                    np.random.binomial(perturb_range_len - 1,
                                       0.5)]

                velocity = max(0, min(velocity, MAX_VELOCITY))

            # correct the duration given scale
            duration *= full_step

            # append the note
            self.__notes.append([[t, index, velocity, duration],
                                 self.channel])

            # update the time
            t += full_step

        self.__t += self.beats_per_bar * bar_count * self.__time_step

        return True
