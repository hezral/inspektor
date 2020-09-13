 
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
 
def reveal_child(button):
    if revealer.get_reveal_child():
        window.resize(203,25)
        revealer.set_visible(False)
        revealer.set_reveal_child(False)
    else:
        revealer.set_visible(True)
        revealer.set_reveal_child(True)

window = Gtk.Window()
window.connect("destroy", Gtk.main_quit)

grid = Gtk.Grid()
window.add(grid)

revealer = Gtk.Revealer()
revealer.set_reveal_child(False)
grid.attach(revealer, 0, 1, 1, 1)

label = Gtk.Label("Label contained in a Revealer widget")
revealer.add(label)

button = Gtk.Button("Reveal")
button.props.expand = True
button.connect("clicked", reveal_child)
grid.attach(button, 0, 0, 1, 1)

window.show_all()

print(window.get_size())
print(label.get_allocated_height())

Gtk.main()