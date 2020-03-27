#!/usr/bin/env python3

'''
   Copyright 2018 Adi Hezral (hezral@gmail.com)

   This file is part of inspektor.

    inspektor is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    inspektor is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with inspektor.  If not, see <http://www.gnu.org/licenses/>.
'''

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from widgets.headerbar import inspektorHeaderBar
from widgets.listboxrow import inspektorListRow
from widgets.infoview import inspektorInfoView
from widgets.listbox import inspektorListBox
from widgets.inspektorview import inspektorView


class inspektorWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        #applicationwindow construct
        self.props.title = "inspektor"
        self.props.resizable = False
        self.props.border_width = 0
        self.set_icon_name("com.github.hezral.inspektor")
        self.get_style_context().add_class("rounded")
        self.set_default_size(360, 480)
        self.set_keep_above(True)
        self.props.window_position = Gtk.WindowPosition.CENTER
        
        #applicationwindow theme
        settings = Gtk.Settings.get_default()
        settings.set_property("gtk-application-prefer-dark-theme", True)

        listbox_view = inspektorListBox()
        #initial launch add some rows
        welcome_text = "Welcome to inspektor"
        welcome_image = Gtk.Image.new_from_icon_name("system-os-installer", Gtk.IconSize.MENU)
        welcome_image.set_pixel_size(96)
        listbox_view.add(inspektorListRow(welcome_image))
        listbox_view.add(inspektorListRow(welcome_text))
        listbox_view.add(inspektorListRow(welcome_image))
        
        # inspektor_view
        self.inspektor_view = inspektorView(listbox_view)

        #welcome_view
        info_view = inspektorInfoView("No inspektor Found","Start Copying Stuffs", "system-os-installer")
        
        #search_view
        #settings_view

        #stack_view
        stack_view = Gtk.Stack()
        stack_view.add_named(self.inspektor_view, "inspektor_view")
        stack_view.add_named(info_view, "info_view")
        stack_view.set_visible_child_name("inspektor_view")

        def toggle_stack(self):
            if stack_view.get_visible_child_name() == 'inspektor_view':
                stack_view.set_visible_child_full("info_view",Gtk.StackTransitionType.CROSSFADE)
            else:
                stack_view.set_visible_child_full("inspektor_view",Gtk.StackTransitionType.CROSSFADE)

        #headerbar construct
        header_bar = inspektorHeaderBar()        
        header_bar.settings_icon.connect('clicked',toggle_stack)

        self.set_titlebar(header_bar)

        self.add(stack_view)
        self.show()
        self.show_all()

        # hide toolbar buttons on all rows by iterating through all the child objects in listbox
        listbox_view.foreach(lambda child, data: child.hide_buttons(), None)
        #print(len(listbox_view))

    def check(self, widget, event):
        print(type(self.inspektor_view))

