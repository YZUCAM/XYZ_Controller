# Closed loop motor Conex CC controller module for xyz stage

""" Modified by Dr. Yi Zhu, University of Cambridge,  01-07-2022"""

"""Initialization Start
    The script within Initialization Start and Initialization End is needed for properly
    initializing Command Interface for CONEX-CC instrument.
    The user should copy this code as is and specify correct paths here.
"""

import sys

#Command Interface DLL can be found here.
print ("Adding location of Newport.CONEXCC.CommandInterface.dll to sys.path")

sys.path.append(r'C:\Program Files\Newport\MotionControl\CONEX-CC\Bin')
sys.path.append(r'C:\Program Files (x86)\Newport\MotionControl\CONEX-CC\Bin')

# The CLR module provide functions for interacting with the underlying NET runtime
# Installed pythonnet package not clr package!

import clr

# Add reference to assembly and import names from namespace
clr.AddReference('Newport.CONEXCC.CommandInterface')
from CommandInterfaceConexCC import *
#import System
#============================================================

# Instrument Initialization
# The key should have double slashes since
# (one of them is escape character)
"""Here is hard coded, COM7, COM8, COM9 are usb port in Cambridge Graphene Center Photonic
lab bay 2 computer"""


class Conex_xyz(ConexCC):

    def __init__(self, com_port):
        super().__init__()

        instrument = com_port
        instrumentKey = instrument
        print ('Instrument Key=>', instrument)

        # create a device instance and open communication with the instrument
        #CC = ConexCC()
        ret = self.OpenInstrument(instrumentKey)
        print ('OpenInstrument => ', ret)           # 0 : no error; 1: error

    def identify(self):
        result, response, errString = self.ID_Get(1, '', '')
        if result == 0:
            print('Stage Identifier => ', response)
        else:
            print('Error=>', errString)

    def get_current_position(self):
        result, response, errString = self.TP(1, 0, '')
        if result == 0:
            print('position=>', response)
        else:
            print('Error=>', errString)
        return response

    def move_absolute(self, target_position):
        self.PA_Set(1, float(target_position), '')

    def home(self):
        """
        only executable in NOT REFERENCED mode
        """
        res, errString = self.OR(1, '')
        if res == 0:
            pass
        else:
            print('Error=>', errString)


if __name__ == '__main__':
    import time
    my_x = Conex_xyz('COM7')
    my_y = Conex_xyz('COM8')
    my_x.identify()
    my_x.move_absolute(12.0)
    #my_xyz.home()
    time.sleep(1)
    res_x = my_x.get_current_position()
    my_y.identify()
    my_y.move_absolute(6.0)
    time.sleep(1)
    res_y = my_y.get_current_position()

    my_x.CloseInstrument()
    my_y.CloseInstrument()

    
        































    














