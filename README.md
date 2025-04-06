<div align="center">
<img src="https://raw.githubusercontent.com/YZUCAM/XYZ_Controller/main/docsrc/xyz_ui_example.png"><br><br>
</div>

# XYZ_Controller
This program is designed particular for lab used xyz three axises piezo translation stage. Very handy for ones doing microscope based data acquisition. 

## Key Features
- real time location monitor
- closed loop coordinates tracking
- Keyboard and mouse compatible
- Keyboard locking
- dynamic moving speed control

## Installation
pip install pyqt5<br>
pip install matplotlib

## How to use
Directly run xyzController_main.py<br>
User can record current location information by simple click + button. Later on, the stage can go back to this location by clicking blue GO button. 

For different piezo stage, users need to configurate their own device and make sure it can talk to the PC.<br>
