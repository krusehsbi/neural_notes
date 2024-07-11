from neurosity import NeurositySDK
from dotenv import load_dotenv
from midi_mapper import cacophony, getScaleOctaves, play_chord
import os
import sys

load_dotenv()

neurosity = NeurositySDK({
    "device_id": os.getenv("NEUROSITY_DEVICE_ID"),
})

neurosity.login({
    "email": os.getenv("NEUROSITY_EMAIL"),
    "password": os.getenv("NEUROSITY_PASSWORD")
})

mode = sys.argv[1]

if(mode == 'brainwaves'):
    unsubscribe = neurosity.brainwaves_raw(getScaleOctaves)
elif(mode == 'kinesis'):
    unsubscribe = neurosity.kinesis('right_arm', play_chord)