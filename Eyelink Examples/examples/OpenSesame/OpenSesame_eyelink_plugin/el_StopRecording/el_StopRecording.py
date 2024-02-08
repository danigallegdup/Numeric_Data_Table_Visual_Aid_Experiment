# -*- coding:utf-8 -*-
# Copyright (C) 2021 SR Research 

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

# Import Python 3 compatibility functions
from libopensesame.py3compat import *
from libopensesame import debug
from libopensesame.item import item
from libqtopensesame.items.qtautoplugin import qtautoplugin

from openexp.canvas import canvas
import pylink


class el_StopRecording(item):
    # Provide an informative description for your plug-in.
    description = u'Stop data recording'

    def reset(self):

        """ desc: Resets plug-in to initial values. """
        # Here we provide default values for the variables that are specified
        # in info.jaml
        self.var.el_log_essential_vars = u'yes'

    def prepare(self):

        """The preparation phase of the plug-in goes here."""

        # Call the parent constructor.
        item.prepare(self)

        # self.experiment.dv_var = [v for v in self.experiment.dv_var
        #                           if not ((v in junk_var) or
        #                                   ('time_' in v) or
        #                                   ('count_' in v) or
        #                                   ('correct_' in v) or
        #                                   ('response_' in v))]
        # self.experiment.dv_var.append('response_time')

    def run(self):

        """The run phase of the plug-in goes here."""

        # non-essential variables saved by the OpenSesame Logger
        junk_var = ['title', 'description', 'foreground', 'background', 'height',
                    'width', 'subject_parity', 'pool_folder',
                    'canvas_backend',
                    'clock_backend', 'color_backend', 'compensation', 'coordinates', 'datetime',
                    'delay_preview_objects', 'description', 'experiment_path', 'experiment_file',
                    'disable_garbage_collection', 'font_bold', 'font_family', 'font_italic',
                    'font_size', 'font_underline', 'form_clicks', 'fullscreen', 
                    'keyboard_backend', 'live_row', 'live_row_block', 'logfile', 'mouse_backend',
                    'opensesame_codename', 'opensesame_version', 'opensesame_codename',
                    'psychopy_suppress_warnings', 'repeat_cycle', 'experiment_file',
                    'round_decimals', 'sampler_backend', 'sound_buf_size', 'sound_channels',
                    'sound_freq', 'sound_sample_size', 'start', 'total_correct', 'uniform_coordinates',
                    'total_response_time', 'total_responses']
        
        if self.experiment.dummy_mode is False:
            # send all task-relevant variables to the tracker

            # stop recording
            pylink.pumpDelay(100)  # wait for 100 msec to catch end events
            self.experiment.eyelink.stopRecording()

            # custom variables are not automatically sent
            for v in self.experiment.var.vars():
                if not (v in junk_var):
                    msg = '!V TRIAL_VAR %s %s' % (v, str(self.experiment.var.get(v)))
                    self.experiment.eyelink.sendMessage(msg)
                    self.sleep(2)

            # send a keyword message to mark the ene of a trial
            self.experiment.eyelink.sendMessage('TRIAL_RESULT 0')
        else:
            pass


class qtel_StopRecording(el_StopRecording, qtautoplugin):

    """ This class handles the GUI aspect of the plug-in. By using qtautoplugin, we
    usually need to do hardly anything, because the GUI is defined in info.json. """

    def __init__(self, name, experiment, script=None):

        # We don't need to do anything here, except call the parent
        # constructors.
        el_StopRecording.__init__(self, name, experiment, script)
        qtautoplugin.__init__(self, __file__)
