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

from gi.repository import Gtk, Gio, Gdk

from .ui import ui
from . import settings
from . import gsettings

class Unitysettings ():
    def __init__(self, container):
        '''Handler Initialisations.
        Obtain all references here.'''
        self.builder = Gtk.Builder()
        self.glade = (os.path.join(settings.UI_DIR,
                                    'unity.ui'))
        self.container = container
# TODO : Use os module to resolve to the full path.
        self.builder.add_from_file(self.glade)
        self.ui = ui(self.builder)
        self.page = self.ui['nb_unitysettings']
        self.page.unparent()
        self.builder.connect_signals(self)

        self.ui['sc_reveal_sensitivity'].add_mark(2.0, Gtk.PositionType.BOTTOM, None)

        self.ui['sc_launcher_transparency'].add_mark(.666, Gtk.PositionType.BOTTOM, None)

        self.ui['sc_panel_transparency'].add_mark(.67, Gtk.PositionType.BOTTOM, None)

        if Gdk.Screen.get_default().get_n_monitors() == 1:
            dependants = ['l_launcher_visibility',
                          'radio_launcher_visibility_all',
                          'radio_launcher_visibility_primary']
            self.ui.unsensitize(dependants)


        self.refresh()

#=====================================================================#
#                                Helpers                              #
#=====================================================================#
    def refresh(self):
        '''Reads the current config and refreshes the displayed values'''

        # ====== Launcher Helpers ===== #

        # Auto hide
        dependants = ['radio_reveal_left',
                    'radio_reveal_topleft',
                    'sc_reveal_sensitivity',
                    'l_launcher_reveal',
                    'l_launcher_reveal_sensitivity']

        if gsettings.unityshell.get_int('launcher-hide-mode'):
            self.ui['sw_launcher_hidemode'].set_active(True)
            self.ui.sensitize(dependants)
        else:
            self.ui['sw_launcher_hidemode'].set_active(False)
            self.ui.unsensitize(dependants)
        del dependants

        # Reveal
        self.ui['radio_reveal_left'].set_active(True if gsettings.unityshell.get_int('reveal-trigger') is 0 else False)
        self.ui['radio_reveal_topleft'].set_active(True if gsettings.unityshell.get_int('reveal-trigger') is 1 else False)
        self.ui['sc_reveal_sensitivity'].set_value(gsettings.unityshell.get_double('edge-responsiveness'))

        # Transparency
        dependants = ['l_launcher_transparency_scale',
                    'sc_launcher_transparency']
        opacity = gsettings.unityshell.get_double('launcher-opacity')
        if opacity == 1:
            self.ui['sw_launcher_transparent'].set_active(False)
            self.ui.unsensitize(dependants)
        else:
            self.ui['sw_launcher_transparent'].set_active(True)
            self.ui.sensitize(dependants)
        self.ui['sc_launcher_transparency'].set_value(0.67)
        del dependants
        del opacity

        # Visibility
        mode = gsettings.unityshell.get_int('num-launchers')
        self.ui['radio_launcher_visibility_all'].set_active(True if mode is 0 else False)
        self.ui['radio_launcher_visibility_primary'].set_active(True if mode is 1 else False)
        del mode

        # Colour
        color = gsettings.unityshell.get_string('background-color')
        if color.endswith('00'):
            self.ui['radio_launcher_color_cham'].set_active(True)
            self.ui.unsensitize(['color_launcher_color_cus'])
        else:
            self.ui['radio_launcher_color_cus'].set_active(True)
            self.ui.sensitize(['color_launcher_color_cus'])
        valid, gdkcolor = Gdk.Color.parse(color[:-2])
        if valid:
            self.ui['color_launcher_color_cus'].set_color(gdkcolor)
        del color, valid, gdkcolor

        # Icons
        self.ui['spin_launcher_icon_size'].set_value(gsettings.unityshell.get_int('icon-size'))
        self.ui['cbox_launcher_icon_colouring'].set_active(gsettings.unityshell.get_int('backlight-mode'))
        self.ui['cbox_urgent_animation'].set_active(gsettings.unityshell.get_int('urgent-animation'))
        self.ui['cbox_launch_animation'].set_active(gsettings.unityshell.get_int('launch-animation'))

        # Show Desktop
        self.ui['sw_launcher_show_desktop'].set_active(True if 'unity://desktop-icon' in gsettings.launcher.get_strv('favorites') else False)


        # ====== Dash Helpers ===== #

        # Blur
        dash_blur = gsettings.unityshell.get_int('dash-blur-experimental')
        dependants = ['radio_dash_blur_smart',
                    'radio_dash_blur_static',
                    'l_dash_blur_type']

        if dash_blur == 0:
            self.ui['sw_dash_blur'].set_active(False)
            self.ui.unsensitize(dependants)
        elif dash_blur == 1:
            self.ui['sw_dash_blur'].set_active(True)
            self.ui.sensitize(dependants)
            self.ui['radio_dash_blur_static'].set_active(True)
        else:
            self.ui['sw_dash_blur'].set_active(True)
            self.ui.sensitize(dependants)
            self.ui['radio_dash_blur_smart'].set_active(True)
        del dependants

        # Suggestions
        dash_suggestions = gsettings.lenses.get_string('remote-content-search')
        if dash_suggestions == 'all':
            self.ui['sw_dash_suggestions'].set_active(True)
        else:
            self.ui['sw_dash_suggestions'].set_active(False)

        # Applications Lens
        self.ui['check_show_recent_apps'].set_active(gsettings.lens_apps.get_boolean('display-recent-apps'))
        self.ui['check_show_available_apps'].set_active(gsettings.lens_apps.get_boolean('display-available-apps'))


        # ====== Panel Helpers ====== #

        self.ui['spin_menu_visible'].set_value(gsettings.unityshell.get_int('menus-discovery-duration'))

        dependants = ['l_transparent_panel',
                    'sc_panel_transparency',
                    'check_panel_opaque']

        opacity = gsettings.unityshell.get_double('panel-opacity')
        if opacity == 1:
            self.ui['sw_transparent_panel'].set_active(False)
            self.ui.unsensitize(dependants)
        else:
            self.ui['sw_transparent_panel'].set_active(True)
            self.ui.sensitize(dependants)
        self.ui['sc_panel_transparency'].set_value(opacity)
        del dependants
        del opacity

        # Panel opacity
        panel_opacity_value = gsettings.unityshell.get_boolean('panel-opacity-maximized-toggle')
        if panel_opacity_value == True:
            self.ui['check_panel_opaque'].set_active(True)
        else:
            self.ui['check_panel_opaque'].set_active(False)
        del panel_opacity_value

        # Date time indicator
        clock_visibility = gsettings.datetime.get_boolean('show-clock')
        dependants = ['radio_12hour',
                    'radio_24hour',
                    'check_date',
                    'check_weekday',
                    'check_calendar',
                    'l_clock',
                    'check_time_seconds']

        if clock_visibility == True:
            self.ui['check_indicator_datetime'].set_active(True)
            self.ui.sensitize(dependants)
        else:
            self.ui['check_indicator_datetime'].set_active(False)
            self.ui.sensitize(dependants)
        del clock_visibility
        del dependants

        # User name indicator
        show_username = gsettings.session.get_boolean('show-real-name-on-panel')
        if show_username == True:
            self.ui['check_indicator_username'].set_active(True)
        else:
            self.ui['check_indicator_username'].set_active(False)
        del show_username

        # Battery status
        battery_status = gsettings.power.get_string('icon-policy')

        dependants = ['check_indicator_battery_life',
                    'radio_power_charging',
                    'radio_power_always']

        if battery_status == 'present':
            self.ui['check_indicator_battery'].set_active(True)
            self.ui.sensitize(dependants)
        elif battery_status == 'charge':
            self.ui['check_indicator_battery'].set_active(True)
            self.ui.sensitize(dependants)
        elif battery_status == 'never':
            self.ui['check_indicator_battery'].set_active(False)
            self.ui.unsensitize(dependants)
        else:
            self.ui['check_indicator_battery'].set_active(True)
            self.ui.sensitize(dependants)
        del battery_status
        del dependants


        # Battery life indicator
        battery_life = gsettings.power.get_boolean('show-time')

        if battery_life == True:
            self.ui['check_indicator_battery_life'].set_active(True)
        else:
            self.ui['check_indicator_battery_life'].set_active(False)
        del battery_life

        # 24 hour time format
        time_format = gsettings.datetime.get_string('time-format')
        if time_format == '12-hour':
            self.ui['radio_12hour'].set_active(True)
        else:
            self.ui['radio_24hour'].set_active(True)
        del time_format

        # Seconds
        show_seconds = gsettings.datetime.get_boolean('show-seconds')
        if show_seconds == True:
            self.ui['check_time_seconds'].set_active(True)
        else:
            self.ui['check_time_seconds'].set_active(False)
        del show_seconds

        # Date
        show_date = gsettings.datetime.get_boolean('show-date')
        if show_date == True:
            self.ui['check_date'].set_active(True)
        else:
            self.ui['check_date'].set_active(False)
        del show_date

        # Day
        show_weekday = gsettings.datetime.get_boolean('show-day')
        if show_weekday == True:
            self.ui['check_weekday'].set_active(True)
        else:
            self.ui['check_weekday'].set_active(False)
        del show_weekday

        # Calendar
        show_calendar = gsettings.datetime.get_boolean('show-calendar')
        if show_calendar == True:
            self.ui['check_calendar'].set_active(True)
        else:
            self.ui['check_calendar'].set_active(False)
        del show_calendar

        # Bluetooth indicator
        show_bluetooth = gsettings.bluetooth.get_boolean('visible')
        if show_bluetooth == True:
            self.ui['check_indicator_bluetooth'].set_active(True)
        else:
            self.ui['check_indicator_bluetooth'].set_active(False)
        del show_bluetooth

        # Sound indicator
        show_sound = gsettings.sound.get_boolean('visible')
        if show_sound == True:
            self.ui['check_indicator_sound'].set_active(True)
        else:
            self.ui['check_indicator_sound'].set_active(False)
        del show_sound

        show_notifyosd = gsettings.sound.get_boolean('show-notify-osd-on-scroll')
        if show_notifyosd == True:
            self.ui['check_scroll_notifyosd'].set_active(True)
        else:
            self.ui['check_scroll_notifyosd'].set_active(False)
        del show_notifyosd

        # Default Player
        interested_players = gsettings.sound.get_strv('interested-media-players')
        preferred_players = gsettings.sound.get_strv('preferred-media-players')

        for player in interested_players:
            self.ui['cbox_default_player'].append_text(player.capitalize())
            if preferred_players[0] in interested_players:
                self.ui['cbox_default_player'].set_active(interested_players.index(preferred_players[0]))
        del player

        # ====== Unity Switcher helpers ====== #

        self.ui['check_switchwindows_all_workspaces'].set_active(True if gsettings.unityshell.get_boolean('alt-tab-bias-viewport') is False else False)
        self.ui['check_switcher_showdesktop'].set_active(True if gsettings.unityshell.get_boolean('disable-show-desktop') is False else False)
        self.ui['check_minimizedwindows_switch'].set_active(gsettings.unityshell.get_boolean('show-minimized-windows'))
        self.ui['check_autoexposewindows'].set_active(gsettings.unityshell.get_boolean('alt-tab-timeout'))


        model = self.ui['list_unity_switcher_windows_accelerators']

        alt_tab_forward = gsettings.unityshell.get_string('alt-tab-forward')
        iter_alt_tab_forward = model.get_iter_first()
        model.set_value(iter_alt_tab_forward, 1, alt_tab_forward)

        alt_tab_prev = gsettings.unityshell.get_string('alt-tab-prev')
        iter_alt_tab_prev = model.iter_next(iter_alt_tab_forward)
        model.set_value(iter_alt_tab_prev, 1, alt_tab_prev)

        alt_tab_forward_all = gsettings.unityshell.get_string('alt-tab-forward-all')
        iter_alt_tab_forward_all = model.iter_next(iter_alt_tab_prev)
        model.set_value(iter_alt_tab_forward_all, 1, alt_tab_forward_all)

        alt_tab_prev_all = gsettings.unityshell.get_string('alt-tab-prev-all')
        iter_alt_tab_prev_all = model.iter_next(iter_alt_tab_forward_all)
        model.set_value(iter_alt_tab_prev_all, 1, alt_tab_prev_all)

        alt_tab_right = gsettings.unityshell.get_string('alt-tab-right')
        iter_alt_tab_right = model.iter_next(iter_alt_tab_prev_all)
        model.set_value(iter_alt_tab_right, 1, alt_tab_right)

        alt_tab_left = gsettings.unityshell.get_string('alt-tab-left')
        iter_alt_tab_left = model.iter_next(iter_alt_tab_right)
        model.set_value(iter_alt_tab_left, 1, alt_tab_left)

        alt_tab_detail_start = gsettings.unityshell.get_string('alt-tab-detail-start')
        iter_alt_tab_detail_start = model.iter_next(iter_alt_tab_left)
        model.set_value(iter_alt_tab_detail_start, 1, alt_tab_detail_start)

        alt_tab_detail_stop = gsettings.unityshell.get_string('alt-tab-detail-stop')
        iter_alt_tab_detail_stop = model.iter_next(iter_alt_tab_detail_start)
        model.set_value(iter_alt_tab_detail_stop, 1, alt_tab_detail_stop)

        alt_tab_next_window = gsettings.unityshell.get_string('alt-tab-next-window')
        iter_alt_tab_next_window = model.iter_next(iter_alt_tab_detail_stop)
        model.set_value(iter_alt_tab_next_window, 1, alt_tab_next_window)

        alt_tab_prev_window = gsettings.unityshell.get_string('alt-tab-prev-window')

        iter_alt_tab_prev_window = model.iter_next(iter_alt_tab_next_window)
        model.set_value(iter_alt_tab_prev_window, 1, alt_tab_prev_window)

        del model

        model = self.ui['list_unity_switcher_launcher_accelerators']

        launcher_switcher_forward = gsettings.unityshell.get_string('launcher-switcher-forward')
        iter_launcher_switcher_forward = model.get_iter_first()
        model.set_value(iter_launcher_switcher_forward, 1, launcher_switcher_forward)

        launcher_switcher_prev = gsettings.unityshell.get_string('launcher-switcher-prev')
        iter_launcher_switcher_prev = model.iter_next(iter_launcher_switcher_forward)
        model.set_value(iter_launcher_switcher_prev, 1, launcher_switcher_prev)

        del model, launcher_switcher_forward, iter_launcher_switcher_forward, launcher_switcher_prev, iter_launcher_switcher_prev


        # ====== Unity additional helpers ======= #

        self.ui['check_shortcuts_hints_overlay'].set_active(gsettings.unityshell.get_boolean('shortcut-overlay'))

        model = self.ui['list_unity_additional_accelerators']

        show_hud = gsettings.unityshell.get_string('show-hud')
        iter_show_hud = model.get_iter_first()
        model.set_value(iter_show_hud, 1, show_hud)

        show_launcher = gsettings.unityshell.get_string('show-launcher')
        iter_show_launcher = model.iter_next(iter_show_hud)
        model.set_value(iter_show_launcher, 1, show_launcher)

        execute_command = gsettings.unityshell.get_string('execute-command')
        iter_execute_command = model.iter_next(iter_show_launcher)
        model.set_value(iter_execute_command, 1, execute_command)

        keyboard_focus = gsettings.unityshell.get_string('keyboard-focus')
        iter_keyboard_focus = model.iter_next(iter_execute_command)
        model.set_value(iter_keyboard_focus, 1, keyboard_focus)

        panel_first_menu = gsettings.unityshell.get_string('panel-first-menu')
        iter_panel_first_menu = model.iter_next(iter_keyboard_focus)
        model.set_value(iter_panel_first_menu, 1, panel_first_menu)

        del model, show_hud, iter_show_hud, show_launcher, iter_show_launcher, execute_command, iter_execute_command, keyboard_focus, iter_keyboard_focus, panel_first_menu, iter_panel_first_menu


