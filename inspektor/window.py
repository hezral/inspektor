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
    def __init__(self, parser, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.basedata = data().basedata
        self.parser = parser

        print(type(parser))
        
        # applicationwindow construct
        self.props.title = "Inspektor"
        self.set_icon_name("com.github.hezral.inspektor")
        self.props.resizable = False
        # self.props.deletable = False
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

        # base info construct
        self.basic_grid = Gtk.Grid()
        self.basic_grid.props.halign = Gtk.Align.FILL
        self.basic_grid.props.valign = Gtk.Align.FILL
        self.basic_grid.props.expand = True
        self.basic_grid.props.margin = 29
        self.basic_grid.props.margin_top = 23
        self.basic_grid.props.column_spacing = 6
        self.basic_grid.props.row_spacing = 6

        # extended info construct
        self.extended_grid = Gtk.Grid()
        self.extended_grid.props.halign = Gtk.Align.FILL
        self.extended_grid.props.valign = Gtk.Align.FILL
        self.extended_grid.props.expand = True
        self.extended_grid.props.margin = 4
        #self.extended_grid.props.margin_top = 18
        self.extended_grid.props.column_spacing = 6
        self.extended_grid.props.row_spacing = 6

        self.scrolled_view = Gtk.ScrolledWindow()
        self.scrolled_view.add(self.extended_grid)
        self.scrolled_view.props.shadow_type = Gtk.ShadowType(3)
        self.scrolled_view.props.vscrollbar_policy = Gtk.PolicyType(1)

        scrolled_grid = Gtk.Grid()
        scrolled_grid.props.halign = Gtk.Align.FILL
        scrolled_grid.props.valign = Gtk.Align.FILL
        scrolled_grid.props.expand = True
        scrolled_grid.props.margin = 24
        scrolled_grid.props.margin_top = 18
        scrolled_grid.props.margin_bottom = 18
        scrolled_grid.props.column_spacing = 6
        scrolled_grid.props.row_spacing = 6
        scrolled_grid.attach(self.scrolled_view, 0, 1, 1, 1)

        # info stack contstruct
        stack = Gtk.Stack()
        stack.add_titled(self.basic_grid, 'basic', 'Basic')
        stack.add_titled(scrolled_grid, 'extended', 'Extended')

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
        export_csv_button = Gtk.Button.new_from_icon_name("open-menu", Gtk.IconSize.LARGE_TOOLBAR)

        separator = Gtk.Separator()
        separator.set_orientation(Gtk.Orientation.HORIZONTAL)
        status_bar = Gtk.Label()
        status_bar.props.margin = 8
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
        self.filename.set_label(str(dict['FileName']))
        # self.filename.set_label(file.get_basename())
        self.filename.set_tooltip_text(self.filename.get_label())

        #clear previous data if the app is invoked while an existing window is open. need to figure out how to do multiple instance
        basic_grid_children = self.basic_grid.get_children()
        for child in basic_grid_children:
            self.basic_grid.remove(child)
        extended_grid_children = self.extended_grid.get_children()
        for child in extended_grid_children:
            self.extended_grid.remove(child)

        i = 1
        for key in self.basedata:
            title = titleLabel(key)
            value = valueLabel(dict[key])
            label = dataLabel(key, str(dict[key]))
            self.basic_grid.attach(label, 0, i, 1, 1)
            #self.basic_grid.attach_next_to(value, title, Gtk.PositionType.RIGHT, 1, 1)
            i = i + 1
        
        i = 1
        for key in sorted (dict.keys()):
            if len(dict.keys()) < 15:
                self.scrolled_view.props.shadow_type = Gtk.ShadowType(0)

            if key not in self.basedata:
                title = titleLabel(key)
                value = valueLabel(str(dict[key]))
                label = dataLabel(key, str(dict[key]))
                self.extended_grid.attach(label, 0, i, 1, 1)
                #self.extended_grid.attach_next_to(value, title, Gtk.PositionType.RIGHT, 1, 1)
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
