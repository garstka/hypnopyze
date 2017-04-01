from miditime.miditime import MIDITime

from hypnopyze.drums import *
from hypnopyze.save_midi import save_midi
from hypnopyze.sequencer import *
from hypnopyze.composer import *
from hypnopyze.scales.blueprint import *


# Tests the scale walking capability.
def test_scales(out="out.mid", bpm=120):
    mt = MIDITime(bpm, out)

    blueprint = ScaleBlueprint([A, C, D, E, G])
    if not blueprint:
        print("Bad blueprint")
        return

    scale = Scale(blueprint, E)
    if not scale:
        print("Bad scale")
        return

    scalewlk = ScaleWalker(scale)
    if not scalewlk:
        print("Bad scale walker")

    notes = []

    # Example:
    # [0, 60, 127, 3]
    # At 0 beats (the start), Middle C with velocity 127, for 3 beats
    # [10, 61, 127, 4]
    # At 10 beats (12 seconds from start), C#5 with velocity 127, for 4 beats

    v = 127

    n = scalewlk.current.midi_note
    t = 0
    d = 2
    notes.append([t, n, v, d])

    scalewlk.walk(1)
    n = scalewlk.current.midi_note
    t += 2
    d = 3
    notes.append([t, n, v, d])

    scalewlk.walk(2)
    n = scalewlk.current.midi_note
    t += 3
    d = 3
    notes.append([t, n, v, d])

    scalewlk.walk(-4)
    n = scalewlk.current.midi_note
    t += 3
    d = 5
    notes.append([t, n, v, d])

    scalewlk.walk(1)
    n = scalewlk.current.midi_note
    t += 5
    d = 6
    notes.append([t, n, v, d])

    mt.add_track(notes)

    # one instrument per channel

    mt.add_track([[[2, 64, 127, 10], 1]])

    mt.add_track([[[12, 61, 127, 5], 2]])

    mt.add_track([[[17, 64, 127, 5], 3]])

    save_midi(mt, [0, 16, 20, 53])


# Tests the drum channel
def test_drums_simple(out="out.mid", bpm=120, beats_per_bar=5):
    mt = MIDITime(bpm, out)

    start = 0
    end = 120

    drums = []

    d = 1
    v = 127
    for t in range(start, end):
        step = t % beats_per_bar
        if step == 0:
            n = BassDrum1
            drums.append([[t, n, v, d], CHANNEL_DRUMS])
        elif step == 2:
            n = AcousticSnare
            drums.append([[t, n, v, d], CHANNEL_DRUMS])
        elif step == 3:
            n = ClosedHiHat
            drums.append([[t, n, v, d], CHANNEL_DRUMS])
        elif step == 4:
            n = BassDrum1
            drums.append([[t, n, v, d], CHANNEL_DRUMS])

    mt.add_track(drums)

    save_midi(mt)


# Tests the sequencer with drums
def test_sequencer_simple(out="out.mid", bpm=120, beats_per_bar=5):
    mt = MIDITime(bpm, out)

    seq = Sequencer(beats_per_bar=beats_per_bar, perturb_velocity_cap=20)

    start = 0
    end = 120

    pi = [BassDrum1, S, AcousticSnare, ClosedHiHat, BassDrum1]
    pv = [H, 0, M, M, H]
    pd = [1, 1, 1, 1, 1]
    pattern = Pattern("drum", 1, pi, pv, pd, repeatable=True)

    seq.time = start
    seq.channel = CHANNEL_DRUMS

    if not seq.compatible(pattern):
        print("Pattern incompatible")
        return

    while seq.time < end:
        if not seq.append(pattern):
            print("Couldn't append")

    # print(seq.notes())

    mt.add_track(seq.notes)

    save_midi(mt)


