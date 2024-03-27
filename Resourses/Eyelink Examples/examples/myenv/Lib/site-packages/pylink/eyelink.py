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
# $Date: 2012/07/17 17:49:00 $
# 

from . import constants
from pylink.pylink_c import EyeLinkCBind
from pylink.pylink_c import msecDelay
from pylink.pylink_c import openCustomGraphicsInternal
from pylink.tracker import ILinkData
from pylink.tracker import EyeLinkCustomDisplay
from pylink.pylink_c import getDisplayInformation as pylink_cgetDisplayInformation


pylinkcg=None
customGraphics=None
imported = False

def getLevelTextInternal(level):
	if level == 0:
		return "OFF"
	elif level == 1:
		return "NORMAL"
	elif level == 2:
		return  "HIGH"


#  EyeLink base class that talks directly to the C api. The constructor of this class only,
#  initialize the eyelink connection. However, it does not connect. This class is very useful for all broadcast programs.
	   
## EyeLinkListener class implements most of the core EyeLink interface. This includes the simple connection
#  to the eye tracker, sending commands and messages to the tracker, opening and saving a recording file,
#  performing calibration and drift correction, real-time access to tracker data and eye movement events
#  (such as fixations, blinks, and saccades), as well as other important operations.
#
#  An instance of the EyeLinkListener class can be created by using the class constructor function. For example,
#
#	\code
#   	try:
#		EYELINK = EyeLinkListener()
#	except:
#		EYELINK = None
#	\endcode
#
#  All of the methods should be called in the format of: EYELINK.functionName(parameters), where EYELINK is 
#  an instance of the EyeLinkListener class.
class EyeLinkListener(EyeLinkCBind):
	def __init__(self):
		# The constructor takes no parameters. However, if the connection suceeds, calibration_type, 
		# gaze_constraint, automatic_calibration commands are sent to the tracker. By default the 
		# calibration type is HV13, the gazeConstraint is AUTO and automatic calibration is turned off.
		EyeLinkCBind.__init__(self)
		self._trackerInfo = ILinkData()
		constants.EYELINK= self
		#TODO: should now remove all methods that are not available to the listener in EyeLinkCBind
	
	## Returns the current tracker information.
	# 
	#  @return 
	#	An instance of the ILinkData class.
	def getTrackerInfo(self):
		self._getDataStatus(self._trackerInfo)
		return self._trackerInfo
	
	## Allow the normal calibration target drawing to proceed at different locations.
	#
	#  This is equivalent to the C API 
	#	\code
	#	INT16 CALLTYPE set_draw_cal_target_hook(INT16 (CALLBACK * erase_cal_target_hook)(HDC hdc), INT16 options);
	#	\endcode
	#
	#  @param position A tuple in the format of (x, y), passing along the position of drift correction target.  X and y are in screen pixels.
	def drawCalTarget(self, position):
		if pylinkcg:
			pylinkcg._drawCalTarget(position)

	## returns the current tracker time.
	def getCurrentTime(self):
		return self.trackerTime()
	
	## returns the current sample rate.
	def getSampleRate(self):
		v = self.getModeData()[1]
		if v == constants.MISSING_DATA:
			return constants.MISSING_DATA
		return v
	
	## returns the current mode data, either PUPIL_ONLY or PUPIL_CR.
	def getCRMode(self):
		v = self.getModeData()[2]
		if v:
			return "PUPIL_CR"
		return "PUPIL_ONLY"

	## returns the Link Filter Level.
	def getLinkFilter(self):
		return getLevelTextInternal(self.getModeData()[4])

	## returns the File Filter Level.
	def getFileFilter(self):
		return getLevelTextInternal(self.getModeData()[3])
		
	## returns the eye used.
	def getEyeUsed(self):
		v = self.eyeAvailable()
		if v == -1:
			return "NONE"
		elif v == 0:
			return "LEFT"
		elif v == 1:
			return "RIGHT"
		else:
			return "BOTH"
	
	## Sends the given message to the connected EyeLink tracker. The message will be written to the EyeLink tracker.
	#
	#@remarks 
	#This is equivalent to the C API 
	#\code
	#int eyecmd_printf(char *fmt, ...);
	#\endcode
	#The maximum text length is 130 characters. If the given string has more than 130 characters, the first 130
	#characters will be sent and if the send passes this function will return 1. If the text is not truncated, 
	#0 will be returned on a successful message send.
	#
	#@param message_text text message to be sent.  It does not support printf() kind of formatting.
	#@param offset time offset in millisencond for the message.
	#@return
	#If there is any problem sending the message, a runtime exception is raised.
	def sendMessage(self,message_text,offset=0):
		cut = 0
		if message_text is None or len(message_text) == 0:
			return 0
		message_text=str(message_text)
		#if len(message_text) > 130 :   #bugfix: api-152
			#msg = msg[0:130]
		#	cut = 1
		#print "About to send: cut=",cut,msg
		rv = EyeLinkCBind.sendMessage(self,message_text,offset)
		#print "sent"
		if rv == 0 and cut ==1:
			return 1
		else:
			return rv

	## Sends the given image file backdrop to the connected EyeLink tracker.
	#
	#  @remarks 
	#  	This will open the image file, convert to bitmap using PIL.Image and call bitmapBackdrop to send the image to host
	#
	# @param filename - full or relative path of the image file name 
	# @param Xs - crop x position
	# @param Ys - crop y position
	# @param width - crop width
	# @param height - crop height
	# @param Xd - xposition - transfer
	# @param Yd - yposition - transfer
	# @param xferoptions - transfer options(BX_AVERAGE,BX_DARKEN,BX_LIGHTEN,BX_MAXCONTRAST,BX_NODITHER,BX_GRAYSCALE)
	#
	# @return if PIL couldn't load, it will return None, otherwise return value of bitmapBackdrop
	def imageBackdrop(self, filename, Xs, Ys, width, height, Xd, Yd, xferoptions):
		from PIL import Image		
		im = Image.open(filename) # open an image with PIL
		w,h = im.size # get the width and height of an image
		pixels = im.load() # load to access pixel data
		# convert pixels to a long list
		pixels_2transfer = [[pixels[i,j] for i in range(w)] for j in range(h)]
		return self.bitmapBackdrop(w, h, pixels_2transfer, Xs, Ys, width, height, Xd, Yd, xferoptions)

