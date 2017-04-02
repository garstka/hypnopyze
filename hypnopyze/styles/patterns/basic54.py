from hypnopyze.patterns.builder import PatternBuilder
from hypnopyze.patterns.pattern import *
from hypnopyze.drums import *


# Builds and registers basic lead patterns.
def build_lead_basic54(builder: PatternBuilder):
    b = builder

    b.instrument = "lead"
    b.use_directions = True

    b.bars = 1
    b.i = [STAY, STAY, STAY, ROOT_DOWN, STAY]
    b.v = [H, M, M, M, M]
    b.d = []
    b.repeat = True
    b.real_time = False

    b.build_and_register()

    b.bars = 1
    b.i = [STAY, NEXT, NEXT, NEXT, NEXT_ROOT]
    b.v = [H, M, M, M, H]
    b.d = []
    b.repeat = True
    b.real_time = True

    b.build_and_register()


# Builds and registers basic bass patterns.
def build_drums_bass_basic54(builder: PatternBuilder):
    b = builder

    b.use_directions = False
    b.use_walks = False

    b.instrument = "drums_bass"

    b.bars = 1
    b.i = [BassDrum1, BassDrum1, S, S, S]
    b.v = [H, M, 0, 0, 0]
    b.d = []
    b.real_time = True
    b.repeat = True

    b.build_and_register()


# Builds and registers basic hi-hat / ride patterns.
def build_drums_hi_ride_basic54(builder: PatternBuilder):
    b = builder

    b.use_directions = False
    b.use_walks = False

    b.instrument = "drums_hi_ride"

    b.bars = 2
    b.i = [ClosedHiHat, S, PedalHiHat, S, ClosedHiHat, S, PedalHiHat, OpenHiHat,
           S, S]
    b.v = []
    b.d = [1, 0, 1, 0, 1, 0, 1, 0, 4, 0]
    b.repeat = True
    b.real_time = True

    b.build_and_register()

    b.bars = 1
    b.i = [RideCymbal2, S, RideCymbal2, S, RideCymbal2, S, RideBell, RideBell,
           CrashCymbal1, S]
    b.v = []
    b.d = []
    b.repeat = True
    b.real_time = True

    b.build_and_register()


# Builds and registers basic mixed, sequential patterns.
def build_drums_mixed_basic54(builder: PatternBuilder):
    b = builder

    b.use_directions = False
    b.use_walks = False

    b.instrument = "drums_mixed"

    b.bars = 2
    b.i = [LowFloorTom, ElectricSnare] * 10
    b.v = []
    b.d = []
    b.repeat = True
    b.real_time = False

    b.build_and_register()
