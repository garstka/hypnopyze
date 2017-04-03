from miditime.miditime import MIDITime

from hypnopyze.players.piano import *
from hypnopyze.players.drummer import *
from hypnopyze.save_midi import save_midi


# Composes a MIDI song, i.e. a few sequences of notes played together
class Composer:
    def __init__(self, out_file: str = "out.mid"):
        self.__mt = MIDITime(StyleManager().style.bpm, out_file)

        self.drummer = Drummer()
        self.player = PianoPlayer()

    def compose(self, bar_groups: int = 4):

        self.drummer.play(bar_groups)
        self.player.play(bar_groups)

    def save(self):

        tracks = self.drummer.tracks + self.player.tracks

        for notes in tracks:
            self.__mt.add_track(notes)

        if tracks:
            save_midi(self.__mt, StyleManager().style.instruments_per_channel)
        else:
            save_midi(self.__mt)  # empty
