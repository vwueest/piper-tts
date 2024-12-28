import time
import subprocess
import pyperclip
import os.path as path
import piper
import os


directory = path.dirname(path.abspath(__file__))
piper_dir = os.path.join(os.path.dirname(piper.__file__),'..','..','..','..','bin','piper')
voice_model = 'en_US-libritts_r-medium.onnx'

def notify(text):
    subprocess.Popen(f"notify-send '{text}'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

def read_aloud_stream(text):
    notify('Reading aloud')
    text = text.replace("'", "`")
    text = text.replace(". ", "., ")
    command = f"echo '{text}' |  {piper_dir} --model {directory}/{voice_model} -s 7 --output-raw | aplay -r 22050 -f S16_LE -t raw -"
    subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print('done')
    time.sleep(0.01)

def read_aloud_file(text):
    notify('Reading aloud')
    text = text.replace("'", "`")
    command = f"echo '{text}' | {piper_dir} --model {directory}/{voice_model} -s 7 --output_file {directory}/output.wav; open {directory}/output.wav"
    print(command)
    subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print('done')
    time.sleep(0.01)

def main():
    clipboard_content = pyperclip.paste()
    print(clipboard_content)
    read_aloud_file(clipboard_content)

if __name__ == "__main__":
    main()