# Tests the sequencer using relative and time-scaled note pattern
def test_sequencer_relative(out="out.mid", bpm=120, beats_per_bar=10):
    mt = MIDITime(bpm, out)

    seq = Sequencer(beats_per_bar=beats_per_bar, perturb_velocity_cap=10)

    start = 0
    end = 120

    # create the pattern as indices within a scale
    pi = [0, S, 1, S, 2]
    pv = [H, 0, M, 0, H]
    pd = [1, 1, 1, 1, 1]
    pattern = Pattern("piano", 1, pi, pv, pd, repeatable=True)

    # convert to sounds
    walker = ScaleWalker(Scale(ScaleBlueprint([A, C, D, E, G]), E))

    print(pattern.indices)
    pattern = pattern.sound_pattern_from_this_walk(walker)
    print(pattern.indices)

    seq.time = start

    if not seq.compatible(pattern):
        print("Pattern incompatible")
        return

    while seq.time < end:
        if not seq.append(pattern):
            print("Couldn't append")

    print(seq.notes)

    mt.add_track(seq.notes)

    save_midi(mt)


# Tests pattern generation from directions
def test_generator(out="out.mid", bpm=120, beats_per_bar=5):
    mt = MIDITime(bpm, out)

    seq = Sequencer(beats_per_bar=beats_per_bar, perturb_velocity_cap=10)

    prng = RandomState(75123481)

    start = 0
    end = 120

    scale = [A, C, D, E, G]

    # create the pattern as directions for a walk within a scale
    pi = [STAY, -1, UP, -1, UP, DOWN, ROOT_DOWN, -1, -1, NEXT_ROOT]
    pv = [H, 0, M, 0, H, H, M, 0, 0, M]
    pd = [2, 1, 1, 3, 1, 1, 3, 0, 0, 1]
    pattern0 = Pattern("piano1", 2, pi, pv, pd, repeatable=True)
    patterns = [pattern0.walk_from_these_directions(len(scale), prng)
                for _ in range(1, 10)]

    patterns = [p for p in patterns if p]
    print("available: ", len(patterns))
    if not patterns:
        print("Couldn't generate any patterns from these directions.")
        return

    for (i, p) in enumerate(patterns):
        print(i, ": ", p.indices)

    pattern = patterns[0]

    # convert to sounds
    walker = ScaleWalker(Scale(ScaleBlueprint(scale), E))
    pattern = pattern.sound_pattern_from_this_walk(walker)

    seq.time = start

    if not seq.compatible(pattern):
        print("Pattern incompatible")
        return

    while seq.time < end:
        if not seq.append(pattern):
            print("Couldn't append")

    print(seq.notes)

    mt.add_track(seq.notes)

    save_midi(mt)


