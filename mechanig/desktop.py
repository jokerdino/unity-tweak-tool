#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Team:
#   J Phani Mahesh <phanimahesh@gmail.com>
#   Barneedhar (jokerdino) <barneedhar@ubuntu.com>
#   Amith KK <amithkumaran@gmail.com>
#   Georgi Karavasilev <motorslav@gmail.com>
#   Sam Tran <samvtran@gmail.com>
#   Sam Hewitt <hewittsamuel@gmail.com>
#
# Description:
#   A One-stop configuration tool for Unity.
#
# Legal Stuff:
#
# This file is a part of Mechanig
#
# Mechanig is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; version 3.
#
# Mechanig is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, see <https://www.gnu.org/licenses/gpl-3.0.txt>

import os, os.path

from gi.repository import Gtk, Gio

from .ui import ui
from . import settings
from . import gsettings

class Desktopsettings ():
    def __init__(self, container):
        '''Handler Initialisations.
        Obtain all references here.'''
        self.builder = Gtk.Builder()
        self.glade = (os.path.join(settings.UI_DIR,
                                    'desktop.ui'))
        self.container = container
# TODO : Use os module to resolve to the full path.
        self.builder.add_from_file(self.glade)
        self.ui = ui(self.builder)
        self.page = self.ui['nb_desktop_settings']
        self.page.unparent()

        self.builder.connect_signals(self)
        self.refresh()

#=====================================================================#
#                                Helpers                              #
#=====================================================================#
    def refresh(self):
        '''Reads the current config and refreshes the displayed values'''

        # ===== Icons ===== #
        desktop_icons = gsettings.background.get_boolean("show-desktop-icons")
        dependants = ['l_desktop_icons_display',
                    'check_desktop_home',
                    'check_desktop_networkserver',
                    'check_desktop_trash',
                    'check_desktop_devices']
        if desktop_icons == True:
            self.ui['check_desktop_icons'].set_active(True)
            self.ui.sensitize(dependants)
        else:
            self.ui['check_desktop_icons'].set_active(False)
            self.ui.unsensitize(dependants)
        del desktop_icons
        del dependants

        home_icon = gsettings.desktop.get_boolean('home-icon-visible')
        if home_icon == True:
            self.ui['check_desktop_home'].set_active(True)
        else:
            self.ui['check_desktop_icons'].set_active(False)
        del home_icon

        network_icon = gsettings.desktop.get_boolean('network-icon-visible')
        if network_icon == True:
            self.ui['check_desktop_networkserver'].set_active(True)
        else:
            self.ui['check_desktop_networkserver'].set_active(False)
        del network_icon

        trash_icon = gsettings.desktop.get_boolean('trash-icon-visible')
        if trash_icon == True:
            self.ui['check_desktop_trash'].set_active(True)
        else:
            self.ui['check_desktop_trash'].set_active(False)
        del trash_icon

        devices = gsettings.desktop.get_boolean('volumes-visible')
        if devices == True:
            self.ui['check_desktop_devices'].set_active(True)
        else:
            self.ui['check_desktop_devices'].set_active(False)
        del devices

        # ===== Security ===== #

        lockscreen = gsettings.lockdown.get_boolean('disable-lock-screen')
        if lockscreen == True:
            self.ui['check_security_lock_screen'].set_active(False)
        else:
            self.ui['check_security_lock_screen'].set_active(True)
        del lockscreen

        logout = gsettings.lockdown.get_boolean('disable-log-out')
        if logout == True:
            self.ui['check_security_logout'].set_active(False)
        else:
            self.ui['check_security_logout'].set_active(True)
        del logout

        printing = gsettings.lockdown.get_boolean('disable-printing')
        if printing == True:
            self.ui['check_security_printing'].set_active(False)
        else:
            self.ui['check_security_printing'].set_active(True)
        del printing

        user_switching = gsettings.lockdown.get_boolean('disable-user-switching')
        if user_switching == True:
            self.ui['check_security_user_switching'].set_active(False)
        else:
            self.ui['check_security_user_switching'].set_active(True)
        del user_switching



