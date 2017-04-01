from hypnopyze.patterns.builder import *
from hypnopyze.instruments import *
from hypnopyze.drums import *
from hypnopyze.styles.manager import *


# Clears the current style
def set_style_empty(bpm):
    style = Style()
    style.bpm = bpm

    sm = StyleManager()
    sm.pattern_collection.clear()
    sm.style = style


# Generates a pattern set for the 5/4 time signature. Returns the
# corresponding style
def set_style_54():
    sm = StyleManager()
    collection = sm.pattern_collection

    style = Style()

    style.use_lead = True
    # style.use_rhythm = False
    style.use_drums = True

    style.lead = BrightAcousticPiano
    # style.rhythm = AcousticBass

    style.base_beats_per_bar = 5

    style.resolution = 4

    style.key = E

    style.bpm = 240
    style.bar_group = 4

    sm.style = style

    #
    # add patterns
    #

    b = PatternBuilder()

    instrument = "lead"

    def build():
        if b.build() == 0:
            print("Unable to build patterns")
        else:
            collection.add_patterns(instrument, b.patterns)
            b.patterns.clear()

    b.use_directions = True
    b.prng = sm.prng

    b.num_walks = 20
    b.real_time = False
    b.repeat = True
    b.key = D

    # b.scale = [A, C, D, E, G]

    b.bars = 1
    b.i = [STAY, STAY, STAY, ROOT_DOWN, STAY]
    b.v = [H, M, M, M, M]
    b.d = []
    build()

    b.bars = 1
    b.real_time = True
    b.i = [STAY, NEXT, NEXT, NEXT, NEXT_ROOT]
    b.v = [H, M, M, M, H]
    b.d = []
    build()

    #
    #
    # add patterns for drums
    #
    #

    b.use_walks = False

    #
    # bass
    #

    instrument = "drums_bass"
    b.real_time = True
    b.use_directions = False

    b.bars = 1
    b.i = [BassDrum1, BassDrum1, S, S, S]

    #
    # snare
    #

    instrument = "drums_snare"
    b.real_time = True

    b.bars = 1
    b.i = [S, S, S, ElectricSnare, S]

    #
    # hi-hat / ride
    #

    instrument = "drums_hiride"

    b.bars = 1
    b.i = [ClosedHiHat, S, PedalHiHat, S, ClosedHiHat, S, PedalHiHat, S,
           OpenHiHat, S]
    build()

    b.i = [RideCymbal2, S, RideCymbal2, S, RideCymbal2, S, RideBell, RideBell,
           CrashCymbal1, S]

    #
    # mixed, sequential
    #

    instrument = "drums_mixed"
    b.real_time = False

    b.bars = 2
    b.i = [LowFloorTom, ElectricSnare] * 10

    # for testing bar lengths:
    # b.i = []
    # b.i.append(LowFloorTom)
    # b.i.extend(([0] * 18))
    # b.i.append(ElectricSnare)
    build()