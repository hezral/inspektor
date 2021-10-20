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

gi.require_version('Handy', '1')
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Handy, Gio, Pango, Granite
from .constants import data, app
from .parser import parser
from .about import AboutInspektor


class InspektorWindow(Handy.ApplicationWindow):
    __gtype_name__ = 'StashedWindow'
    
    Handy.init()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.parser = parser()
        self.file = None
        
        self.props.title = app.app_name
        self.props.resizable = False
        # self.set_keep_above(True)
        self.props.window_position = Gtk.WindowPosition.CENTER_ON_PARENT
        self.props.border_width = 0
        self.get_style_context().add_class("rounded")
        self.set_default_size(400, 560)

        # header label filename construct
        self.filename = Gtk.Label()
        self.filename.set_label('unknown')
        self.filename.props.halign = Gtk.Align.START
        self.filename.props.valign = Gtk.Align.FILL
        self.filename.props.max_width_chars = 40
        self.filename.props.ellipsize = Pango.EllipsizeMode.MIDDLE
        self.filename.props.selectable = False
        self.filename.props.margin_top = 4
        
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
        comments_textview.props.wrap_mode = Gtk.WrapMode.WORD_CHAR
        comments_textview.connect('focus-out-event',self.update_file_comments)

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
        base_grid.attach(Gtk.Separator(), 0, 2, 1, 1)
        base_grid.attach(comments_grid, 0, 3, 1, 1)

        # extended data grid construct
        self.extended_data_grid = Gtk.Grid()
        self.extended_data_grid.props.halign = Gtk.Align.FILL
        self.extended_data_grid.props.valign = Gtk.Align.FILL
        self.extended_data_grid.props.expand = True
        self.extended_data_grid.props.margin = 4
        self.extended_data_grid.props.column_spacing = 6
        self.extended_data_grid.props.row_spacing = 6

        self.extended_scrolledview = Gtk.ScrolledWindow()
        self.extended_scrolledview.add(self.extended_data_grid)
        self.extended_scrolledview.props.shadow_type = Gtk.ShadowType(3)
        self.extended_scrolledview.props.vscrollbar_policy = Gtk.PolicyType(1)

        # base grid for stack
        extended_grid = Gtk.Grid()
        extended_grid.props.expand = True
        extended_grid.props.margin = 24
        extended_grid.props.column_spacing = 6
        extended_grid.props.row_spacing = 6
        extended_grid.attach(self.extended_scrolledview, 0, 1, 1, 1)

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

        # export construct
        export_button = Gtk.Button(label="Export", image=Gtk.Image.new_from_icon_name("document-export", Gtk.IconSize.LARGE_TOOLBAR))
        export_button.set_always_show_image(True)
        export_button.props.halign = Gtk.Align.START
        export_button.get_style_context().add_class('flat')
        export_button.connect('clicked', self.on_export)

        export_json_button = Gtk.Button(label="Export to JSON", image=Gtk.Image.new_from_icon_name("text-css", Gtk.IconSize.LARGE_TOOLBAR))
        export_json_button.set_always_show_image(True)
        export_json_button.props.halign = Gtk.Align.FILL
        export_json_button.props.xalign = 0.0
        export_json_button.connect('clicked', self.on_export_json)

        export_csv_button = Gtk.Button(label="Export to CSV ", image=Gtk.Image.new_from_icon_name("application-vnd.ms-excel", Gtk.IconSize.LARGE_TOOLBAR))
        export_csv_button.set_always_show_image(True)
        export_csv_button.props.halign = Gtk.Align.FILL
        export_csv_button.props.xalign = 0.0
        export_csv_button.connect('clicked', self.on_export_csv)

        export_txt_button = Gtk.Button(label="Export to TXT ", image=Gtk.Image.new_from_icon_name("text-x-generic", Gtk.IconSize.LARGE_TOOLBAR))
        export_txt_button.set_always_show_image(True)
        export_txt_button.props.halign = Gtk.Align.FILL
        export_txt_button.props.xalign = 0.0
        export_txt_button.connect('clicked', self.on_export_txt)

        popover_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        popover_box.props.margin_left = 10
        popover_box.props.margin_right = 10
        popover_box.props.margin_top = 8
        popover_box.props.margin_bottom = 6
        popover_box.pack_start(export_json_button, True, True, 4)
        popover_box.pack_start(export_csv_button, True, True, 4)
        popover_box.pack_start(export_txt_button, True, True, 4)

        self.export_popover = Gtk.Popover()
        self.export_popover.add(popover_box)
        self.export_popover.set_position(Gtk.PositionType.RIGHT)
        self.export_popover.set_modal(True)

        # about
        # about_button = Gtk.Button(image=Gtk.Image.new_from_icon_name(app.app_id, Gtk.IconSize.LARGE_TOOLBAR))
        # about_button.set_always_show_image(True)
        # about_button.get_style_context().add_class('flat')
        # about_button.connect('clicked', self.on_about)

        # # actions box construct
        # action_box = Gtk.HBox()
        # action_box.pack_start(export_button, True, True, 0)
        # action_box.pack_end(about_button, False, False, 0)

        # layout contruct
        layout = Gtk.Grid()
        layout.attach(header_label_grid, 0, 1, 1, 1)
        layout.attach(stack_switcher, 0, 2, 1, 1)
        layout.attach(stack, 0, 3, 1, 1)
        # layout.attach(Gtk.Separator(), 0, 4, 1, 1)
        # layout.attach(action_box, 0, 5, 1, 1)
        layout.props.expand = True

        self.header = self.generate_headerbar()
        self.grid = Gtk.Grid()
        self.grid.props.name = "main"
        self.grid.props.expand = True
        self.grid.attach(self.header, 0, 0, 1, 1)
        self.grid.attach(layout, 0, 1, 1, 1)

        self.add(self.grid)

    def generate_headerbar(self):
        header = Handy.HeaderBar()
        header.props.hexpand = True
        header.props.has_subtitle = False
        header.props.show_close_button = True
        header.get_style_context().add_class(Granite.STYLE_CLASS_DEFAULT_DECORATION)
        header.get_style_context().add_class(Gtk.STYLE_CLASS_FLAT)
        return header

    def on_export_json(self, button):
        self.parser.export_json(self.file.get_path())
        self.export_popover.hide()
    
    def on_export_csv(self, button):
        self.parser.export_csv(self.file.get_path())
        self.export_popover.hide()

    def on_export_txt(self, button):
        self.parser.export_txt(self.file.get_path())
        self.export_popover.hide()

    def on_export(self, button):
        self.export_popover.set_relative_to(button)
        self.export_popover.show_all()
        self.export_popover.popup()

    def on_about(self, button):
        about = AboutInspektor(self)
        about.show_all()


    def update_file_comments(self, textview, event):
        startIter, endIter = textview.get_buffer().get_bounds()
        text = textview.get_buffer().get_text(startIter, endIter, True)
        if text != self.get_comments:
            self.parser.set_file_comments(self.file.get_path(),text)
        pass

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
        # get selected file
        self.file = file

        # get file comments
        self.get_comments = self.parser.get_file_comments(self.file.get_path())
        self.file_comments.set_text(self.get_comments)

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

        # add error checking if exiftool doesn't support a file format
        if 'Error' in dict.keys():
            self.basedata = data().mindata
            i = 1
            for key in self.basedata:
                label = dataLabel(key, str(dict[key]))
                self.base_data_grid.attach(label, 0, i, 1, 1)
                i = i + 1

            self.extended_scrolledview.props.shadow_type = Gtk.ShadowType(0)
            label = dataLabel('Error', 'Unsupported file format. No metadata info to show')
            self.extended_data_grid.attach(label, 0, 1, 1, 1)
                    
        else:
            self.basedata = data().basedata
            i = 1
            for key in self.basedata:
                label = dataLabel(key, str(dict[key]))
                self.base_data_grid.attach(label, 0, i, 1, 1)
                i = i + 1

            i = 1
            for key in sorted (dict.keys()):
                if len(dict.keys()) < 15:
                    self.extended_scrolledview.props.shadow_type = Gtk.ShadowType(0)

                if key not in self.basedata:
                    label = dataLabel(key, str(dict[key]))
                    self.extended_data_grid.attach(label, 0, i, 1, 1)
                    i = i + 1

        # present the window again in case its behind any window. usually if invoked from contractor menu
        self.present()


class dataLabel(Gtk.Label):
    def __init__(self, title, value):
        super().__init__()
        self.props.halign = Gtk.Align.START
        self.props.valign = Gtk.Align.START
        self.props.wrap = True
        self.props.selectable = True
        self.props.max_width_chars = 48
        self.props.ellipsize = Pango.EllipsizeMode.END
        label = title + ': ' + value
        self.set_label(label)
        if len(label) > 50:
            self.set_tooltip_text(label)
