# SoundTriggeredKeyPress 
SoundTriggeredKeyPress listens for a specific sound level and triggers keyboard events based on the detected sound intensity. <br />
It starts by waiting for a mouse click to activate sound detection. Once activated, if the sound level exceeds a specified threshold, it simulates pressing the spacebar.<br />
Well designed for use with Droidstar,DUDE-Star to adding voice-activated switch capability.<br />
<br />
Required python library: <br />
pip install pyaudio numpy pyautogui <br />
<br />
or download from release that well packed into single executeable.<br />
<br />
## Options: <br />
  --time [seconds]     : Duration to sleep after each keydown event. Default is 2 seconds. <br />
  --thres [level]      : Sound intensity threshold to trigger the keydown event. Default is 500. <br />
  -s [device index]    : Index of the audio device to use for input. Use -l to list all devices. <br />
  -l                   : List all available audio input devices and exit. <br />
<br />
## Usage Examples: <br />
  List available audio input devices: python SoundTriggeredKeyPress.py -l <br />
  Start detection with custom settings: python SoundTriggeredKeyPress.py --time 1.5 --thres 600 -s 2 <br />
  
