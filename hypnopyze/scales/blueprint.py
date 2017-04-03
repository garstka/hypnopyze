from typing import List
from hypnopyze.notes import *

# some blueprints

MajorPentatonic = [E, Fs, Gs, B, Cs]
MinorPentatonic = [E, G, A, B, D]
PhrygianMode = [E, F, G, A, B, C, D]
DoubleHarmonic = [E, F, Gs, A, B, C, D]
PhrygianDominant = [C, Df, E, F, G, Af, Bf]

MajorScale = [C, D, E, F, G, A, B]  # i.e. ionian mode
LydianMode = [F, G, A, B, C, D, E]  # major
MixolydianMode = [G, A, B, C, D, E, F]  # major
DorianMode = [D, E, F, G, A, B, C]  # minor
AeolianMode = [A, B, C, D, E, F, G]  # minor
LocrianMode = [B, C, D, E, F, G, A]  # diminished


# Acts as a blueprint for a full scale.
class ScaleBlueprint:
    # Constructs from an ascending list of notes, e.g. [E,G,A,B,D],
    # where the first one is the root
    #
    # Notes shouldn't span more than one octave, e.g. [E,G,E,F] are not
    # valid base_notes. The scale will then be reduced to [E,G]
    def __init__(self, base_notes: List[int]):

        if len(base_notes) == 0:
            self.__offsets = []
            return

        # find notes with regard to the root note
        start_root = Note(OCTAVE_0, base_notes[0])
        notes = [start_root]
        prev = start_root
        for i in base_notes[1:]:
            prev = prev.note_above(i)
            notes.append(prev)

        # convert notes to offsets
        start_root_midi = start_root.midi_note
        self.__offsets = [start_root_midi - i.midi_note for i in notes]

        # discard notes more than 1 octave apart from root
        self.__offsets = [i for i in self.__offsets if i < BASE_NOTE_COUNT]

    # Returns the offsets
    @property
    def offsets(self) -> List[int]:
        return self.__offsets

    # Returns true, if a valid scale blueprint
    @property
    def good(self):
        return bool(self.__offsets)

    def __bool__(self):
        return self.good
