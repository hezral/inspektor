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

import sys
import gi
import argparse
import shutil
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GLib
from window import inspektorWindow
from parser import parser
from constants import app

class inspektorApp(Gtk.Application):
    def __init__(self):
        super().__init__()

        self.props.application_id = app.application_id
        self.props.flags=Gio.ApplicationFlags.HANDLES_OPEN

        self.window = None
        self.file = None

        #check if exiftool is installed
        try:
            self.exiftool = shutil.which("exiftool")
            print("Found exiftool installed at", self.exiftool)
        except shutil.Error as error:
            print("Shutil: ", error)
        
        self.parser = parser(self.exiftool)

        

    def do_startup(self):
        Gtk.Application.do_startup(self)
        
        # Support quiting app using Super+Q
        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", self.on_quit_action)
        self.add_action(quit_action)
        self.set_accels_for_action("app.quit", ["<Ctrl>Q", "Escape"])


    def do_activate(self):
        # We only allow a single window and raise any existing ones
        if self.window is None:
            # Windows are associated with the application 
            # when the last one is closed the application shuts down
            self.window = inspektorWindow(self.parser, application=self)
            self.add_window(self.window)

        if self.file is None:
            self.file = self.window.filechooser() #GLocalFile object
        else:
            self.file = self.file[0] #GLocalFile object

        if self.file:
            self.file_path = self.file.get_path()
            self.file_parent = self.file.get_parent().get_path()

            jsondata = self.parser.get_jsondata(self.file_path)

            self.window.update_data_grid(self.file, jsondata)
            
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


if __name__ == "__main__":
    app = inspektorApp()
    app.run(sys.argv)
