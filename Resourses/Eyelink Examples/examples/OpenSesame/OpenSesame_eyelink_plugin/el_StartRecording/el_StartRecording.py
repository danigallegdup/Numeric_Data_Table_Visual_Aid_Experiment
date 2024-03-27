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
import pylink


class el_StartRecording(item):
    # Provide an informative description for your plug-in.
    description = u'Start data recording'

    def reset(self):

        """ desc: Resets plug-in to initial values. """

        # Here we provide default values for the variables that are specified
        # in info.jaml
        self.var.el_link_data_events = u'yes'
        self.var.el_link_data_samples = u'yes'
        self.var.el_file_data_events = u'yes'
        self.var.el_file_data_samples = u'yes'
        self.var.el_recording_status_msg = u''

    def prepare(self):

        """The preparation phase of the plug-in goes here."""

        # Call the parent constructor.
        item.prepare(self)

    def run(self):

        """The run phase of the plug-in goes here."""
        link_events = 0
        link_samples = 0
        file_events = 0
        file_samples = 0
        if self.var.el_link_data_events == u'yes':
            link_events = 1
        if self.var.el_link_data_samples == u'yes':
            link_samples = 1
        if self.var.el_file_data_events == u'yes':
            file_events = 1
        if self.var.el_file_data_samples == u'yes':
            file_samples = 1

        if self.experiment.dummy_mode is False:
            # we first send a keyword message to the tracker to mark the start of a new trial
            self.experiment.eyelink.sendMessage('TRIALID')

            # send a recording status message to the tracker.
           
            self.experiment.eyelink.sendCommand("record_status_message '%s'" % self.var.el_recording_status_msg)

            # start recording and specify what data is saved in file and what data are available over link
            self.experiment.eyelink.startRecording(file_samples, file_events, link_samples, link_events)
            pylink.pumpDelay(100)  # wait for 100 msec to allow the tracker to buffer some samples
        else:
            pass
        print(self.var.el_recording_status_msg)


class qtel_StartRecording(el_StartRecording, qtautoplugin):

    """ This class handles the GUI aspect of the plug-in. By using qtautoplugin, we
    usually need to do hardly anything, because the GUI is defined in info.json. """

    def __init__(self, name, experiment, script=None):

        # We don't need to do anything here, except call the parent
        # constructors.
        el_StartRecording.__init__(self, name, experiment, script)
        qtautoplugin.__init__(self, __file__)
