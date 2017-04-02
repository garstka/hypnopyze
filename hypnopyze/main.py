from hypnopyze.test import run_tests
from hypnopyze.styles.sample import *
from hypnopyze.composer import Composer
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--out", default="out.mid",
                        type=str,
                        help="set the output file")

    parser.add_argument("--key", default="E",
                        choices=["C", "C#", "D", "D#", "E", "F",
                                 "F#", "G", "G#", "A", "A#", "B"],
                        type=str,
                        help="set the song key")

    parser.add_argument("--seed",
                        type=str,
                        help="set a different seed")

    parser.add_argument("-t", "--test", help="run tests",
                        action="store_true")

    args = parser.parse_args()

    key_to_int = {"C": C, "C#": Cs, "D": D, "D#": Ds, "E": E,
                  "F": F, "F#": Fs, "G": G, "G#": Gs, "A": A,
                  "A#": As, "B": B}

    style = style_54()

    style.key = key_to_int[args.key]
    # style.scale = PhrygianDominant
    # style.lead = Lead7_fifths

    if args.seed:
        StyleManager().reseed(args.seed)

    set_style_54(style)

    composer = Composer(args.out)
    composer.compose()

    if args.test:
        run_tests()