## The EyeLink class is an extension of the EyeLinkListener class with additional utility functions.  Most 
#  of these functions are used to perform tracker setups (For current information on the EyeLink tracker 
#  configuration, examine the *.INI files in the EYELINK2\\EXE\\ or ELCL\\EXE\\ directory of the eye tracker computer).  An 
#  instance of the EyeLink class can be created by using the class constructor function.  For example,
#
# 	\code
#	try:
#		EYELINK = EyeLink()
#	except:
#		EYELINK = None
#	\endcode
#
#  An instance of EyeLink class can directly use all of the EyeLinkListener methods.  In addition, it has 
#  its own methods as listed in the following.  All of the methods should be called in the format of: 
#  EYELINK.functionName(parameters), where EYELINK is an instance of EyeLink class. 


#  This class extends off of EyelinkListener. If any address is given, the 
#  constructor will connect to the address, otherwise, it connects to the 
#  tracker at 100.1.1.1 with sub net mask 255.255.255.0.
class EyeLink(EyeLinkListener):
	## Constructor.
	# @param trackeraddress optional tracker address. If no parameters passed in, default address of 
	# 100.1.1.1 is used.  If None is passed as the address, the connection is opened in dummy mode.
	#
	def __init__(self,trackeraddress="100.1.1.1"):
		# The constructor takes no parameters. However, if the connection suceeds, calibration_type, 
		# gaze_constraint, automatic_calibration commands are sent to the tracker. By default the 
		# calibration type is HV13, the gazeConstraint is AUTO and automatic calibration is turned off.
		EyeLinkListener.__init__(self)
		
		constants.EYELINK= None #reset the value since this will be set in the eyelinklistener too
		if trackeraddress is None:
			self.dummy_open()
			self.__dummyMode__ = True
			self.trackeraddress = "MISSING_DATA"
		else:
			self.open(trackeraddress,0)
			self.__dummyMode__ = False
			self.trackeraddress = trackeraddress
			
		
		constants.EYELINK= self
		#print globals()["EYELINK"]
		self.sendCommand("file_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON")
		self.sendCommand("file_sample_data  = LEFT,RIGHT,GAZE,AREA,GAZERES,STATUS,HREF,PUPIL")
		msecDelay(2);
		self.sendCommand("link_event_filter = LEFT,RIGHT,FIXATION,FIXUPDATE,SACCADE,BLINK,BUTTON")
		self.sendCommand("link_sample_data  = LEFT,RIGHT,GAZE,GAZERES,AREA,STATUS")
		msecDelay(2);
		self.setRecordingParseType('GAZE')
		self.setSaccadeVelocityThreshold(30)
		msecDelay(2);
		self.setAccelerationThreshold(8000)
		self.setMotionThreshold(0.15)
		msecDelay(2);
		self.setPursuitFixup(60)
		self.setUpdateInterval(0)
		msecDelay(2);
		self.sendCommand("fixation_update_interval = 50")
		self.sendCommand("fixation_update_accumulate = 50") 
		msecDelay(2);
		self.setAcceptTargetFixationButton(5)
	
		self.__linkFilter__=1
		self.__fileFilter__=2
		self.__sampleSizeForVelAndAccel__ = constants.FIVE_SAMPLE_MODEL
		#self.__autoCalibrationMessage__=False
		msecDelay(1);
		
	## prints out the file transfer progress to the console.
	#  This is called after the call to receiveDataFile 
	#  
	#  @param size Size of the file.
	#  @param received Size received so far.
	def progressUpdate(self,size,received):
		#print("\r",received,"/",size,)
		return
		
	## prints out the sending file progress to the console.
	#  This is called after the call to sendDataFile 
	#  
	#  @param size Size of the file.
	#  @param sent Size sent so far.
	def progressSendDataUpdate(self,size,sent):
		print("\s",sent,"/",size,)	


	## Sets the sample model to be used for velocity and acceleration calculation.
	#  @param sm sample model to be used. Valid values are \c FIVE_SAMPLE_MODEL, 
	#  \c NINE_SAMPLE_MODEL,\c SEVENTEEN_SAMPLE_MODEL, and \c EL1000_TRACKER_MODEL
	#
	#
	def setSampleSizeForVelAndAcceleration(self,sm):
		self.__sampleSizeForVelAndAccel__=sm

	## Returns the sample model used for velocity and acceleration calculation.
	def getSampleSizeForVelAndAcceleration(self):
		return self.__sampleSizeForVelAndAccel__
	
	## Sets the sample model to be used for velocity and acceleration calculation. Same as 
	# setSampleSizeForVelAndAcceleration excepts this interprets string message.
	#  @param sm sample model to be used. Valid values are \c 5-sample \c Model, 
	#  \c 9-sample \c Model,\c 17-sample \c Model, and \c EL1000 \c Tracker \c Model
	#
	#
	def setVelocityAccelerationModel(self,sm):
		# sets the velocity acceleration model to use.
		if sm == "5-sample Model":
			self.setSampleSizeForVelAndAcceleration(constants.FIVE_SAMPLE_MODEL)
		elif sm == "9-sample Model":
			self.setSampleSizeForVelAndAcceleration(constants.NINE_SAMPLE_MODEL)
		elif sm == "17-sample Model":
			self.setSampleSizeForVelAndAcceleration(constants.SEVENTEEN_SAMPLE_MODEL)
		else :
			self.setSampleSizeForVelAndAcceleration(constants.EL1000_TRACKER_MODEL)

	## Returns the sample model used for velocity and acceleration calculation in text form.
	def getVelocityAccelerationModel(self):
		# returns the velocity acceleration model name currently in use.
		v = self.getSampleSizeForVelAndAcceleration()
		if v == constants.FIVE_SAMPLE_MODEL:
			return "5-sample Model"
		elif v == constants.NINE_SAMPLE_MODEL:
			return "9-sample Model"
		elif v == constants.SEVENTEEN_SAMPLE_MODEL:
			return "17-sample Model"
		else:
			return "EL1000 Tracker Model"

	## Returns the tracker address.
	def getTrackerAddress(self):
		return self.trackeraddress

	## Returns whether in dummy mode or not.
	def getDummyMode(self):
		return self.__dummyMode__
		
	## Switches the EyeLink tracker to the Setup menu, from which camera setup, calibration,
	#  validation, drift correction, and configuration may be performed.  Pressing the 'Esc'
	#  key on the tracker keyboard will exit the Setup menu and return from this function. Calling
	#  \c exitCalibration() from an event handler will cause any call to \c do_tracker_setup() in
	#  progress to return immediately.  
	#
	#  @param width	Width of the screen.
	#  @param height Height of he screen.
	def doTrackerSetup(self,width=None,height=None):
		if width is not None and height is not None:
			displayCoords = " 0 0 %d %d"%(width,height)
			self.sendMessage("DISPLAY_COORDS" + displayCoords)
			self.sendCommand("screen_pixel_coords" + displayCoords)
		
		EyeLinkCBind.doTrackerSetup(self)
	
	## This programs a specific button for use in drift correction.  
	#
	#  @remarks
	# 	This function is equivalent to 
	#	\code
	#	getEYELINK().sendCommand("button_function %d 'accept_target_fixation'"%button);
	#	\endcode
	#
	#  @param button Id of the button that is used to accept target fixation.
	def setAcceptTargetFixationButton(self, button):
		self.sendCommand("button_function %d 'accept_target_fixation'"%button);
	
	## This command sets the calibration type, and recomputed the calibration targets after a display resolution change.
	#
	#  @remarks
	#	This function is equivalent to 
	#	\code
	#	getEYELINK().sendCommand("calibration_type=%s"%caltype);
	#	\endcode
	#
	#  @param type One of these calibration type codes listed below:
	#		<table>
	#		<tr><td>\c H3</td><td>horizontal 3-point calibration</td></tr>
	#		<tr><td>\c HV3</td><td>3-point calibration, poor linearization</td></tr>
	#		<tr><td>\c HV5</td><td>5-point calibration, poor at corners</td></tr>
	#		<tr><td>\c HV9</td><td>9-point grid calibration, best overall</td></tr>
	# 		<tr><td>\c HV13</td><td>13-point calibration for large calibration region (EyeLink II version 2.0 or later; EyeLink 1000)</td></tr>
	#		</table>
	def setCalibrationType(self,type):
		if(self.isConnected()):
			self.sendCommand("calibration_type=%s"%(type))
		
	## Locks the x part of gaze position data. Usually set to \c AUTO: this will use the last drift-correction 
	#  target position when in \c H3 mode.
	#
	#  @remarks
	#	This function is equivalent to 
	#	\code
	#	getEYELINK().sendCommand("x_gaze_constraint=%s"%(str(value)));
	# 	\endcode
	#
	#  @param x_position x gaze coordinate, or \c AUTO.
	def setXGazeConstraint(self, x_position = "AUTO"):
		if(self.isConnected()):
			self.sendCommand("x_gaze_constraint=%s"%(str(x_position)))
	
	## Locks the y part of gaze position data. Usually set to \c AUTO: this will use the last drift-correction 
	#  target position when in \c H3 mode.
	#
	#  @remarks
	#	This function is equivalent to 
	#	\code
	#	getEYELINK().sendCommand("y_gaze_constraint=%s"%(str(value)));
	# 	\endcode
	#
	#  @param y_position y gaze coordinate, or \c AUTO.
	def setYGazeConstraint(self, y_position = "AUTO"):
		if(self.isConnected()):
			self.sendCommand("y_gaze_constraint=%s"%(str(y_position)))
	
	## Enables the auto calibration mechanism.  By default, this mechanism is turned off.
	#
	#  @remarks
	#	This function is equivalent to 
	#	\code
	#	if(getEYELINK().isConnected()):
	#		getEYELINK().sendCommand("enable_automatic_calibration=YES")
	#	\endcode
	def enableAutoCalibration(self):
		if(self.isConnected()):
			self.sendCommand("enable_automatic_calibration=YES")
			
	## Disables the auto calibration mechanism.  By default, this mechanism is turned off.
	#
	#  @remarks
	#	This function is equivalent to 
	#	\code
	#	if(getEYELINK().isConnected()):
	#		getEYELINK().sendCommand("enable_automatic_calibration=NO")
	#	\endcode
	def disableAutoCalibration(self):
		if(self.isConnected()):
			self.sendCommand("enable_automatic_calibration=NO")

	## Sets automatic calibration pacing.  \c 1000 is a good value for most subjects, \c 1500 for slow 
	#  subjects and when interocular data is required. 
	#
	#  @remarks
	#	This function is equivalent to
	#	\code
	#	getEYELINK().sendCommand("automatic_calibration_pacing=%d"%(time))
	#	\endcode
	#
	#  @param pace shortest delay.
	def setAutoCalibrationPacing(self,pace):
		self.sendCommand("automatic_calibration_pacing=%d"%(pace))
	
	## Sends a command to the tracker to read the specified io port
	# @param ioport port id of the io port.
	def readIOPort(self, ioport):
		# Performs a dummy read of I/O port.  Useful to configure I/O cards.
		self.sendCommand("read_ioport=%s"%(ioport))
		return self.commandResult()
	
	## Sends a command to the tracker to write the specified io port
	#  @param ioport byte hardware I/O port address. The port address for the C and D 
	#  ports on the EyeLink analog output card are 4 and 5, respectively; the print 
	#  port address will typically be 0x378 (please see the buttons.ini settings).
	#  @param data data to write
	def writeIOPort(self, ioport,data):
		# Writes data to I/O port.  Useful to configure I/O cards.
		self.sendCommand("write_ioport=%s,%s"%(ioport,data))
			
	## EyeLink II only:
	#  Can be used to set level of filtering on the link and analog output, and on file data.  
	#  An additional delay of 1 sample is added to link or analog data for each filter level.  
	#  If an argument of &lt;on&gt; is used, link filter level is set to \c 1 to match EyeLink I delays.  
	#  The file filter level is not changed unless two arguments are supplied.  
	#  The default file filter level is \c 2.
	#
	#  @remarks
	#	This function is equivalent to 
	#	\code
	#	if(getEYELINK().getTrackerVersion() >=2):
	#		if(filefilter == -1):
	#			getEYELINK().sendCommand("heuristic_filter %d"%(linkfilter))
	#		else:
	#			getEYELINK().sendCommand(" %d %d"%(linkfilter, filefilter));
	#	\endcode
	#
	#  @param linkfilter Filter level of the link data.
	#		\c 0 or \c OFF disables link filter.
	#	   	\c 1 or \c ON sets filter to 1 (moderate filtering, 1 sample delay).
	#	   	\c 2 applies an extra level of filtering (2 sample delay).
	#  @param filefilter Filter level of the data written to EDF file.
	#		\c 0 or \c OFF disables link filter.
	#	   	\c 1 or \c ON sets filter to 1 (moderate filtering, 1 sample delay).
	#	   	\c 2 applies an extra level of filtering (2 sample delay).
	def setHeuristicLinkAndFileFilter(self,linkfilter, filefilter=-1):
		if(self.getTrackerVersion() >=2):
			if(filefilter == -1):
				self.sendCommand("heuristic_filter %d"%(linkfilter))
			else:
				self.sendCommand("heuristic_filter %d %d"%(linkfilter, filefilter))
	
	## EyeLink 1 Only: Can be used to enable filtering, increases system delay by 4 msec if the filter 
	#  was originally off.  NEVER TURN OFF THE FILTER WHEN ANTIREFLECTION IS TURNED ON.  
	#  For EyeLink II and newer eye tracker models, you should use the \c setHuresticFileAndLinkFilter() method instead. 
	#
	#  @remarks
	#	This function is equivalent to 
	#	\code
	#	getEYELINK().sendCommand("heuristic_filter=ON");
	#	\endcode		
	def setHeuristicFilterOn(self):
		self.sendCommand("heuristic_filter=ON")
	
	## EyeLink 1 Only: Can be used to disable filtering, reduces system delay by 4 msec.  
	#  NEVER TURN OFF THE FILTER WHEN ANTIREFLECTION IS TURNED ON. 
	#  For EyeLink II and newer eye tracker models, you should use the following \c setHuresticFileAndLinkFilter() method instead. 
	#  
	#  @remarks
	#	This function is equivalent to 
	#	\code
	#	getEYELINK().sendCommand("heuristic_filter = OFF");
	#	\endcode
	def setHeuristicFilterOff(self):
		self.sendCommand("heuristic_filter=OFF")
	
	## Can be used to determine pupil size information to be recorded. 
	#
	#  @remarks
	#	This function is equivalent to 
	#	\code
	#	getEYELINK().sendCommand("pupil_size_diameter = %s"%(value));	
	#	\endcode
	#
	#  @param value \c YES to convert pupil area to diameter; \c NO to output pupil area data.
	def setPupilSizeDiameter(self, value):
		self.sendCommand("pupil_size_diameter = %s"%(value))
		
	## Can be used to turn off head tracking if not used.  Do this before calibration.
	#
	#  @remarks
	#	This function is equivalent to 
	#	\code
	#	getEYELINK().sendCommand("simulate_head_camera = %s"%(value));
	#	\endcode
	#
	#  @param value \c YES to disable head tracking; \c NO to enable head tracking.
	def setSimulationMode(self, value):
		self.sendCommand("simulate_head_camera = %s"%(value))
		
	## Used to compute correct visual angles and velocities when head tracking not used.
	#
	#  @remarks
	#	This function is equivalent to 
	#	\code
	#	getEYELINK().sendCommand("simulation_screen_distance = %s"%(distance));
	#	\endcode
	#	
	#  @param distance simulated distance from display to subject in millimeters.
	def setScreenSimulationDistance(self, distance):
		self.sendCommand("simulation_screen_distance  = %s"%(distance))
		
	## Marks the location in the data file from which playback will begin at the next call to 
	#  \c EYEYLINK.startPlayBack().  When this command is not used (or on older tracker versions), playback 
	#  starts from the beginning of the previous recording block.  This default behavior is suppressed after 
	#  this command is used, until the tracker application is shut down.
	#
	#  @remarks
	#	This function is equivalent to 
	#	\code
	#	getEYELINK().sendCommand("mark_playback_start");	
	#	\endcode
	def markPlayBackStart(self):
		self.sendCommand("mark_playback_start")
		
	## Selects what types of events can be sent over the link while not recording (e.g between trials).  
	#  This command has no effect for EyeLink II, and messages cannot be enabled for versions of EyeLink I before v2.1.
	#
	#  @remarks
	#	This function is equivalent to 
	#	\code
	#	re = []
	#	if(message):
	#		re.append("MESSAGE ")
	#	if(button):
	#		re.append("BUTTON ")
	#	if(inputevent):
	#		re.append("INPUT ")
	#	getEYELINK().sendCommand("link_nonrecord_events = %s"%"".join(re));
	#	\endcode
	#
	#  @param message \c 1 to enable the recording of EyeLink messages.
	#  @param button \c 1 to enable recording of buttons (1..8 press or release).
	#  @param inputevent \c 1 to enable recording of changes in input port lines.
	def setNoRecordEvents(self, message=False, button = False, inputevent =False):
		re = []
		if(message):
			re.append("MESSAGE")
		if(button):
			re.append("BUTTON")
		if(inputevent):
			re.append("INPUT")
		self.sendCommand("link_nonrecord_events = %s %s %s "%re)

	## Sets data in samples written to EDF file.  See tracker file "DATA.INI" for types.
	#
	#  @remarks
	#	This function is equivalent to 
	#	\code
	#	getEYELINK().sendCommand("file_sample_data = %s"%list)
	#	\endcode
	#
	#  @param list list of the following data types, separated by spaces or commas.
	#		<table>
	#		<tr><td>\c GAZE</td><td>screen x/y (gaze) position</td></tr>
	#		<tr><td>\c GAZERES</td><td>units-per-degree screen resolution</td></tr>
	#		<tr><td>\c HREF</td><td>head-referenced gaze</td></tr>
	#		<tr><td>\c PUPIL</td><td>raw eye camera pupil coordinates</td></tr>
	#		<tr><td>\c AREA</td><td>pupil area</td></tr>
	#		<tr><td>\c STATUS</td><td>warning and error flags</td></tr>
	#		<tr><td>\c BUTTON</td><td>button state and change flags</td></tr>
	#		<tr><td>\c INPUT</td><td>input port data lines</td></tr>
	#		</table>
	def setFileSampleFilter(self,list):
		self.sendCommand("file_sample_data = %s"%list)
		
	## Sets data in events written to EDF file.  See tracker file "DATA.INI" for types.
	#
	#  @remarks
	#	This function is equivalent to 
	#	\code
	#	getEYELINK().sendCommand("file_event_data = %s"%list);
	#	\endcode
	#
	#  @param list list of the following event data types, separated by spaces or commas.
	#		<table>
	#		<tr><td>\c GAZE</td><td>screen xy (gaze) position</td></tr>
	#		<tr><td>\c GAZERES</td><td>units-per-degree angular resolution</td></tr>
	#		<tr><td>\c HREF</td><td>HREF gaze position</td></tr>
	#		<tr><td>\c AREA</td><td>pupil area or diameter</td></tr>
	#		<tr><td>\c VELOCITY</td><td>velocity of eye motion (avg, peak)</td></tr>
	#		<tr><td>\c STATUS</td><td>warning and error flags for event</td></tr>
	#		<tr><td>\c FIXAVG</td><td>include ONLY average data in ENDFIX events</td></tr>
	#		<tr><td>\c NOSTART</td><td>start events have no data, just time stamp</td></tr>
	#		</table>
	def setFileEventData(self,list):
		self.sendCommand("file_event_data = %s"%list)
	
	## Sets which types of events will be written to EDF file.  See tracker file "DATA.INI" for types.
	#
	#  @remarks
	#	This function is equivalent to 
	#	\code
	#	getEYELINK().sendCommand("file_event_filter = %s"%list);
	#	\endcode
	#
	#  @param list list of the following event types, separated by spaces or commas.
	#		<table>
	#		<tr><td>\c LEFT, \c RIGHT</td><td>events for one or both eyes</td></tr> 
	#		<tr><td>\c FIXATION</td><td>fixation start and end events</td></tr>
	#		<tr><td>\c FIXUPDATE</td><td>fixation (pursuit) state updates</td></tr>
	#		<tr><td>\c SACCADE</td><td>saccade start and end</td></tr>
	#		<tr><td>\c BLINK</td><td>blink start an end</td></tr>
	#		<tr><td>\c MESSAGE</td><td>messages (user notes in file)</td></tr>
	#		<tr><td>\c BUTTON</td><td>button 1..8 press or release</td></tr>
	#		<tr><td>\c INPUT</td><td>changes in input port lines;</td></tr>
	#		</table>
	def setFileEventFilter(self,list):
		self.sendCommand("file_event_filter = %s"%list)
	
	## Sets data in samples sent through link.  See tracker file "DATA.INI" for types.
	#
	#  @remarks
	#	This function is equivalent to 
	#	\code
	#	getEYELINK().sendCommand("link_sample_data = %s"%list)
	#	\endcode
	#
	#  @param list list of data types, separated by spaces or commas.
	#		<table>
	#		<tr><td>\c GAZE</td><td>screen xy (gaze) position</td></tr>
	#		<tr><td>\c GAZERES</td><td>units-per-degree screen resolution</td></tr>
	#		<tr><td>\c HREF</td><td>head-referenced gaze</td></tr>
	#		<tr><td>\c PUPIL</td><td>raw eye camera pupil coordinates</td></tr>
	#		<tr><td>\c AREA</td><td>pupil area</td></tr>
	#		<tr><td>\c STATUS</td><td>warning and error flags</td></tr>
	#		<tr><td>\c BUTTON</td><td>button state and change flags</td></tr>
	#		<tr><td>\c INPUT</td><td>input port data lines</td></tr>
	#		</table>
	def setLinkSampleFilter(self,list):
		self.sendCommand("link_sample_data = %s"%list)
	
	## Sets data in events sent through link.  See tracker file "DATA.INI" for types.
	#
	#  @remarks
	#	This function is equivalent to 
	#	\code
	#	getEYELINK().sendCommand("link_event_data = %s"%list);
	#	\endcode
	#
	#  @param list list of data types, separated by spaces or commas.
	#		<table>
	#		<tr><td>\c GAZE</td><td>screen xy (gaze) position</td></tr>
	#		<tr><td>\c GAZERES</td><td>units-per-degree angular resolution</td></tr>
	#		<tr><td>\c HREF</td><td>HREF gaze position</td></tr>
	#		<tr><td>\c AREA</td><td>pupil area or diameter</td></tr>
	#		<tr><td>\c VELOCITY</td><td>velocity of eye motion (avg, peak)</td></tr>
	#		<tr><td>\c STATUS</td><td>warning and error flags for event</td></tr>
	#		<tr><td>\c FIXAVG</td><td>include ONLY average data in ENDFIX events</td></tr>
	#		<tr><td>\c NOSTART</td><td>start events have no data, just time stamp</td></tr>
	#		</table>
	def setLinkEventData(self,list):
		self.sendCommand("link_event_data = %s"%list)
		
	## Sets which types of events will be sent through link.  See tracker file "DATA.INI" for types.
	#
	#  @remarks
	#	This function is equivalent to 
	#	\code
	#	getEYELINK().sendCommand("link_event_filter = %s"%list);
	#	\endcode
	#
	#  @param list list of event types.
	#		<table> 		
	#		<tr><td>\c LEFT, \c RIGHT</td><td>events for one or both eyes</td></tr>
	#		<tr><td>\c FIXATION</td><td>fixation start and end events</td></tr>
	#		<tr><td>\c FIXUPDATE</td><td>fixation (pursuit) state updates</td></tr>
	#		<tr><td>\c SACCADE</td><td>saccade start and end</td></tr>
	#		<tr><td>\c BLINK</td><td>blink start an end</td></tr>
	#		<tr><td>\c MESSAGE</td><td>messages (user notes in file)</td></tr>
	#		<tr><td>\c BUTTON</td><td>button 1-8 press or release</td></tr>
	#		<tr><td>\c INPUT</td><td>changes in input port lines;</td></tr>
	#		</table>
	def setLinkEventFilter(self,list):
		self.sendCommand("link_event_filter = %s"%list)
	
	## Sets velocity threshold of saccade detector: usually \c 30 for cognitive research, \c 22 for 
	#  pursuit and neurological work.
	#
	#  @remarks
	#	This function is equivalent to 
	#	\code
	#	getEYELINK().sendCommand("saccade_velocity_threshold =%d"%(vel));
	#	\endcode
	#
	#  @param vel minimum velocity (°/sec) for saccades.
	def setSaccadeVelocityThreshold(self, vel):
		self.sendCommand("saccade_velocity_threshold =%d"%(vel))

	## Sets acceleration threshold of saccade detector: usually \c 9500 for cognitive research, 
	#  \c 5000 for pursuit and neurological work.
	#
	#  @remarks
	#	This function is equivalent to 
	#	\code
	#	getEYELINK().sendCommand("saccade_acceleration_threshold  =%d"%(accl));
	#	\endcode
	#
	#  @param accel minimum acceleration (°/sec/sec) for saccades.
	def setAccelerationThreshold(self, accel):
		self.sendCommand("saccade_acceleration_threshold  =%d"%(accel))
	
	## Sets a spatial threshold to shorten saccades.  Usually \c 0.15 for cognitive research, 
	#  \c 0 for pursuit and neurological work.
	#
	#  @remarks
	#	This function is equivalent to 
	#	\code
	#	getEYELINK().sendCommand("saccade_motion_threshold  =%d"%(deg));
	#	\endcode
	#
	#  @param deg minimum motion (degrees) out of fixation before saccade onset allowed.
	def setMotionThreshold(self, deg):
		self.sendCommand("saccade_motion_threshold  =%d"%(deg))
	
	## Sets the maximum pursuit velocity accommodation by the saccade detector.  Usually set to \c 60.
	#
	#  @remarks
	#	This function is equivalent to 
	#	\code
	#	getEYELINK().sendCommand("saccade_pursuit_fixup =  %d"%(v));
	#	\endcode
	#
	#  @param maxvel maximum pursuit velocity fixup (°/sec).
	def setPursuitFixup(self,maxvel):
		self.sendCommand("saccade_pursuit_fixup =  %d"%(maxvel))
		
	## Normally set to \c 0 to disable fixation update events.  Set to \c 50 or \c 100 milliseconds 
	#  to produce updates for gaze-controlled interface applications.
	#
	#  @remarks
	#	This function is equivalent to 
	#	\code
	#	getEYELINK().sendCommand("fixation_update_interval =  %d"%(time));
	#	\endcode
	#
	#  @param time milliseconds between fixation updates, \c 0 turns off.
	def setUpdateInterval(self,time):
		self.sendCommand("fixation_update_interval =  %d"%(time))

	## Normally set to \c 0 to disable fixation update events.  Set to \c 50 or \c 100 milliseconds 
	#  to produce updates for gaze-controlled interface applications.  Set to \c 4 to collect 
	#  single sample rather than average position.
	#
	#  @remarks
	#	This function is equivalent to 
	#	\code
	#	getEYELINK().sendCommand("fixation_update_accumulate =  %d"%(time));
	#	\endcode
	#
	#  @param time milliseconds to collect data before fixation update for average gaze position.	
	def setFixationUpdateAccumulate(self, time):
		self.sendCommand("fixation_update_accumulate =  %d"%(time))

	## Sets how velocity information for saccade detection is computed.
	#
	#  @remarks
	#	This function is equivalent to 
	#	\code
	#	getEYELINK().sendCommand("recording_parse_type %s"%(rtype));
	#	\endcode
	#
	#  @param rtype \c GAZE or \c HREF; Almost always left to \c GAZE.
	def setRecordingParseType(self, rtype="GAZE"):
		self.sendCommand("recording_parse_type %s"%(rtype))
		
	# methods to draw graphics to the tracker record screen
	
	## Draws text, coordinates are gaze-position display coordinates.
	#
	#  @remarks
	#	This function is equivalent to 
	#	\code
	#	getEYELINK().sendCommand("print_position= %d %d"%pos)
	#	getEYELINK().sendCommand("echo %s"%(text))
	#	\endcode
	#
	#  @param text text to print in quotes.
	#  @param pos Center point of text; Default position is (\c -1, \c -1).
	def drawText(self, text, pos=(-1,-1)):
		#  Prints text at current print position to tracker screen, gray on black only.
		#  Coordinates are text row and column, similar to C gotoxy() function.  NOTE: row cannot be set higher than 25.  
		#  Use draw_text command to print anywhere on the tracker display.
		if(pos[0] >= 0 and pos[1] >= 0 and pos[0] <=25 and pos[1] <= 80):
			self.sendCommand("print_position= %d %d"%pos)
		self.sendCommand("echo %s"%(text))
			
	## Clear tracker screen for drawing background graphics or messages.
	#
	#  @remarks
	#	This function is equivalent to 
	#	\code
	#	getEYELINK().sendCommand("clear_screen %d"%(color));
	#	\endcode
	#
	#  @param color \c 0 to \c 15.
	def clearScreen (self, color):
		self.sendCommand("clear_screen %d"%(color))
	
	## Draws line, coordinates are gaze-position display coordinates.
	#
	#  @remarks
	#	This function is equivalent to 
	#	\code
	#	getEYELINK().sendCommand("draw_line %d %d %d %d %d"%
	#		(firstPoint[0],firstPoint[1],secondPoint[0],secondPoint[1], color));
	#	\endcode	
	#	
	#  @param firstPoint a two-item tuple, containing the x, y coordinates of the start point.
	#  @param secondPoint a two-item tuple, containing the x, y coordinates of the end point.
	#  @param color \c 0 to \c 15.
	def drawLine(self, firstPoint, secondPoint, color):
		self.sendCommand("draw_line %d %d %d %d %d"%(firstPoint[0],firstPoint[1],secondPoint[0],secondPoint[1], color))
	
	## Draws an empty box, coordinates are gaze-position display coordinates.
	#
	#  @remarks
	#	This function is equivalent to 
	#	\code
	#	getEYELINK().sendCommand("draw_box %d %d %d %d %d"%(x,y,x+width,y+height,color));
	#	\endcode
	#
	#  @param x x coordinates for the top-left corner of the rectangle.
	#  @param y y coordinates for the top-left corner of the rectangle.
	#  @param width width of the filled rectangle.
	#  @param height height of the filled rectangle.
	#  @param color \c 0 to \c 15.
	def drawBox(self, x,y, width, height, color):
		self.sendCommand("draw_box %d %d %d %d %d"%(x,y,x+width,y+height,color))
	
	## Draws a solid block of color, coordinates are gaze-position display coordinates.
	#
	#  @remarks
	#	This function is equivalent to 
	#	\code
	#	getEYELINK().sendCommand("draw_filled_box %d %d %d %d %d"%(x,y,x+width,y+height,color));
	# 	\endcode
	#
	#  @param x x coordinates for the top-left corner of the rectangle.
	#  @param y y coordinates for the top-left corner of the rectangle.
	#  @param width width of the filled rectangle.
	#  @param height height of the filled rectangle.
	#  @param color \c 0 to \c 15.
	def drawFilledBox(self,x,y, width, height, color):
		self.sendCommand("draw_filled_box %d %d %d %d %d"%(x,y,x+width,y+height,color))
	
	## Returns the fixation update interval value.  This does not query the tracker, only valid if
	# setFixationUpdateInterval is called prior to calling this function.
	def getFixationUpdateInterval(self):
		return self.__fixation_update_interval_

	## Returns the fixation update accumulate value. This does not query the tracker, only valid if
	# setFixationUpdateAccumulate is called prior to calling this function.
	def getFixationUpdateAccumulate(self):
		return self.__fixation_update_accumulate_

	## Sends a command to the tracker to update the FixationUpdateInterval
	#@param interval value for fixation update interval
	#
	def setFixationUpdateInterval(self,interval):
		self.__fixation_update_interval_=interval
		self.sendCommand("fixation_update_interval = %d"%(interval))

	## Sends a command to the tracker to update the FixationUpdateAccumulate
	#@param accumulate value for fixation update accumulate
	#
	def setFixationUpdateAccumulate(self,accumulate):
		self.__fixation_update_accumulate_=accumulate
		self.sendCommand("fixation_update_accumulate = %d"%(accumulate))
	
	## Prints text at current print position to tracker screen, gray on black only.
	#  @param text text to print in quotes.
	#  @param pos position of the text to display
	#  @remarks
	#	This function is equivalent to 
	#	\code
	#	getEYELINK().sendCommand("echo %s"%text)
	#	\endcode
	#
	def echo(self, text, pos=(-1,-1)):
		drawText(self,text,pos)

	## Draws a small "+" to mark a target point.
	#
	#  @remarks
	#	This function is equivalent to 
	#	\code
	#	getEYELINK().sendCommand("draw_cross %d %d %d"%(x,y, color));
	#	\endcode
	#
	#  @param x x coordinates for the center point of cross.
	#  @param y y coordinates for the center point of cross.
	#  @param color \c 0 to \c 15 (\c 0 for black; \c 1 for blue; \c 2 for green; \c 3 for cyan; 
	#		\c 4 for red; \c 5 for magenta; \c 6 for brown; \c 7 for light gray; \c 8 for 
	#		dark gray; \c 9 for light blue; \c 10 for light green; \c 11 for light cyan; 
	#		\c 12 for light red; \c 13 for bright magenta; \c 14 for yellow; \c 15 for bright white).
	def drawCross(self, x, y, color):
		self.sendCommand("draw_cross %d %d %d"%(x,y, color))





