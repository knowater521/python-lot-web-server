#!/bin/bash

path="/home/pi/pythonproject/web-server"

chmod 777 $path/appRelay.py
sudo nohup python3 $path/appRelay.py &