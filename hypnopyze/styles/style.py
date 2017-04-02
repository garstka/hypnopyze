from hypnopyze.notes import *
from hypnopyze.instruments import *
from hypnopyze.drums import CHANNEL_DRUMS
from hypnopyze.scales.blueprint import *


# General parameters for music generation.
class Style:
    def __init__(self):
        #
        # instruments
        #

        self.use_lead = True
        self.use_rhythm = False
        self.use_drums = True

        self.lead = AcousticGrandPiano
        self.rhythm = AcousticBass

        #
        # beats per bar
        #

        self.base_beats_per_bar = 5  # base beats per bar

        self.resolution = 4  # multiplier

        #
        # key
        #

        self.key = E
        self.scale = MajorScale

        # pattern octave shifts mid-song

        self.octave_shift_prob = 0.5
        self.octave_shifts = [-1]

        self.octave_shift_rhythm = False

        #
        # speed and structure
        #

        self.bpm = 120
        self.bar_group = 4

        # self.silent_bars_at_end = 0.5

        #
        # velocity perturbation per instrument
        #

        self.lead_perturb = 20
        self.rhythm_perturb = 10

        self.bass_perturb = 20
        self.hi_ride_perturb = 40
        self.mixed_perturb = 10

        #
        # channels
        #

        self.lead_channel = 0
        self.rhythm_channel = 1
        self.drums_channel = CHANNEL_DRUMS

    # Returns the actual beats per bar.
    @property
    def beats_per_bar(self):
        return self.base_beats_per_bar * self.resolution

    # Returns the number of bars per minute.
    @property
    def bars_per_minute(self):
        return self.bpm / self.beats_per_bar

    # Returns the array [instrument_channel_0, instrument_channel_1, ...]
    @property
    def instruments_per_channel(self):
        return [self.lead, self.rhythm]