## \defgroup graphics_functions EyeLink Graphics Functions
## \defgroup pylink_utility_functions EyeLink Utility Functions

## \ingroup pylink_utility_functions		
# Returns the EyeLink tracker object
#
#  The returned instance had been created when calling \c EyeLink().
#
#  @remarks
#  This function replaces the previous convention of using \c EYELINK.
#  (\c EYELINK is no longer constant, it is now initialized with \c None)
#
def getEYELINK():
	return constants.EYELINK




## \ingroup graphics_functions
#  Allow one to configure the graphics with EyeLinkCustomDisplay.
#  See \ref EyeLinkCustomDisplay for more details.
#  
#  \code
#  genv = EyeLinkCoreGraphicsPsychoPy(el_tracker, win)
#  pylink.openGraphicsEx(genv)
#  \endcode
#  @param eyeCustomDisplay instance of EyeLinkCustomDisplay for the desired platform. This cannot be used with eyelink_core_graphics library or \ref openGraphics
#
def openGraphicsEx(eyeCustomDisplay):
	global customGraphics
	if pylinkcg:
		raise RuntimeError("Unable to use EyeLinkCustomDisplay when Core Graphics is active. Call closeGraphics() before calling openGraphicsEx()")

	if customGraphics:
		raise RuntimeError("Unable to use new EyeLinkCustomDisplay when a previous EyeLinkCustomDisplay is active. Call closeGraphics() before calling openGraphicsEx()")
		
	if(isinstance(eyeCustomDisplay,EyeLinkCustomDisplay)):
		rv = openCustomGraphicsInternal(eyeCustomDisplay)
		customGraphics=eyeCustomDisplay
		return rv
	else:
		raise RuntimeError("Expecting object of type EyeLinkCustomDisplay got "+ eyeCustomDisplay.__class__.__name__)			




