import time
import subprocess
import pyperclip
import os.path as path
import piper
import os
import sys
from pynput import keyboard
import threading

directory = path.dirname(path.abspath(__file__))
piper_dir = os.path.join(os.path.dirname(piper.__file__),'..','..','..','..','bin','piper')
voice_model = [directory + "/" + 'en_US-libritts_r-medium.onnx','-s','7']
voice_parameters = ["--sentence-silence", "0.2", "--noise-scale", "0.3", "--length-scale", "1.2"]
pressed_keys = set()

def notify(text):
    subprocess.Popen(f"notify-send '{text}'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

def read_aloud_stream(text):
    text = text.replace('*', '')
    text = text.replace('\n', ' ')
    notify('Reading aloud, press CTRL+ALT to stop')
    echo_process = subprocess.Popen(["echo", text], stdout=subprocess.PIPE)
    piper_process = subprocess.Popen([piper_dir, "--model"] + voice_model + voice_parameters + ["--output-raw"], stdin=echo_process.stdout, stdout=subprocess.PIPE)
    aplay_process = subprocess.Popen(["aplay", "-r", "22050", "-f", "S16_LE", "-t", "raw", "-"], stdin=piper_process.stdout, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    echo_process.stdout.close()
    piper_process.stdout.close()
    return aplay_process

def read_aloud_file(text):
    notify('Reading aloud')
    echo_process = subprocess.Popen(["echo", text], stdout=subprocess.PIPE)
    print([piper_dir, "--model"] + voice_model + voice_parameters + ["--output_file", directory+'/output.wav'])
    piper_process = subprocess.Popen([piper_dir, "--model"] + voice_model + voice_parameters + ["--output_file", directory+'/output.wav'], stdin=echo_process.stdout, stdout=subprocess.PIPE)
    time.sleep(0.1)
    aplay_process = subprocess.Popen(["open",directory+"/output.wav"], stdin=piper_process.stdout, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    echo_process.stdout.close()
    piper_process.stdout.close()
    aplay_process.stdout.close()

def on_press(key):
    pressed_keys.add(key)
    
    # Check if both CTRL and ALT are pressed
    if keyboard.Key.alt in pressed_keys and (keyboard.Key.ctrl_l in pressed_keys or keyboard.Key.ctrl_r in pressed_keys):
        return False  

def on_release(key):
    # Remove the released key from the set
    pressed_keys.discard(key)

def get_selected_text():
    try:
        return subprocess.check_output(['xclip', '-o', '-selection', 'primary']).decode('utf-8').strip()
    except:
        subprocess.run(["notify-send", "Install xclip"])

def clean_text(text):
    return text.replace('*', '').replace('\n', ' ')

def main():
    if len(sys.argv) > 1:
        # If a file is provided as an argument, read from the file
        with open(sys.argv[1], 'r') as file:
            text_to_read = file.read()
        print('converting the following text:')
        print(text_to_read)
        read_aloud_file(text_to_read)
        print('done')
    else:
        # If no file is provided, use the original method to get the text
        text_to_read = get_selected_text()
        text_to_read = clean_text(text_to_read)

        print(text_to_read)

        # Start recording
        read_aloud_stream(text_to_read)

        # Start listening to keyboard events
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()  # Wait for the listener to finish

        subprocess.Popen(f"killall piper", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

if __name__ == "__main__":
    main()
