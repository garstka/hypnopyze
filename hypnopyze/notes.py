
# base notes

C = 0
Cs = 1
Df = Cs
D = 2
Ds = 3
Ef = Ds
E = 4
F = 5
Fs = 6
Gf = Fs
G = 7
Gs = 8
Af = Gs
A = 9
As = 10
Bf = As
B = 11
BASE_NOTE_COUNT = 12

# all notes

MIN_NOTE = C
MAX_NOTE = 127

# octaves

OCTAVE_0 = 0
OCTAVE_1 = 1
OCTAVE_2 = 2
OCTAVE_3 = 3
OCTAVE_4 = 4
OCTAVE_5 = 5
OCTAVE_6 = 6
OCTAVE_7 = 7
OCTAVE_8 = 8
OCTAVE_9 = 9
FULL_OCTAVE_COUNT = 10
OCTAVE_10 = 10
OCTAVE_COUNT = 11


DEFAULT_OCTAVE = OCTAVE_5


# Note in an octave.
# Note must be checked if it's good() before being used.
class Note:

    # Constructs from octave number and base note.
    def __init__(self, octave: int, base_note: int):
        self.__midi_note = octave * BASE_NOTE_COUNT + base_note

    # Returns the next note below that corresponds to base_note.
    def note_below(self, base_note):
        if base_note < self.base_note():  # if in the same octave
            return Note(self.octave(), base_note)

        # in the previous octave
        return Note(self.octave() - 1, base_note)

    # Returns the next note above that corresponds to base_note.
    def note_above(self, base_note):
        if self.base_note() < base_note:  # if in the same octave
            return Note(self.octave(), base_note)

        # in the next octave
        return Note(self.octave() + 1, base_note)

    # Returns the note corresponding to an offset by some half-steps
    # (can be negative).
    def note_by_offset(self, offset):
        new_midi = self.__midi_note + offset
        return Note(new_midi // BASE_NOTE_COUNT, new_midi % BASE_NOTE_COUNT)

    # Returns true, if a correct midi note.
    def good(self):
        return MIN_NOTE <= self.__midi_note <= MAX_NOTE

    # Returns the note value usable for midi files.
    def midi_note(self):
        return self.__midi_note

    # Returns the base note
    def base_note(self):
        return self.__midi_note % BASE_NOTE_COUNT

    # Returns the octave
    def octave(self):
        return self.__midi_note // BASE_NOTE_COUNT

    def __eq__(self, other):
        return self.__midi_note == other.__midi_note

    def __lt__(self, other):
        return self.__midi_note < other.__midi_note

    def __hash__(self):
        return self.__midi_note

    def __bool__(self):
        return self.good()