# TODO : Find a clever way or set each one manually.
# Do it the dumb way now. BIIIG refactoring needed later.



# ===== BEGIN: Unity settings =====
# ----- BEGIN: Launcher -----

    def on_sw_launcher_hidemode_active_notify(self, widget, udata = None):
        dependants = ['radio_reveal_left',
                    'radio_reveal_topleft',
                    'sc_reveal_sensitivity',
                    'l_launcher_reveal',
                    'l_launcher_reveal_sensitivity']

        if self.ui['sw_launcher_hidemode'].get_active():
            gsettings.unityshell.set_int("launcher-hide-mode", 1)
            gsettings.unityshell.set_double('edge-responsiveness', 2.0)
            self.ui.sensitize(dependants)
        else:
            gsettings.unityshell.set_int("launcher-hide-mode", 0)
            self.ui.unsensitize(dependants)

    def on_radio_reveal_left_toggled(self, button, udata = None):
        radio = self.ui['radio_reveal_left']
        mode = 0 if radio.get_active() else 1
        gsettings.unityshell.set_int('reveal-trigger', mode)

# XXX :Strictly speaking, only one of these two will suffice.
    def on_radio_reveal_topleft_toggled(self, button, udata = None):
        radio = self.ui['radio_reveal_topleft']
        mode = 0 if not radio.get_active() else 1
        gsettings.unityshell.set_int('reveal-trigger', mode)

    def on_sc_reveal_sensitivity_value_changed(self, widget, udata = None):
        slider = self.ui['sc_reveal_sensitivity']
        val = slider.get_value()
        gsettings.unityshell.set_double('edge-responsiveness', val)

    def on_sw_launcher_transparent_active_notify(self, widget, udata = None):
        dependants = ['l_launcher_transparency_scale',
                    'sc_launcher_transparency']

        opacity = self.ui['sc_launcher_transparency'].get_value()

        if widget.get_active():
            self.ui.sensitize(dependants)
            if self.ui['sc_launcher_transparency'].get_value() == 1.0:
                self.ui['sc_launcher_transparency'].set_value(0.67)
                gsettings.unityshell.set_double('launcher-opacity', 0.33)
            else:
                panel_transparency = self.ui['sc_panel_transparency'].get_value()
                gsettings.unityshell.set_double('launcher-opacity', opacity)
        else:
            self.ui.unsensitize(dependants)
            gsettings.unityshell.set_double('launcher-opacity', 1.00)

    def on_sc_launcher_transparency_value_changed(self, widget, udata = None):
        opacity = self.ui['sc_launcher_transparency'].get_value()
        gsettings.unityshell.set_double('launcher-opacity', opacity)

    def on_radio_launcher_visibility_all_toggled(self, widget, udata = None):
        if self.ui['radio_launcher_visibility_all'].get_active():
            gsettings.unityshell.set_int('num-launchers', 0)
        else:
            gsettings.unityshell.set_int('num-launchers', 1)

    def on_radio_launcher_color_cus_toggled(self, widget, udata = None):
        dependants = ['color_launcher_color_cus']
        color = self.ui['color_launcher_color_cus'].get_color()
        colorhash = gsettings.color_to_hash(color)
        if self.ui['radio_launcher_color_cus'].get_active():
            self.ui.sensitize(dependants)
            gsettings.unityshell.set_string('background-color', colorhash)
        else:
            self.ui.unsensitize(dependants)
            gsettings.unityshell.set_string('background-color', colorhash[:-2]+'00')

    def on_color_launcher_color_cus_color_set(self, widget, udata = None):
        color = self.ui['color_launcher_color_cus'].get_color()
        colorhash = gsettings.color_to_hash(color)
        gsettings.unityshell.set_string('background-color', colorhash)

    def on_spin_launcher_icon_size_value_changed(self, widget, udata = None):
        size = self.ui['spin_launcher_icon_size'].get_value()
        gsettings.unityshell.set_int('icon-size', size)

    def on_cbox_launcher_icon_colouring_changed(self, widget, udata = None):
        mode = self.ui['cbox_launcher_icon_colouring'].get_active()
        gsettings.unityshell.set_int('backlight-mode', mode)

    def on_cbox_urgent_animation_changed(self, widget, udata = None):
        mode = self.ui['cbox_urgent_animation'].get_active()
        gsettings.unityshell.set_int('urgent-animation', mode)

    def on_cbox_launch_animation_changed(self, widget, udata = None):
        mode = self.ui['cbox_launch_animation'].get_active()
        gsettings.unityshell.set_int('launch-animation', mode)

    def on_sw_launcher_show_desktop_active_notify(self, widget, udata = None):
        fav = gsettings.launcher.get_strv('favorites')
        desktop = "unity://desktop-icon"
        if self.ui['sw_launcher_show_desktop'].get_active():
            if desktop not in fav:
                fav.append(desktop)
                gsettings.launcher.set_strv('favorites', fav)
        else:
            if desktop in fav:
                fav.remove(desktop)
                gsettings.launcher.set_strv('favorites', fav)

    def on_b_unity_launcher_reset_clicked(self, widget):
        gsettings.unityshell.reset('launch-animation')
        gsettings.unityshell.reset('urgent-animation')
        gsettings.unityshell.reset('backlight-mode')
        gsettings.unityshell.reset('icon-size')
        gsettings.unityshell.reset('background-color')
        gsettings.unityshell.reset('num-launchers')
        gsettings.unityshell.reset('panel-opacity')
        gsettings.unityshell.reset('launcher-opacity')
        gsettings.unityshell.reset('launcher-hide-mode')
        gsettings.unityshell.reset('edge-responsiveness')
        gsettings.unityshell.reset('reveal-trigger')

        # Remove "Show Desktop" icon
        fav = gsettings.launcher.get_strv('favorites')
        desktop = "unity://desktop-icon"
        if desktop in fav:
            fav.remove(desktop)
            gsettings.launcher.set_strv('favorites', fav)

        self.refresh()

