from hypnopyze.notes import *

class ScaleBuilder:

    # Starts building the scale at a root base note
    def __init__(self, root_base_note):
        self.root = root_base_note
        self.after_root = [int]
        self.before_root = [int]

    # Sets the list of base notes that come after the root (ascending).
    def after(self, base_note_list):
        self.after_root = base_note_list

    # Sets the list of base notes that come before the root (descending).
    def before(self, base_note_list):
        self.before_root = base_note_list

    # Builds the Scale. Returns None if failed
    def build(self):
        before_root = self.before_root
        after_root = self.after_root
        before_legal = [0 <= n <= BaseNoteCount for n in before_root]
        after_legal = [0 <= n <= BaseNoteCount for n in after_root]

        if not (all(before_legal) and all(after_legal)):
            print("Illegal base notes.")
            return None
        #
        return Scale([])



# An ascending set of notes that fit together
class Scale:

    # constructs from a root Note, and
    def __init__(self, root_note, note_offsets):
        self.note_offsets = note_offsets
        #self.start_index =

    #def change_root(self):
        #

