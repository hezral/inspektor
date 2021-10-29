# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2021 Adi Hezral <hezral@gmail.com>
 
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gtk, GdkPixbuf, Gio

from pydbus import SessionBus

 
class PreviewBackend(GObject.GObject):
    def __init__(self):
        GObject.GObject.__init__(self)

        self.bus = SessionBus()
        self.cancelable = Gio.Cancellable.new()
        self.proxy = self.bus.get("org.freedesktop.thumbnails.Thumbnailer1",
                                  "/org/freedesktop/thumbnails/Thumbnailer1")

        print(self.proxy)

