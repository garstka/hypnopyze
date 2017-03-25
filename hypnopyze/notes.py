
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
BaseNoteCount = 12

DefaultOctave = 5

# Note in an octave
class Note:

    # Constructs from octave number and base note.
    def __init__(self, octave, base_note):
        self.octave = octave
        self.base_note = base_note

    # Returns the next note below that corresponds to base_note.
    def note_below(self, base_note):
        if base_note < self.base_note:  # if in the same octave
            return Note(self.octave, base_note)

        # in the previous octave
        return Note(self.octave - 1, base_note)

    # Returns the next note above that corresponds to base_note.
    def note_above(self, base_note):
        if self.base_note < base_note:  # if in the same octave
            return Note(self.octave, base_note)

        # in the next octave
        return Note(self.octave + 1, base_note)

    # Returns the note corresponding to the step (one guitar fret).
    # step can be negative
    def step(self, step):

        new_midi_note = self.midi_note() + step
        self.base_note = new_midi_note % BaseNoteCount
        #self.octave =


    # Returns true, if a correct midi note.
    def good(self):
        return 0 <= self.midi_note() < 128

    # Returns the note value usable for midi files.
    def midi_note(self):
        return self.octave * self.base_note