# Plays all drum sounds
def test_different_drum_sounds(out="out.mid", bpm=120, beats_per_bar=5):
    mt = MIDITime(bpm, out)

    seq = Sequencer(beats_per_bar=beats_per_bar, perturb_velocity_cap=10)

    start = 0
    end = 120

    pi = []  # length, character, ability to be looped
    pi.append(AcousticBassDrum)  # short, dead, repeat
    pi.append(BassDrum1)  # short, bassy, repeat
    pi.append(SideStick)  # very short, single
    pi.append(AcousticSnare)  # unimpressive tsh, single
    pi.append(HandClap)  # unimpressive clap, single
    pi.append(ElectricSnare)  # cool snare, single
    pi.append(LowFloorTom)  # roomy tom, some
    pi.append(ClosedHiHat)  # very short tss, repeat
    pi.append(HighFloorTom)  # roomy tom 2, some
    pi.append(PedalHiHat)  # very short tss 2, repeat
    pi.append(LowTom)  # roomy tom 3, some
    pi.append(OpenHiHat)  # long tss, some
    pi.append(LowMidTom)  # short tom, some
    pi.append(HiMidTom)  # short tom 2, some
    pi.append(CrashCymbal1)  # long crash, some
    pi.append(HighTom)  # short tom, some
    pi.append(RideCymbal1)  # long crash, some
    pi.append(ChineseCymbal)  # different crash, long, single
    pi.append(RideBell)  # long bell, repeat
    pi.append(Tambourine)  # short, single
    pi.append(SplashCymbal)  # long, single
    pi.append(Cowbell)  # short cowbell, repeat
    pi.append(CrashCymbal2)  # long, single
    pi.append(Vibraslap)  # weird, single
    pi.append(RideCymbal2)  # long, single
    pi.append(HiBongo)  # short, some
    pi.append(LowBongo)  # short, dead, single
    pi.append(MuteHiConga)  # very short, dead, single
    pi.append(OpenHiConga)  # drummy, some
    pi.append(LowConga)  # drummy 2, some
    pi.append(HighTimbale)  # different drummy, single
    pi.append(LowTimbale)  # different drummy 2, single
    pi.append(HighAgogo)  # very short jingle, single
    pi.append(LowAgogo)  # very short jingle 2, single
    pi.append(Cabasa)  # short, sandy, single
    pi.append(Maracas)  # very short, single
    pi.append(ShortWhistle)  # short, single
    pi.append(LongWhistle)  # long, already annoying, some (annoying)
    pi.append(ShortGuiro)  # buzzy, single
    pi.append(LongGuiro)  # scratchy, some (annoying)
    pi.append(Claves)  # hammery, single
    pi.append(HiWoodBlock)  # knocky, some
    pi.append(LowWoodBlock)  # knocky 2, some
    pi.append(MuteCuica)  # woo, single
    pi.append(OpenCuica)  # moo, single
    pi.append(MuteTriangle)  # short, repeat
    pi.append(OpenTriangle)  # long, single

    pv = []
    pd = []

    pattern = Pattern("drums", int(ceil(len(pi) / beats_per_bar)), pi, pv, pd, \
                      repeatable=True)

    seq.channel = CHANNEL_DRUMS
    seq.time = start

    if not seq.compatible(pattern):
        print("Pattern incompatible")
        return

    while seq.time < end:
        if not seq.append(pattern):
            print("Couldn't append")

    mt.add_track(seq.notes)

    save_midi(mt)


# Plays all drum sounds
def test_useful_drum_sounds(out="out.mid", bpm=160, beats_per_bar=5):
    mt = MIDITime(bpm, out)

    seq = Sequencer(beats_per_bar=beats_per_bar, perturb_velocity_cap=10)

    start = 0
    end = 120

    pi = []  # length, character, ability to be looped

    # drummer - main
    pi = []
    pi.append(AcousticBassDrum)  # short, dead, repeat
    pi.append(BassDrum1)  # short, bassy, repeat
    pi.append(SideStick)  # very short, single
    pi.append(ElectricSnare)  # cool snare, single
    pi.append(LowFloorTom)  # roomy tom, some
    pi.append(ClosedHiHat)  # very short tss, repeat
    pi.append(HighFloorTom)  # roomy tom 2, some
    pi.append(PedalHiHat)  # very short tss 2, repeat
    pi.append(LowTom)  # roomy tom 3, some
    pi.append(OpenHiHat)  # long tss, single
    pi.append(LowMidTom)  # short tom, some
    pi.append(HiMidTom)  # short tom 2, some
    pi.append(CrashCymbal1)  # long crash, single
    pi.append(HighTom)  # short tom, some
    pi.append(RideCymbal1)  # long crash, some
    pi.append(RideBell)  # long bell, repeat
    pi.append(CrashCymbal2)  # long, single
    pi.append(RideCymbal2)  # long, repeat

    # drummer - limited usefulness

    pi.append(SplashCymbal)  # long, single
    pi.append(AcousticSnare)  # unimpressive tsh, single
    pi.append(MuteTriangle)  # short, repeat
    pi.append(ChineseCymbal)  # different crash, long, single

    # cowbell operator

    pi.append(Cowbell)  # short cowbell, repeat

    # background drums

    pi.append(HiBongo)  # short, some
    pi.append(OpenHiConga)  # drummy, some
    pi.append(LowConga)  # drummy 2, some
    pi.append(LowBongo)  # short, dead, single
    pi.append(MuteHiConga)  # very short, dead, single
    pi.append(HighTimbale)  # different drummy, single
    pi.append(LowTimbale)  # different drummy 2, single
    pi.append(HiWoodBlock)  # knocky, some
    pi.append(LowWoodBlock)  # knocky 2, some

    # background jingling sounds

    pi.append(Tambourine)  # short, single
    pi.append(HighAgogo)  # very short jingle, single
    pi.append(LowAgogo)  # very short jingle 2, single
    pi.append(Claves)  # hammery, single
    pi.append(OpenTriangle)  # long, single

    # weird person-related sounds
    pi.append(HandClap)  # unimpressive clap, single
    pi.append(LongWhistle)  # long, already annoying, some (annoying)
    pi.append(ShortWhistle)  # short, single
    pi.append(MuteCuica)  # woo, single
    pi.append(OpenCuica)  # moo, single

    # weird instrument sounds
    pi.append(Vibraslap)  # weird, single
    pi.append(Cabasa)  # short, sandy, single
    pi.append(Maracas)  # very short, single
    pi.append(ShortGuiro)  # buzzy, single
    pi.append(LongGuiro)  # scratchy, some (annoying)

    # pi = [val for val in pi for _ in range(0, 4)]
    pv = []
    pd = []

    pattern = Pattern("drums", int(ceil(len(pi) / beats_per_bar)), pi, pv, pd,
                      repeatable=True)

    seq.channel = CHANNEL_DRUMS
    seq.time = start

    if not seq.compatible(pattern):
        print("Pattern incompatible")
        return

    while seq.time < end:
        if not seq.append(pattern):
            print("Couldn't append")

    mt.add_track(seq.notes)

    save_midi(mt)


