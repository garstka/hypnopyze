from hypnopyze.notes import E
from hypnopyze.instruments import BrightAcousticPiano, AcousticBass
from hypnopyze.drums import CHANNEL_DRUMS


# General parameters for music generation.
class Style:
    def __init__(self):
        #
        # instruments
        #

        self.use_lead = True
        self.use_rhythm = False
        self.use_drums = True

        self.lead = BrightAcousticPiano
        self.rhythm = AcousticBass

        #
        # beats per bar
        #

        self.base_beats_per_bar = 5  # base beats per bar

        # multipliers

        self.lead_res = 2
        self.rhythm_res = 4
        self.drums_res = 4

        #
        # key
        #

        self.key = E

        self.bpm = 120
        self.bar_group = 4

        #
        # velocity perturbation per instrument
        #

        self.lead_perturb = 20
        self.rhythm_perturb = 10

        self.bass_perturb = 20
        self.stick_perturb = 10
        self.snare_perturb = 10
        self.toms_perturb = 40
        self.ride_perturb = 40
        self.hi_hat_perturb = 40
        self.crash_perturb = 40
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
        return self.base_beats_per_bar * self.max_res

    # Returns the number of bars per minute.
    @property
    def bars_per_minute(self):
        return self.bpm / self.beats_per_bar

    # Returns the time step size for the given target resolution.
    def time_step_given_res(self, target_res):
        return self.max_res // target_res

    # Returns the target beats per bar for the given the target resolution.
    def beats_per_bar_given_res(self, target_res):
        return self.base_beats_per_bar * target_res

    # Maximum resolution for any instrument.
    @property
    def max_res(self):
        return max(self.lead_res, self.rhythm_res,
                   self.drums_res)
