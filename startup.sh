#!/bin/bash
sudo pigpiod &
python3 /home/renessmey/apps/astroboy/astroIR.py | tee -a /home/renessmey/apps/astroboy/log.txt
