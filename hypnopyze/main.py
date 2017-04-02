from hypnopyze.test import *
from hypnopyze.styles.sample import *
import argparse

parser = argparse.ArgumentParser()
# parser.add_argument("seed")
parser.parse_args()


def main():
    print("Test")
    set_style_54(style_54())

    test_scales()
    test_compose()
