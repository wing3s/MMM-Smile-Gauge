#!/bin/bash
DIRECTORY=$(cd `dirname $0` && pwd)

# Download opencv data
mkdir -p data
wget --directory-prefix=$DIRECTORY/data https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_smile.xml 
wget --directory-prefix=$DIRECTORY/data https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml
