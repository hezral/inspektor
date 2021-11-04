# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2021 Adi Hezral <hezral@gmail.com>

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib, Gio

class DropView(Gtk.Grid):

    def __init__(self, app, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.app = app

        self.props.halign = Gtk.Align.FILL
        self.props.valign = Gtk.Align.FILL
        self.props.expand = True
        self.props.column_spacing = 6
        self.props.row_spacing = 6
        self.set_size_request(-1, 200)

        drop_label = Gtk.Label("Drag file here")
        drop_label.props.name = "drop"
        drop_label.props.expand = True
        drop_label.props.valign = Gtk.Align.CENTER
        drop_label.props.halign = Gtk.Align.CENTER

        drop_box = Gtk.EventBox()
        drop_box.add(drop_label)

        self.attach(drop_box, 0, 0, 1, 1)

        self.drag_and_drop_setup_drop_view(drop_box)

    def drag_and_drop_setup_drop_view(self, widget):
        widget.drag_dest_set(Gtk.DestDefaults.ALL, [], Gdk.DragAction.COPY)
        widget.drag_dest_add_uri_targets()
        widget.connect("drag_data_received", self.on_drag_data_received)

    def drag_and_drop_setup_main_window(self, widget):
        widget.drag_dest_set(Gtk.DestDefaults.ALL, [], Gdk.DragAction.COPY)
        widget.drag_dest_add_uri_targets()
        widget.connect("drag_motion", self.on_drag_motion)

    def on_drag_motion(self, *args):
        self.app.window.stack.set_visible_child_name("drop-view")
        self.app.window.show_all()

    def on_drag_end(self, widget, drag_context):
        ...

    def on_drag_begin(self, widget, drag_context):
        ...

    def on_drag_data_get(self, widget, drag_context, data, info, timestamp):
        ...
        
    def on_drag_data_received(self, widget, context, x, y, data, info, timestamp):
        from urllib.parse import urlparse
        import os

        uris = data.get_uris()
        for uri in uris:
            parsed_uri = urlparse(uri)
            path, hostname = GLib.filename_from_uri(uri)
            if os.path.exists(path):
                if os.path.isfile(path):
                    self.app.file = Gio.File.new_for_uri(uri)
                    self.app.do_initialize_inspeck_obj(self.app.file)
                    self.app.window.do_show_window()
                    self.hide()
                    self.drag_and_drop_setup_main_window(self.app.window.headerbar)

        Gtk.drag_finish(context, True, False, timestamp)
