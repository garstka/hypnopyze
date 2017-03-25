from hypnopyze.scales import *
from miditime.miditime import MIDITime


def test():
    mt = MIDITime(120, 'test.mid')

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

    mt.save_midi()
