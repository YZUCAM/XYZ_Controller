# Initialization Start
# The script within Initialization Start and Initialization End is needed for properly
# initializing Command Interface for CONEX-CC instrument.
# The user should copy this code as is and specify correct paths here.
import sys

# Command Interface DLL can be found here.
print("Adding location of Newport.CONEXCC.CommandInterface.dll to sys.path")

sys.path.append(r'C:\Program Files (x86)\Newport\MotionControl\CONEX-CC\Bin')
sys.path.append(r'C:\Program Files\Newport\MotionControl\CONEX-CC\Bin')

# The CLR module provide functions for interacting with the underlying
# .NET runtime
import clr

# Add reference to assembly and import names from namespace
clr.AddReference('Newport.CONEXCC.CommandInterface')
from CommandInterfaceConexCC import *

# import System
# ============================================================

# Instrument Initialization
# The key should have double slashes since
# (one of them is escape character)
instrument = "COM7"
instrumentKey = instrument
print('Instrument Key=>', instrument)

# create a device instance and open communication with the instrument
CC = ConexCC()
ret = CC.OpenInstrument(instrumentKey)
print('OpenInstrument => ', ret)

"""                
# Get positive software limit
result, response, errString = CC.SR_Get(1)
if result == 0 :
    print ('positive software limit=>', response)
else:
    print ('Error=>',errString)

# Get negative software limit
result, response, errString = CC.SL_Get(1)
if result == 0 :
    print ('negative software limit=>', response)
else:
    print ('Error=>',errString)
"""
result, errString = CC.OR(1, '')
if result == 0:
    print('controller revision=>', result)
else:
    print('Error=>', errString)

# Get controller revision information
# result, response, errString = CC.VE(1, '', '')
# if result == 0:
#     print('controller revision=>', response)
# else:
#     print('Error=>', errString)
#
# # Get current position
# result, response, errString = CC.TP(1, 0, '')
# if result == 0:
#     print('position=>', response)
# else:
#     print('Error=>', errString)

# Unregister device
CC.CloseInstrument()
