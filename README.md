# Piper for text to speech

Ever want to read an article, but actually have some dishes or other manual task to do? No problem, just use Piper-TTS to listen to it instead. 

Piper-TTS is a lightweight, easy script to read marked text to you! Mark, hit shortcut, listen ... 🗣️💬

Piper-TTS is based on the popular [piper project](https://github.com/rhasspy/piper).

## Installation

This project depends on xclip on linux. Install with
```bash
sudo apt-get install xclip
```

You may want to create a conda env
```bash
conda create python=3.11 --no-default-packages --name "piper"
```

Install the required python packages with
```bash
pip install -r requirements.txt
```

Download models from [here](https://github.com/rhasspy/piper/blob/master/VOICES.md) and rename the json file to `{model}.onnx.json`. By default we use `en_US-libritts_r-medium.onnx` and its config file `en_US-libritts_r-medium.onnx.json`. Currently , these can be downloaded with the following commands:
```bash
wget https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/libritts_r/medium/en_US-libritts_r-medium.onnx
wget https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/libritts_r/medium/en_US-libritts_r-medium.onnx.json
```

To find other voices, find available examples [here](https://rhasspy.github.io/piper-samples/).

## Usage
The easiest way to use Piper-TTS is by running the `piper-tts.py` file when hitting a keyboard shortcut. On linux, you can for example assing CTRL+ALT+R to run `$HOME/anaconda/envs/piper/bin/piper/python3 $HOME/src/piper-tts/piper-tts.py`. 

That's it, mark some text, hit the shortcut and listen.

## License

Like Piper, this project is published under the MIT License.
