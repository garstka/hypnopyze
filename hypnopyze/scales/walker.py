from hypnopyze.scales.scale import Scale
from hypnopyze.notes import *


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
    # If the corresponding note is not good, this object ceases to be
    # good, until a valid jump() is performed.
    def jump(self, octave: int):
        root = Note(octave, self.__scale.base_root)

        try:
            self.__start_index = self.__scale.notes.index(root)
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
    def range(self, offset) -> bool:
        return 0 <= self.__current_index + offset < len(self.__scale.notes)

    # Walks the scale up (offset > 0), or down (offset < 0).
    def walk(self, offset: int):
        self.__current_index += offset

    # Returns the current note.
    @property
    def current(self) -> Note:
        if not self:
            return Note(-1, -1)
        return self.__scale.notes[self.__current_index]

    # Returns true if currently on a valid note.
    @property
    def good(self) -> bool:
        return 0 <= self.__current_index < len(self.__scale.notes)

    def __bool__(self):
        return self.good
