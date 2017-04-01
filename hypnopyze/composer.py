from miditime.miditime import MIDITime

from hypnopyze.players.piano import *
from hypnopyze.players.drummer import *
from hypnopyze.save_midi import save_midi


# Composes a MIDI song, i.e. a few sequences of notes played together
class Composer:
    def __init__(self, out_file: str = "out.mid"):
        self.__mt = MIDITime(StyleManager().style.bpm, out_file)

    def compose(self):

        drummer = Drummer()
        player = PianoPlayer()

        drummer.play(10)
        player.play(10)

        for notes in drummer.tracks:
            self.__mt.add_track(notes)

        for notes in player.tracks:
            self.__mt.add_track(notes)

        save_midi(self.__mt)
