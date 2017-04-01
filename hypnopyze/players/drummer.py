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
        self.beats_per_bar = style.beats_per_bar_given_res(style.drums_res)
        self.bar_group = style.bar_group
        self.time_step = style.time_step_given_res(style.drums_res)
        self.__t = start_time if start_time >= 0 else 0

        # bass - beat or timing element with basic pulse patterns
        self.seq_bass = Sequencer(self.beats_per_bar, self.time_step,
                                  style.bass_perturb)
        self.seq_bass.channel = CHANNEL_DRUMS
        self.seq_bass.time = start_time

        # stick - intro
        self.seq_stick = Sequencer(self.beats_per_bar, self.time_step,
                                   style.stick_perturb)
        self.seq_stick.channel = CHANNEL_DRUMS
        self.seq_stick.time = start_time

        # snare - regular accents, fills
        self.seq_snare = Sequencer(self.beats_per_bar, self.time_step,
                                   style.snare_perturb)
        self.seq_snare.channel = CHANNEL_DRUMS
        self.seq_snare.time = start_time

        # tom - fills and solos
        self.seq_toms = Sequencer(self.beats_per_bar, self.time_step,
                                  style.toms_perturb)
        self.seq_toms.channel = CHANNEL_DRUMS
        self.seq_toms.time = start_time

        # ride - constant-rhythm pattern
        # & hi-hat - similar to ride, not at the same time
        self.seq_hi_ride = Sequencer(self.beats_per_bar, self.time_step,
                                     style.ride_perturb)
        self.seq_hi_ride.channel = CHANNEL_DRUMS
        self.seq_hi_ride.time = start_time

        # crash - accent markers, major changes
        self.seq_crash = Sequencer(self.beats_per_bar, self.time_step,
                                   style.crash_perturb)
        self.seq_crash.channel = CHANNEL_DRUMS
        self.seq_crash.time = start_time

        # mixed, sequential
        self.seq_mixed = Sequencer(self.beats_per_bar, self.time_step,
                                   style.mixed_perturb)
        self.seq_mixed.channel = CHANNEL_DRUMS
        self.seq_mixed.time = start_time

    def play(self, bar_groups):

        sm = StyleManager()
        prng = sm.prng
        collection = sm.pattern_collection
        patterns_bass = collection.patterns("drums_bass")
        patterns_mixed = collection.patterns("drums_mixed")

        def rand_bass():
            return patterns_bass[prng.choice(len(patterns_bass))]

        def rand_mixed():
            return patterns_mixed[prng.choice(len(patterns_mixed))]

        total_time = bar_groups * self.bar_group * \
                     self.beats_per_bar * self.time_step
        
        bass = self.seq_bass
        while bass.time < total_time:
            if not patterns_bass:
                print("drums_bass collection empty")
                break
            pattern = rand_bass()
            if not bass.compatible(pattern):
                print("Not compatible - bass")
                return

            bass.append(pattern)

        mixed = self.seq_mixed
        while mixed.time < total_time:
            if not patterns_mixed:
                print("drums_mixed collection empty")
                break
            pattern = rand_mixed()
            if not mixed.compatible(pattern):
                print("Not compatible - mixed")
                return

            mixed.append(pattern)

    # Returns all the tracks
    @property
    def tracks(self):
        return [l for l in [self.seq_bass.notes,
                            self.seq_stick.notes,
                            self.seq_snare.notes,
                            self.seq_toms.notes,
                            self.seq_hi_ride.notes,
                            self.seq_crash.notes,
                            self.seq_mixed.notes] if l]
