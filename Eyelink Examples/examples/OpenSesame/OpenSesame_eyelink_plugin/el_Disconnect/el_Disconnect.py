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


class el_Disconnect(item):
    # Provide an informative description for your plug-in.
    description = u'Terminate the link to the EyeLink tracker.'

    def reset(self):
        """ desc:Resets plug-in to initial values """

        # Here we provide default values for the variables that are specified
        # in info.jaml
        pass

    def prepare(self):

        """The preparation phase of the plug-in goes here."""

        # Call the parent constructor.
        item.prepare(self)
        self.data_transfer_canvas = canvas(self.experiment)
        self.data_transfer_canvas.clear()
        self.data_transfer_canvas.text('Retrieving EDF data file from the EyeLink Host PC...')

    def run(self):

        """The run phase of the plug-in goes here."""

        if self.experiment.dummy_mode is not True:

            # File transfer and cleanup!
            self.experiment.eyelink.setOfflineMode()
            pylink.pumpDelay(100)

            # Close the file and transfer it to Display PC
            self.experiment.eyelink.closeDataFile()
            pylink.pumpDelay(100)
            # shwo the "retrieving EDF data file ..." message during data transfer
            self.data_transfer_canvas.show()
            self.experiment.eyelink.receiveDataFile(self.experiment.edf_data_file,
                                                    self.experiment.edf_data_folder + self.experiment.edf_data_file)
            pylink.pumpDelay(1000)  # make sure the transfer file message shows for at least 1 sec
            self.experiment.eyelink.close()
        else:
            pass
            # print('No tracker is connected!')


class qtel_Disconnect(el_Disconnect, qtautoplugin):

    """ this class handles the GUI aspect of the plug-in. By using qtautoplugin, we
    usually need to do hardly anything, because the GUI is defined in info.json.	"""

    def __init__(self, name, experiment, script=None):

        # We don't need to do anything here, except call the parent
        # constructors.
        el_Disconnect.__init__(self, name, experiment, script)
        qtautoplugin.__init__(self, __file__)
