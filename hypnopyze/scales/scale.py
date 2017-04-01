from hypnopyze.scales.blueprint import ScaleBlueprint
from hypnopyze.notes import *


# An ascending set of notes that fit together, spanning all octaves.
class Scale:
    # Constructs from a blueprint and the base root note
    def __init__(self, blueprint: ScaleBlueprint, base_root_note: int):
        if not blueprint or not (MIN_NOTE <= base_root_note < BASE_NOTE_COUNT):
            self.__notes = []
            return

        notes = []
        for octave in range(OCTAVE_0 - 1, OCTAVE_COUNT + 1):
            root_in_octave = Note(octave, base_root_note)
            notes.extend([root_in_octave.note_by_offset(offset)
                          for offset in blueprint.offsets])

        # make sure all are valid and unique
        self.__base_root_note = base_root_note
        self.__notes = list(set([note for note in notes if note.good]))
        self.__notes.sort()

    # Returns the base root note, e.g. C
    @property
    def base_root(self):
        return self.__base_root_note

    # Returns all notes
    @property
    def notes(self):
        return self.__notes

    # Returns true, if a valid scale
    @property
    def good(self):
        return bool(self.__notes)

    def __bool__(self):
        return self.good
