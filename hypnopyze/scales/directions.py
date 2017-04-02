from typing import List
from numpy.random import RandomState
from hypnopyze.notes import *

# directions for generating scale walks for patterns

STAY = 0  # play the previous note again
ROOT = 1  # play the current octave's root note
NEXT_ROOT = 2  # play the next octave's root note
PREV_ROOT = 3  # play the previous octave's root note

NEXT = 4  # play the next note
PREV = 5  # play the previous note

UP = 6  # play random in (current, NEXT_ROOT), closer to current are more likely
DOWN = 7  # play random in (ROOT, current), closer to current are more likely

ROOT_DOWN = 8  # play random in (PREV_ROOT, ROOT), closer to ROOT are more likely

PREV_UP = 9  # switch to PREV_ROOT -> UP
PREV_DOWN = 10  # switch to PREV_ROOT -> ROOT_DOWN

NEXT_UP = 11  # switch to NEXT_ROOT -> UP
NEXT_DOWN = 12  # switch to NEXT_ROOT -> ROOT_DOWN


# Treats the indices as general directions for a walk, and
# returns a scale walk (relative offsets within a scale)
#  - scale walk is for this scale size
#  - may produce different results each time, as it uses a PRNG
# Returns [] if the directions are invalid for a scale of this size,
# or the imperfect algorithm failed (for now).
def directions_to_walk(indices,
                       scale_size: int,
                       prng: RandomState):
    #
    # Example:
    # for
    # [CURRENT, UP, UP, DOWN, DOWN, NEXT_ROOT, PREV_ROOT]
    # scale_size = 5
    # one possibility would be:
    # absolute offsets: [0, 1, 3, 2, 1, 4, 0]
    # walk offsets: [0, 1, 2, -1, -1, 3, -4]

    if scale_size == 0:
        return []

    new_indices = []
    current_offset = 0

    def current_root():
        return current_offset - (current_offset % scale_size)

    def next_root():
        return current_root() + scale_size

    def prev_root():
        return current_root() - scale_size

    def rand(max_val):
        return abs(prng.binomial(2 * max_val, 0.5) - max_val)

    def rand_nonzero(max_val):
        result = 0
        while result == 0:
            result = rand(max_val)
        return result

    for i in indices:

        if i == PREV_UP:  # switch to PREV_ROOT -> UP
            current_offset = prev_root()
            i = UP
        elif i == PREV_DOWN:  # switch to PREV_ROOT -> ROOT_DOWN
            current_offset = prev_root()
            i = ROOT_DOWN
        elif i == NEXT_UP:  # switch to NEXT_ROOT -> UP
            current_offset = next_root()
            i = UP
        elif i == NEXT_DOWN:  # switch to NEXT_ROOT -> ROOT_DOWN
            current_offset = next_root()
            i = ROOT_DOWN

        if i == STAY:  # play the previous note again
            pass
        elif i == NEXT:  # play the next note
            current_offset += 1
        elif i == PREV:  # play the previous note
            current_offset -= 1
        elif i == UP:  # go up (staying within the same octave)

            top = next_root() - 1
            bottom = current_offset + 1
            if bottom > top:
                return []  # can be fixed, perhaps

            off = rand_nonzero(top - bottom + 1)
            current_offset = bottom - 1 + off

        elif i == DOWN:  # go down (staying within the same octave)

            top = current_offset - 1
            bottom = current_root() + 1
            if bottom > top:

                if current_offset == current_root():
                    print("Invalid directions: can't go DOWN from root")

                return []  # can be fixed, perhaps

            off = rand_nonzero(top - bottom + 1)
            current_offset = top + 1 - off

        elif i == ROOT:  # play the current root
            current_offset = current_root()
        elif i == PREV_ROOT:  # root note one octave below
            current_offset = prev_root()
        elif i == NEXT_ROOT:  # root note one octave above
            current_offset = next_root()
        elif i == ROOT_DOWN:  # play random in (PREV_ROOT, ROOT)

            top = current_root() - 1
            bottom = prev_root() + 1

            if bottom > top:
                return []  # can be fixed, perhaps

            off = rand_nonzero(top - bottom + 1)
            current_offset = top + 1 - off

        else:
            new_indices.append(SILENCE)
            continue

        new_indices.append(current_offset)

    # convert absolute to relative offsets

    last_index = 0
    for i in range(0, len(new_indices)):
        this_index = new_indices[i]

        # ignore silence
        if this_index == SILENCE:
            continue

        new_indices[i] = this_index - last_index
        last_index = this_index

    return new_indices