## \ingroup graphics_functions
#   Opens the graphics if the display mode is not set. If the display mode is already set, uses the existing
#	display mode.
#
#	@remarks This is equivalent to the SDL version C API
#	\code
#	INT16 init_expt_graphics(SDL_Surface * s, DISPLAYINFO *info);
#	\endcode
#	@param dimension Two-item tuple of display containing width and height information.
#	@param bits Color bits.
#	@return None or run-time error.
#	@remarks  This function only works with SDL 1.2 in conjunction with eyelink_core_graphics library and cannot be used with EyeLinkCustomDisplay
#
def openGraphics(*args):
	global pylinkcg
	global imported
	if pylinkcg:
		raise RuntimeError("Unable to use openGraphics when a previous Core Graphics is active. Call closeGraphics() before calling openGraphics()")

	if customGraphics:
		raise RuntimeError("Unable to use new EyeLinkCustomDisplay when a previous EyeLinkCustomDisplay is active. Call closeGraphics() before calling openGraphicsEx()")

	if not imported:
		imported=True
		from platform import architecture 
		from sys import platform, version_info
		if version_info >= (3, 8, 0) and platform == 'win32':
			import os
			
			win32 = True
			setuparch = os.getenv('SETUPARCH')
			if ('64' in architecture()[0] or (not setuparch==None and '64' in setuparch)):
				win32=False

			if  'PATH' in os.environ:
				for p in os.environ['PATH'].split(';'):
					if p :
						addtopath = False
						if win32:
							if "win64" not in p and "x64" not in p:
								addtopath = True
						else:
							addtopath = True

						if addtopath:
							try:
								os.add_dll_directory(p)
							except:
								pass
	import pylink.pylink_cg
	pylinkcg=pylink.pylink_cg
	return pylinkcg.openGraphics(*args)



