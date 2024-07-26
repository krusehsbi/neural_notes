import numpy as np

# Function to normalize data to the range 0-127
def normalize(data, new_min=0, new_max=127):
    """
    Normalize a 2D list of EEG data to a new range [new_min, new_max].

    Args:
    - data (list of lists): 2D list of EEG values.
    - new_min (int, optional): The minimum value of the normalized range. Defaults to 0.
    - new_max (int, optional): The maximum value of the normalized range. Defaults to 127.

    Returns:
    - list of lists: Normalized EEG data in the new range.
    """
    flattened_data = np.array(data).flatten()
    old_min, old_max = np.min(flattened_data), np.max(flattened_data)
    
    if old_max == old_min:
        return np.full(flattened_data.shape, new_min).tolist()
    
    normalized_data = (flattened_data - old_min) / (old_max - old_min) * (new_max - new_min) + new_min
    return normalized_data.tolist()



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
