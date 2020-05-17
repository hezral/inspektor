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
from gi.repository import Gtk, Gio, Pango


class inspektorWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # applicationwindow construct
        self.props.title = "Inspektor"
        self.set_icon_name("com.github.hezral.inspektor")
        self.props.resizable = False
        # self.props.deletable = False
        # self.set_keep_above(True)
        self.props.window_position = Gtk.WindowPosition.CENTER_ON_PARENT
        self.props.border_width = 0
        self.get_style_context().add_class("rounded")
        self.set_default_size(320, -1)


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

        # header label construct
        header_label_grid = Gtk.Grid()
        header_label_grid.props.margin_top = 12
        header_label_grid.props.margin_left = 24
        header_label_grid.props.margin_right = 24
        header_label_grid.props.column_spacing = 12
        header_label_grid.attach(self.fileicon, 0, 1, 1, 1)
        header_label_grid.attach_next_to(self.filename, self.fileicon, Gtk.PositionType.RIGHT, 1, 1)


        # basic info construct
        basic_directory = titleLabel('Directory')
        basic_filesize = titleLabel('Size')
        basic_filemodifydate = titleLabel('Modify Date')
        basic_fileaccessdate = titleLabel('Access Date')
        basic_filechangedate = titleLabel('Change Date')
        basic_filepermissions = titleLabel('Permissions')
        basic_filetype = titleLabel('Type')
        basic_fileextension = titleLabel('Type Extension')
        basic_filemimetype = titleLabel('MIME Type')

        self.basic_directory_value = valueLabel()
        self.basic_filesize_value = valueLabel()
        self.basic_filemodifydate_value = valueLabel()
        self.basic_fileaccessdate_value = valueLabel()
        self.basic_filechangedate_value = valueLabel()
        self.basic_filepermissions_value = valueLabel()
        self.basic_filetype_value = valueLabel()
        self.basic_fileextension_value = valueLabel()
        self.basic_filemimetype_value = valueLabel()


        basic_grid = Gtk.Grid()
        basic_grid.props.halign = Gtk.Align.FILL
        basic_grid.props.valign = Gtk.Align.FILL
        basic_grid.props.expand = True
        basic_grid.props.margin = 24
        basic_grid.props.margin_top = 18
        basic_grid.props.column_spacing = 6
        basic_grid.props.row_spacing = 6
        basic_grid.attach(basic_directory, 0, 1, 1, 1)
        basic_grid.attach_next_to(self.basic_directory_value, basic_directory, Gtk.PositionType.RIGHT, 1, 1)
        basic_grid.attach(basic_filesize, 0, 2, 1, 1)
        basic_grid.attach_next_to(self.basic_filesize_value, basic_filesize, Gtk.PositionType.RIGHT, 1, 1)
        basic_grid.attach(basic_filemodifydate, 0, 3, 1, 1)
        basic_grid.attach_next_to(self.basic_filemodifydate_value, basic_filemodifydate, Gtk.PositionType.RIGHT, 1, 1)
        basic_grid.attach(basic_fileaccessdate, 0, 4, 1, 1)
        basic_grid.attach_next_to(self.basic_fileaccessdate_value, basic_fileaccessdate, Gtk.PositionType.RIGHT, 1, 1)
        basic_grid.attach(basic_filechangedate, 0, 5, 1, 1)
        basic_grid.attach_next_to(self.basic_filechangedate_value, basic_filechangedate, Gtk.PositionType.RIGHT, 1, 1)
        basic_grid.attach(basic_filepermissions, 0, 6, 1, 1)
        basic_grid.attach_next_to(self.basic_filepermissions_value, basic_filepermissions, Gtk.PositionType.RIGHT, 1, 1)
        basic_grid.attach(basic_filetype, 0, 7, 1, 1)
        basic_grid.attach_next_to(self.basic_filetype_value, basic_filetype, Gtk.PositionType.RIGHT, 1, 1)
        basic_grid.attach(basic_fileextension, 0, 8, 1, 1)
        basic_grid.attach_next_to(self.basic_fileextension_value, basic_fileextension, Gtk.PositionType.RIGHT, 1, 1)
        basic_grid.attach(basic_filemimetype, 0, 9, 1, 1)
        basic_grid.attach_next_to(self.basic_filemimetype_value, basic_filemimetype, Gtk.PositionType.RIGHT, 1, 1)

        # extended info construct
        extended_grid = Gtk.Grid()
        extended_grid.props.column_spacing = 6
        extended_grid.props.row_spacing = 6

        # info stack contstruct
        stack = Gtk.Stack()
        stack.add_titled(basic_grid, 'basic', 'Basic')
        stack.add_titled(extended_grid, 'extended', 'Extended')

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
        # filechooserdialog.set_title("Choose a file")
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

    def update_basic_grid(self, file, dict):
        # set the file icon
        self.get_fileicon(file.get_path())
        # set file name
        self.filename.set_label(file.get_basename())
        self.filename.set_tooltip_text(self.filename.get_label())
        # set the directory path
        self.basic_directory_value.set_label(file.get_parent().get_path())
        # set the basic info
        self.basic_filepermissions_value.set_label()

        # self.basic_directory_value = valueLabel()
        # self.basic_filesize_value = valueLabel()
        # self.basic_filemodifydate_value = valueLabel()
        # self.basic_fileaccessdate_value = valueLabel()
        # self.basic_filechangedate_value = valueLabel()
        # self.basic_filepermissions_value = valueLabel()
        # self.basic_filetype_value = valueLabel()
        # self.basic_fileextension_value = valueLabel()
        # self.basic_filemimetype_value = valueLabel()
        pass

    def update_extended_grid(self, dict):
        pass


class valueLabel(Gtk.Label):
    def __init__(self):
        super().__init__()

        self.props.halign = Gtk.Align.START
        self.props.valign = Gtk.Align.START
        self.props.selectable = True
        self.props.max_width_chars = 24
        self.props.wrap = True
        self.props.wrap_mode = Pango.WrapMode.CHAR
        self.set_label('unknown')


class titleLabel(Gtk.Label):
    def __init__(self, title):
        super().__init__()

        self.props.halign = Gtk.Align.END
        self.props.valign = Gtk.Align.START
        self.props.wrap = True
        self.props.wrap_mode = Pango.WrapMode.WORD_CHAR
        title = title + ': '
        self.set_label(title)