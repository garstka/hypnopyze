from hypnopyze.test import *
import argparse

parser = argparse.ArgumentParser()
# parser.add_argument("seed")
parser.parse_args()


def main():
    print("Test")
    test_scales()
    test_compose()
