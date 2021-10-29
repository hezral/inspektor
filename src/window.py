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
from .about import AboutInspektor
from .drop_view import DropView
from .base_view import BaseView, DataLabel
from .extended_view import ExtendedView
from .mode_switch import ModeSwitch

class InspektorWindow(Handy.ApplicationWindow):
    __gtype_name__ = 'InspektorWindow'
    
    Handy.init()

    file = None
    comments = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.app = self.props.application
        
        self.set_keep_above(True)
        self.props.title = app.app_name

        self.props.halign = Gtk.Align.FILL
        self.props.valign = Gtk.Align.START
        self.props.window_position = Gtk.WindowPosition.CENTER_ON_PARENT
        self.set_default_size(400, 320)
        # self.set_size_request(400, -1)

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
        # self.connect("grab_notify", self.on_configure_event)
        self.connect("delete-event", self.on_close_window)

    def on_configure_event(self, widget, was_grabbed):
        print(locals())

    def generate_headerbar(self):
        self.export_button = Gtk.Button(image=Gtk.Image.new_from_icon_name("document-export", Gtk.IconSize.LARGE_TOOLBAR))
        self.export_button.set_always_show_image(True)
        # self.export_button.connect('clicked', self.on_export)

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
            self.headerbar.pack_start(self.app.inspeck_obj.icon)
            self.headerbar.pack_start(self.app.inspeck_obj.name_label)
            self.headerbar.pack_end(self.export_button)
            self.headerbar.props.title = ""
            self.stack.set_visible_child_name("base-view")
            self.load_metadata()
            
        self.show_all()

    def load_metadata(self):

        self.base_view.file_comments.set_text(self.app.inspeck_obj.comments)

        # if "image" in self.app.inspeck_obj.metadata['MIMEType']:
        if self.app.inspeck_obj.preview_available is True:
            self.base_view.preview_grid.attach(self.app.inspeck_obj.preview, 0, 0, 1, 1)
        
        self.base_view.dimension.props.label = self.app.inspeck_obj.dimension

        # add error checking if exiftool doesn't support a file format
        dict = self.app.inspeck_obj.metadata
        if 'Error' in dict.keys():
            self.basedata = data().mindata
            i = 1
            for key in self.basedata:
                label = DataLabel(key[1], str(dict[key[0]]), self.app)
                self.base_view.base_grid.attach(label, 0, i, 1, 1)
                i = i + 1

            # self.extended_scrolledview.props.shadow_type = Gtk.ShadowType(0)
            # label = DataLabel('Error', 'Unsupported file format. No metadata info to show')
            # self.extended_data_grid.attach(label, 0, 1, 1, 1)
                    
        else:
            self.basedata = data().basedata
            i = 1
            for key in self.basedata:
                label = DataLabel(key[1], str(dict[key[0]]), self.app)
                self.base_view.base_grid.attach(label, 0, i, 1, 1)
                i = i + 1

            # i = 1
            # for key in sorted (dict.keys()):
            #     if len(dict.keys()) < 15:
            #         self.extended_scrolledview.props.shadow_type = Gtk.ShadowType(0)

            #     if key not in self.basedata:
            #         label = DataLabel(key, str(dict[key]))
            #         self.extended_data_grid.attach(label, 0, i, 1, 1)
            #         i = i + 1

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


# class DataLabel(Gtk.Label):
#     def __init__(self, title, value):
#         super().__init__()
#         self.props.halign = Gtk.Align.START
#         self.props.valign = Gtk.Align.START
#         self.props.wrap = True
#         self.props.selectable = True
#         self.props.max_width_chars = 48
#         self.props.ellipsize = Pango.EllipsizeMode.END
#         label = title + ': ' + value
#         self.set_label(label)
#         if len(label) > 50:
#             self.set_tooltip_text(label)

#     def generate_copy_to_clipboard(self):
#         copy_button = Gtk.Button(label="Copy", image=Gtk.Image().new_from_icon_name("edit-copy-symbolic", Gtk.IconSize.SMALL_TOOLBAR))
#         copy_button.connect("clicked", self.)

#         self.copy_revealer = Gtk.Revealer()
#         self.copy_revealer.add(copy_button)
#         self.copy_revealer.props.transition_type = Gtk.RevealerTransitionType.CROSSFADE
