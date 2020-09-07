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

import re
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, Pango
from constants import data


class inspektorWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.basedata = data().basedata
        
        # applicationwindow construct
        self.props.title = "Inspektor"
        self.set_icon_name("com.github.hezral.inspektor")
        self.props.resizable = False
        # self.props.deletable = False
        # self.set_keep_above(True)
        self.props.window_position = Gtk.WindowPosition.CENTER_ON_PARENT
        self.props.border_width = 0
        self.get_style_context().add_class("rounded")
        self.set_default_size(400, -1)


        # header label filename construct
        self.filename = Gtk.Label()
        self.filename.set_label('unknown')
        self.filename.props.halign = Gtk.Align.START
        self.filename.props.valign = Gtk.Align.FILL
        self.filename.props.max_width_chars = 30
        self.filename.props.ellipsize = Pango.EllipsizeMode.MIDDLE
        self.filename.props.selectable = True
        
        # header label fileicon construct
        self.fileicon = Gtk.Image.new_from_icon_name("unknown", Gtk.IconSize.DIALOG)
        self.fileicon.props.halign = Gtk.Align.START
        self.fileicon.set_valign(Gtk.Align.CENTER)

        # header label grid construct
        header_label_grid = Gtk.Grid()
        header_label_grid.props.margin_top = 12
        header_label_grid.props.margin_left = 24
        header_label_grid.props.margin_right = 24
        header_label_grid.props.column_spacing = 12
        header_label_grid.attach(self.fileicon, 0, 1, 1, 1)
        header_label_grid.attach_next_to(self.filename, self.fileicon, Gtk.PositionType.RIGHT, 1, 1)

        # actions grid construct
        action_grid = Gtk.Grid()
        action_grid.props.margin_top = 12
        action_grid.props.margin_left = 24
        action_grid.props.margin_right = 24
        action_grid.props.column_spacing = 12

        # base info construct
        self.base_grid = Gtk.Grid()
        self.base_grid.props.halign = Gtk.Align.FILL
        self.base_grid.props.valign = Gtk.Align.FILL
        self.base_grid.props.expand = True
        self.base_grid.props.margin = 24
        self.base_grid.props.margin_top = 18
        self.base_grid.props.column_spacing = 6
        self.base_grid.props.row_spacing = 6

        # extended info construct
        self.extended_grid = Gtk.Grid()
        self.extended_grid.props.halign = Gtk.Align.FILL
        self.extended_grid.props.valign = Gtk.Align.FILL
        self.extended_grid.props.expand = True
        self.extended_grid.props.margin = 24
        self.extended_grid.props.margin_top = 18
        self.extended_grid.props.column_spacing = 6
        self.extended_grid.props.row_spacing = 6

        # info stack contstruct
        stack = Gtk.Stack()
        stack.add_titled(self.base_grid, 'base', 'Base')
        stack.add_titled(self.extended_grid, 'extended', 'Extended')

        # info stack switcher contruct
        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.props.homogeneous = True
        stack_switcher.props.margin_top = 18
        stack_switcher.props.margin_left = 24
        stack_switcher.props.margin_right = 24
        stack_switcher.props.no_show_all = True
        stack_switcher.props.stack = stack
        stack_switcher.props.expand = True
        stack_switcher.show()

        # layout contruct
        layout = Gtk.Grid()
        layout.attach(header_label_grid, 0, 1, 1, 1)
        layout.attach(stack_switcher, 0, 2, 2, 1)
        layout.attach(stack, 0, 3, 2, 1)
        layout.props.expand = True

        self.add(layout)

    
    def filechooser(self):
        filechooserdialog = Gtk.FileChooserDialog()
        filechooserdialog.add_button("_Open", Gtk.ResponseType.OK)
        filechooserdialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        filechooserdialog.set_default_response(Gtk.ResponseType.OK)
        filechooserdialog.set_transient_for(self)
        filechooserdialog.set_destroy_with_parent(True)
        filechooserdialog.set_position(Gtk.WindowPosition.MOUSE)
        
        response = filechooserdialog.run()
        file = None
        if response == Gtk.ResponseType.OK:
            file = filechooserdialog.get_file() #return a GLocalFile object
            filechooserdialog.destroy()
        else:
            filechooserdialog.destroy()
            self.destroy()
        if file is not None:
            return file

    def get_fileicon(self, file):
        size = 48
        filedata = Gio.File.new_for_path(file)
        info = filedata.query_info('standard::icon' , 0 , Gio.Cancellable())
        fileicon = None
        for icon_name in info.get_icon().get_names():
            if fileicon is None:
                try:
                    fileicon = Gtk.IconTheme.get_default().load_icon(icon_name, size, 0)
                    self.fileicon.set_from_pixbuf(fileicon)
                except:
                    pass

    def update_data_grid(self, file, dict):
        # set the file icon
        self.get_fileicon(file.get_path())
        # set file name
        self.filename.set_label(file.get_basename())
        self.filename.set_tooltip_text(self.filename.get_label())

        i = 1
        for key in self.basedata:
            title = titleLabel(key)
            value = valueLabel(dict[key])
            self.base_grid.attach(title, 0, i, 1, 1)
            self.base_grid.attach_next_to(value, title, Gtk.PositionType.RIGHT, 1, 1)
            i = i + 1
        
        i = 1
        for key in dict:
            if key not in self.basedata:
                title = titleLabel(key)
                value = valueLabel(str(dict[key]))
                self.extended_grid.attach(title, 0, i, 1, 1)
                self.extended_grid.attach_next_to(value, title, Gtk.PositionType.RIGHT, 1, 1)
                i = i + 1
        

class valueLabel(Gtk.Label):
    def __init__(self, title):
        super().__init__()
        self.props.halign = Gtk.Align.START
        self.props.valign = Gtk.Align.START
        self.props.selectable = True
        self.props.max_width_chars = 30
        self.props.wrap = True
        self.props.wrap_mode = Pango.WrapMode.CHAR
        if title is None:
            self.set_label('unknown')
        else:
            self.set_label(title)


class titleLabel(Gtk.Label):
    def __init__(self, title):
        super().__init__()
        self.props.halign = Gtk.Align.END
        self.props.valign = Gtk.Align.START
        self.props.wrap = True
        self.props.selectable = True
        self.props.wrap_mode = Pango.WrapMode.WORD_CHAR
        title = title + ': '
        self.set_label(title)