# ----- END: Launcher -----

# ----- BEGIN: Dash -----

    def on_sw_dash_blur_active_notify(self, widget, udata = None):
        dependants = ['radio_dash_blur_smart',
                    'radio_dash_blur_static',
                    'l_dash_blur_type']

        if self.ui['sw_dash_blur'].get_active():
            self.ui.sensitize(dependants)

            # Setting it to Active blur (2) instead of static blur (1)
            gsettings.unityshell.set_int('dash-blur-experimental', 2)
            self.ui['radio_dash_blur_smart'].set_active(True)

        else:
            self.ui.unsensitize(dependants)
            gsettings.unityshell.set_int('dash-blur-experimental', 0)

    def on_radio_dash_blur_smart_toggled(self, button, udata = None):
        mode = 2 if button.get_active() else 1
        gsettings.unityshell.set_int('dash-blur-experimental', mode)

    def on_sw_dash_suggestions_active_notify(self, widget, udata = None):
        if self.ui['sw_dash_suggestions'].get_active():
            gsettings.lenses.set_string('remote-content-search', "all")

        else:
            gsettings.lenses.set_string('remote-content-search', "none")

    def on_check_show_recent_apps_toggled(self, widget, udata = None):
        gsettings.lens_apps.set_boolean('display-recent-apps',
                            self.ui['check_show_recent_apps'].get_active())

    def on_check_show_available_apps_toggled(self, widget, udata = None):
        gsettings.lens_apps.set_boolean('display-available-apps',
                            self.ui['check_show_available_apps'].get_active())


    def on_b_unity_dash_reset_clicked(self, widget):
        gsettings.unityshell.reset('dash-blur-experimental')
        gsettings.lenses.reset('remote-content-search')
        gsettings.lens_apps.reset('display-recent-apps')
        gsettings.lens_apps.reset('display-available-apps')
        self.refresh()

