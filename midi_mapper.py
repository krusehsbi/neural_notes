from utility import getNoteMinor, normalize
import mido
from mido import Message
import time
import numpy as np

# Open a MIDI output port
output_port = mido.open_output()

def cacophony(eeg_data):
        for channel in eeg_data['data']:
            normalized_data = normalize(channel)
            for note in normalized_data:
                output_port.send(Message('note_on', note=note, velocity=64, time=0))
                output_port.send(Message('note_off', note=note, velocity=64, time=100))


def getScaleOctaves(brainwaves, base=60, sleep=0.5, start=0, end=127, octaves=1):
    """
    Process incoming brainwaves data and convert it to MIDI signals.

    Args:
    - brainwaves (dict): The brainwaves data from Neurosity, expected to contain a 'data' key with EEG values.
    - output_port (mido.Output): The MIDI output port to send messages to.
    - base (int, optional): Base MIDI note number (Middle C = 60). Defaults to 60.
    - sleep (float, optional): Duration to wait between notes in seconds. Defaults to 0.5.
    - start (int, optional): Start of the EEG data range (normalized). Defaults to 0.
    - end (int, optional): End of the EEG data range (normalized). Defaults to 127.
    - octaves (int, optional): Number of octaves to span. Defaults to 2.
    """
    velocity = 64  # Fixed velocity
    eeg_values = brainwaves.get('data', [])  # Safely get EEG data

    if not eeg_values:
        print("Error: No EEG data provided.")
        return

    # Normalize the EEG data
    normalized_data = normalize(eeg_values)
    print("Normalized EEG Data:", normalized_data)

    # Aggregate the normalized data (using mean or median)
    aggregated_value = np.mean(normalized_data)  # or np.median(normalized_data)
    print("Aggregated EEG Value:", aggregated_value)

    # Map the aggregated value to a MIDI note
    note_range = octaves * 12  # Number of semitones in the range
    scale_value = (aggregated_value - start) / (end - start) * note_range
    midi_note = base + int(scale_value)

    # Bound the MIDI note to a valid range
    midi_note = max(0, min(127, midi_note))
    print("Calculated MIDI Note:", midi_note)

    # Send the note off for previous note
    if hasattr(getScaleOctaves, "aktuelleNote") and getScaleOctaves.aktuelleNote:
        msg = mido.Message('note_off', note=getScaleOctaves.aktuelleNote)
        output_port.send(msg)

    # Send the note on message
    getScaleOctaves.aktuelleNote = midi_note  # Store the current note
    msg = mido.Message('note_on', note=midi_note, velocity=velocity)
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