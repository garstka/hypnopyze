from miditime.miditime import MIDITime
from hypnopyze.drums import *
from hypnopyze.piano import *
from hypnopyze.save_midi import save_midi


# Composes a MIDI song, i.e. a few sequences of notes played together
class Composer:
    def __init__(self, out_file: str = "out.mid",
                 beats_per_minute: int = 120, beats_per_bar: int = 5):
        self.__beats_per_bar = beats_per_bar
        # self.__bars_group = 4
        # self.__bars_per_minute = beats_per_minute / self.__beats_per_bar
        self.__mt = MIDITime(beats_per_minute, out_file)

    def compose(self):
        drummer = Drummer(self.__beats_per_bar * 4)
        player = PianoPlayer(self.__beats_per_bar * 2)

        drummer.play(10)
        player.play(10)

        for notes in drummer.tracks:
            self.__mt.add_track(notes)

        for notes in player.tracks:
            self.__mt.add_track(notes)

        save_midi(self.__mt)
