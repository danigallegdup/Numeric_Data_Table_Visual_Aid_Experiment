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

import os
import pylink
from libopensesame.item import item
from libopensesame.py3compat import *
from libqtopensesame.items.qtautoplugin import qtautoplugin


class el_Connect(item):
    # Provide an informative description for your plug-in.
    description = u'Establish a link to the EyeLink tracker'

    def reset(self):
        """
        desc:
            Resets plug-in to initial values.
        """

        # Here we provide default values for the variables that are specified
        # in info.jaml
        self.var.el_ip = u'100.1.1.1'
        self.var.el_tracker_version = u'EyeLink 1000 Plus'
        self.var.el_camera_mount = u'Desktop'
        self.var.el_mount_usage = u'Head Stabilized'
        self.var.el_dummy_mode = u'no'

        self.var.el_link_filter = u'STANDARD'
        self.var.el_file_filter = u'EXTRA'
        self.var.el_eye_event_data = u'GAZE'
        self.var.el_saccade_sensitivity = u'NORMAL'
        self.var.el_tracking_mode = u'PUPIL-CR'
        self.var.el_pupil_detection = u'CENTROID'
        self.var.el_sampling_rate = u'1000'

        self.var.el_eye_to_track = u'RIGHT'
        self.var.el_pupil_size = u'AREA'

        self.var.el_edf_folder_name = u'edf_data'

    def prepare(self):

        """The preparation phase of the plug-in goes here."""

        item.prepare(self)

    def run(self):

        """The run phase of the plug-in goes here."""

        if self.var.el_dummy_mode == u'yes':  # check if we have dummy mode enabled
            self.experiment.eyelink = pylink.EyeLink(None)
            self.experiment.dummy_mode = True
        else:
            self.experiment.eyelink = pylink.EyeLink(self.var.el_ip)
            self.experiment.dummy_mode = False
	
# add 'eyelink' to the Python workspace, so users can reference to "eyelink" directly
        self.python_workspace[u'eyelink'] = self.experiment.eyelink

        if self.experiment.dummy_mode is False:  # set up a few parameters if not in dummy mode
            # check tracker version, and set data stored in data file and passed over the link (online)
            eyelinkVer = self.experiment.eyelink.getTrackerVersion()
            self.experiment.eyelink.sendCommand("file_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON,INPUT")
            self.experiment.eyelink.sendCommand("link_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,BUTTON,FIXUPDATE,INPUT")
            if eyelinkVer >= 3:  # eyelink 1000/1000 plus
                self.experiment.eyelink.sendCommand("file_sample_data = LEFT,RIGHT,GAZE,HREF,RAW,AREA,HTARGET,GAZERES,BUTTON,STATUS,INPUT")
                self.experiment.eyelink.sendCommand("link_sample_data = LEFT,RIGHT,GAZE,GAZERES,AREA,HTARGET,STATUS,INPUT")
            else:  # Eyelink II/I
                self.experiment.eyelink.sendCommand("file_sample_data = LEFT,RIGHT,GAZE,HREF,RAW,AREA,GAZERES,BUTTON,STATUS,INPUT")
                self.experiment.eyelink.sendCommand("link_sample_data = LEFT,RIGHT,GAZE,GAZERES,AREA,STATUS,INPUT")

            # Link and file filter level
            if self.var.el_link_filter == u'NO_FILTER':
                link_filter = 0
            elif self.var.el_link_filter == u'STANDARD':
                link_filter = 1
            else:
                link_filter = 2

            if self.var.el_file_filter == u'NO_FILTER':
                file_filter = 0
            elif self.var.el_file_filter == u'STANDARD':
                file_filter = 1
            else:
                file_filter = 2

            self.experiment.eyelink.sendCommand('heuristic_filter %d %d' % (link_filter, file_filter))

            # tracking setting
            # Eye event type
            if self.var.el_eye_event_data == u'GAZE':
                self.experiment.eyelink.sendCommand("recording_parse_type GAZE")
            else:
                self.experiment.eyelink.sendCommand("recording_parse_type HREF")

            # saccade sensitivity
            if self.var.el_saccade_sensitivity == u'NORMAL':
                self.experiment.eyelink.sendCommand('select_parser_configuration 0')
            else:
                self.experiment.eyelink.sendCommand('select_parser_configuration 1')

            # tracking mode/algorithm, only set this option for EyeLink II
            if eyelinkVer == 2:
                if self.var.el_tracking_mode == u'PUPIL-CR':
                    self.experiment.eyelink.sendCommand('corneal_mode YES')
                else:
                    self.experiment.eyelink.sendCommand('corneal_mode NO')

            # sampling rate
            if eyelinkVer >= 3:
                self.experiment.eyelink.sendCommand('sample_rate %s' % self.var.el_sampling_rate)

            # eyes to track
            if self.var.el_eye_to_track == u'BOTH':
                self.experiment.eyelink.sendCommand('binocular_enabled YES')
            else:
                self.experiment.eyelink.sendCommand('binocular_enabled NO')
                self.experiment.eyelink.sendCommand('active_eye %s' % self.var.el_eye_to_track)

            # pupil size measure, AREA vs. DIAMETER
            if self.var.el_pupil_size == u'AREA':
                self.experiment.eyelink.sendCommand('pupil_size_diameter AREA')
            else:
                self.experiment.eyelink.sendCommand('pupil_size_diameter DIAMETER')

            # after a link has been established, create an EDF data folder to save the EDF data files
            # check if it's Windows or a linux machine
            if os.name == u'nt': 
            	self.experiment.edf_data_folder = self.experiment.experiment_path + '\\' + self.var.el_edf_folder_name + '\\'
            else:  
            	self.experiment.edf_data_folder = self.experiment.experiment_path + '/' + self.var.el_edf_folder_name + '/'
            if not os.path.exists(self.experiment.edf_data_folder):
                os.makedirs(self.experiment.edf_data_folder)

            # use subject number to name the EDF data file; the EDF file name cannot exceed 8 characters
            self.experiment.edf_data_file = '{:.8}'.format(str(self.experiment.subject_nr)) + '.EDF'
            self.experiment.eyelink.openDataFile(self.experiment.edf_data_file)

            # write file preable text
            self.experiment.eyelink.sendCommand("add_file_preamble_text '%s'" % self.experiment.title)
      


