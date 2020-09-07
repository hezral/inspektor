import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class ResizeWindow:

 def __init__(self):
    self.window = Gtk.Window()
    button = Gtk.Button("Resize")
    self.window.add(button)
    button.connect("clicked", self.resizewin)
    self.window.set_default_size(Gtk.gdk.screen_width(),500)
    self.window.move(0, 0)
    self.window.show_all()
    self.window.window.property_change("_NET_WM_STRUT", "CARDINAL", 32,
           Gtk.gdk.PROP_MODE_REPLACE, [0, 0, 100, 0])

 def resizewin(self, widget, *args):
    self.window.resize(Gtk.gdk.screen_width(),100)

if __name__ == '__main__':
  ResizeWindow()
  Gtk.main()