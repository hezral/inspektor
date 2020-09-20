#!/usr/bin/env python3
 
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Pango
 
def set_wrap_mode(radiobutton, wrap_mode):
    textview.set_wrap_mode(wrap_mode)
 
def set_style_text(checkbutton):
    start, end = textbuffer.get_bounds()
 
    if checkbuttonBold.get_active():
        textbuffer.apply_tag(texttagBold, start, end)
    else:
        textbuffer.remove_tag(texttagBold, start, end)
 
    if checkbuttonItalic.get_active():
        textbuffer.apply_tag(texttagItalic, start, end)
    else:
        textbuffer.remove_tag(texttagItalic, start, end)
 
    if checkbuttonUnderline.get_active():
        textbuffer.apply_tag(texttagUnderline, start, end)
    else:
        textbuffer.remove_tag(texttagUnderline, start, end)
 
window = Gtk.Window()
window.set_default_size(250, 300)
window.connect("destroy", Gtk.main_quit)
 
grid = Gtk.Grid()
window.add(grid)
 
scrolledwindow = Gtk.ScrolledWindow()
scrolledwindow.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
grid.attach(scrolledwindow, 0, 0, 2, 1)
 
textbuffer = Gtk.TextBuffer()
texttagBold = textbuffer.create_tag("Bold", weight=Pango.Weight.BOLD)
texttagItalic = textbuffer.create_tag("Italic", style=Pango.Style.ITALIC)
texttagUnderline = textbuffer.create_tag("Underline", underline=Pango.Underline.SINGLE)



textbuffer.set_text("GTK+, or the GIMP Toolkit, is a multi-platform toolkit for creating graphical user interfaces. Offering a complete set of widgets, GTK+ is suitable for projects ranging from small one-off tools to complete application suites.")
 
textview = Gtk.TextView(buffer=textbuffer)
textview.set_vexpand(True)
textview.set_hexpand(True)
scrolledwindow.add(textview)
 
radiobuttonWrapNone = Gtk.RadioButton(group=None, label="None")
radiobuttonWrapNone.connect("toggled", set_wrap_mode, Gtk.WrapMode.NONE)
grid.attach(radiobuttonWrapNone, 0, 1, 1, 1)
 
radiobuttonWrapChar = Gtk.RadioButton(group=radiobuttonWrapNone, label="Character")
radiobuttonWrapChar.connect("toggled", set_wrap_mode, Gtk.WrapMode.CHAR)
grid.attach(radiobuttonWrapChar, 0, 2, 1, 1)
 
radiobuttonWrapWord = Gtk.RadioButton(group=radiobuttonWrapNone, label="Word")
radiobuttonWrapWord.connect("toggled", set_wrap_mode, Gtk.WrapMode.WORD)
grid.attach(radiobuttonWrapWord, 0, 3, 1, 1)
 
radiobuttonWrapWordChar = Gtk.RadioButton(group=radiobuttonWrapNone, label="Word & Character")
radiobuttonWrapWordChar.connect("toggled", set_wrap_mode, Gtk.WrapMode.WORD_CHAR)
grid.attach(radiobuttonWrapWordChar, 0, 4, 1, 1)
 
checkbuttonBold = Gtk.CheckButton(label="Bold")
checkbuttonBold.connect("toggled", set_style_text)
grid.attach(checkbuttonBold, 1, 1, 1, 1)
 
checkbuttonItalic = Gtk.CheckButton(label="Italic")
checkbuttonItalic.connect("toggled", set_style_text)
grid.attach(checkbuttonItalic, 1, 2, 1, 1)
 
checkbuttonUnderline = Gtk.CheckButton(label="Underline")
checkbuttonUnderline.connect("toggled", set_style_text)
grid.attach(checkbuttonUnderline, 1, 3, 1, 1)
 
window.show_all()
 
Gtk.main()