import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import sys

class Main(object):
    def __init__(self):
        self.window = None
        self.width = 500
        self.height = 500

        # create application
        self.app = Gtk.Application.new("org.example.sztest", 0)
        self.app.connect('activate', self.on_app_activate)

    def on_button_pressed(self, btn, event):
        if self.width > self.height:
            self.width -= 50
        else:
            self.height -= 50

        self.window.resize(self.width, self.height)
        return True

    def on_app_activate(self, app):
        self.window = Gtk.ApplicationWindow.new(self.app)
        self.window.set_title("Size test")
        self.window.resize(self.width, self.height)
        self.window.connect("button-press-event", self.on_button_pressed)
        self.window.connect("destroy", lambda a: self.app.quit())
        self.window.show_all()


def main():
    m = Main()
    m.app.run(sys.argv)

if __name__ == "__main__": main()