## \ingroup graphics_functions
#   Passes the colors of the display background and fixation target to the eyelink_core_graphics
#	library. During calibration, camera image display, and drift correction, the display background
#	should match the brightness of the experimental stimuli as closely as possible, in order to
#	maximize tracking accuracy. This function passes the colors of the display background and
#	fixation target to the eyelink_core_graphics library. This also prevents flickering of the
#	display at the beginning and end of drift correction.
#
#	@remarks This is equivalent to the C API
#	\code
#	void set_calibration_colors(SDL_Color *fg, SDL_Color *bg);
#	\endcode
#	@param foreground_color Color for foreground calibration target.
#	@param background_color Color for foreground calibration background.
#
#	Both colors must be a three-integer (from 0 to 255) tuple encoding the red, blue, and green
#	color component.
#
#	\b Example:
#	\code
#	setCalibrationColors((0, 0, 0), (255, 255, 255))
#
#	This sets the calibration target in black and calibration background in white.
#	\endcode
#	@remarks  This function only works with SDL 1.2 in conjunction with eyelink_core_graphics library and cannot be used with EyeLinkCustomDisplay
#
def setCalibrationColors(*args):
	if not pylinkcg:
		raise RuntimeError("Unable to use setCalibrationColors before calling openGraphics()")

	if customGraphics:
		raise RuntimeError("Unable to use new setCalibrationColors on EyeLinkCustomDisplay ")

	return pylinkcg.setCalibrationColors(*args)


