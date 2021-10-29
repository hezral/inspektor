# mode_switch.py
#
# Copyright 2021 adi
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 

import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, GObject, Gdk

class ModeSwitch(Gtk.Grid):
    '''Gtk only basic port of https://github.com/elementary/granite/blob/master/lib/Widgets/ModeSwitch.vala'''

    __gtype_name__ = "ModeSwitch"

    CSS = """
    .modeswitch slider {min-height: 16px; min-width: 16px;}
    .modeswitch:checked {background-clip: border-box; background-color: rgba(0,0,0,0.1); background-image: none;}
    """
    
    css_provider = Gtk.CssProvider()
    css_provider.load_from_data(CSS.encode())
    Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
    
    active = GObject.Property(type=bool, default=True)
    
    def __init__(self, primary_widget, secondary_widget, primary_widget_callback, secondary_widget_callback, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.primary_widget = primary_widget
        self.secondary_widget = secondary_widget

        self.primary_widget_callback = primary_widget_callback
        self.secondary_widget_callback = secondary_widget_callback
        
        if self.primary_widget is not None:
            self.primary_widget.connect("button-release-event", self.on_primary_widget_pressed)
            self.primary_widget.props.valign = Gtk.Align.CENTER
            self.primary_widget.props.halign = Gtk.Align.END
            self.attach(self.primary_widget, 0, 0, 1, 1)

        if self.secondary_widget is not None:
            self.secondary_widget.connect("button-release-event", self.on_secondary_widget_pressed)
            self.secondary_widget.props.valign = Gtk.Align.CENTER
            self.secondary_widget.props.halign = Gtk.Align.START
            self.attach(self.secondary_widget, 2, 0, 1, 1)
    
        self.switch = Gtk.Switch()
        self.switch.get_style_context().add_class("modeswitch")
        self.switch.props.can_focus = False
        self.switch.props.valign = Gtk.Align.CENTER
        self.switch.set_size_request(32, -1)
        self.attach(self.switch, 1, 0, 1, 1)

        self.props.column_spacing = 6
        self.props.margin_top = 6
        self.props.margin_right = 6

    def on_primary_widget_pressed(self, *args):
        self.active = False
        if self.primary_widget_callback is not None:
            self.primary_widget_callback()
        return Gdk.EVENT_STOP

    def on_secondary_widget_pressed(self, *args):
        self.active = True
        if self.secondary_widget_callback is not None:
            self.secondary_widget_callback()
        return Gdk.EVENT_STOP
