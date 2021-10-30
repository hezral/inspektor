# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2021 Adi Hezral <hezral@gmail.com>

from json import load
import re
import gi

gi.require_version('Handy', '1')
gi.require_version('Granite', '1.0')
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Handy, Gio, Pango, Granite, Gdk, GdkPixbuf
from .constants import data, app
from .drop_view import DropView
from .base_view import BaseView, DataLabel

class InspektorWindow(Handy.ApplicationWindow):
    __gtype_name__ = 'InspektorWindow'
    
    Handy.init()

    file = None
    comments = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.app = self.props.application
        
        self.props.title = app.app_name
        self.props.halign = Gtk.Align.FILL
        self.props.valign = Gtk.Align.START
        self.props.window_position = Gtk.WindowPosition.CENTER_ON_PARENT
        self.set_default_size(400, 320)
        self.set_size_request(400, -1)

        geometry = Gdk.Geometry()
        setattr(geometry, 'max_height', 800)
        setattr(geometry, 'max_width', 400)
        self.set_geometry_hints(None, geometry, Gdk.WindowHints.MAX_SIZE)

        self.drop_view = DropView(app=self.app)
        self.base_view = BaseView(app=self.app)

        self.stack = Gtk.Stack()
        self.stack.props.expand = True
        self.stack.props.transition_type = Gtk.StackTransitionType.CROSSFADE
        self.stack.add_named(self.drop_view, "drop-view")
        self.stack.add_named(self.base_view, "base-view")

        self.layout = Gtk.Grid()
        self.layout.props.name = "main"
        self.layout.props.expand = True
        self.layout.props.row_spacing = 10
        self.layout.attach(self.generate_headerbar(), 0, 0, 1, 1)
        self.layout.attach(self.stack, 0, 1, 1, 1)

        self.add(self.layout)
        self.show_all()
        self.connect("delete-event", self.on_close_window)

    def generate_headerbar(self):
        self.headerbar = Handy.HeaderBar()
        self.headerbar.set_size_request(-1, 44)
        self.headerbar.props.hexpand = True
        self.headerbar.props.has_subtitle = False
        self.headerbar.props.show_close_button = True
        self.headerbar.props.decoration_layout = "close:"
        self.headerbar.props.title = "Inspektor"
        return self.headerbar

    def do_show_window(self):
        if self.app.file:
            self.load_metadata()
        self.show_all()

    def load_metadata(self):

       #clear previous data if the app is invoked while an existing window is open. need to figure out how to do multiple instance
        for child in self.base_view.base_grid.get_children():
            self.base_view.base_grid.remove(child)
        for child in self.base_view.extended_grid.get_children():
            self.base_view.extended_grid.remove(child)
        for child in self.base_view.preview_grid.get_children():
            self.base_view.preview_grid.remove(child)
        for child in self.headerbar.get_children():
            self.headerbar.remove(child)

        self.headerbar.pack_start(self.app.inspeck_obj.icon)
        self.headerbar.pack_start(self.app.inspeck_obj.name_label)
        # self.headerbar.pack_end(self.export_button)
        self.headerbar.props.title = ""
        self.stack.set_visible_child_name("base-view")

        self.base_view.file_comments.set_text(self.app.inspeck_obj.comments)

        if self.app.inspeck_obj.preview_available is True:
            self.base_view.preview_grid.attach(self.app.inspeck_obj.preview, 0, 0, 1, 1)

        self.base_view.preview_grid.attach(self.app.inspeck_obj.dimension, 0, 1, 1, 1)

        # add error checking if exiftool doesn't support a file format
        dict = self.app.inspeck_obj.metadata
        if 'Error' in dict.keys():
            self.basedata = data().mindata
            i = 1
            for key in self.basedata:
                label = DataLabel(key[1], str(dict[key[0]]), self.app)
                self.base_view.base_grid.attach(label, 0, i, 1, 1)
                i = i + 1

            label = DataLabel('Error', 'Unsupported file format', self.app)
            self.base_view.extended_grid.attach(label, 0, 0, 1, 1)
                    
        else:
            self.basedata = data().basedata
            i = 1
            for key in self.basedata:
                label = DataLabel(key[1], str(dict[key[0]]), self.app)
                self.base_view.base_grid.attach(label, 0, i, 1, 1)
                i = i + 1

            base_keys = []
            for item in self.basedata:
                base_keys.append(item[0])

            i = 1
            for key in sorted (dict.keys()):
                if "FileType" not in key or "ExifToolVersion" not in key:
                    if key not in base_keys:
                        label = DataLabel(key, str(dict[key]), self.app)
                        self.base_view.extended_grid.attach(label, 0, i, 1, 1)
                        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
                        separator.props.expand = True
                        self.base_view.extended_grid.attach(separator, 0, i+1, 1, 1)
                        i = i + 2

        # present the window again in case its behind any window. usually if invoked from contractor menu
        self.base_view.on_view_visible()
        self.present()

    def on_close_window(self, window=None, event=None):
        if self.app.inspeck_obj is not None:
            if "image" in self.app.inspeck_obj.metadata['MIMEType']:
                if self.app.inspeck_obj.preview.play_gif_thread is not None:
                    self.app.inspeck_obj.preview.stop_threads = True
                    self.app.inspeck_obj.preview.play_gif_thread.join()
                    self.app.inspeck_obj.preview.play_gif_thread = None
        self.destroy()
