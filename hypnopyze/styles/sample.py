from hypnopyze.patterns.builder import *
from hypnopyze.instruments import *
from hypnopyze.drums import *
from hypnopyze.styles.manager import *
from .patterns.basic54 import *


# Returns a style for the 5/4 signature (for customization before set_style_54)
def style_54():
    style = Style()

    style.use_lead = True
    style.use_rhythm = True
    style.use_drums = True

    style.lead = AcousticGrandPiano

    style.base_beats_per_bar = 5

    style.resolution = 4

    style.key = E

    style.bpm = 240
    style.bar_group = 4

    return style


# Generates a pattern set for the 5/4 time signature.
# - Takes the 5/4 style from style_54 (possibly modified)
# Returns the style with the StyleManager
def set_style_54(style: Style):
    b = PatternBuilder()

    b.num_walks = 20
    b.key = style.key

    # b.scale = [A, C, D, E, G]
    b.base_octave = DEFAULT_OCTAVE

    StyleManager().style = style

    build_lead_basic54(b)
    build_drums_bass_basic54(b)
    build_drums_hi_ride_basic54(b)
    build_drums_mixed_basic54(b)