##	\ingroup graphics_functions
#   The standard calibration and drift correction target is a disk (for peripheral delectability)
#	with a central "hole" target (for accurate fixation). The sizes of these features may be set
#	with this function.
#
#	@remarks This function is equivalent to the C API
#	\code
#	void set_target_size(UINT16 diameter, UINT16 holesize);
#	\endcode
#	@param diameter Size of outer disk, in pixels.
#	@param holesize Size of central feature, in pixels.  If holesize is \c 0, no central feature
#					will be drawn.  The disk is drawn in the calibration foreground color, and
#					the hole is drawn in the calibration background color.
#	@remarks  This function only works with SDL 1.2 in conjunction with eyelink_core_graphics library and cannot be used with EyeLinkCustomDisplay
#
def setTargetSize(*args):
	if not pylinkcg:
		raise RuntimeError("Unable to use setTargetSize before calling openGraphics()")

	if customGraphics:
		raise RuntimeError("Unable to use new setTargetSize on EyeLinkCustomDisplay ")

	return pylinkcg.setTargetSize(*args)
	


##	\ingroup graphics_functions
#   Selects the sounds to be played during \c do_tracker_setup(), including calibration, validation
#	and drift correction. These events are the display or movement of the target, successful
#	conclusion of calibration or good validation, and failure or interruption of calibration or validation.
#
#	@remarks If no sound card is installed, the sounds are produced as "beeps" from the PC speaker.
#	Otherwise, sounds can be selected by passing a string. If the string is "" (empty), the default
#	sounds are played. If the string is "off", no sound will be played for that event. Otherwise,
#	the string should be the name of a .WAV file to play.  This function is equivalent to the C API
#	\code
#	void set_cal_sounds(char *target, char *good, char *error);
#	\endcode
#	@param target Sets sound to play when target moves.
#	@param good Sets sound to play on successful operation.
#	@param error Sets sound to play on failure or interruption.
#	@remarks  This function only works with SDL 1.2 in conjunction with eyelink_core_graphics library and cannot be used with EyeLinkCustomDisplay
#
def setCalibrationSounds(*args):
	if not pylinkcg:
		raise RuntimeError("Unable to use setCalibrationSounds before calling openGraphics()")

	if customGraphics:
		raise RuntimeError("Unable to use new setCalibrationSounds on EyeLinkCustomDisplay ")

	pylinkcg.setCalibrationSounds(*args)
	
