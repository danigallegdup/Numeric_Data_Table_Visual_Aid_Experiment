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


class el_SendMessage(item):
    # Provide an informative description for your plug-in.
    description = u'Send message(s) to the tracker'

    def reset(self):
        """ desc: Resets plug-in to initial values. """

        # Here we provide default values for the variables that are specified
        # in info.jaml
        self.var.el_message_to_send = u''

    def prepare(self):

        """The preparation phase of the plug-in goes here."""

        # Call the parent constructor.
        item.prepare(self)

    def run(self):

        """The run phase of the plug-in goes here."""

        if self.experiment.eyelink is not None:
            #print('message to send: ' + self.var.el_message_to_send)
            msg = self.var.el_message_to_send.split('\n')
            for m in msg:
                self.experiment.eyelink.sendMessage(m)
        else:
            pass


class qtel_SendMessage(el_SendMessage, qtautoplugin):

    """ This class handles the GUI aspect of the plug-in. By using qtautoplugin, we
    usually need to do hardly anything, because the GUI is defined in info.json. """

    def __init__(self, name, experiment, script=None):

        # We don't need to do anything here, except call the parent
        # constructors.
        el_SendMessage.__init__(self, name, experiment, script)
        qtautoplugin.__init__(self, __file__)
