from hypnopyze.test import run_tests
from hypnopyze.styles.sample import *
from hypnopyze.composer import Composer
import argparse


def main():
    def restricted_float(x):
        x = float(x)
        if x < 0.0 or x > 1.0:
            raise argparse.ArgumentTypeError(
                "%r not in range [0.0, 1.0]" % (x,))
        return x

    def positive_int(x):
        x = int(x)
        if x <= 0:
            raise argparse.ArgumentTypeError(
                "%r must be greater than 0" % (x,))
        return x

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-o", "--out", default="out.mid",
                        type=str,
                        help="set the output file")

    parser.add_argument("--seed",
                        type=str,
                        help="set a different seed")

    parser.add_argument("--bpm",
                        type=positive_int,
                        help="override beats per minute")

    parser.add_argument("--lead",
                        type=restricted_float,
                        default=1.0,
                        help="fine-tune lead coherence vs variety")

    parser.add_argument("--rhythm",
                        type=restricted_float,
                        default=1.0,
                        help="fine-tune rhythm coherence vs variety")

    parser.add_argument("--drums",
                        type=restricted_float,
                        default=1.0,
                        help="fine-tune drums coherence vs variety")

    parser.add_argument("--length",
                        help="length in bar groups",
                        default=4,
                        type=positive_int)

    parser.add_argument("--key", default="E",
                        choices=["C", "C#", "D", "D#", "E", "F",
                                 "F#", "G", "G#", "A", "A#", "B"],
                        type=str,
                        help="set the song key")

    parser.add_argument("--scale", default="Major",
                        choices=["Major",
                                 "LydianMode",
                                 "MixolydianMode",
                                 "AeolianMode",
                                 "DorianMode",
                                 "PhrygianMode",
                                 "PhrygianDominant",
                                 "DoubleHarmonic"],
                        type=str,
                        help="set the scale")

    parser.add_argument("-t", "--test", help="run tests",
                        action="store_true")

    args = parser.parse_args()

    key_to_int = {"C": C, "C#": Cs, "D": D, "D#": Ds, "E": E,
                  "F": F, "F#": Fs, "G": G, "G#": Gs, "A": A,
                  "A#": As, "B": B}

    scale_to_blueprint = {"Major": MajorScale,
                          "LydianMode": LydianMode,
                          "MixolydianMode": MixolydianMode,
                          "AeolianMode": AeolianMode,
                          "DorianMode": DorianMode,
                          "PhrygianMode": PhrygianMode,
                          "LocrianMode": LocrianMode,
                          "PhrygianDominant": PhrygianDominant,
                          "DoubleHarmonic": DoubleHarmonic}

    style = style_54()

    # style.lead = Lead7_fifths
    # style.rhythm = Lead2_sawtooth

    style.key = key_to_int[args.key]

    style.scale = scale_to_blueprint[args.scale]

    style.lead_amount = args.lead
    style.rhythm_amount = args.rhythm
    style.drums_amount = args.drums

    if args.seed:
        StyleManager().reseed(args.seed)

    if args.bpm:
        style.bpm = args.bpm

    set_style_54(style)

    composer = Composer(args.out)
    composer.compose(args.length)
    composer.save()

    if args.test:
        run_tests()
