from hypnopyze.notes import *


# Acts as a blueprint for a full scale.
class ScaleBlueprint:

    # Constructs from an ascending list of notes, e.g. [E,G,A,B,D],
    # where the first one is the root
    #
    # Notes shouldn't span more than one octave, e.g. [E,G,E,F] are not
    # valid base_notes. The scale will then be reduced to [E,G]
    def __init__(self, base_notes: [int]):

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
        start_root_midi = start_root.midi_note()
        self.__offsets = [start_root_midi - i.midi_note() for i in notes]

        # discard notes more than 1 octave apart from root
        self.__offsets = [i for i in self.__offsets if i < BASE_NOTE_COUNT]

    # Returns the offsets
    def offsets(self) -> [int]:
        return self.__offsets

    # Returns true, if a valid scale blueprint
    def good(self):
        return bool(self.__offsets)

    def __bool__(self):
        return self.good()


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
                          for offset in blueprint.offsets()])

        # make sure all are valid and unique
        self.__base_root_note = base_root_note
        self.__notes = list(set([note for note in notes if note.good()]))
        self.__notes.sort()

    # Returns the base root note, e.g. C
    def base_root(self):
        return self.__base_root_note

    # Returns all notes
    def notes(self):
        return self.__notes

    # Returns true, if a valid scale
    def good(self):
        return bool(self.__notes)

    def __bool__(self):
        return self.good()


# Helps with walking a scale up and down
class ScaleWalker:
    # Constructs from a scale
    def __init__(self, scale: Scale):
        if not scale:
            self.__current_index = -1
            return

        self.__scale = scale
        self.__start_index = -1
        self.__current_index = -1
        self.jump(DEFAULT_OCTAVE)

    # Jumps to the root in this octave and sets it as the starting point.
    # If the corresponding note is not good(), this object ceases to be
    # good(), until a valid jump() is performed.
    def jump(self, octave: int):
        root = Note(octave, self.__scale.base_root())

        try:
            self.__start_index = self.__scale.notes().index(root)
            self.__current_index = self.__start_index
        except ValueError:
            self.__start_index = -1
            self.__current_index = -1
            return

    # Goes back to the starting root note from jump()
    def back(self):
        self.__current_index = self.__start_index

    # Returns true, if walking the scale up (offset > 0) or down (offset < 0)
    # would produce a valid note.
    def range(self, offset):
        return 0 <= self.__current_index + offset < len(self.__scale.notes())

    # Walks the scale up (offset > 0), or down (offset < 0).
    def walk(self, offset: int):
        self.__current_index += offset

    # Returns the current note.
    def current(self):
        if not self:
            return Note(-1, -1)
        return self.__scale.notes()[self.__current_index]

    # Returns true if currently on a valid note.
    def good(self):
        return 0 <= self.__current_index < len(self.__scale.notes())

    def __bool__(self):
        return self.good()
