from hypnopyze.patterns import *


# Generates a pattern set for the 5/4 time signature
def patterns_54():
    collection = PatternCollection()
    instrument = "piano"
    prng = RandomState(75123481)

    base = 5
    num_walks = 20
    key = E
    scale = [A, C, D, E, G]
    walker = ScaleWalker(Scale(ScaleBlueprint(scale), key))

    pi = []
    pv = []
    pd = []

    def render():
        walks = list(set([Pattern("", base, pi, pv, pd, True) \
                         .walk_from_these_directions(len(scale), prng)
                          for _ in range(0, num_walks)]))

        sounds = []
        for walk in walks:
            walker.back()
            sounds.append(walk.sound_pattern_from_this_walk(walker))

        sounds = [i for i in sounds if i]

        collection.add_patterns(instrument, sounds)

    base = 5
    pi = [STAY, STAY, STAY, ROOT_DOWN, STAY]
    pv = [H, M, M, M, M]
    pd = []
    render()

    base = 10
    pi = [STAY, NEXT, NEXT, NEXT, NEXT_ROOT]
    pv = [H, M, M, M, H]
    pd = []
    render()
