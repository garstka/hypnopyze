from miditime.miditime import MIDITime


# Composes a MIDI song, i.e. a few sequences of notes played together
class Composer:

    def __init__(self, out_file: str = "out.mid",
                 beats_per_minute: int = 120, beats_per_bar: int=4):
        self.__beats_per_bar = beats_per_bar
        # self.__bars_group = 4
        # self.__bars_per_minute = beats_per_minute / self.__beats_per_bar
        self.__mt = MIDITime(beats_per_minute, out_file)