#----- END: Dash -------

#----- BEGIN: Panel -----

    def on_spin_menu_visible_value_changed(self, widget, udata = None):

        seconds = self.ui['spin_menu_visible'].get_value()
        gsettings.unityshell.set_int('menus-discovery-duration', seconds)


    # selective selection in unity-panel  part 1

    def on_sw_transparent_panel_active_notify(self, widget, udata = None):
        dependants = ['sc_panel_transparency',
                    'l_transparent_panel',
                    'check_panel_opaque']

        if widget.get_active():
            self.ui.sensitize(dependants)

            if self.ui['sc_panel_transparency'].get_value() == 1.0:
                self.ui['sc_panel_transparency'].set_value(0.67)
                self.ui['check_panel_opaque'].set_active(True)
                gsettings.unityshell.set_double('panel-opacity', 0.33)
                gsettings.unityshell.set_boolean('panel-opacity-maximized-toggle', True)

            else:
                panel_transparency = self.ui['sc_panel_transparency'].get_value()
                gsettings.unityshell.set_double('panel-opacity', panel_transparency)

        else:
            self.ui.unsensitize(dependants)
            gsettings.unityshell.set_double('panel-opacity', 1.00)

    def on_sc_panel_transparency_value_changed(self, widget, udata = None):
        panel_transparency = widget.get_value()
        gsettings.unityshell.set_double('panel-opacity', panel_transparency)

    def on_check_panel_opaque_toggled(self, widget, udata = None):

        if widget.get_active():
            gsettings.unityshell.set_boolean('panel-opacity-maximized-toggle', True)
        else:
            gsettings.unityshell.set_boolean('panel-opacity-maximized-toggle', False)

    def on_check_indicator_username_active(self, widget, udata = None):

        if widget.get_active():
            gsettings.session.set_boolean('show-real-name-on-panel', True)
        else:
            gsettings.session.set_boolean('show-real-name-on-panel', False)

    def on_check_indicator_battery_toggled(self, widget, udata = None):
        dependants = ['check_indicator_battery_life',
                    'radio_power_charging',
                    'radio_power_always']

        if self.ui['check_indicator_battery'].get_active() == True:
            gsettings.power.set_string('icon-policy', 'charge')
            self.ui.sensitize(dependants)
        else:
            gsettings.power.set_string('icon-policy', 'never')
            self.ui.unsensitize(dependants)

    def on_radio_power_charging_toggled(self, button, udata = None):

        mode = self.ui['radio_power_charging'].get_active()

        if mode == 'True':
            gsettings.power.set_string('icon-policy', "charge")
        else:
            gsettings.power.set_string('icon-policy', "present")

    def on_radio_power_always_toggled(self, button, udata = None):

        mode = self.ui['radio_power_always'].get_active()

        if mode == 'True':
            gsettings.power.set_string('icon-policy', "present")
        else:
            gsettings.power.set_string('icon-policy', "charge")

    def on_check_indicator_battery_life_toggled(self, widget, udata = None):

        if widget.get_active():
            gsettings.power.set_boolean('show-time', True)
        else:
            gsettings.power.set_boolean('show-time', False)

    def on_check_indicator_datetime_active(self, widget, udata = None):
        dependants = ['radio_12hour',
                    'radio_24hour',
                    'check_date',
                    'check_weekday',
                    'l_clock',
                    'check_calendar',
                    'check_time_seconds']

        if widget.get_active():
            gsettings.datetime.set_boolean('show-clock', True)
            self.ui.sensitize(dependants)
        else:
            gsettings.datetime.set_boolean('show-clock', False)
            self.ui.unsensitize(dependants)

    def on_radio_12hour_toggled(self, button, udata = None):

        mode = self.ui['radio_12hour'].get_active()

        if mode == 'True':
            gsettings.datetime.set_string('time-format', '24-hour')
        else:
            gsettings.datetime.set_string('time-format', '12-hour')

    def on_radio_24hour_toggled(self, button, udata = None):

        mode = self.ui['radio_24hour'].get_active()

        if mode == 'True':
            gsettings.datetime.set_string('time-format', '12-hour')
        else:
            gsettings.datetime.set_string('time-format', '24-hour')


    def on_check_time_seconds_toggled(self, widget, udata = None):
        gsettings.datetime.set_boolean('show-seconds',
                  self.ui['check_time_seconds'].get_active())

    def on_check_date_toggled(self, widget, udata = None):
        gsettings.datetime.set_boolean('show-date',
                  self.ui['check_date'].get_active())

    def on_check_weekday_toggled(self, widget, udata = None):
        gsettings.datetime.set_boolean('show-day',
                  self.ui['check_weekday'].get_active())

    def on_check_calendar_toggled(self, widget, udata = None):
        gsettings.datetime.set_boolean('show-calendar',
                  self.ui['check_calendar'].get_active())

    def on_check_indicator_bluetooth_toggled(self, widget, udata = None):

        if widget.get_active():
            gsettings.bluetooth.set_boolean('visible', True)
        else:
            gsettings.bluetooth.set_boolean('visible', False)

    def on_check_indicator_sound_toggled(self, widget, udata = None):

        if widget.get_active():
            gsettings.sound.set_boolean('visible', True)
        else:
            gsettings.sound.set_boolean('visible', False)

    def on_check_scroll_notifyosd_toggled(self, widget, udata = None):

        if widget.get_active():
            gsettings.sound.set_boolean('show-notify-osd-on-scroll', True)
        else:
            gsettings.sound.set_boolean('show-notify-osd-on-scroll', False)

    def on_cbox_default_player_changed(self, widget, udata = None):
        combobox_text = self.ui['cbox_default_player'].get_active_text()
        gsettings.sound.set_strv('preferred-media-players', [combobox_text.lower()])

    def on_b_unity_panel_reset_clicked(self, widget):
        gsettings.sound.reset('visible')
        gsettings.bluetooth.reset('visible')
        gsettings.datetime.reset('show-calendar')
        gsettings.datetime.reset('show-day')
        gsettings.datetime.reset('show-date')
        gsettings.datetime.reset('show-seconds')
        gsettings.datetime.reset('show-clock')
        gsettings.datetime.reset('time-format')
        gsettings.power.reset('show-time')
        gsettings.power.reset('icon-policy')
        gsettings.session.reset('show-real-name-on-panel')
        gsettings.unityshell.reset('panel-opacity-maximized-toggle')
        gsettings.unityshell.reset('panel-opacity')
        gsettings.sound.reset('preferred-media-players')
        gsettings.sound.reset('show-notify-osd-on-scroll')
        self.refresh()

