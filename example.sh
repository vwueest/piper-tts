#!/usr/bin/bash

echo 'This is a short example text to remember how this all worked exactly' |  piper --model ./en_US-libritts_r-medium.onnx -s 7 --output-raw |   aplay -r 22050 -f S16_LE -t raw -
