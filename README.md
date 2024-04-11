# DroidstarVox
SoundTriggeredKeyPress listens for a specific sound level and triggers keyboard events based on the detected sound intensity. It starts by waiting for a mouse click to activate sound detection. Once activated, if the sound level exceeds a specified threshold,  it simulates pressing the spacebar.

Options:
  --time [seconds]     : Duration to sleep after each keydown event. Default is 2 seconds.
  --thres [level]      : Sound intensity threshold to trigger the keydown event. Default is 500.
  -s [device index]    : Index of the audio device to use for input. Use -l to list all devices.
  -l                   : List all available audio input devices and exit.

Usage Examples:
  List available audio input devices: python SoundTriggeredKeyPress.py -l
  Start detection with custom settings: python SoundTriggeredKeyPress.py --time 1.5 --thres 600 -s 2
  
