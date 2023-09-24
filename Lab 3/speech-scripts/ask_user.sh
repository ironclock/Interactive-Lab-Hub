#!/bin/bash

echo 'What is your zip code?' | piper --model en_US-lessac-medium --output-raw | aplay -r 22050 -f S16_LE -t raw -

python test_microphone.py -m en
