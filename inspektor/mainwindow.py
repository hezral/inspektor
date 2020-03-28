#!/usr/bin/env python3

'''
   Copyright 2020 Adi Hezral (hezral@gmail.com)

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


class inspektorWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        #applicationwindow construct
        self.props.title = "Inspektor"
        self.set_icon_name("com.github.hezral.inspektor")

        self.set_default_size(240, -1)
        self.props.resizable = False

        self.props.border_width = 0
        self.props.deletable = False
        self.get_style_context().add_class("rounded")
        
        self.set_keep_above(True)
        self.props.window_position = Gtk.WindowPosition.CENTER_ON_PARENT

        #print(self.get_toplevel())

        info_label = Gtk.Label("Info")
        extended_label = Gtk.Label("Metadata:")
        extended_label.set_halign (Gtk.Align.START)

        header_label = Gtk.Box()
        header_label.props.margin_bottom = 10
        header_label.add(info_label)

        basic_grid = Gtk.Grid()
        basic_grid.props.column_spacing = 6
        basic_grid.props.row_spacing = 6
        basic_grid.attach(header_label, 0, 0, 2, 1)
        basic_grid.attach(extended_label, 0, 1, 1, 1)

        extended_grid = Gtk.Grid()
        extended_grid.props.column_spacing = 6
        extended_grid.props.row_spacing = 6
        #extended_grid.attach(extended_label, 0, 0, 2, 1)

        stack = Gtk.Stack()
        stack.add_titled(basic_grid, 'Basic', 'Basic')
        stack.add_titled(extended_grid, 'Extended', 'Extended')

        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.props.homogeneous = True
        stack_switcher.props.margin = 12
        stack_switcher.props.no_show_all = True
        stack_switcher.props.stack = stack
        stack_switcher.show()

        layout = Gtk.Grid ()
        layout.props.margin = 12
        layout.props.margin_top = 0
        layout.props.column_spacing = 12
        layout.props.row_spacing = 6
        layout.attach(stack_switcher, 0, 1, 2, 1)
        layout.attach(stack, 0, 2, 2, 1)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.props.expand = True
        box.pack_start(layout, True, True, 1)
        box.set_halign(Gtk.Align.CENTER)
        self.add(box)   
        self.show_all()