#----- END: Panel -----

#----- BEGIN: Switcher -----

    def on_check_switchwindows_all_workspaces_toggled(self, widget, udata = None):

        if widget.get_active():
            gsettings.unityshell.set_boolean('alt-tab-bias-viewport', False)

        else:
            gsettings.unityshell.set_boolean('alt-tab-bias-viewport', True)


    def on_check_switcher_showdesktop_toggled(self, widget, udata = None):

        if widget.get_active():
            gsettings.unityshell.set_boolean("disable-show-desktop", False)

        else:
            gsettings.unityshell.set_boolean("disable-show-desktop", True)

    def on_check_minimizedwindows_switch_toggled(self, widget, udata = None):

        if widget.get_active():
            gsettings.unityshell.set_boolean("show-minimized-windows", True)

        else:
            gsettings.unityshell.set_boolean("show-minimized-windows", False)

    def on_check_autoexposewindows_toggled(self, widget, udata = None):

        if widget.get_active():
            gsettings.unityshell.set_boolean('alt-tab-timeout', True)

        else:
            gsettings.unityshell.set_boolean('alt-tab-timeout', False)

    # keyboard widgets in unity-windows-switcher

    def on_craccel_unity_switcher_windows_accel_edited(self, craccel, path, key, mods, hwcode, model = None):
        model = self.ui['list_unity_switcher_windows_accelerators']
        accel = Gtk.accelerator_name(key, mods)
        titer = model.get_iter(path)
        model.set_value(titer, 1, accel)
        # Python has no switch statement, right?

        if path == '0':
            gsettings.unityshell.set_string('alt-tab-forward', accel)
        elif path == '1':
            gsettings.unityshell.set_string('alt-tab-prev', accel)
        elif path == '2':
            gsettings.unityshell.set_string('alt-tab-forward-all', accel)
        elif path == '3':
            gsettings.unityshell.set_string('alt-tab-prev-all', accel)
        elif path == '4':
            gsettings.unityshell.set_string('alt-tab-right', accel)
        elif path == '5':
            gsettings.unityshell.set_string('alt-tab-left', accel)
        elif path == '6':
            gsettings.unityshell.set_string('alt-tab-detail-start', accel)
        elif path == '7':
            gsettings.unityshell.set_string('alt-tab-detail-stop', accel)
        elif path == '8':
            gsettings.unityshell.set_string('alt-tab-next-window', accel)
        elif path == '9':
            gsettings.unityshell.set_string('alt-tab-prev-window', accel)

    def on_craccel_unity_switcher_windows_accel_cleared(self, craccel, path, model = None):
        model = self.ui['list_unity_switcher_windows_accelerators']
        titer = model.get_iter(path)
        model.set_value(titer, 1, "Disabled")
        if path == '0':
            gsettings.unityshell.set_string('alt-tab-forward', "Disabled")
        elif path == '1':
            gsettings.unityshell.set_string('alt-tab-prev', "Disabled")
        elif path == '2':
            gsettings.unityshell.set_string('alt-tab-forward-all', "Disabled")
        elif path == '3':
            gsettings.unityshell.set_string('alt-tab-prev-all', "Disabled")
        elif path == '4':
            gsettings.unityshell.set_string('alt-tab-right', "Disabled")
        elif path == '5':
            gsettings.unityshell.set_string('alt-tab-left', "Disabled")
        elif path == '6':
            gsettings.unityshell.set_string('alt-tab-detail-start', "Disabled")
        elif path == '7':
            gsettings.unityshell.set_string('alt-tab-detail-stop', "Disabled")
        elif path == '8':
            gsettings.unityshell.set_string('alt-tab-next-window', "Disabled")
        elif path == '9':
            gsettings.unityshell.set_string('alt-tab-prev-window', "Disabled")

    # keyboard widgets in unity-launcher-switcher

    def on_craccel_unity_switcher_launcher_accel_edited(self, craccel, path, key, mods, hwcode, model = None):
        model = self.ui['list_unity_switcher_launcher_accelerators']
        accel = Gtk.accelerator_name(key, mods)
        titer = model.get_iter(path)
        model.set_value(titer, 1, accel)
        # Python has no switch statement, right?

        if path == '0':
            gsettings.unityshell.set_string('launcher-switcher-forward', accel)
        else:
            gsettings.unityshell.set_string('launcher-switcher-prev', accel)

    def on_craccel_unity_switcher_launcher_accel_cleared(self, craccel, path, model = None):
        model = self.ui['list_unity_switcher_launcher_accelerators']
        titer = model.get_iter(path)
        model.set_value(titer, 1, "Disabled")
        if path == '0':
            gsettings.unityshell.set_string('launcher-switcher-forward', "Disabled")
        else:
            gsettings.unityshell.set_string('launcher-switcher-prev', "Disabled")

    def on_b_unity_switcher_reset_clicked(self, widget):
        gsettings.unityshell.reset('alt-tab-bias-viewport')
        gsettings.unityshell.reset('disable-show-desktop')
        gsettings.unityshell.reset('show-minimized-windows')
        gsettings.unityshell.reset('alt-tab-timeout')
        gsettings.unityshell.reset('alt-tab-forward')
        gsettings.unityshell.reset('alt-tab-prev')
        gsettings.unityshell.reset('alt-tab-forward-all')
        gsettings.unityshell.reset('alt-tab-prev-all')
        gsettings.unityshell.reset('alt-tab-right')
        gsettings.unityshell.reset('alt-tab-left')
        gsettings.unityshell.reset('alt-tab-detail-start')
        gsettings.unityshell.reset('alt-tab-detail-stop')
        gsettings.unityshell.reset('alt-tab-next-window')
        gsettings.unityshell.reset('alt-tab-prev-window')
        gsettings.unityshell.reset('launcher-switcher-forward')
        gsettings.unityshell.reset('launcher-switcher-prev')
        self.refresh()