##	\ingroup graphics_functions
#   Selects the sounds to be played during \c doDriftCorrect(). These events are the display or movement of
#	the target, successful conclusion of drift correction, and pressing the 'ESC' key to start the Setup menu.
#
#	@remarks If no sound card is installed, the sounds are produced as "beeps" from the PC speaker.
#	Otherwise, sounds can be selected by passing a string. If the string is "" (empty), the default sounds
#	are played. If the string is "off", no sound will be played for that event. Otherwise, the string should
#	be the name of a .WAV file to play.  This function is equivalent to the C API
#	\code
#	void set_dcorr_sounds(char *target, char *good, char *setup);
#	\endcode
#	@param target Sets sound to play when target moves.
#	@param good Sets sound to play on successful operation.
#	@param setup Sets sound to play on 'ESC' key pressed.
#	@remarks  This function only works with SDL 1.2 in conjunction with eyelink_core_graphics library and cannot be used with EyeLinkCustomDisplay
#
def setDriftCorrectSounds(*args):
	if not pylinkcg:
		raise RuntimeError("Unable to use setDriftCorrectSounds before calling openGraphics()")

	if customGraphics:
		raise RuntimeError("Unable to use new setDriftCorrectSounds on EyeLinkCustomDisplay ")

	return pylinkcg.setDriftCorrectSounds(*args)
	
