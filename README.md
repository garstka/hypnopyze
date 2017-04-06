# hypnopyze
Hypnotic tune generator in Python.

## What it does

Generates pseudo-random MIDI tunes from a set of patterns for lead, rhythm and 
drums. Songs can be customized by choosing a seed, length, bpm, key, scale used
 by rhythm and lead, pattern diversity, and instrument set.

    python3 hypno.py --help 

## Requirements

Python 3 with numpy, miditime, and typing.

## Notes

Created as an assignment for a Python course, and there's much room 
for improvement. I haven't had the time to implement an elaborate song 
structure planner. Current approach is that patterns are randomly chosen 
from a subset of all patterns, which are interchangeable (compatible time 
signature). I also included only one sample "style", though it should be
 relatively simple to add an alternative by specifying another pattern set.
 
## Credits

For actual MIDI building I used MIT-licensed MIDITime by Michael Corey. I 
duplicated some of the functionality with minor changes, allowing for 
multiple instruments.