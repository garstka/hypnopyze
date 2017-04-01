from hypnopyze.test import *
from hypnopyze.styles import patterns_54
import argparse

parser = argparse.ArgumentParser()
# parser.add_argument("seed")
parser.parse_args()


def main():
    print("Test")
    patterns_54()

    test_scales()
    test_compose()
