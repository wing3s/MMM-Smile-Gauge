

## Requirements
- Python 2.7
  - openCV > 3.4
  - imutils
- Node.js

## Installation
### Smile Gauge Module
```bash
# Go to MagicMirror main directory
cd MagicMirror/modules
git clone https://github.com/wing3s/MMM-Smile-Gauge.git
cd MMM-Smile-Gauge
bash detector/setup.sh  # Download Haar cascade data
```
### Configuration
Add following in `MagicMirror/config/config.js` to register the module.
```javascript
// Example
{
    module: "MMM-Smile-Gauge",
    position: "lower_third"
},
```


### Python Packages
#### openCV
###### Mac OSX
```pip install opencv-python```
###### Raspberry Pi
- [Basic for quick start](https://www.pyimagesearch.com/2017/09/04/raspbian-stretch-install-opencv-3-python-on-your-raspberry-pi)
or
- [Advanced with NEON & VFPV3 optimizations on ARM processors](https://www.pyimagesearch.com/2017/10/09/optimizing-opencv-on-the-raspberry-pi)

#### Imutils
```pip install imutils```

### Camera
###### Mac OSX
Will prompt window to ask permission of camera.
###### Raspberry Pi
- [Hardware and setup instructions](https://thepihut.com/blogs/raspberry-pi-tutorials/16021420-how-to-install-use-the-raspberry-pi-camera)
- [Turn on camera permission](https://stackoverflow.com/questions/51645531/error-displaying-video-stream-using-opencv-on-raspberry-pi) by `sudo modprobe bcm2835-v4l2`


## Test
```bash
# Check if python, opencv, webcam are installed properly
cd MMM-Smile-Gauge/detector
python detector.py
```

## Customization
### Face/smile detector parameters
  Fine tune parameters in `MMM-Smile-Gauge/detector/detector.py`.
### Replace gauge images
  Simply change square images in `MMM-Smile-Gauge/public` folder.

## Performance
[Enabling Open GL driver for Raspberry Pi](https://github.com/MichMich/MagicMirror/wiki/Configuring-the-Raspberry-Pi) is required. Both face detection and Electron for Magic Mirror are CPU heavy.

## Reference
- [Real-time smile detection](http://pushbuttons.io/blog/2015/4/27/smile-detection-in-python-opencv)
- [Improve Python openCV FPS of webcam](https://www.pyimagesearch.com/2015/12/21/increasing-webcam-fps-with-python-and-opencv/)