# Main drummer sounds
def test_drummer_sounds(out="out.mid", bpm=120, beats_per_bar=5):
    mt = MIDITime(bpm, out)

    seq = Sequencer(beats_per_bar=beats_per_bar, perturb_velocity_cap=30)

    start = 0
    end = 120

    pi = []  # length, character, ability to be looped

    # drummer - main
    pi = []

    # bass - beat or timing element with basic pulse patterns
    pi.append(AcousticBassDrum)  # short, dead, repeat
    pi.append(BassDrum1)  # short, bassy, repeat

    # stick - intro

    pi.append(SideStick)  # very short, single

    # snare - regular accents, fills
    pi.append(ElectricSnare)  # cool snare, single

    # tom - fills and solos
    pi.append(LowFloorTom)  # roomy tom, some
    pi.append(HighFloorTom)  # roomy tom 2, some
    pi.append(LowTom)  # roomy tom 3, some
    pi.append(LowMidTom)  # short tom, some
    pi.append(HiMidTom)  # short tom 2, some
    pi.append(HighTom)  # short tom, some

    # ride - constant-rhythm pattern
    pi.append(RideCymbal1)  # long crash, some
    pi.append(RideCymbal2)  # long, repeat
    pi.append(RideBell)  # long bell, repeat

    # hi-hat - similar to ride, not at the same time
    pi.append(ClosedHiHat)  # very short tss, repeat
    pi.append(PedalHiHat)  # very short tss 2, repeat
    pi.append(OpenHiHat)  # long tss, single

    # crash - accent markers, major changes
    pi.append(CrashCymbal1)  # long crash, single
    pi.append(CrashCymbal2)  # long, single

    pi.append(RideCymbal2)  # long, repeat
    pi.append(RideCymbal2)  # long, repeat
    pi.append(OpenHiHat)  # long tss, single
    pi.append(RideCymbal2)  # long, repeat
    pi.append(RideCymbal1)  # long crash, some

    pi.append(RideCymbal1)  # long crash, some
    pi.append(RideCymbal1)  # long crash, some
    pi.append(OpenHiHat)  # long tss, single
    pi.append(RideCymbal1)  # long crash, some
    pi.append(RideCymbal1)  # long crash, some

    pi.append(PedalHiHat)  # very short tss 2, repeat
    pi.append(PedalHiHat)  # very short tss 2, repeat
    pi.append(PedalHiHat)  # very short tss 2, repeat
    pi.append(PedalHiHat)  # very short tss 2, repeat
    pi.append(OpenHiHat)  # long tss, single

    pi.append(ClosedHiHat)  # very short tss, repeat
    pi.append(ClosedHiHat)  # very short tss, repeat
    pi.append(ClosedHiHat)  # very short tss, repeat
    pi.append(ClosedHiHat)  # very short tss, repeat
    pi.append(OpenHiHat)  # long tss, single

    pi = [val for val in pi for _ in range(0, 4)]

    pv = []
    pd = []

    pattern = Pattern("drums", int(ceil(len(pi) / beats_per_bar)), pi, pv, pd,
                      repeatable=True)

    seq.channel = CHANNEL_DRUMS
    seq.time = start

    if not seq.compatible(pattern):
        print("Pattern incompatible")
        return

    while seq.time < end:
        if not seq.append(pattern):
            print("Couldn't append")

    mt.add_track(seq.notes)

    save_midi(mt)


