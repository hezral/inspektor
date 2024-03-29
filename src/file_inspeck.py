# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2021 Adi Hezral <hezral@gmail.com>

from dataclasses import dataclass, field
from subprocess import call

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GdkPixbuf, Gtk, Gio, Gdk, GLib, Pango

import tempfile

from .utils import HelperUtils

import os

@dataclass
class FileInspeck:

    giofile: Gio.File
    name: str = ""
    path: str = ""
    uri: str = ""
    name_label: Gtk.Label = Gtk.Label(name)
    icon: Gtk.Image = Gtk.Image.new_from_icon_name("application-octet-stream", Gtk.IconSize.LARGE_TOOLBAR)
    metadata: dict = field(default_factory=dict)
    comments: str = ""
    preview_available: bool = False
    preview: Gtk.Image = Gtk.Image.new_from_icon_name("image-generic", Gtk.IconSize.DIALOG)
    dimension: Gtk.Label = Gtk.Label()

    def __post_init__(self):
        self.name = self.giofile.get_basename()
        self.path = self.giofile.get_path()
        self.uri = self.giofile.get_uri()

        self.name_label.props.label = self.name
        self.name_label.props.max_width_chars = 48
        self.name_label.props.ellipsize = Pango.EllipsizeMode.END
        self.name_label.props.selectable = False
        self.name_label.props.has_tooltip = True
        self.name_label.props.tooltip_text = self.name
        
        self.set_fileicon()

        utils = HelperUtils()

        type = self.metadata['MIMEType']

        if "image" in type:
            self.preview_available = True
            self.preview = PreviewContainer(self.path, self.metadata['MIMEType'], None)
            if "svg" in type:
                self.dimension.props.label = "Dimension: {0}x{1}".format(self.metadata['SvgWidth'],self.metadata['SvgHeight'])
            else:
                self.dimension.props.label = "Dimension: {0}".format(self.metadata['ImageSize'])

        elif "audio" in type:
            self.preview_available = True

            temp_filename = next(tempfile._get_candidate_names()) + tempfile.gettempprefix()
            temp_cache_uri = os.path.join(GLib.get_user_cache_dir(), temp_filename)

            audio_art = utils.get_audio_art(infile=self.path, outfile=temp_cache_uri)
            if audio_art is None:
                audio_icon = Gtk.IconTheme.get_default().lookup_icon("audio-x-generic", 128, 0)
                audio_art = audio_icon.get_filename()

            self.preview = PreviewContainer(audio_art, self.metadata['MIMEType'], (utils.open_file_with_default_app, self.path))
            self.dimension.props.label = "Duration: {0}".format(self.metadata['Duration'])

        elif "video" in type:
            self.preview_available = True

            temp_filename = next(tempfile._get_candidate_names()) + tempfile.gettempprefix()
            temp_cache_uri = os.path.join(GLib.get_user_cache_dir(), temp_filename)

            video_frame = utils.get_video_frame(infile=self.path, outfile=temp_cache_uri)
            if video_frame is None:
                video_icon = Gtk.IconTheme.get_default().lookup_icon("video-x-generic", 128, 0)
                video_frame = video_icon.get_filename()

            self.preview = PreviewContainer(video_frame, self.metadata['MIMEType'], (utils.open_file_with_default_app, self.path), self.metadata['ImageWidth'], self.metadata['ImageHeight'])
            self.dimension.props.label = "Dimension: {0} Duration: {1}".format(self.metadata['ImageSize'], self.metadata['Duration'])

        else:
            self.dimension.props.label = "unavailable"

    def set_fileicon(self):
        size = 24
        info = self.giofile.query_info('standard::icon' , 0 , Gio.Cancellable())
        for icon_name in info.get_icon().get_names():
            try:
                self.icon.set_from_pixbuf(Gtk.IconTheme.get_default().load_icon(icon_name, size, 0))
                break
            except:
                pass


