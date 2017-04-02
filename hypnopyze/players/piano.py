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

        self.__seq_lead = Sequencer(self.beats_per_bar, style.lead_perturb)
        self.__seq_lead.channel = style.lead_channel
        self.__seq_lead.time = start_time

        self.__seq_rhythm = Sequencer(self.beats_per_bar, style.rhythm_perturb)
        self.__seq_rhythm.channel = style.rhythm_channel
        self.__seq_rhythm.time = start_time

    def play(self, bar_groups):

        sm = StyleManager()
        style = sm.style
        prng = sm.prng

        collection = sm.pattern_collection

        is_rhythm = [False, True]
        patterns = [collection.patterns("lead"),
                    collection.patterns("rhythm")]

        seqs = [self.__seq_lead,
                self.__seq_rhythm]

        total_time = bar_groups * self.bar_group * self.beats_per_bar
        for i in range(0, len(patterns)):

            pattern_list = patterns[i]
            seq = seqs[i]

            pattern_count = len(pattern_list)
            if pattern_count == 0:
                print("Piano collection ", i, " is empty.")
                continue

            def rand():  # fetches a pattern
                chosen = pattern_list[prng.choice(pattern_count)]

                if is_rhythm[i] and not style.octave_shift_rhythm:
                    return chosen

                # perform an octave shift according to the probability
                do_octave_shift = prng.binomial(1, style.octave_shift_prob)
                if do_octave_shift and style.octave_shifts:
                    which_shift = prng.choice(len(style.octave_shifts))
                    chosen = chosen.octave_shifted(
                        style.octave_shifts[which_shift])

                return chosen

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
        return [l for l in [self.__seq_lead.notes,
                            self.__seq_rhythm.notes] if l]