# TODO : Find a clever way or set each one manually.
# Do it the dumb way now. BIIIG refactoring needed later.

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\
# Dont trust glade to pass the objects properly.            |
# Always add required references to init and use them.      |
# That way, mechanig can resist glade stupidity.            |
# Apologies Gnome devs, but Glade is not our favorite.      |
#___________________________________________________________/


#======== Begin Desktop Icons Settings
    def on_check_desktop_icons_toggled(self, widget, udata = None):
        dependants = ['l_desktop_icons_display',
                    'check_desktop_home',
                    'check_desktop_networkserver',
                    'check_desktop_trash',
                    'check_desktop_devices']

        if self.ui['check_desktop_icons'].get_active() == True:
            gsettings.background.set_boolean("show-desktop-icons", True)
            self.ui.sensitize(dependants)

        else:
            self.ui.unsensitize(dependants)
            gsettings.background.set_boolean("show-desktop-icons", False)

    def on_check_desktop_home_toggled(self, widget, udata = None):
        gsettings.desktop.set_boolean('home-icon-visible',
                                 self.ui['check_desktop_home'].get_active())

    def on_check_desktop_networkserver_toggled(self, widget, udata = None):
        gsettings.desktop.set_boolean('network-icon-visible',
                            self.ui['check_desktop_networkserver'].get_active())

    def on_check_desktop_trash_toggled(self, widget, udata = None):
        gsettings.desktop.set_boolean('trash-icon-visible',
                            self.ui['check_desktop_trash'].get_active())

    def on_check_desktop_devices_toggled(self, widget, udata = None):
        gsettings.desktop.set_boolean('volumes-visible',
                            self.ui['check_desktop_devices'].get_active())

    def on_b_desktop_settings_icons_reset_clicked(self, widget):
        gsettings.desktop.reset('show-desktop-icons')
        gsettings.desktop.reset('home-icon-visible')
        gsettings.desktop.reset('network-icon-visible')
        gsettings.desktop.reset('trash-icon-visible')
        gsettings.desktop.reset('volumes-visible')
        self.refresh()

#======== Begin Desktop Security Settings

    def on_check_security_lock_screen_toggled(self, widget, udata = None):
        if self.ui['check_security_lock_screen'].get_active() == True :
            gsettings.lockdown.set_boolean('disable-lock-screen', False)
        else:
            gsettings.lockdown.set_boolean('disable-lock-screen', True)

    def on_check_security_logout_toggled(self, widget, udata = None):
        if self.ui['check_security_logout'].get_active() == True :
            gsettings.lockdown.set_boolean('disable-log-out', False)
        else:
            gsettings.lockdown.set_boolean('disable-log-out', True)

    def on_check_security_printing_toggled(self, widget, udata = None):
        if self.ui['check_security_printing'].get_active() == True :
            gsettings.lockdown.set_boolean('disable-printing', False)
            gsettings.lockdown.set_boolean('disable-print-setup', False)
        else:
            gsettings.lockdown.set_boolean('disable-printing', True)
            gsettings.lockdown.set_boolean('disable-print-setup', True)

    def on_check_security_user_switching_toggled(self, widget, udata = None):
        if self.ui['check_security_user_switching'].get_active() == True :
            gsettings.lockdown.set_boolean('disable-user-switching', False)
        else:
            gsettings.lockdown.set_boolean('disable-user-switching', True)

    def on_b_desktop_settings_security_reset_clicked(self, widget):
        gsettings.lockdown.reset('disable-lock-screen')
        gsettings.lockdown.reset('disable-log-out')
        gsettings.lockdown.reset('disable-printing')
        gsettings.lockdown.reset('disable-print-setup')
        gsettings.lockdown.reset('disable-user-switching')
        self.refresh()

if __name__ == '__main__':
# Fire up the Engines
    Desktopsettings()
