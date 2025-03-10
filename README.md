# Piper for text to speech

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
wget https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/libritts_r/medium/en_US-libritts_r-medium.onnx.json -o en_US-libritts_r-medium.onnx.json
```

find available voice examples [here](https://rhasspy.github.io/piper-samples/)

