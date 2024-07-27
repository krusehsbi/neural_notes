from utility import getNoteMinor, normalize
import mido
from mido import Message
import time
import numpy as np

# Open a MIDI output port
output_port = mido.open_output()

# Global variable to store the time of the last processed data
last_processed_time = 0

def cacophony(eeg_data):
        for channel in eeg_data['data']:
            normalized_data = normalize(channel)
            for note in normalized_data:
                output_port.send(Message('note_on', note=note, velocity=64, time=0))
                output_port.send(Message('note_off', note=note, velocity=64, time=100))


def getScaleOctaves(brainwaves, base=60, interval=0.25, start=0, end=127, octaves=2):
    """
    Process incoming brainwaves data at specified intervals and convert to MIDI signals.

    Args:
    - brainwaves (dict): The brainwaves data from Neurosity.
    - output_port (mido.Output): The MIDI output port to send messages to.
    - base (int): Base MIDI note number (Middle C = 60).
    - interval (float): Time interval in seconds between data processing.
    - start (int): Start of the EEG data range (normalized).
    - end (int): End of the EEG data range (normalized).
    - octaves (int): Number of octaves to span.
    """
    global last_processed_time

    current_time = time.time()
    if current_time - last_processed_time < interval:
        return  # Skip processing if interval has not passed

    last_processed_time = current_time  # Update the last processed time
    velocity = 64  # Fixed velocity
    eeg_values = brainwaves.get('data', [])  # Safely get EEG data

    if not eeg_values:
        print("Error: No EEG data provided.")
        return

    # Normalize the EEG data
    normalized_data = normalize(eeg_values)

    # Aggregate the normalized data (using mean or median)
    aggregated_value = np.mean(normalized_data)  # or np.median(normalized_data)

    # Map the aggregated value to a MIDI note
    note_range = octaves * 12  # Number of semitones in the range
    scale_value = (aggregated_value - start) / (end - start) * note_range
    midi_note = base + int(scale_value)

    # Bound the MIDI note to a valid range
    midi_note = max(0, min(127, midi_note))

    # Send the note off for previous note
    if hasattr(getScaleOctaves, "aktuelleNote") and getScaleOctaves.aktuelleNote:
        msg = mido.Message('note_off', note=getScaleOctaves.aktuelleNote)
        output_port.send(msg)

    # Send the note on message
    getScaleOctaves.aktuelleNote = midi_note  # Store the current note
    msg = mido.Message('note_on', note=midi_note, velocity=velocity)
    output_port.send(msg)

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
        output_port.send(msg)# Define a mapping of EEG bands to MIDI chords


# Define a mapping of EEG bands to MIDI chords
BAND_TO_CHORD = {
    'alpha': [60, 64, 67],  # C major chord
    'beta': [62, 65, 69],   # D minor chord
    'delta': [64, 67, 71],  # E minor chord
    'gamma': [65, 69, 72],  # F major chord
    'theta': [67, 71, 74]   # G major chord
}

# Define thresholds for each band
BAND_THRESHOLDS = {
    'alpha': 1.5,
    'beta': 1.5,
    'delta': 5.0,
    'gamma': 1.5,
    'theta': 3.0
}

def play_chord_specific(chord, velocity=64):
    """Sends a chord to the MIDI output."""
    for note in chord:
        note = int(note)
        msg = mido.Message('note_on', note=note)
        output_port.send(msg)

def stop_chord(chord):
    """Stops playing a chord."""
    for note in chord:
        note = int(note)
        msg = mido.Message('note_off', note=note)
        output_port.send(msg)

def processPowerByBand(data, play_interval=1.0):
    """
    Processes EEG power band data and plays the chord for the loudest band.
    
    Args:
    - data (dict): Dictionary containing power levels for each EEG band.
    - output_port (mido.Output): The MIDI output port to send messages to.
    """
    global last_processed_time
    power_by_band = data.get('data', {})
    current_time = time.time()

    # Check if the interval time has passed
    if current_time - last_processed_time < play_interval:
        return  # Skip processing if the interval has not passed

    # Find the band with the maximum average power level
    max_band = None
    max_power = -float('inf')

    for band, power_levels in power_by_band.items():
        if not power_levels:
            continue

        # Calculate the average power level for the band
        avg_power = np.mean(power_levels)

        # Check if this band is louder than previous ones
        if avg_power > BAND_THRESHOLDS.get(band, 0) and avg_power > max_power:
            max_power = avg_power
            max_band = band

    # Stop all chords if a loudest band was found
    for band in BAND_TO_CHORD:
        chord = BAND_TO_CHORD[band]
        stop_chord(chord)

    # Play the chord for the loudest band
    if max_band:
        chord = BAND_TO_CHORD.get(max_band, [])
        if chord:
            play_chord(chord)
    
    last_processed_time = current_time  # Update last processed time

    # Debugging output
    print(f"Loudest Band: {max_band}, Avg Power: {max_power}, Threshold: {BAND_THRESHOLDS.get(max_band, 0)}")