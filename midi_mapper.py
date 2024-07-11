from utility import getNoteMinor, normalize
import mido
from mido import Message
import time

def cacophony(eeg_data):
    with mido.open_output() as output:

        for channel in eeg_data['data']:
            normalized_data = normalize(channel)
            for note in normalized_data:
                output.send(Message('note_on', note=note, velocity=64, time=0))
                output.send(Message('note_off', note=note, velocity=64, time=100))


def getScaleOctaves(brainwaves):
    """
    Callback function to handle incoming brainwaves data and convert it to MIDI signals.
    
    Args:
    - brainwaves (dict): The brainwaves data from Neurosity.
    """
    base = 60  # Middle C (C4)
    sleep = 0.5  # 500ms between notes
    start = -1000  # Adjust based on your EEG data range
    end = 1000  # Adjust based on your EEG data range
    octaves = 2  # Number of octaves to play

    # Open a MIDI output port
    output_port = mido.open_output('Neural Notes')

    medianEEGData = []
    velocity = 64
    aktuelleNote = 0

    eeg_values = brainwaves['data']  # Assuming brainwaves['data'] is a list of EEG values

    # Normalize and flatten the EEG data
    medianEEGData.extend(normalize(eeg_values))

    # Adjust for normalization
    medianEEGData[-1] += 1000

    # Release the previous note
    if aktuelleNote != 0:
        msg = mido.Message('note_off', note=aktuelleNote)
        output_port.send(msg)

    # For debugging and understanding the notes being played
    print("Current Note:", aktuelleNote)
    print("EEG Data:", medianEEGData[-1])
    print("Velocity:", velocity)

    # Determine the appropriate note from EEG data
    aktuelleNote = getNoteMinor(medianEEGData[-1], base, start, end, octaves)

    # Create and send the MIDI message
    msg = mido.Message('note_on', note=aktuelleNote, velocity=velocity)
    output_port.send(msg)
    time.sleep(sleep)

def play_chord(brainwaves):
    """
    Play a chord by sending multiple MIDI note_on messages simultaneously.
    
    Args:
    - notes (list): List of MIDI note numbers to play.
    - duration (float): Duration to hold the chord in seconds.
    - velocity (int): Velocity of the MIDI notes.
    """
    chord_notes = [60, 64, 67]
    duration = 2
    velocity = 64

    # Open a MIDI output port
    output_port = mido.open_output('Your MIDI Port Name')

    # Send note_on messages for all notes in the chord
    for note in chord_notes:
        msg = mido.Message('note_on', note=note, velocity=velocity)
        output_port.send(msg)

    # Hold the chord for the specified duration
    time.sleep(duration)

    # Send note_off messages for all notes in the chord
    for note in chord_notes:
        msg = mido.Message('note_off', note=note)
        output_port.send(msg)