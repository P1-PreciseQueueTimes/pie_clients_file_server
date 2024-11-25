#! /bin/bash

python -m venv .venv
source .venv/bin/activate
pip install pyshark
pip install requests
curl https://main-server-5few.onrender.com/get/testing/receiver --output output.zip
unzip -o output.zip
python receiver.py

