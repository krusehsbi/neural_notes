import numpy as np

# Function to normalize data to the range 0-127
def normalize(data):
    min_val = np.min(data)
    max_val = np.max(data)
    return [int((value - min_val) / (max_val - min_val) * 127) for value in data]

def getNoteMinor(eegData, base, start, end, octaves):
    """
    Determine the MIDI note to play based on EEG data.
    
    Args:
    - eegData (float): The current EEG value.
    - base (int): The base note.
    - start (float): The lowest EEG data value that maps to the lowest note.
    - end (float): The highest EEG data value.
    - octaves (int): Number of octaves to play.
    
    Returns:
    - int: The MIDI note number.
    """
    # Steps for a minor scale (1: half step, 2: whole step)
    noteSteps = [0, 2, 1, 2, 2, 1, 2]

    # Expand steps for multiple octaves
    if octaves > 1:
        noteSteps += [2, 2, 1, 2, 2, 1, 2] * (octaves - 1)

    # Clamp eegData to within the start and end range
    if eegData < start:
        return base
    elif eegData > end:
        return base + sum(noteSteps)

    # Calculate the steps to take based on the EEG data
    notes = octaves * 7
    rang = end - start
    steps = rang / notes
    data = eegData - start
    ds = data / steps

    note = base
    for i in range(int(ds + 1)):
        if i < len(noteSteps):
            note += noteSteps[i]

    return note
