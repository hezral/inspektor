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
from parser import parser


class inspektorWindow(Gtk.ApplicationWindow):
    def __init__(self, parser, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.basedata = data().basedata
        self.parser = parser
        self.file = None
        
        # applicationwindow construct
        self.props.title = "Inspektor"
        #self.set_icon_name("com.github.hezral.inspektor")
        self.props.resizable = False
        # self.props.deletable = False
        # self.set_keep_above(True)
        self.props.window_position = Gtk.WindowPosition.CENTER_ON_PARENT
        self.props.border_width = 0
        self.get_style_context().add_class("rounded")
        self.set_default_size(400, 560)
        #self.set_icon_name("accessories-camera")


        # header label filename construct
        self.filename = Gtk.Label()
        self.filename.set_label('unknown')
        self.filename.props.halign = Gtk.Align.START
        self.filename.props.valign = Gtk.Align.FILL
        self.filename.props.max_width_chars = 40
        self.filename.props.ellipsize = Pango.EllipsizeMode.MIDDLE
        self.filename.props.selectable = False
        
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


        # basic data grid construct
        self.base_data_grid = Gtk.Grid()
        self.base_data_grid.props.halign = Gtk.Align.FILL
        self.base_data_grid.props.valign = Gtk.Align.FILL
        self.base_data_grid.props.expand = False
        self.base_data_grid.props.column_spacing = 6
        self.base_data_grid.props.row_spacing = 6
        self.base_data_grid.props.margin_top = 5
        self.base_data_grid.props.margin_left = 5
        self.base_data_grid.props.margin_right = 5

        # file comments constructor
        self.file_comments = Gtk.TextBuffer()
        self.file_comments.set_text("")
        comments_textview = Gtk.TextView(buffer=self.file_comments)
        comments_textview.props.margin = 4

        comments_scrolledview = Gtk.ScrolledWindow()
        comments_scrolledview.add(comments_textview)
        comments_scrolledview.props.shadow_type = Gtk.ShadowType(3)
        comments_scrolledview.props.vscrollbar_policy = Gtk.PolicyType(1)
        comments_scrolledview.props.expand = True

        comments_grid = Gtk.Grid()
        comments_grid.props.column_spacing = 6
        comments_grid.props.row_spacing = 6
        comments_grid.props.expand = True
        comments_grid_label = Gtk.Label(label="Comments:")
        comments_grid_label.props.halign = Gtk.Align.START
        comments_grid_label.props.margin_left = 5
        comments_grid.attach(comments_grid_label, 0, 1, 1, 1)
        comments_grid.attach(comments_scrolledview, 0, 2, 1, 1)

        # base grid for stack
        base_grid = Gtk.Grid()
        base_grid.props.expand = True
        base_grid.props.margin = 24
        base_grid.props.column_spacing = 6
        base_grid.props.row_spacing = 12
        base_grid.attach(self.base_data_grid, 0, 1, 1, 1)
        base_grid.attach(Gtk.HSeparator(), 0, 2, 1, 1)
        base_grid.attach(comments_grid, 0, 3, 1, 1)



        # extended data grid construct
        self.extended_data_grid = Gtk.Grid()
        self.extended_data_grid.props.halign = Gtk.Align.FILL
        self.extended_data_grid.props.valign = Gtk.Align.FILL
        self.extended_data_grid.props.expand = True
        self.extended_data_grid.props.margin = 4
        self.extended_data_grid.props.column_spacing = 6
        self.extended_data_grid.props.row_spacing = 6

        extended_scrolledview = Gtk.ScrolledWindow()
        extended_scrolledview.add(self.extended_data_grid)
        extended_scrolledview.props.shadow_type = Gtk.ShadowType(3)
        extended_scrolledview.props.vscrollbar_policy = Gtk.PolicyType(1)

        # base grid for stack
        extended_grid = Gtk.Grid()
        extended_grid.props.expand = True
        extended_grid.props.margin = 24
        extended_grid.props.column_spacing = 6
        extended_grid.props.row_spacing = 6
        extended_grid.attach(extended_scrolledview, 0, 1, 1, 1)

        # info stack contstruct
        stack = Gtk.Stack()
        stack.add_titled(base_grid, 'base', 'Base')
        stack.add_titled(extended_grid, 'extended', 'Extended')

        # info stack switcher contruct
        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.props.homogeneous = True
        stack_switcher.props.margin_top = 18
        stack_switcher.props.margin_left = 24
        stack_switcher.props.margin_right = 24
        stack_switcher.props.no_show_all = True
        stack_switcher.props.stack = stack
        stack_switcher.props.expand = False
        stack_switcher.show()


        # actions grid construct
        action_grid = Gtk.Grid()
        action_grid.props.margin_top = 12
        action_grid.props.margin_left = 24
        action_grid.props.margin_right = 24
        action_grid.props.column_spacing = 12
        export_json_button = Gtk.Button.new_from_icon_name("open-menu", Gtk.IconSize.LARGE_TOOLBAR)
        export_json_button.get_style_context().add_class('flat')
        export_csv_button = Gtk.Button.new_from_icon_name("open-menu", Gtk.IconSize.LARGE_TOOLBAR)


        separator = Gtk.Separator()
        separator.set_orientation(Gtk.Orientation.HORIZONTAL)
        status_bar = Gtk.Label()
        status_bar.props.margin = 10
        status_bar.props.halign = Gtk.Align.END


        # layout contruct
        layout = Gtk.Grid()
        layout.attach(header_label_grid, 0, 1, 1, 1)
        layout.attach(stack_switcher, 0, 2, 2, 1)
        layout.attach(stack, 0, 3, 2, 1)
        layout.attach(separator, 0, 4, 2, 1)
        layout.attach(status_bar, 0, 5, 2, 4)
        layout.props.expand = True

        self.add(layout)


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

    def load_metadata(self, file, dict):

        self.file = file

        # set the file icon
        self.get_fileicon(file.get_path())
        # set file name
        self.filename.set_label(str(dict['FileName']))
        self.filename.set_tooltip_text(self.filename.get_label())

        #clear previous data if the app is invoked while an existing window is open. need to figure out how to do multiple instance
        base_data_grid_children = self.base_data_grid.get_children()
        for child in base_data_grid_children:
            self.base_data_grid.remove(child)
        extended_data_grid_children = self.extended_data_grid.get_children()
        for child in extended_data_grid_children:
            self.extended_data_grid.remove(child)

        i = 1
        for key in self.basedata:
            # title = titleLabel(key)
            # value = valueLabel(dict[key])
            label = dataLabel(key, str(dict[key]))
            self.base_data_grid.attach(label, 0, i, 1, 1)
            #self.base_data_grid.attach_next_to(value, title, Gtk.PositionType.RIGHT, 1, 1)
            i = i + 1
        
        i = 1
        for key in sorted (dict.keys()):
            if len(dict.keys()) < 15:
                self.extended_scrolledview.props.shadow_type = Gtk.ShadowType(0)

            if key not in self.basedata:
                # title = titleLabel(key)
                # value = valueLabel(str(dict[key]))
                label = dataLabel(key, str(dict[key]))
                self.extended_data_grid.attach(label, 0, i, 1, 1)
                #self.extended_data_grid.attach_next_to(value, title, Gtk.PositionType.RIGHT, 1, 1)
                i = i + 1
        
        

class valueLabel(Gtk.Label):
    def __init__(self, title):
        super().__init__()
        self.props.halign = Gtk.Align.START
        self.props.valign = Gtk.Align.START
        self.props.selectable = True
        #self.props.max_width_chars = 30
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


class dataLabel(Gtk.Label):
    def __init__(self, title, value):
        super().__init__()
        self.props.halign = Gtk.Align.START
        self.props.valign = Gtk.Align.START
        self.props.wrap = True
        self.props.selectable = True
        #self.props.wrap_mode = Pango.WrapMode.CHAR
        self.props.max_width_chars = 48
        self.props.ellipsize = Pango.EllipsizeMode.END
        #self.props.expand = True
        label = title + ': ' + value
        self.set_label(label)
        if len(label) > 50:
            self.set_tooltip_text(label)
