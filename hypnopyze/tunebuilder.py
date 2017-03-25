from miditime.miditime import MIDITime


class TuneBuilder:

    def __init__(self):
        self.mt = MIDITime()
        self.mt = MIDITime(120, 'out.mid')

    def generate(self):
        mt = self.mt
        #


