from hypnopyze.sequencer import *
from hypnopyze.instruments import *


class PianoPlayer:
    # - beats_per_bar - how many beats in a bar, i.e. the resolution
    # - bar_group - arbitrary group of bars
    # - start_time - starting time of the first bar
    def __init__(self,
                 beats_per_bar: int = 5,
                 bar_group: int = 4,
                 time_step: int = 1,
                 instrument: int = AcousticGrandPiano,
                 start_time: int = 0):
        self.beats_per_bar = beats_per_bar
        self.bar_group = bar_group
        self.time_step = time_step
        self.__t = start_time if start_time >= 0 else 0

        self.seq = Sequencer(beats_per_bar, time_step, 20)
        self.seq.channel = 0
        self.seq.time = start_time

    def play(self, bar_groups):

        collection = PatternCollection().patterns("piano")
        collection_size = len(collection)
        prng = RandomState(75123481)

        def rand_pattern():
            return collection[prng.choice(collection_size)]

        total_time = bar_groups * self.bar_group * self.time_step
        seq = self.seq
        while seq.time < total_time:
            pattern = rand_pattern()
            if not seq.compatible(pattern):
                print("Not compatible")
                return

            seq.append(pattern)

    # Returns all the tracks
    @property
    def tracks(self):
        return [l for l in [self.seq.notes] if l]
