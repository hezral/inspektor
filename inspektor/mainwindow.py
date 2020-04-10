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
from gi.repository import Gtk, Gio


class inspektorWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # applicationwindow construct
        self.props.title = "Inspektor"
        self.set_icon_name("com.github.hezral.inspektor")
        self.props.resizable = False
        #self.props.deletable = False
        self.set_keep_above(True)
        self.props.window_position = Gtk.WindowPosition.CENTER_ON_PARENT
        self.props.border_width = 0
        self.get_style_context().add_class("rounded")
        self.set_default_size(300, -1)

        # header label filename construct
        self.filename = Gtk.Label()
        self.filename.props.expand = True
        self.filename.set_label(".ext")
        # self.filename.set_halign(Gtk.Align.START)
        
        # header label fileicon construct
        self.fileicon = Gtk.Image.new_from_icon_name("unknown", Gtk.IconSize.DIALOG)
        self.fileicon.set_halign = Gtk.Align.START
        self.fileicon.set_valign = Gtk.Align.CENTER

        # header label construct
        header_label_grid = Gtk.Grid()
        header_label_grid.props.margin_left = 18
        header_label_grid.props.margin_right = 18
        header_label_grid.props.column_spacing = 6
        header_label_grid.props.row_spacing = 6
        # header_label_grid.set_halign(Gtk.Align.CENTER)
        # header_label_grid.set_valign(Gtk.Align.FILL)
        #header_label_grid.props.expand = True
        header_label_grid.attach(self.fileicon, 0, 1, 1, 1)
        header_label_grid.attach_next_to(self.filename, self.fileicon, Gtk.PositionType.RIGHT, 1, 1)

        # basic info construct
        self.basic_grid = Gtk.Grid()
        self.basic_grid.props.column_spacing = 6
        self.basic_grid.props.row_spacing = 6
        #self.basic_grid.attach(header_label, 0, 0, 2, 1)
        #self.basic_grid.attach(Gtk.Label("Testingthis"), 0, 1, 1, 1)

        # extended info construct
        self.extended_grid = Gtk.Grid()
        self.extended_grid.props.column_spacing = 6
        self.extended_grid.props.row_spacing = 6
        #self.extended_grid.attach(extended_label, 0, 0, 2, 1)

        # info stack contstruct
        stack = Gtk.Stack()
        stack.add_titled(self.basic_grid, 'Basic', 'Basic')
        stack.add_titled(self.extended_grid, 'Extended', 'Extended')

        # info stack switcher contruct
        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.props.homogeneous = True
        stack_switcher.props.margin = 24
        stack_switcher.props.margin_top = 12
        stack_switcher.props.no_show_all = True
        stack_switcher.props.stack = stack
        stack_switcher.props.expand = True
        stack_switcher.show()

        # layout contruct
        layout = Gtk.Grid()
        layout.props.margin = 0
        layout.props.margin_top = 18
        layout.props.column_spacing = 0
        layout.props.row_spacing = 6
        layout.attach(header_label_grid, 0, 1, 1, 1)
        layout.attach(stack_switcher, 0, 2, 2, 1)
        layout.attach(stack, 0, 3, 2, 1)
        layout.props.expand = True

        # window construct
        self.add(layout)   
        # self.show_all()
    
    def filechooser(self):
        filechooserdialog = Gtk.FileChooserDialog()
        filechooserdialog.set_title("Choose a file")
        filechooserdialog.add_button("_Open", Gtk.ResponseType.OK)
        filechooserdialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        filechooserdialog.set_default_response(Gtk.ResponseType.OK)
        filechooserdialog.set_transient_for(self)
        filechooserdialog.set_destroy_with_parent(True)
        filechooserdialog.set_position(Gtk.WindowPosition.MOUSE)
        
        response = filechooserdialog.run()
        file = None
        if response == Gtk.ResponseType.OK:
            file = filechooserdialog.get_filename()
            filechooserdialog.destroy()
        else:
            filechooserdialog.destroy()
            self.destroy()
        if file is not None:
            return file

    def get_fileicon(self, file):
        size = 32
        filedata = Gio.File.new_for_path(file)
        info = filedata.query_info('standard::icon' , 0 , Gio.Cancellable())
        fileicon = None
        for icon_name in info.get_icon().get_names():
            if fileicon is None:
                try:
                    fileicon = Gtk.IconTheme.get_default().load_icon(icon_name, size, 0)
                except:
                    pass
        #print(fileicon)
        return fileicon

    def update_info_grid(self, data):
        pass


