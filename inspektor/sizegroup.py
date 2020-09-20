import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
 
class SizeGroup(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.connect("destroy", Gtk.main_quit)
 
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
        self.add(box)
 
        sizegroup = Gtk.SizeGroup()
        sizegroup.set_mode(Gtk.SizeGroupMode.HORIZONTAL)
 
        button = Gtk.Button(label="Arch")
        sizegroup.add_widget(button)
        box.pack_start(button, True, True, 0)
 
        button = Gtk.Button(label="Debian")
        sizegroup.add_widget(button)
        box.pack_start(button, True, True, 0)
 
        button = Gtk.Button(label="Red Hat\nEnterprise Linux")
        sizegroup.add_widget(button)
        box.pack_start(button, True, True, 0)
 
window = SizeGroup()
window.show_all()
 
Gtk.main()