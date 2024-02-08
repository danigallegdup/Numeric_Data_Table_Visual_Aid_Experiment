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


class el_DriftCheck(item):
    # Provide an informative description for your plug-in.
    description = u'Perform drift-correction/check'

    def reset(self):

        """ desc: Resets plug-in to initial values. """

        # Here we provide default values for the variables that are specified
        # in info.jaml
        self.var.el_drift_tar_x = u'%d' % 0
        self.var.el_drift_tar_y = u'%d' % 0
        self.var.el_allow_setup = u'yes'
        self.var.el_force_drift_correct = u'no'
        self.var.el_dc_target_type = u'SameAsCalibration'
        self.var.el_dc_target_file = u''

    def prepare(self):

        """The preparation phase of the plug-in goes here."""

        # Call the parent constructor.
        item.prepare(self)

        # prepare the drift-correction display
        self.dc_canvas = canvas(self.experiment)

    def run(self):

        """The run phase of the plug-in goes here."""

        if self.experiment.dummy_mode is False:
            print('connected to tracker')
            # decide if you the drawing routine in the CoreGraphics to draw the drift
            # correction target, 1=yes, 0=no
            target_sameAsCalibration = 1
            if self.var.el_dc_target_type == u'Image':
                target_sameAsCalibration = 0
            # load image as calibration target
            if self.var.el_dc_target_type == u'Image':
                target_img = self.experiment.pool[self.var.el_dc_target_file]
                self.dc_canvas.image(target_img, True, x=int(self.var.el_drift_tar_x),
                                     y=int(self.var.el_drift_tar_y))
                self.dc_canvas.show()
            # decide if allow setup
            allow_setup = 0
            if self.var.el_allow_setup == u'yes':
                allow_setup = 1

            while True:
                try:
                    err = self.experiment.eyelink.doDriftCorrect(int(self.var.el_drift_tar_x+self.dc_canvas.width/2.0),
                                                                 int(self.var.el_drift_tar_y+self.dc_canvas.height/2.0),
                                                                 target_sameAsCalibration, allow_setup)
                    if err == 0:  # break following a success drift-check
                        break
                except:
                    pass
        else:
            pass
		

class qtel_DriftCheck(el_DriftCheck, qtautoplugin):

    """
    This class handles the GUI aspect of the plug-in. By using qtautoplugin, we
    usually need to do hardly anything, because the GUI is defined in info.json.
    """

    def __init__(self, name, experiment, script=None):
        # We don't need to do anything here, except call the parent
        # constructors.
        el_DriftCheck.__init__(self, name, experiment, script)
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
        ''' all necessary option changes for the tracker.'''

        if self.combobox_el_dc_target_type.currentIndex() == 0:
            self.filepool_el_dc_target_file.setEnabled(False)
        else:
            self.filepool_el_dc_target_file.setEnabled(True)
