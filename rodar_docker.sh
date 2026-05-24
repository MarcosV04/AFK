#!/bin/bash

xhost +local:docker

docker run -it \
--device=/dev/video0 \
-e DISPLAY=$DISPLAY \
-v /tmp/.X11-unix:/tmp/.X11-unix \
afk-game