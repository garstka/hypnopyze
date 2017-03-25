from miditime.miditime import MIDITime
from hypnopyze.save_midi import save_midi
from hypnopyze.scales import *
from hypnopyze.instruments import *
from hypnopyze.drums import *
from hypnopyze.sequencer import *
from hypnopyze.patterns import *


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

    n = scalewlk.current().midi_note()
    t = 0
    d = 2
    notes.append([t, n, v, d])

    scalewlk.walk(1)
    n = scalewlk.current().midi_note()
    t += 2
    d = 3
    notes.append([t, n, v, d])

    scalewlk.walk(2)
    n = scalewlk.current().midi_note()
    t += 3
    d = 3
    notes.append([t, n, v, d])

    scalewlk.walk(-4)
    n = scalewlk.current().midi_note()
    t += 3
    d = 5
    notes.append([t, n, v, d])

    scalewlk.walk(1)
    n = scalewlk.current().midi_note()
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

    beats_per_bar = 5

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

    seq = Sequencer(beats_per_bar=5, time_step=1,
                    perturb_velocity_cap=20)

    start = 0
    end = 120

    pi = [BassDrum1, S, AcousticSnare, ClosedHiHat, BassDrum1]
    pv = [H, 0, M, M, H]
    pd = [1, 1, 1, 1, 1]
    pattern = Pattern("drum", len(pi), pi, pv, pd, repeatable=True)

    seq.set_time(start)
    seq.set_channel(CHANNEL_DRUMS)

    if not seq.compatible(pattern):
        print("Pattern incompatible")
        return

    while seq.time() < end:
        if not seq.append(pattern):
            print("Couldn't append")

    # print(seq.notes())

    mt.add_track(seq.notes())

    save_midi(mt)


# Tests the sequencer using relative and time-scaled note pattern
def test_sequencer_relative(out="out.mid", bpm=120, beats_per_bar=10):

    mt = MIDITime(bpm, out)

    seq = Sequencer(beats_per_bar=beats_per_bar, time_step=1,
                    perturb_velocity_cap=10)

    start = 0
    end = 120

    # create the pattern as indices within a scale
    pi = [0, S, 1, S, 2]
    pv = [H, 0, M, 0, H]
    pd = [1, 1, 1, 1, 1]
    pattern = Pattern("piano", len(pi), pi, pv, pd, repeatable=True)

    # convert to sounds
    walker = ScaleWalker(Scale(ScaleBlueprint([A, C, D, E, G]), E))

    print(pattern.indices())
    pattern = pattern.sound_pattern_from_this_walk(walker)
    print(pattern.indices())

    seq.set_time(start)

    if not seq.compatible(pattern):
        print("Pattern incompatible")
        return

    while seq.time() < end:
        if not seq.append(pattern):
            print("Couldn't append")

    print(seq.notes())

    mt.add_track(seq.notes())

    save_midi(mt)


def test_compose():

    test_scales("test0.mid")
    test_drums_simple("test1.mid")
    test_sequencer_simple("test2.mid")
    test_sequencer_relative("test3.mid")