# Tom configuration
def test_tom_sounds(out="out.mid", bpm=240, beats_per_bar=5):
    mt = MIDITime(bpm, out)

    seq = Sequencer(beats_per_bar=beats_per_bar, perturb_velocity_cap=30)

    start = 0
    end = 120

    pi = []  # length, character, ability to be looped

    # drummer - main
    pi = []

    # tom - fills and solos
    pi.append(HiMidTom)  # short tom 2, some
    pi.append(HiMidTom)  # short tom 2, some
    pi.append(SILENCE)
    pi.append(HighFloorTom)  # roomy tom 2, some
    pi.append(SILENCE)
    pi.append(HighFloorTom)  # roomy tom 2, some
    pi.append(SILENCE)
    pi.append(HiMidTom)  # short tom 2, some

    pi.append(HiMidTom)  # short tom 2, some
    pi.append(HiMidTom)  # short tom 2, some
    pi.append(SILENCE)
    pi.append(HighFloorTom)  # roomy tom 2, some
    pi.append(SILENCE)
    pi.append(HighFloorTom)  # roomy tom 2, some
    pi.append(SILENCE)
    pi.append(HiMidTom)  # short tom 2, some

    pi.append(LowFloorTom)  # roomy tom, some
    pi.append(HighFloorTom)  # roomy tom 2, some
    pi.append(LowTom)  # roomy tom 3, some
    pi.append(LowMidTom)  # short tom, some
    pi.append(HiMidTom)  # short tom 2, some
    pi.append(HighTom)  # short tom, some

    # pi = [val for val in pi for _ in range(0, 4)]

    pv = []
    pd = []

    pattern = Pattern("drums", int(ceil(len(pi) / beats_per_bar)), pi, pv, pd,
                      repeatable=True)

    seq.channel = CHANNEL_DRUMS
    seq.time = start

    if not seq.compatible(pattern):
        print("Pattern incompatible")
        return

    while seq.time < end:
        if not seq.append(pattern):
            print("Couldn't append")

    mt.add_track(seq.notes)

    save_midi(mt)


