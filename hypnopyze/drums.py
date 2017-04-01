from hypnopyze.patterns import *
from hypnopyze.sequencer import *

AcousticBassDrum = 35
BassDrum1 = 36
SideStick = 37
AcousticSnare = 38
HandClap = 39
ElectricSnare = 40
LowFloorTom = 41
ClosedHiHat = 42
HighFloorTom = 43
PedalHiHat = 44
LowTom = 45
OpenHiHat = 46
LowMidTom = 47
HiMidTom = 48
CrashCymbal1 = 49
HighTom = 50
RideCymbal1 = 51
ChineseCymbal = 52
RideBell = 53
Tambourine = 54
SplashCymbal = 55
Cowbell = 56
CrashCymbal2 = 57
Vibraslap = 58
RideCymbal2 = 59
HiBongo = 60
LowBongo = 61
MuteHiConga = 62
OpenHiConga = 63
LowConga = 64
HighTimbale = 65
LowTimbale = 66
HighAgogo = 67
LowAgogo = 68
Cabasa = 69
Maracas = 70
ShortWhistle = 71
LongWhistle = 72
ShortGuiro = 73
LongGuiro = 74
Claves = 75
HiWoodBlock = 76
LowWoodBlock = 77
MuteCuica = 78
OpenCuica = 79
MuteTriangle = 80
OpenTriangle = 81

CHANNEL_DRUMS = 9


class Drummer:
    # - beats_per_bar - how many beats in a bar, i.e. the resolution
    # - bar_group - arbitrary group of bars
    # - start_time - starting time of the first bar
    def __init__(self,
                 beats_per_bar: int = 5,
                 bar_group: int = 4,
                 time_step: int = 1,
                 start_time: int = 0):
        self.beats_per_bar = beats_per_bar
        self.bar_group = bar_group
        self.time_step = time_step
        self.__t = start_time if start_time >= 0 else 0

        # bass - beat or timing element with basic pulse patterns
        self.seq_bass = Sequencer(beats_per_bar, time_step, 20)
        self.seq_bass.channel = CHANNEL_DRUMS
        self.seq_bass.time = start_time

        # stick - intro
        self.seq_stick = Sequencer(beats_per_bar, time_step, 10)
        self.seq_stick.channel = CHANNEL_DRUMS
        self.seq_stick.time = start_time

        # snare - regular accents, fills
        self.seq_snare = Sequencer(beats_per_bar, time_step, 10)
        self.seq_snare.channel = CHANNEL_DRUMS
        self.seq_snare.time = start_time

        # tom - fills and solos
        self.seq_toms = Sequencer(beats_per_bar, time_step, 40)
        self.seq_toms.channel = CHANNEL_DRUMS
        self.seq_toms.time = start_time

        # ride - constant-rhythm pattern
        self.seq_ride = Sequencer(beats_per_bar, time_step, 40)
        self.seq_ride.channel = CHANNEL_DRUMS
        self.seq_ride.time = start_time

        # hi-hat - similar to ride, not at the same time
        self.seq_hi_hat = Sequencer(beats_per_bar, time_step, 40)
        self.seq_hi_hat.channel = CHANNEL_DRUMS
        self.seq_hi_hat.time = start_time

        # crash - accent markers, major changes
        self.seq_crash = Sequencer(beats_per_bar, time_step, 40)
        self.seq_crash.channel = CHANNEL_DRUMS
        self.seq_crash.time = start_time

        # mixed, sequential
        self.seq_mixed = Sequencer(beats_per_bar, time_step, 40)
        self.seq_mixed.channel = CHANNEL_DRUMS
        self.seq_mixed.time = start_time

    def play(self, bar_groups):

        # Quick pattern
        def p(m_bpb, i, name=None, v=None):
            return Pattern(name if name else "",
                           m_bpb,
                           i,
                           v if v else [],
                           [],
                           True)

        # bass - beat or timing element with basic pulse patterns
        patterns_bass = []

        base = 5 * 2 * 2
        patt = [BassDrum1] * base
        patt[4] = -1
        patt[7] = -1
        # patterns_bass.append(p(base, patt))

        # stick - intro
        patterns_stick = []

        # snare - regular accents, fills
        patterns_snare = []

        # tom - fills and solos
        patterns_toms = []

        # ride - constant-rhythm pattern
        patterns_ride = []

        # hi-hat - similar to ride, not at the same time
        patterns_hi_hat = []

        # crash - accent markers, major changes
        patterns_crash = []

        # mixed - sequential
        patterns_mixed = []

        base = 10 * 2
        patt = [LowFloorTom, ElectricSnare] * 10
        patterns_mixed.append(p(base, patt))

        total_time = bar_groups * self.bar_group * self.time_step
        bass = self.seq_bass
        while bass.time < total_time:
            if not patterns_bass:
                break
            if not bass.compatible(patterns_bass[0]):
                print("Not compatible - bass")
                return

            bass.append(patterns_bass[0])

        mixed = self.seq_mixed
        while mixed.time < total_time:
            if not mixed.compatible(patterns_mixed[0]):
                print("Not compatible - mixed")
                return

            mixed.append(patterns_mixed[0])

    # Returns all the tracks
    @property
    def tracks(self):
        return [l for l in [self.seq_bass.notes,
                            self.seq_stick.notes,
                            self.seq_snare.notes,
                            self.seq_toms.notes,
                            self.seq_ride.notes,
                            self.seq_hi_hat.notes,
                            self.seq_crash.notes,
                            self.seq_mixed.notes] if l]
