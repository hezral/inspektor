# main.py
#
# Copyright 2021 Adi Hezral
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import gi
import argparse
import shutil
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gio, GLib, Granite

from .window import InspektorWindow
from .parser import parser
from .constants import app


class Application(Gtk.Application):
    def __init__(self):
        super().__init__()

        self.props.application_id = app.app_id
        self.props.flags=Gio.ApplicationFlags.HANDLES_OPEN

        self.gio_settings = Gio.Settings(schema_id=app.app_id)
        self.gtk_settings = Gtk.Settings().get_default()
        self.granite_settings = Granite.Settings.get_default()

        self.window = None
        self.file = None
        self.parser = None


    def do_startup(self):
        Gtk.Application.do_startup(self)
        
        # Support quiting app using Super+Q
        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", self.on_quit_action)
        self.add_action(quit_action)
        self.set_accels_for_action("app.quit", ["<Ctrl>Q", "Escape"])

        prefers_color_scheme = self.granite_settings.get_prefers_color_scheme()
        self.gtk_settings.set_property("gtk-application-prefer-dark-theme", prefers_color_scheme)
        self.granite_settings.connect("notify::prefers-color-scheme", self.on_prefers_color_scheme)

        if "io.elementary.stylesheet" not in self.gtk_settings.props.gtk_theme_name:
            self.gtk_settings.set_property("gtk-theme-name", "io.elementary.stylesheet.blueberry")



    def do_activate(self):
        # parser instance
        if self.parser is None:
            self.parser = parser()

        # We only allow a single window and raise any existing ones
        if self.window is None:
            # Windows are associated with the application 
            # when the last one is closed the application shuts down
            self.window = InspektorWindow(application=self)
            self.add_window(self.window)

            self.window.show_all()

        if self.file is None:
            self.file = self.filechooser() #GLocalFile object
        else:
            self.file = self.file[0] #GLocalFile object

        if self.file:
            self.file_path = self.file.get_path()

            metadata = self.parser.get_jsondata(self.file_path)

            self.window.load_metadata(self.file, metadata)
            
            self.window.show_all()
        else:
            self.quit()
        

        

    def do_open(self, files, *hint):
        self.file = files
        self.do_activate()
        return 0

    def on_quit_action(self, action, param):
        if self.window is not None:
            self.window.destroy()

    def filechooser(self):
        filechooserdialog = Gtk.FileChooserDialog()
        filechooserdialog.add_button("_Open", Gtk.ResponseType.OK)
        filechooserdialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        filechooserdialog.set_default_response(Gtk.ResponseType.OK)
        filechooserdialog.set_transient_for(self.window)
        filechooserdialog.set_destroy_with_parent(False)
        filechooserdialog.set_position(Gtk.WindowPosition.MOUSE)
        filechooserdialog.set_size_request(320, 480)
        filechooserdialog.set_default_size(320, 480)
        
        response = filechooserdialog.run()
        file = None
        if response == Gtk.ResponseType.OK:
            file = filechooserdialog.get_file() #return a GLocalFile object
            filechooserdialog.destroy()
        else:
            filechooserdialog.destroy()
            #self.window.destroy()
        if file is not None:
            return file


    def on_prefers_color_scheme(self, *args):
        prefers_color_scheme = self.granite_settings.get_prefers_color_scheme()
        self.gtk_settings.set_property("gtk-application-prefer-dark-theme", prefers_color_scheme)
    

def main(version):
    app = Application()
    return app.run(sys.argv)
