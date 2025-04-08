# Piper for text to speech

Ever want to read an article, but actually have some dishes or other manual task to do? No problem, just use Piper-TTS to listen to it instead.

Piper-TTS is lightweight, easy script to read marked text to you! Mark, hit shortcut, listen ...

Based on the popular [piper project](https://github.com/rhasspy/piper).

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

based on the [piper project](https://github.com/rhasspy/piper)

download models from [here](https://github.com/rhasspy/piper/blob/master/VOICES.md) and rename the json file to `{model}.onnx.json`. By default we use `en_US-libritts_r-medium.onnx` and its config file `en_US-libritts_r-medium.onnx.json`. Currently , these can be downloaded with the following commands:
```bash
wget https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/libritts_r/medium/en_US-libritts_r-medium.onnx
wget https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/libritts_r/medium/en_US-libritts_r-medium.onnx.json
```

find available voice examples [here](https://rhasspy.github.io/piper-samples/)

## Usage
The easiest way to use Piper-TTS by connecting the `piper-tts.py` file to a keyboard shortcut. On linux, you can for example assing CTRL+ALT+R to run `/usr/bin/python3 $HOME/src/piper-tts/piper-tts.py`. 

That's it, mark some text, hit the shortcut and listen.

## License

Like Piper, this project is published under the MIT License.
