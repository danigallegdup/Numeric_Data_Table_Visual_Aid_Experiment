# -*- coding:utf-8 -*-
# Copyright (C) 2020 Zhiguo Wang

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or (at
# your option) any later version.
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from __future__ import print_function
from openexp.canvas import canvas
from openexp.keyboard import keyboard
from openexp.mouse import mouse
from openexp.synth import synth
from numpy import linspace
from math import sin, cos, pi
from PIL import Image, ImageDraw
from moviepy.video.io.VideoFileClip import VideoFileClip
import array
import string
import pylink
import os.path
import tempfile
import time
import pygame


class EyeLinkCoreGraphicsOpensesame(pylink.EyeLinkCustomDisplay):
    def __init__(self, experiment, tracker):

        '''  Initialize a Custom EyeLinkCoreGraphics

        tracker: an eye-tracker instance
        sticanvas: the OpenSesame display we plan to use for stimulus presentation  '''
	
        pylink.EyeLinkCustomDisplay.__init__(self)
        self.experiment = experiment
        self.display = canvas(self.experiment)
        self.keyboard = keyboard(self.experiment, timeout=0)
        self.mouse = mouse(self.experiment, timeout=1)

        # Simple warning beeps
        self.__target_beep__ = synth(self.experiment, length=50)
        self.__target_beep__done__ = synth(self.experiment, freq=880, length=200)
        self.__target_beep__error__ = synth(self.experiment, freq=220, length=200)

        self.buffer_type = 'I'
        self.imagebuffer = array.array(self.buffer_type)
        self.pal = None
        self.size = (192, 160)
        self.SF = 2.0
        self.cam_img = os.path.join(tempfile.gettempdir(), '_el_cam_.jpg')
        self.vid_img = os.path.join(tempfile.gettempdir(), '_vid_img.jpg')
        self._img_title_ = ''

        # initialize the mediadecoder if using animated calibration targets (videos)
        if self.experiment.cal_target_type == 'image':
            self.cal_target_img = self.experiment.cal_target_img

        if self.experiment.cal_target_type == 'video':
            self.cal_target_vid = self.experiment.cal_target_vid
            self.vid = VideoFileClip(self.experiment.get_file(self.cal_target_vid), audio=0)
            self.vid_start_time = 0.0
            self.vid_current_time = 0.0
            self.vid_X = -32768
            self.vid_Y = -32768
            self.vid_show = False

        self.last_mouse_state = -1

        # set a couple tracker parameters
        self.tracker = tracker
        self.tracker.setOfflineMode()
        # screen resolution
        self.tracker.sendCommand("screen_pixel_coords = 0 0 %d %d" % (self.display.width-1, self.display.height-1))
        self.tracker_version = self.tracker.getTrackerVersion()
        if self.tracker_version >= 3:
            self.tracker.sendCommand("enable_search_limits=YES")
            self.tracker.sendCommand("track_search_limits=YES")
            self.tracker.sendCommand("autothreshold_click=YES")
            self.tracker.sendCommand("autothreshold_repeat=YES")
            self.tracker.sendCommand("enable_camera_position_detect=YES")

    def get_frame_img(self, mov, frame_time):
        ''' this helps to get the current frame of a video'''
        numpy_frame = mov.get_frame(frame_time)
        img = Image.fromarray(numpy_frame)
        img.save(self.vid_img)

    def cal_instructions(self):
        ''' just show the calibration instruction on screen'''

        x = -self.display.width/2+20
        y = -self.display.height/2+20
        y_span = 22
        self.display.text('Enter: Show/hide camera image', False, x, y, font_size=20)
        self.display.text('Left/Right: Switch camera view', False, x, y+y_span, font_size=20)
        self.display.text('C: Calibration', False, x, y+y_span*2, font_size=20)
        self.display.text('V: Validation', False, x, y+y_span*3, font_size=20)
        self.display.text('O: Start Recording', False, x, y+y_span*4, font_size=20)
        self.display.text('+=/-: CR threshold', False, x, y+y_span*5, font_size=20)
        self.display.text('Up/Down: Pupil threshold', False, x, y+y_span*6, font_size=20)
        self.display.text('F1: F1 = EyeLink Hotkey-ESCAPE', False, x, y+y_span*7, font_size=20)

    def setup_cal_display(self):
        ''' Set up the calibration display before entering the calibration/validation routine'''

        self.display.clear()
        #self.cal_instructions()
        self.display.show()

    def clear_cal_display(self):
        ''' Clear the calibration display'''

        self.display.clear()
        self.display.show()

    def exit_cal_display(self):
        ''' Exit the calibration/validation routine'''

        self.display.clear()
        self.display.show()

    def record_abort_hide(self):
        ''' This function is called if aborted'''

        pass

    def erase_cal_target(self):
        ''' Erase the calibration/validation & drift-check target'''

        self.vid_show = False
        self.display.clear()
        self.display.show()

    def draw_cal_target(self, x, y):
        ''' Draw the calibration/validation & drift-check  target'''

        self.display.clear()
        tarX = x - self.display.width/2
        tarY = y - self.display.height/2
        if self.experiment.cal_target_type == 'default':  # dot as calibration target
            self.display.fixdot(tarX, tarY, style='large-open')
        elif self.experiment.cal_target_type == 'image':  # image as custom calibration target
            self.display.image(self.cal_target_img, True, tarX, tarY)
        else:      # video as custom calibration target
            self.vid_start_time = time.time()
            self.get_frame_img(self.vid, self.vid_current_time)
            self.display.image(self.vid_img, True, tarX, tarY)
            self.vid_X = tarX
            self.vid_Y = tarY
            self.vid_show = True

        self.display.show()

    def play_beep(self, beepid):
        ''' Play a sound during calibration/drift correct. '''

        # Simple warning beeps
        self.__target_beep__ = synth(self.experiment, length=50)
        self.__target_beep__done__ = synth(self.experiment, freq=880, length=200)
        self.__target_beep__error__ = synth(self.experiment, freq=220, length=200)

        if beepid == pylink.CAL_TARG_BEEP or beepid == pylink.DC_TARG_BEEP:
            self.__target_beep__.play()
        if beepid == pylink.CAL_ERR_BEEP or beepid == pylink.DC_ERR_BEEP:
            self.__target_beep__error__.play()
        if beepid in [pylink.CAL_GOOD_BEEP, pylink.DC_GOOD_BEEP]:
            self.__target_beep__done__.play()

    def getColorFromIndex(self, colorindex):
        ''' Return psychopy colors for elements in the camera image'''

        if colorindex == pylink.CR_HAIR_COLOR:
            return (255, 255, 255)
        elif colorindex == pylink.PUPIL_HAIR_COLOR:
            return (255, 255, 255)
        elif colorindex == pylink.PUPIL_BOX_COLOR:
            return (0, 255, 0)
        elif colorindex == pylink.SEARCH_LIMIT_BOX_COLOR:
            return (255, 0, 0)
        elif colorindex == pylink.MOUSE_CURSOR_COLOR:
            return (255, 0, 0)
        else:
            return (128,128,128)

    def draw_line(self, x1, y1, x2, y2, colorindex):
        ''' Draw a line. This is used for drawing crosshairs/squares'''

        color = self.getColorFromIndex(colorindex)

        if self.size[0] > 192:
            w,h = self.__img__.im.size
            x1 = int((float(x1) / 192) * w)
            x2 = int((float(x2) / 192) * w)
            y1 = int((float(y1) / 160) * h)
            y2 = int((float(y2) / 160) * h)
        # draw the line
        if not True in [x <0 for x in [x1, x2, y1, y2]]:
            self.__img__.line([(x1, y1), (x2, y2)], color)

    def draw_lozenge(self, x, y, width, height, colorindex):
        ''' draw a lozenge to show the defined search limits
        (x,y) is top-left corner of the bounding box'''

        color = self.getColorFromIndex(colorindex)
        
        if self.size[0] > 192:
            w,h = self.__img__.im.size
            x = int((float(x) / 192) * w)
            y = int((float(y) / 160) * h)
            width  = int((float(width) / 192) * w)
            height = int((float(height) / 160) * h)
	
        if width > height:
            rad = int(height / 2.)
            if rad == 0:
                return
            else:
                self.__img__.line([(x + rad, y), (x + width - rad, y)], color, 1)
                self.__img__.line([(x + rad, y + height), (x + width - rad, y + height)], color, 1)
                self.__img__.arc([x, y, x + rad*2, y + rad*2], 90, 270, color, 1)
                self.__img__.arc([x + width - rad*2, y, x + width, y + height], 270, 90, color, 1)
        else:
            rad = int(width / 2.)
            if rad == 0:
                return
            else:
                self.__img__.line([(x, y + rad), (x, y + height - rad)], color, 1)
                self.__img__.line([(x + width, y + rad), (x + width, y + height - rad)], color, 1)
                self.__img__.arc([x, y, x + rad*2, y + rad*2], 180, 360, color, 1)
                self.__img__.arc([x, y + height-rad*2, x + rad*2, y + height], 0, 180, color, 1)
            

    def get_mouse_state(self):
        '''Get the current mouse position and status'''
        
        state = self.mouse.get_pressed()[0]
        (x, y), timestamp = self.mouse.get_pos()
        if state is None:
            state = -1
       
        x = (x + self.size[0]/2)/2
        y = (y + self.size[1]/2)/2

        return ((x, y), state)

    def get_input_key(self):
        ''' this function will be constantly pools, update the stimuli here is you need
        dynamic calibration target '''

        # update the current video frame if animation calibration target is used
        if self.experiment.cal_target_type == 'video':
            if self.vid_show:
                self.vid_current_time = time.time() - self.vid_start_time
                if self.vid_current_time < self.vid.duration:
                    self.get_frame_img(self.vid, self.vid_current_time)
                    self.display.image(self.vid_img, True,self.vid_X, self.vid_Y)
                    self.display.show()
                else:
                    self.vid_start_time = time.time()
                
        ky=[]
        try:
            keycode, keyTime = self.keyboard.get_key()
            modifier = self.keyboard.get_mods()
            if keycode   in ['f1', 'F1']: k = pylink.ESC_KEY #pylink.F1_KEY
            elif keycode in ['f2', 'F2']: k = pylink.F2_KEY
            elif keycode in ['f3', 'F3']: k = pylink.F3_KEY
            elif keycode in ['f4', 'F4']: k = pylink.F4_KEY
            elif keycode in ['f5', 'F5']: k = pylink.F5_KEY
            elif keycode in ['f6', 'F6']: k = pylink.F6_KEY
            elif keycode in ['f7', 'F7']: k = pylink.F7_KEY
            elif keycode in ['f8', 'F8']: k = pylink.F8_KEY
            elif keycode in ['f9', 'F9']: k = pylink.F9_KEY
            elif keycode in ['f10','F10']: k = pylink.F10_KEY
            elif keycode in ['pageup','PAGEUP','PAGE UP']: k = pylink.PAGE_UP
            elif keycode in ['pagedown','PAGEDOWN', 'PAGE DOWN']: k = pylink.PAGE_DOWN
            elif keycode in ['up','UP']: k = pylink.CURS_UP
            elif keycode in ['down','DOWN']: k = pylink.CURS_DOWN
            elif keycode in ['left','LEFT']: k = pylink.CURS_LEFT
            elif keycode in ['right','RIGHT']: k = pylink.CURS_RIGHT
            elif keycode in ['backspace','BACKSPACE']: k = ord('\b')
            elif keycode in ['return','RETURN']: k = pylink.ENTER_KEY
            elif keycode in ['space','SPACE']: k = ord(' ')
            elif keycode in ['escape','ESCAPE']: k = pylink.ESC_KEY
            elif keycode in ['tab','TAB']: k = ord('\t')
            elif (len(keycode)==1) and (keycode in string.ascii_letters):
                if keycode in ['q', 'Q']:
                    self.experiment.end()
                else:
                    k = ord(keycode)
            else: k = 0

            # plus/equal & minux signs for CR adjustment
            if keycode in ['num_add', 'NUM_ADD', 'EQUAL', 'equal','=']: k = ord('+')
            if keycode in ['num_subtract', 'NUM_SUBTRACT','MINUS', 'minus','-']: k = ord('-')
            
            if 'alt' in modifier:
                mod = 256
            elif 'ctrl' in modifier:
                mod = 64
            elif 'shift' in modifier:
                mod = 1
            else:
                mod = 0
    
            ky.append(pylink.KeyInput(k, mod))

        except:
            ky.append(pylink.KeyInput(0, 0))

        return ky

    def exit_image_display(self):
        '''Clcear the camera image'''
        
        self.mouse.show_cursor(show=True)        
        self.clear_cal_display()

    def alert_printf(self,msg):
        '''Print error messages.'''
        
        print("Error: " + msg)

    def setup_image_display(self, width, height):
        ''' set up the camera image, for newer APIs, the size is 384 x 320 pixels'''

        self.last_mouse_state = -1
        self.mouse.show_cursor(show=False)
        
        self.size = (width, height)
        self.vid_show = False

        return 1

    def image_title(self, text):
        '''Draw title text below the camera image'''

        self._img_title_=text
        
    def draw_image_line(self, width, line, totlines, buff):
        '''Display image pixel by pixel, line by line'''
        
        for i in range(width):
            try:
                self.imagebuffer.append(self.pal[buff[i]])
            except:
                pass
                
        if line == totlines:
            bufferv = self.imagebuffer.tostring()
            try:
                img = Image.frombytes("RGBX", (width, totlines), bufferv)
                self.__img__ = ImageDraw.Draw(img)
                self.draw_cross_hair()
                img = img.resize(self.size)
                img.save(self.cam_img)
                self.display.clear()
                self.display.image(self.cam_img)#, scale=2.0)
                # instructions
                self.cal_instructions()
                # image title
                self.display.text(self._img_title_, True, x=0, y=self.size[0]/2.0-20, font_size=20)
                # cross hairs
                self.display.show()
            except:
                pass
            
            self.imagebuffer = array.array(self.buffer_type)

    def set_image_palette(self, r, g, b):
        ''' Given a set of RGB colors, create a list of 24bit numbers representing the pallet.
        I.e., RGB of (1,64,127) would be saved as 82047, or the number 00000001 01000000 011111111'''

        self.imagebuffer = array.array(self.buffer_type)
        # self.clear_cal_display()
        sz = len(r)
        i =0
        self.pal = []
        while i < sz:
            rf = int(b[i])
            gf = int(g[i])
            bf = int(r[i])
            self.pal.append((rf << 16) | (gf << 8) | (bf))
            i = i+1
