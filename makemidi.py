from midiutil import MIDIFile


def create_midi(midi_filename="major-scale.mid"):
    degrees = [60, 62, 64, 65, 67, 69, 71, 72]  # MIDI note number
    track = 0
    channel = 0
    time = 0    # In beats
    duration = 1    # In beats
    tempo = 60   # In BPM
    volume = 100  # 0-127, as per the MIDI standard

    # One track, defaults to format 1 (tempo track is created
    MyMIDI = MIDIFile(1, adjust_origin=True)
    # automatically)
    MyMIDI.addTempo(track, time, tempo)

    for i, pitch in enumerate(degrees):
        MyMIDI.addNote(track, channel, pitch, time + i, duration, volume)

    with open(midi_filename, "wb") as output_file:
        MyMIDI.writeFile(output_file)
