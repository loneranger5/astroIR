#!/bin/bash
kill -9 `pidof pigpiod`
kill -9 `ps -aux | grep astroIR.py | grep python3 | awk '{print $2}'`
echo "astro killed @ `date`" >> /home/renessmey/apps/astroboy/kill_log.txt
