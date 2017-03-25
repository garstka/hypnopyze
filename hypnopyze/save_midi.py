from midiutil.MidiFile3 import MIDIFile
from miditime.miditime import MIDITime


# MIDITime.save_midi() method altered to allow many instruments
def save_midi(self: MIDITime, instruments_per_channel: [int] = None):
    if instruments_per_channel is None:
        instruments_per_channel = []

    # Create the MIDIFile Object with 1 track
    self.MIDIFile = MIDIFile(len(self.tracks))

    for channel, instrument in enumerate(instruments_per_channel):
        self.MIDIFile.addProgramChange(0, channel, 0, instrument)

    for i, note_list in enumerate(self.tracks):

        # Tracks are numbered from zero. Times are measured in beats.
        track = i
        time = 0

        # Add track name and tempo.
        self.MIDIFile.addTrackName(track, time, "Track %s" % i)
        self.MIDIFile.addTempo(track, time, self.tempo)

        for n in note_list:
            if len(n) == 2:
                note = n[0]
                channel = n[1]
            else:
                note = n
                channel = 0
            self.add_note(track, channel, note)

    # And write it to disk.
    binfile = open(self.outfile, 'wb')
    self.MIDIFile.writeFile(binfile)
    binfile.close()
