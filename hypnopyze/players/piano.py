from hypnopyze.sequencer import *
from hypnopyze.instruments import *
from hypnopyze.styles.manager import *


class PianoPlayer:
    # - beats_per_bar - how many beats in a bar, i.e. the resolution
    # - bar_group - arbitrary group of bars
    # - start_time - starting time of the first bar
    def __init__(self,
                 start_time: int = 0):

        style = StyleManager().style

        self.beats_per_bar = style.beats_per_bar
        self.bar_group = style.bar_group

        self.__seq = Sequencer(self.beats_per_bar, style.lead_perturb)
        self.__seq.channel = style.lead_channel
        self.__seq.time = start_time

    def play(self, bar_groups):

        sm = StyleManager()
        prng = sm.prng

        collection = sm.pattern_collection.patterns("lead")
        collection_size = len(collection)

        if not collection:
            print("Collection empty")
            return

        def rand_pattern():
            return collection[prng.choice(collection_size)]

        total_time = bar_groups * self.bar_group * self.beats_per_bar
        seq = self.__seq
        while seq.time < total_time:
            pattern = rand_pattern()
            if not seq.compatible(pattern):
                print("Not compatible")
                return

            seq.append(pattern)

    # Returns all the tracks
    @property
    def tracks(self):
        return [l for l in [self.__seq.notes] if l]
