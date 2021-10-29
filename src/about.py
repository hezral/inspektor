# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2021 Adi Hezral <hezral@gmail.com>
 
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GdkPixbuf
from .constants import app
 
class AboutInspektor(Gtk.AboutDialog):
    def __init__(self, window, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_title("About Inspektor")
        self.set_transient_for(window)
        self.set_destroy_with_parent(True)
        self.set_modal(True)

        self.set_program_name(app.about_program_name)
        self.set_version(app.about_version)
        self.set_comments(app.about_comments)
        self.set_website(app.about_website)
        self.set_website_label(app.about_website_label)
        self.set_authors(app.about_authors)
        self.set_license(app.about_license)
        #self.set_license_type(app.about_license_type)
        self.set_logo_icon_name(app.about_logo_icon_name)
        self.add_credit_section("ElementaryPython",["Mirko Brombin"])
        self.add_credit_section("ExifTool",["Phil Harvey"])
        self.add_credit_section("Extended Filesystem Attributes", ["setfattr/getfattr"])
        self.connect("response", self.on_response)
 
    def on_response(self, dialog, response):
        self.destroy()