class qtel_Connect(el_Connect, qtautoplugin):

    """
    This class handles the GUI aspect of the plug-in. By using qtautoplugin, we
    usually need to do hardly anything, because the GUI is defined in info.json.
    """

    def __init__(self, name, experiment, script=None):

        # We don't need to do anything here, except call the parent constructors.
        el_Connect.__init__(self, name, experiment, script)
        qtautoplugin.__init__(self, __file__)

    def apply_edit_changes(self):

        # Applies the controls.
        if not qtautoplugin.apply_edit_changes(self) or self.lock:
            return False
        self.custom_interactions()

    def edit_widget(self):

        # Refreshes the controls.
        if self.lock:
            return

        self.lock = True
        w = qtautoplugin.edit_widget(self)
        self.custom_interactions()
        self.lock = False
        return w

    def custom_interactions(self):

        """ all necessary option changes for the tracker."""

        # Force ELLIPSE mode when operating in 'Remote' mode
        if self.combobox_el_mount_usage.currentIndex() == 1:  # 0-Head-stabilized, 1-Remote
            self.combobox_el_pupil_detection.setCurrentIndex(1)  # 0-CENTROID, 1-ELLIPSE
            self.combobox_el_pupil_detection.setEnabled(False)
        else:
            self.combobox_el_pupil_detection.setEnabled(True)

        # pupil tracking algorithm for different tracker models
        if self.combobox_el_tracker_version.currentIndex() == 0:  # EyeLink I -Pupil ONLY
            self.combobox_el_tracking_mode.setCurrentIndex(1)  # 0-Pupil_CR, 1-Pupil_only

        if self.combobox_el_tracker_version.currentIndex() in [2, 3, 4]:  # EyeLink 1000/1000Plus/PortableDUO
            self.combobox_el_tracking_mode.setCurrentIndex(0)  # 0-Pupil_CR, 1-Pupil_only

        if self.combobox_el_tracker_version.currentIndex() == 1:  # EyeLink II
            self.combobox_el_tracking_mode.setEnabled(True)
        else:
            self.combobox_el_tracking_mode.setEnabled(False)

        # Disable sampling rate setting for EyeLink I/II, & set up default sampling rate
        if self.combobox_el_tracker_version.currentIndex() == 0:  # eyelink I, 250 Hz
            self.combobox_el_sampling_rate.setCurrentIndex(0)
        elif self.combobox_el_tracker_version.currentIndex() == 1:  # EyeLink II, 500 Hz
            if self.combobox_el_tracking_mode.currentIndex == 0:
                # 250 Hz, when PUPIL_CR mode is selected
                self.combobox_el_sampling_rate.setCurrentIndex(0)
            else:
                self.combobox_el_sampling_rate.setCurrentIndex(1)
        else:
            self.combobox_el_sampling_rate.setEnabled(True)
            if self.combobox_el_mount_usage.currentIndex() == 1:  # remote mode,
                self.combobox_el_sampling_rate.setCurrentIndex(1)  # 500 Hz by default
            elif self.combobox_el_tracker_version.currentIndex() == 4:  # portable DUO
                self.combobox_el_sampling_rate.setCurrentIndex(1)  # 500 Hz by default
            else:
                self.combobox_el_sampling_rate.setCurrentIndex(2)  # otherwise, 1000 Hz by default

        # disable the mount options for EyeLink I/II, portable DUO
        if self.combobox_el_tracker_version.currentIndex() in [0, 1, 4]:
            self.combobox_el_camera_mount.setCurrentIndex(0)  # set to 'Desktop' & disable
            self.combobox_el_camera_mount.setEnabled(False)
        else:
            self.combobox_el_camera_mount.setEnabled(True)

        # disable the tracking mode (head-stabilized or remote) in Long-range & Tower mount
        if self.combobox_el_camera_mount.currentIndex() in [1, 3]:
            self.combobox_el_mount_usage.setEnabled(False)
        else:
            self.combobox_el_mount_usage.setEnabled(True)

        # disable the tracking mode (head-stabilized or remote) in EyeLink I/II
        if self.combobox_el_tracker_version.currentIndex() in [0, 1]:
            self.combobox_el_mount_usage.setEnabled(False)
        else:
            self.combobox_el_mount_usage.setEnabled(True)

        # gray out sampling rate selectionf for EyeLink I/II
        if self.combobox_el_tracker_version.currentIndex() in [0, 1]:
            self.combobox_el_sampling_rate.setEnabled(False)
        else:
            self.combobox_el_sampling_rate.setEnabled(True)
