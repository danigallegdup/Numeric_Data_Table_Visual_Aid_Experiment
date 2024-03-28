# -*- coding: utf-8 -*-
#
# Copyright (c) 1996-2023, SR Research Ltd., All Rights Reserved
#
# For use by SR Research licencees only. Redistribution and use in source
# and binary forms, with or without modification, are NOT permitted.
#
# Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in
# the documentation and/or other materials provided with the distribution.
#
# Neither name of SR Research Ltd nor the name of contributors may be used
# to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS ``AS
# IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# $Date: 2009/11/02 16:14:37 $
#

"""Performing research with eye-tracking equipment typically requires a long-term investment in software
tools to collect, process, and analyze data. Much of this involves real-time data collection, saccadic
analysis, calibration routines, and so on.
The EyeLink® eye-tracking system is designed to implement most of the required software base for data
collection and conversion. It is most powerful when used with the Ethernet link interface, which allows
remote control of data collection and real-time data transfer. The PyLink toolkit includes Pylink module,
which implements all core EyeLink functions and classes for EyeLink connection and the eyelink graphics,
such as the display of camera image, calibration, validation, and drift correct. The EyeLink graphics is
currently implemented using Simple Direct Media Layer (SDL: www.libsdl.org).


The Pylink library contains a set of classes and functions, which are used to program experiments on many
different platforms, such as MS-DOS, Windows, Linux, and the Macintosh. Some programming standards,
such as placement of messages in the EDF file by your experiment, and the use of special data types, have
been implemented to allow portability of the development kit across platforms. The standard messages
allow general analysis tools such as EDF2ASC converter or EyeLink Data Viewer to process your EDF files.


"""

from pylink.constants import *

from pylink.pylink_c import inRealTimeMode
from pylink.pylink_c import flushGetkeyQueue
from pylink.pylink_c import beginRealTimeMode
from pylink.pylink_c import currentTime
from pylink.pylink_c import currentUsec
#from pylink.pylink_c import currentDoubleUsec
from pylink.pylink_c import endRealTimeMode
from pylink.pylink_c import pumpDelay
from pylink.pylink_c import msecDelay
from pylink.pylink_c import alert
from pylink.pylink_c import enableExtendedRealtime
from pylink.pylink_c import getLastError
from pylink.pylink_c import enablePCRSample



try:
	from pylink.pylink_c import enableUTF8EyeLinkMessages
except:
	#means no win32 defined
	pass
from pylink.pylink_c import openCustomGraphicsInternal
from pylink.pylink_c import bitmapSave
from pylink.pylink_c import sendMessageToFile
from pylink.pylink_c import openMessageFile
from pylink.pylink_c import closeMessageFile

from pylink.tracker import EndBlinkEvent
from pylink.tracker import StartBlinkEvent
from pylink.tracker import StartNonBlinkEvent
from pylink.tracker import FixUpdateEvent
from pylink.tracker import StartFixationEvent
from pylink.tracker import EndFixationEvent
from pylink.tracker import StartSaccadeEvent
from pylink.tracker import EndSaccadeEvent
from pylink.tracker import EyeLinkAddress
from pylink.tracker import EyelinkMessage
from pylink.tracker import EyeLinkCustomDisplay
from pylink.tracker import KeyInput
from pylink.tracker import ILinkData
from pylink.tracker import IOEvent
from pylink.tracker import ButtonEvent
from pylink.tracker import MessageEvent
from pylink.tracker import Sample
from pylink.tracker import rawSample



from pylink.eyelink import EyeLinkListener
from pylink.eyelink import EyeLink
from pylink.eyelink import getEYELINK
from pylink.eyelink import openGraphicsEx




from pylink.eyelink import setCalibrationColors
from pylink.eyelink import setTargetSize
from pylink.eyelink import setCalibrationSounds
from pylink.eyelink import setDriftCorrectSounds
from pylink.eyelink import setCameraPosition
from pylink.eyelink import getDisplayInformation
from pylink.eyelink import openGraphics
from pylink.eyelink import closeGraphics
from pylink.eyelink import resetBackground

from pylink.eyelink import setCalibrationAnimationTarget
from pylink.eyelink import enableExternalCalibrationDevice



from pylink.__version__ import *

