# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2021 Adi Hezral <hezral@gmail.com>

import gi
gi.require_version("Gtk", "3.0")
gi.require_version("Gst", "1.0")
from gi.repository import Gtk, Gst, Gio

class Playvideo():
    Gst.init(None)
    Gst.init_check(None)

    def __init__(self, giofile, *args, **kwargs):
        self.giofile = giofile

        # self.parent_widget = parent_widget
        # self.parent_widget.connect("realize", self.on_realize)

        self.player = Gst.ElementFactory.make("playbin")
        self.player.set_property("uri", self.giofile.get_uri())
        self.player.set_state(Gst.State.NULL)
        self.bus = self.player.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect("message", self.on_message)

    def set_parent_widget(self, widget):
        self.parent_widget = widget
        self.parent_widget.connect("realize", self.on_realize)

    def on_realize(self, widget):
        playerFactory = self.player.get_factory()
        gtksink = playerFactory.make('gtksink')
        self.player.set_property("video-sink", gtksink)
        gtkgstwidget = gtksink.props.widget
        gtkgstwidget.props.expand = True
        gtkgstwidget.props.halign = Gtk.Align.FILL
        gtkgstwidget.props.valign = Gtk.Align.FILL

        widget.add(gtkgstwidget)
        gtkgstwidget.show()

    def play_pause(self, *args):
        if self.is_playing() is False:
            self.player.set_state(Gst.State.PLAYING)
        else:
            self.player.set_state(Gst.State.PAUSED)

    def is_playing(self, *args):
        playerState = self.player.get_state(Gst.SECOND).state
        if playerState <= Gst.State.PAUSED:
            return False
        elif playerState is Gst.State.PLAYING:
            return True
        # if self.player.get_state(Gst.CLOCK_TIME_NONE).state.value_name == "GST_STATE_NULL":
        #     return False
        # else:
        #     return True

    def on_message(self, bus, message):
        # print(message.type)
        if message.type == Gst.MessageType.EOS:
            self.player.set_state(Gst.State.NULL)
        elif message.type == Gst.MessageType.ERROR:
            self.player.set_state(Gst.State.NULL)
            err, debug = message.parse_error()
            print("Error: %s" % err, debug)

# class MainWindow(Gtk.Window):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         filepath = "/home/adi/Downloads/d.mkv"
#         self.file = Gio.File.new_for_path(filepath)

#         self.box = Gtk.Box()
#         self.box.props.expand = True
#         self.box.props.halign = Gtk.Align.FILL
#         self.box.props.valign = Gtk.Align.FILL
#         self.set_default_size(720, 560)
#         # self.set_size_request(720, 560)

#         self.playvideo = Playvideo(self.file, self.box)

#         self.play_button = Gtk.Button(label="Play")
#         self.play_button.connect("clicked", self.playvideo.play_pause)

#         grid = Gtk.Grid()
#         grid.attach(self.box, 0, 0, 1, 1)
#         grid.attach(self.play_button, 0, 1, 1, 1)
#         self.add(grid)
#         self.show_all()


#     def on_btnPlay_clicked(self, widget):
#         playerState = self.player.get_state(Gst.SECOND).state
#         if playerState <= Gst.State.PAUSED:
#             self.player.set_state(Gst.State.PLAYING)
#             self.btnPlay.set_label("Pause")
#         elif playerState is Gst.State.PLAYING:
#             self.player.set_state(Gst.State.PAUSED)
#             self.btnPlay.set_label("Play")

# win = MainWindow()
# win.connect("destroy", Gtk.main_quit)
# # win.show_all()
# Gtk.main()