##	\ingroup graphics_functions
#   Sets the camera position on the display computer.  Moves the top left hand corner of the camera position
#	to new location.
#
#	@param left X coordinate of upper-left corner of the camera image window.
#	@param top Y coordinate of upper-left corner of the camera image window.
#	@param right X coordinate of lower-right corner of the camera image window.
#	@param bottom Y coordinate of lower-right corner of the camera image window.
#	@remarks  This function only works with SDL 1.2 in conjunction with eyelink_core_graphics library and cannot be used with EyeLinkCustomDisplay
#
def setCameraPosition(*args):
	if not pylinkcg:
		raise RuntimeError("Unable to use setCameraPosition before calling openGraphics()")

	if customGraphics:
		raise RuntimeError("Unable to use new setCameraPosition on EyeLinkCustomDisplay ")

	return pylinkcg.setCameraPosition(*args)
	

##	\ingroup graphics_functions
#   Returns the display configuration.
#
#	@return Instance of DisplayInfo class. The width, height, bits, and refresh rate of the display can be
#			accessed from the returned value.
#
#	\b Example:
#	\code
#	display = getDisplayInformation()
#	print display.width, display.height, display.bits, display.refresh
#	\endcode
def getDisplayInformation(*args):
	if pylinkcg:
		return pylinkcg.getDisplayInformation(*args)

	if customGraphics:
		raise RuntimeError("Unable to use new setCgetDisplayInformationalibrationColors on EyeLinkCustomDisplay ")

	return pylink_cgetDisplayInformation()
	

##	\ingroup graphics_functions
#   Notifies the eyelink_core_graphics or the \ref EyeLinkCustomDisplay to close or release the graphics.
#
#
def closeGraphics():
	global customGraphics
	if pylinkcg:
		return pylinkcg.closeGraphics()

	if customGraphics:
		openCustomGraphicsInternal(None)

		customGraphics=None
		return None
	

def resetBackground(*args):
	if not pylinkcg:
		raise RuntimeError("Unable to use resetBackground before calling openGraphics()")

	if customGraphics:
		raise RuntimeError("Unable to use new resetBackground on EyeLinkCustomDisplay ")

	return pylinkcg.resetBackground(*args)
	
def setCalibrationAnimationTarget(*args):
	if not pylinkcg:
		raise RuntimeError("Unable to use setCalibrationAnimationTarget before calling openGraphics()")

	if customGraphics:
		raise RuntimeError("Unable to use new setCalibrationAnimationTarget on EyeLinkCustomDisplay ")

	return pylinkcg.setCalibrationAnimationTarget(*args)
	
def enableExternalCalibrationDevice(*args):
	if not pylinkcg:
		raise RuntimeError("Unable to use enableExternalCalibrationDevice before calling openGraphics()")

	if customGraphics:
		raise RuntimeError("Unable to use new enableExternalCalibrationDevice on EyeLinkCustomDisplay ")

	return pylinkcg.enableExternalCalibrationDevice(*args)





#try:    
#	if(pyLinkDefaults.EYELINK_OBJECTTYPE == pyLinkDefaults.EYELINK_OBJECT):
#		EyeLink()
#	else:
#
#		EyeLinkListener()
#except :
#	global EYELINK
#	EYELINK = None
#	print "NOTE: Running in NON-EyeLink Mode"
