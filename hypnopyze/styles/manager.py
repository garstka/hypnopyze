from hypnopyze.patterns.collection import PatternCollection
from hypnopyze.styles.style import Style
from numpy.random import RandomState


# Borg that controls the style of the generated songs.
class StyleManager:
    __shared_state = {}

    __pattern_collection = PatternCollection()
    __style = Style()
    __prng = RandomState(75123481)

    def __init__(self):
        self.__dict__ = self.__shared_state

    # Returns the property collection
    @property
    def pattern_collection(self):
        return self.__pattern_collection

    # Returns the current style
    @property
    def style(self):
        return self.__style

    # Changes the current style
    @style.setter
    def style(self, value):
        self.__style = value

    # Returns the prng
    @property
    def prng(self):
        return self.__prng

    # Reseeds the prng
    def reseed(self, seed):
        self.__prng = RandomState(hash(seed))