# Hi-hat / ride
def test_hi_ride_sounds(out="out.mid", bpm=180, beats_per_bar=5):
    mt = MIDITime(bpm, out)

    seq = Sequencer(beats_per_bar=beats_per_bar, perturb_velocity_cap=30)

    start = 0
    end = 120

    pi = []  # length, character, ability to be looped

    # drummer - main
    pi = []

    pi.append(ClosedHiHat)  # very short tss, repeat
    pi.append(SILENCE)
    pi.append(PedalHiHat)  # very short tss 2, repeat
    pi.append(SILENCE)
    pi.append(ClosedHiHat)  # very short tss, repeat
    pi.append(SILENCE)
    pi.append(PedalHiHat)  # very short tss 2, repeat
    pi.append(OpenHiHat)  # long tss, single
    pi.append(RideCymbal2)  # long, repeat
    pi.append(SILENCE)
    pi.append(RideCymbal2)  # long, repeat
    pi.append(SILENCE)
    pi.append(RideCymbal2)  # long, repeat
    pi.append(SILENCE)
    pi.append(RideBell)  # long bell, repeat
    pi.append(CrashCymbal1)  # long crash, single

    # pi = [val for val in pi for _ in range(0, 4)]
    pv = []
    pd = []

    pattern = Pattern("drums", int(ceil(len(pi) / beats_per_bar)), pi, pv, pd,
                      repeatable=True)

    seq.channel = CHANNEL_DRUMS
    seq.time = start

    if not seq.compatible(pattern):
        print("Pattern incompatible")
        return

    while seq.time < end:
        if not seq.append(pattern):
            print("Couldn't append")

    mt.add_track(seq.notes)

    save_midi(mt)


# Hi-hat / ride + toms
def test_fill_sounds(out="out.mid", bpm=240, beats_per_bar=4):
    mt = MIDITime(bpm, out)

    seq = Sequencer(beats_per_bar=beats_per_bar, perturb_velocity_cap=30)

    start = 0
    end = 120

    # drummer - main

    pi = []
    pi.append(LowFloorTom)  # roomy tom, some
    pi.append(HighFloorTom)  # roomy tom 2, some
    pi.append(LowTom)  # roomy tom 3, some
    pi.append(LowMidTom)  # short tom, some
    pi.append(HiMidTom)  # short tom 2, some
    pi.append(HighTom)  # short tom, some

    pi = []

    pi.append(ClosedHiHat)  # very short tss, repeat
    pi.append(LowFloorTom)  # roomy tom, some
    pi.append(PedalHiHat)  # very short tss 2, repeat
    pi.append(HighFloorTom)  # roomy tom 2, some
    pi.append(ClosedHiHat)  # very short tss, repeat
    pi.append(LowTom)  # roomy tom 3, some
    pi.append(PedalHiHat)  # very short tss 2, repeat
    pi.append(OpenHiHat)  # long tss, single
    pi.append(RideCymbal2)  # long, repeat
    pi.append(LowMidTom)  # short tom, some
    pi.append(RideCymbal2)  # long, repeat
    pi.append(HiMidTom)  # short tom 2, some
    pi.append(RideCymbal2)  # long, repeat
    pi.append(HighTom)  # short tom, some
    pi.append(RideBell)  # long bell, repeat
    pi.append(CrashCymbal1)  # long crash, single

    # pi = [val for val in pi for _ in range(0, 4)]
    pv = []
    pd = []

    pattern = Pattern("drums", int(ceil(len(pi) / beats_per_bar)), pi, pv, pd,
                      repeatable=True)

    seq.channel = CHANNEL_DRUMS
    seq.time = start

    if not seq.compatible(pattern):
        print("Pattern incompatible")
        return

    while seq.time < end:
        if not seq.append(pattern):
            print("Couldn't append")

    mt.add_track(seq.notes)

    save_midi(mt)


# Test wip composer
def test_composer(out="out.mid"):
    composer = Composer(out)
    composer.compose()


def test_compose():
    # test_scales("test0.mid")
    # test_drums_simple("test1.mid")
    # test_sequencer_simple("test2.mid")
    # test_sequencer_relative("test3.mid")
    # test_generator("test4.mid")
    # test_different_drum_sounds("test5_drums.mid")
    # test_useful_drum_sounds("test6_usefuldrummer.mid")
    # test_drummer_sounds("test7_drummer.mid")
    # test_tom_sounds("test8_toms.mid")
    test_composer("test9_compose.mid")
    # test_hi_ride_sounds("test10_hiride.mid")
    # test_fill_sounds("test11_fill.mid")
