# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2021 Adi Hezral <hezral@gmail.com>

import sys
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, Gio

class Playaudio():
    Gst.init(None)

    def __init__(self, giofile, *args, **kwargs):
        self.giofile = giofile

        self.player = Gst.ElementFactory.make("playbin", "player")
        fakesink = Gst.ElementFactory.make("fakesink", "fakesink")
        self.player.set_property("video-sink", fakesink)
        self.player.props.uri = self.giofile.get_uri()
        self.bus = self.player.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect("message", self.on_message)

    def play_pause(self, *args):
        if self.is_playing() is False:
            self.player.set_state(Gst.State.PLAYING)
            print("playing")
        else:
            self.player.set_state(Gst.State.NULL)
            print("pausing")
        print(self.player.get_state(Gst.CLOCK_TIME_NONE).state.value_name)

    def is_playing(self, *args):
        if self.player.get_state(Gst.CLOCK_TIME_NONE).state.value_name == "GST_STATE_NULL":
            return False
        else:
            return True

    def on_message(self, bus, message):
        # print(message.type)
        if message.type == Gst.MessageType.EOS:
            self.player.set_state(Gst.State.NULL)
        elif message.type == Gst.MessageType.ERROR:
            self.player.set_state(Gst.State.NULL)
            err, debug = message.parse_error()
            print("Error: %s" % err, debug)

# if __name__ == '__main__':
#     filename = sys.argv[1]

#     gfile = Gio.File.new_for_path(filename)

#     player = Playaudio(gfile)
#     player.play_pause()
