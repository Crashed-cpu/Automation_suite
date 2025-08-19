#!/bin/bash

# Install system dependencies
apt-get update
apt-get install -y \
    python3-pyaudio \
    portaudio19-dev \
    python3-dev \
    espeak

# Install Python dependencies
pip install -r requirements.txt
