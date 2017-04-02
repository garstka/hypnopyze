from hypnopyze.patterns.builder import PatternBuilder
from hypnopyze.scales.directions import *
from hypnopyze.patterns.pattern import *
from hypnopyze.drums import *
from hypnopyze.instruments import *


# More lead patterns
def build_lead_ext4(builder: PatternBuilder):
    b = builder

    b.instrument = "lead"
    b.use_directions = True
    b.base_octave = DEFAULT_OCTAVE

    # b.bars = 1
    # b.name = "up down burst"
    # b.i = [ROOT, NEXT_DOWN, ROOT_DOWN, S, S, NEXT_UP, NEXT_DOWN]
    # b.v = []
    # b.d = [1] * 6 + [4]
    #  b.repeat = False
    #
    # b.build_and_register()

    # b.bars = 1
    # b.name = "up burst"
    # b.i = [ROOT, NEXT, NEXT_DOWN, NEXT_ROOT, S, S, ROOT, S, ROOT, S]
    #  b.v = []
    #  b.d = [1] * 6 + [2] * 4
    #   b.repeat = False
    #   b.real_time = True
    #
    # b.build_and_register()

    b.bars = 1
    b.name = "t4"
    b.i = [STAY, NEXT, S, ROOT_DOWN, NEXT, PREV_ROOT]
    b.v = []
    b.d = [1, 3, 1, 1, 1, 3]
    b.repeat = False
    b.real_time = False

    b.build_and_register()

    b.bars = 1
    b.name = "h1"
    b.i = [STAY, STAY, S, STAY, ROOT_DOWN]
    b.v = []
    b.d = []
    b.repeat = True
    b.real_time = True

    # b.build_and_register()

    # b.bars = 1
    # b.name = "bad1"
    # b.i = [STAY, NEXT, NEXT, NEXT_ROOT, PREV, PREV, PREV, PREV, NEXT_ROOT,
    # ROOT_DOWN]
    # b.v = []
    # b.d = []
    # b.repeat = True
    # b.real_time = True

    # b.build_and_register()


    b.bars = 1
    b.name = "bad1_a"
    b.i = [STAY, NEXT, NEXT, NEXT_ROOT, PREV]
    b.v = []
    b.d = []
    b.repeat = True
    b.real_time = True

    b.build_and_register()

    b.bars = 1
    b.name = "bad1_b"
    b.i = [NEXT_DOWN, PREV, PREV, NEXT_ROOT, ROOT_DOWN]
    b.v = []
    b.d = []
    b.repeat = True
    b.real_time = True

    b.build_and_register()

    b.bars = 1
    b.name = "revvy"
    b.i = [STAY, PREV, DOWN, DOWN, PREV_ROOT]
    b.v = []
    b.d = []
    b.repeat = True
    b.real_time = True

    b.build_and_register()


# Builds and registers basic rhythm patterns.
def build_rhythm_ext54(builder: PatternBuilder):
    b = builder

    b.instrument = "rhythm"
    b.use_directions = True
    b.base_octave = DEFAULT_OCTAVE - 1

    b.bars = 2
    b.name = "downwards"
    b.i = [ROOT_DOWN, STAY, STAY, STAY, STAY, DOWN, PREV, ROOT, S, S]
    b.v = []
    b.d = []
    b.repeat = True
    b.real_time = True

    b.build_and_register()

    # b.bars = 2
    # b.name = "downwards"
    # b.i = [ROOT_DOWN, PREV, NEXT, PREV, NEXT, PREV, NEXT, NEXT_ROOT,
    #       PREV_ROOT, S]
    # b.v = []
    # b.d = []
    # b.repeat = True
    # b.real_time = True

    # b.build_and_register()

    b.bars = 1
    b.name = "downwards_a"
    b.i = [ROOT_DOWN, PREV, NEXT, PREV, NEXT]
    b.v = []
    b.d = []
    b.repeat = True
    b.real_time = True

    b.build_and_register()

    b.bars = 1
    b.name = "downwards_b"
    b.i = [ROOT_DOWN, NEXT, NEXT_ROOT, PREV_ROOT, S]
    b.v = []
    b.d = []
    b.repeat = True
    b.real_time = True

    b.build_and_register()


# More bass
def build_drums_bass_ext54(builder: PatternBuilder):
    b = builder

    b.use_directions = False
    b.use_walks = False

    b.instrument = "drums_bass"

    b.bars = 1
    b.i = [BassDrum1, BassDrum1, BassDrum1, BassDrum1, S]
    b.v = [H, M, M, M, M]
    b.d = []
    b.real_time = True
    b.repeat = True

    b.build_and_register()


# Builds and registers basic hi-hat / ride patterns.
def build_drums_hi_ride_ext54(builder: PatternBuilder):
    b = builder

    b.use_directions = False
    b.use_walks = False

    b.instrument = "drums_hi_ride"

    b.bars = 2
    b.name = "bhi_nocrash"
    b.i = [ClosedHiHat, S, PedalHiHat, S, ClosedHiHat, S, PedalHiHat, S,
           ClosedHiHat, S]
    b.v = []
    b.d = []
    b.repeat = True
    b.real_time = True

    b.build_and_register()

    b.bars = 1
    b.name = "bride_nocrash"
    b.i = [RideCymbal1, S, RideCymbal1, S, RideCymbal1]
    b.v = []
    b.d = []
    b.repeat = True
    b.real_time = True

    b.build_and_register()


# More mixed
def build_drums_mixed_ext54(builder: PatternBuilder):
    b = builder

    b.use_directions = False
    b.use_walks = False

    b.instrument = "drums_mixed"

    b.bars = 2
    b.name = "tom1"
    b.i = [LowFloorTom, ElectricSnare, HighFloorTom, ElectricSnare,
           LowFloorTom, AcousticSnare, S, LowFloorTom, LowFloorTom, S]
    b.v = []
    b.d = []
    b.repeat = True
    b.real_time = True

    b.build_and_register()
