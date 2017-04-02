from hypnopyze.drums import *
from hypnopyze.patterns import *
from hypnopyze.sequencer import *
from hypnopyze.styles.manager import StyleManager


class Drummer:
    # - beats_per_bar - how many beats in a bar, i.e. the resolution
    # - bar_group - arbitrary group of bars
    # - start_time - starting time of the first bar
    def __init__(self,
                 start_time: int = 0):

        style = StyleManager().style
        self.beats_per_bar = style.beats_per_bar
        self.bar_group = style.bar_group

        # bass - beat or timing element with basic pulse patterns
        self.__seq_bass = Sequencer(self.beats_per_bar, style.bass_perturb)
        self.__seq_bass.channel = CHANNEL_DRUMS
        self.__seq_bass.time = start_time

        # ride - constant-rhythm pattern
        # & hi-hat - similar to ride, not at the same time
        # & crash - accent markers, major changes
        self.__seq_hi_ride = Sequencer(self.beats_per_bar,
                                       style.hi_ride_perturb)
        self.__seq_hi_ride.channel = CHANNEL_DRUMS
        self.__seq_hi_ride.time = start_time

        # mixed, sequential
        # snare - regular accents, fills
        # & tom - fills and solos
        self.__seq_mixed = Sequencer(self.beats_per_bar, style.mixed_perturb)
        self.__seq_mixed.channel = CHANNEL_DRUMS
        self.__seq_mixed.time = start_time

    def play(self, bar_groups):

        sm = StyleManager()
        prng = sm.prng
        collection = sm.pattern_collection

        patterns = [collection.patterns("drums_bass"),
                    collection.patterns("drums_mixed"),
                    collection.patterns("drums_hi_ride")]

        # for i, p in enumerate(patterns):
        #    print("Drum collection ", i, ": ", len(p))

        seqs = [self.__seq_bass,
                self.__seq_mixed,
                self.__seq_hi_ride]

        total_time = bar_groups * self.bar_group * self.beats_per_bar
        for i in range(0, len(patterns)):

            pattern_list = patterns[i]
            seq = seqs[i]

            pattern_count = len(pattern_list)
            if pattern_count == 0:
                print("Drum collection ", i, " is empty.")
                continue

            def rand():  # random pattern
                return pattern_list[prng.choice(pattern_count)]

            while seq.time < total_time:
                pattern = rand()

                if not seq.compatible(pattern):
                    print("Incompatible pattern encountered.")
                    seq.time = seq.time + self.beats_per_bar
                    continue

                seq.append(pattern)

    # Returns all the tracks
    @property
    def tracks(self):
        return [l for l in [self.__seq_bass.notes,
                            self.__seq_hi_ride.notes,
                            self.__seq_mixed.notes] if l]