#----- END: Switch -----

#----- BEGIN: Additional -----

    def on_check_shortcuts_hints_overlay_toggled(self, widget, udata = None):

        if widget.get_active():
            gsettings.unityshell.set_boolean('shortcut-overlay', True)

        else:
            gsettings.unityshell.set_boolean('shortcut-overlay', False)


    # keyboard widgets in unity-additional

    def on_craccel_unity_additional_accel_edited(self, craccel, path, key, mods, hwcode, model = None):
        # Glade has a habit of swapping arguments. beware.
        model = self.ui['list_unity_additional_accelerators']
        accel = Gtk.accelerator_name(key, mods)
        titer = model.get_iter(path)
        model.set_value(titer, 1, accel)

        # Python has no switch statement, right?

        if path == '0':
            gsettings.unityshell.set_string('show-hud', accel)
        elif path == '1':
            gsettings.unityshell.set_string('show-launcher', accel)
        elif path == '2':
            gsettings.unityshell.set_string('execute-command', accel)
        elif path == '3':
            gsettings.unityshell.set_string('keyboard-focus', accel)
        else:
            gsettings.unityshell.set_string('panel-first-menu', accel)

    def on_craccel_unity_additional_accel_cleared(self, craccel, path, model = None):
        model = self.ui['list_unity_additional_accelerators']
        titer = model.get_iter(path)
        model.set_value(titer, 1, "Disabled")
        if path == '0':
            gsettings.unityshell.set_string('show-hud', "Disabled")
        elif path == '1':
            gsettings.unityshell.set_string('show-launcher', "Disabled")
        elif path == '2':
            gsettings.unityshell.set_string('execute-command', "Disabled")
        elif path == '3':
            gsettings.unityshell.set_string('keyboard-focus', "Disabled")
        else:
            gsettings.unityshell.set_string('panel-first-menu', "Disabled")

    def on_b_unity_additional_reset_clicked(self, widget):
        gsettings.unityshell.reset('shortcut-overlay')
        gsettings.unityshell.reset('show-hud')
        gsettings.unityshell.reset('show-launcher')
        gsettings.unityshell.reset('execute-command')
        gsettings.unityshell.reset('keyboard-focus')
        gsettings.unityshell.reset('panel-first-menu')
        self.refresh()

#----- END: Additional -----

if __name__ == '__main__':
# Fire up the Engines
    Unitysettings()
