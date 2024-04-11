import argparse
import pyaudio
import numpy as np
import pyautogui
import time
from pynput import mouse

# Program Instructions
program_description = """
SoundTriggeredKeyPress listens for a specific sound level and triggers keyboard events based on the detected sound intensity. 
It starts by waiting for a mouse click to activate sound detection. Once activated, if the sound level exceeds a specified threshold, 
it simulates pressing the spacebar.

Options:
  --time [seconds]     : Duration to sleep after each keydown event. Default is 2 seconds.
  --thres [level]      : Sound intensity threshold to trigger the keydown event. Default is 500.
  -s [device index]    : Index of the audio device to use for input. Use -l to list all devices.
  -l                   : List all available audio input devices and exit.

Usage Examples:
  List available audio input devices: python SoundTriggeredKeyPress.py -l
  Start detection with custom settings: python SoundTriggeredKeyPress.py --time 1.5 --thres 600 -s 2
  
by Watchara Amasiri
awatchar@engr.tu.ac.th
Thammasat School of Engineering
THAILAND
"""

print(program_description)  # Echo program instructions and details

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Starts sound level detection upon a mouse click and triggers a key press when the sound exceeds a threshold.',
                                 formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('--time', type=float, default=1.5, help='Time in seconds to sleep after each keydown event. Default is 2 seconds.')
parser.add_argument('--thres', type=int, default=500, help='Threshold for sound detection to trigger the keydown event. Default is 500.')
parser.add_argument('-s', type=int, help='Index of the audio device to use for input.')
parser.add_argument('-l', action='store_true', help='List all available audio input devices and exit.')
args = parser.parse_args()

# Initialize PyAudio
p = pyaudio.PyAudio()

# List devices if requested
if args.l:
    def list_audio_devices(p):
        info = p.get_host_api_info_by_index(0)
        num_devices = info.get('deviceCount')
        for i in range(0, num_devices):
            if p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels') > 0:
                print("Device ID:", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
    list_audio_devices(p)
    p.terminate()
    exit()

# Get device name
def get_device_name(device_index):
    if device_index is not None:
        device_info = p.get_device_info_by_index(device_index)
        return device_info.get('name')
    return "Default Device"

# Callback for mouse click: begins sound detection process
def on_click(x, y, button, pressed):
    if pressed:
        print(f"Mouse clicked at ({x}, {y}) with {button}.")
        print(f"Starting sound detection with device '{get_device_name(args.s)}', time to sleep: {args.time}s, threshold: {args.thres}")
        return False  # Stop listener

# Wait for a mouse click to start the main process
with mouse.Listener(on_click=on_click) as listener:
    listener.join()

# Parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
SOUND_THRESHOLD = args.thres
sleep_time = args.time
device_index = args.s

# Callback function to process audio input
def callback(in_data, frame_count, time_info, status):
    audio_data = np.frombuffer(in_data, dtype=np.int16)
    if np.abs(audio_data).mean() > SOUND_THRESHOLD:
        print(f"PTT Keyed.")
        pyautogui.keyDown('space')
        time.sleep(sleep_time)
    else:
        pyautogui.keyUp('space')
    return (in_data, pyaudio.paContinue)

# Open stream with callback and specified device index
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                stream_callback=callback,
                input_device_index=device_index)

# Start the stream
stream.start_stream()

# Keep the stream active; stop with Ctrl+C or similar interrupt
try:
    while stream.is_active():
        pass
except KeyboardInterrupt:
    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()
    print("Stream stopped")
