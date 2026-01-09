#!/bin/bash
# https://www.javatpoint.com/steps-to-write-and-execute-a-shell-script
# chmod +x xbox_codesys.sh
# execute: ./xbox_codesys.sh
# crontab -e
# @reboot sudo bash /home/xlh/xemax/xbox/xbox_codesys.sh
# python -m venv venv
# source venv/bin/activate
cd /home/xlh/xbox
source venv/bin/activate
python xbox_codesys.py
deactivate