class PreviewContainer(Gtk.Grid):

    stop_threads = False
    play_gif_thread = None
    alpha = False

    def __init__(self, filepath, type, callback=None, width=None, height=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.props.halign = self.props.valign = Gtk.Align.FILL
        self.props.expand = True
        self.type = type
        self.filepath = filepath
        if callback is not None:
            self.callback = callback[0]
            self.callback_data = callback[1]

        self.get_style_context().add_class("dropshadow")

        if "gif" in self.type:
            self.pixbuf_original = GdkPixbuf.PixbufAnimation.new_from_file(filepath)
            self.pixbuf_original_height = self.pixbuf_original.get_height()
            self.pixbuf_original_width = self.pixbuf_original.get_width()
            self.iter = self.pixbuf_original.get_iter()
            if self.iter.get_pixbuf().get_has_alpha():
                self.alpha = True
        else:
            self.pixbuf_original = GdkPixbuf.Pixbuf.new_from_file(filepath)
            self.pixbuf_original_height = self.pixbuf_original.props.height
            self.pixbuf_original_width = self.pixbuf_original.props.width
            if self.pixbuf_original.get_has_alpha():
                self.alpha = True

        if self.alpha and "image" in self.type:
            self.get_style_context().add_class("checkerboard")

        self.ratio_h_w = self.pixbuf_original_height / self.pixbuf_original_width
        self.ratio_w_h = self.pixbuf_original_width / self.pixbuf_original_height

        if "generic" not in self.filepath:
            preview_width = 256
            preview_height = preview_width * self.ratio_h_w
        else:
            preview_width = self.pixbuf_original_width
            preview_height = self.pixbuf_original_height
        self.set_size_request(preview_width, preview_height)

        drawing_area = Gtk.DrawingArea()
        drawing_area.props.expand = True
        drawing_area.connect("draw", self.draw)
        drawing_area.props.can_focus = False

        preview_box = drawing_area

        if "gif" in self.type or "audio" in self.type or "video" in self.type:
            self.generate_play_pause_icons()

            overlay = Gtk.Overlay()
            overlay.add(preview_box)
            overlay.add_overlay(self.pause_revealer)
            overlay.add_overlay(self.play_revealer)
            eventbox = Gtk.EventBox()
            eventbox.props.above_child = True
            eventbox.add(overlay)
            eventbox.connect("enter-notify-event", self.on_hover_enter)
            eventbox.connect("leave-notify-event", self.on_hover_leave)

            if "gif" in self.type:
                eventbox.connect("button-press-event", self.toggle_gif_animation)
            else:
                eventbox.connect("button-press-event", self.open_file)
            
            self.attach(eventbox, 0, 0, 1, 1)
        else:
            self.attach(preview_box, 0, 0, 1, 1)

    def generate_play_pause_icons(self):
        play_image = Gtk.Image().new_from_icon_name("media-playback-start-symbolic", Gtk.IconSize.SMALL_TOOLBAR)
        play_image.get_style_context().add_class("icon-dropshadow")
        play_icon = Gtk.Button(image=play_image)
        play_icon.props.always_show_image = True
        play_icon.props.halign = Gtk.Align.CENTER
        play_icon.props.valign = Gtk.Align.CENTER
        play_icon.set_size_request(32, 32)
        play_icon.get_style_context().add_class("play-pause-shadow")
        self.play_revealer = Gtk.Revealer()
        self.play_revealer.props.transition_type = Gtk.RevealerTransitionType.CROSSFADE
        self.play_revealer.add(play_icon)

        pause_image = Gtk.Image().new_from_icon_name("media-playback-pause-symbolic", Gtk.IconSize.SMALL_TOOLBAR)
        pause_image.get_style_context().add_class("icon-dropshadow")
        pause_icon = Gtk.Button(image=pause_image)
        pause_icon.props.always_show_image = True
        pause_icon.props.halign = Gtk.Align.CENTER
        pause_icon.props.valign = Gtk.Align.CENTER
        pause_icon.set_size_request(32, 32)
        pause_icon.get_style_context().add_class("play-pause-shadow")
        self.pause_revealer = Gtk.Revealer()
        self.pause_revealer.props.transition_type = Gtk.RevealerTransitionType.CROSSFADE
        self.pause_revealer.add(pause_icon)

    def open_file(self, eventbox, eventbutton):
        if eventbutton.button == 1 and eventbutton.type.value_name == "GDK_BUTTON_PRESS":
            self.callback(self.callback_data)

    def toggle_gif_animation(self, eventbox, eventbutton):
        if eventbutton.button == 1 and eventbutton.type.value_name == "GDK_BUTTON_PRESS":
            if self.play_gif_thread is not None:
                self.stop_threads = True
                self.play_gif_thread.join()
                self.play_gif_thread = None
            else:
                import threading
                self.stop_threads = False
                self.play_gif_thread = threading.Thread(target=self.animation_func)
                self.play_gif_thread.start()

    def on_hover_enter(self, *args):
        proceed = False
        if "audio" in self.type or "video" in self.type:
            proceed = True
        if "gif" in self.type and self.play_gif_thread is not None:
            proceed = True
        if proceed:
            if "audio" in self.type or "video" in self.type:
                self.play_revealer.set_reveal_child(True)
            else:
                self.pause_revealer.set_reveal_child(True)
        else:
            self.play_revealer.set_reveal_child(True)

    def on_hover_leave(self, *args):
        self.pause_revealer.set_reveal_child(False)
        self.play_revealer.set_reveal_child(False)

    def animation_func(self, *args):
        import time
        while True:
            self.iter.advance()
            self.queue_draw()
            time.sleep(self.iter.get_delay_time()/1000)
            if self.stop_threads:
                break

    def draw(self, drawing_area, cairo_context, hover_scale=1):
        '''
        Forked and ported from https://github.com/elementary/greeter/blob/master/src/Widgets/BackgroundImage.vala
        '''
        from math import pi

        scale = self.get_scale_factor()
        width = self.get_allocated_width() * scale * hover_scale
        height = self.get_allocated_height() * scale * hover_scale
        radius = 4 * scale #Off-by-one to prevent light bleed

        if "gif" in self.type:
            pixbuf = GdkPixbuf.PixbufAnimationIter.get_pixbuf(self.iter)
            pixbuf_fitted = GdkPixbuf.Pixbuf.new(pixbuf.get_colorspace(), pixbuf.get_has_alpha(), pixbuf.get_bits_per_sample(), width, height)
        else:
            pixbuf = self.pixbuf_original
            pixbuf_fitted = GdkPixbuf.Pixbuf.new(pixbuf.get_colorspace(), pixbuf.get_has_alpha(), pixbuf.get_bits_per_sample(), width, height)

        if int(width * self.ratio_h_w) < height:
            scaled_pixbuf = pixbuf.scale_simple(int(height * self.ratio_w_h), height, GdkPixbuf.InterpType.BILINEAR)
        else:
            scaled_pixbuf = pixbuf.scale_simple(width, int(width * self.ratio_h_w), GdkPixbuf.InterpType.BILINEAR)

        if self.pixbuf_original_width * self.pixbuf_original_height < width * height:
            # Find the offset we need to center the source pixbuf on the destination since its smaller
            y = abs((height - self.pixbuf_original_height) / 2)
            x = abs((width - self.pixbuf_original_width) / 2)
            final_pixbuf = self.pixbuf_original
        else:
            # Find the offset we need to center the source pixbuf on the destination
            y = abs((height - scaled_pixbuf.props.height) / 2)
            x = abs((width - scaled_pixbuf.props.width) / 2)
            scaled_pixbuf.copy_area(x, y, width, height, pixbuf_fitted, 0, 0)
            # Set coordinates for cairo surface since this has been fitted, it should be (0, 0) coordinate
            x = y = 0
            final_pixbuf = pixbuf_fitted

        # cairo_context.set_operator(cairo.Operator.SOURCE)

        cairo_context.save()
        cairo_context.scale(1.0 / scale, 1.0 / scale)
        # cairo_context.new_sub_path()

        # draws rounded rectangle
        # cairo_context.arc(width - radius, radius, radius, 0-pi/2, 0) # top-right-corner
        # cairo_context.arc(width - radius, height - radius, radius, 0, pi/2) # bottom-right-corner
        # cairo_context.arc(radius, height - radius, radius, pi/2, pi) # bottom-left-corner
        # cairo_context.arc(radius, radius, radius, pi, pi + pi/2) # top-left-corner
    
        # cairo_context.close_path()

        Gdk.cairo_set_source_pixbuf(cairo_context, final_pixbuf, x, y)

        # cairo_context.clip()
        cairo_context.paint()
        cairo_context.restore()