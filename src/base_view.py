# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2021 Adi Hezral <hezral@gmail.com>

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Pango

class BaseView(Gtk.Grid):

    def __init__(self, app, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.app = app

        self.props.halign = Gtk.Align.FILL
        self.props.valign = Gtk.Align.START
        self.props.expand = True
        self.props.column_spacing = 6
        self.props.row_spacing = 6
        self.props.margin_bottom = 10

        self.attach(self.generate_comments_section(), 0, 0, 1, 1)
        self.attach(Gtk.Separator(), 0, 1, 1, 1)
        self.attach(self.generate_base_info(), 0, 2, 1, 1)
        self.attach(Gtk.Separator(), 0, 3, 1, 1)
        self.attach(self.generate_extended_info(), 0, 4, 1, 1)
        self.attach(Gtk.Separator(), 0, 5, 1, 1)
        self.attach(self.generate_preview(), 0, 6, 1, 1)
        self.attach(Gtk.Separator(), 0, 7, 1, 1)
        self.attach(self.generate_utils(), 0, 8, 1, 1)

    def on_view_visible(self):
        if self.app.inspeck_obj.comments != "":
            self.comment_expander.props.expanded = True
        self.base_expander.props.expanded = True
        
    def update_file_comments(self, textview, event):
        startIter, endIter = textview.get_buffer().get_bounds()
        text = textview.get_buffer().get_text(startIter, endIter, True)
        if text != self.app.inspeck_obj.comments:
            self.app.utils.set_file_comments(self.app.inspeck_obj.path,text)
            self.app.inspeck_obj.comments = text

    def generate_comments_section(self):
        self.file_comments = Gtk.TextBuffer()

        comments_textview = Gtk.TextView(buffer=self.file_comments)
        comments_textview.props.wrap_mode = Gtk.WrapMode.WORD_CHAR
        comments_textview.connect('focus-out-event',self.update_file_comments)

        comments_scrolledview = Gtk.ScrolledWindow()
        comments_scrolledview.add(comments_textview)
        comments_scrolledview.props.halign = Gtk.Align.FILL
        comments_scrolledview.props.valign = Gtk.Align.START
        comments_scrolledview.props.vscrollbar_policy = Gtk.PolicyType(1)
        comments_scrolledview.props.expand = True
        comments_scrolledview.props.margin_top = 6
        comments_scrolledview.props.margin_bottom = 6
        comments_scrolledview.set_size_request(-1, 60)

        self.comment_expander = Gtk.Expander()
        self.comment_expander.props.label = "Comments"
        self.comment_expander.props.spacing = 10
        self.comment_expander.props.margin_left = 10
        self.comment_expander.props.margin_right = 10
        self.comment_expander.add(comments_scrolledview)

        return self.comment_expander

    def generate_base_info(self):
        self.base_grid = Gtk.Grid()
        self.base_grid.props.halign = Gtk.Align.FILL
        self.base_grid.props.valign = Gtk.Align.START
        self.base_grid.props.expand = True
        self.base_grid.props.row_spacing = 6
        self.base_grid.props.margin_top = 5
        self.base_grid.props.margin_left = 5
        self.base_grid.props.margin_right = 5

        self.base_expander = Gtk.Expander()
        self.base_expander.props.label = "Base Info"
        self.base_expander.props.spacing = 10
        self.base_expander.props.margin_left = 10
        self.base_expander.props.margin_right = 10
        self.base_expander.add(self.base_grid)

        return self.base_expander

    def generate_extended_info(self):
        self.extended_grid = Gtk.Grid()
        self.extended_grid.props.halign = Gtk.Align.FILL
        self.extended_grid.props.valign = Gtk.Align.START
        self.extended_grid.props.expand = True
        self.extended_grid.props.row_spacing = 4
        self.extended_grid.props.margin_top = 5
        self.extended_grid.props.margin_left = 5
        self.extended_grid.props.margin_right = 5

        self.extended_scrolledwindow = Gtk.ScrolledWindow()
        self.extended_scrolledwindow.props.margin_top = 5
        self.extended_scrolledwindow.set_size_request(-1, 300)
        self.extended_scrolledwindow.add(self.extended_grid)
        self.extended_scrolledwindow.set_shadow_type(Gtk.ShadowType.NONE)

        self.extended_expander = Gtk.Expander()
        self.extended_expander.props.label = "Extended Info"
        self.extended_expander.props.spacing = 20
        self.extended_expander.props.margin_left = 10
        self.extended_expander.props.margin_right = 10
        self.extended_expander.add(self.extended_scrolledwindow)

        return self.extended_expander

    def generate_preview(self):
        self.preview_grid = Gtk.Grid()
        self.preview_grid.props.halign = Gtk.Align.FILL
        self.preview_grid.props.valign = Gtk.Align.START
        self.preview_grid.props.expand = True
        self.preview_grid.props.row_spacing = 6
        self.preview_grid.props.margin_top = 10
        self.preview_grid.props.margin_left = 5
        self.preview_grid.props.margin_right = 5

        self.preview_expander = Gtk.Expander()
        self.preview_expander.props.label = "Preview"
        self.preview_expander.props.spacing = 10
        self.preview_expander.props.margin_left = 10
        self.preview_expander.props.margin_right = 10
        self.preview_expander.add(self.preview_grid)

        return self.preview_expander

    def generate_utils(self):

        def generate_export_menu(name, menu_label, icon_name, callback):
            image = Gtk.Image.new_from_icon_name(icon_name, Gtk.IconSize.LARGE_TOOLBAR)
            button = Gtk.Button(label=menu_label,image=image)
            button.props.name = name
            button.props.always_show_image = True
            button.props.image_position = Gtk.PositionType.TOP
            button.props.expand = True
            button.get_style_context().add_class("flat")
            button.connect("clicked", callback)
            return button

        self.utils_grid = Gtk.Grid()
        self.utils_grid.props.halign = Gtk.Align.FILL
        self.utils_grid.props.valign = Gtk.Align.START
        self.utils_grid.props.expand = True
        self.utils_grid.props.row_spacing = 6
        self.utils_grid.props.margin_top = 10
        self.utils_grid.props.margin_left = 5
        self.utils_grid.props.margin_right = 5
        self.utils_grid.attach(generate_export_menu("json", "Export JSON", "text-css", self.on_button_clicked), 0, 0, 1, 1)
        self.utils_grid.attach(generate_export_menu("csv", "Export CSV", "application-vnd.ms-excel", self.on_button_clicked), 1, 0, 1, 1)
        self.utils_grid.attach(generate_export_menu("txt", "Export TXT", "text-x-generic", self.on_button_clicked), 2, 0, 1, 1)

        self.utils_expander = Gtk.Expander()
        self.utils_expander.props.label = "Utilities"
        self.utils_expander.props.spacing = 10
        self.utils_expander.props.margin_left = 10
        self.utils_expander.props.margin_right = 10
        self.utils_expander.add(self.utils_grid)

        return self.utils_expander

    def on_button_clicked(self, button):
        if button.props.name == "json":
            self.app.utils.export_json(self.app.inspeck_obj.path)
        if button.props.name == "csv":
            self.app.utils.export_csv(self.app.inspeck_obj.path)
        if button.props.name == "txt":
            self.app.utils.export_txt(self.app.inspeck_obj.path)

class DataLabel(Gtk.EventBox):
    def __init__(self, title, value, app, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.app = app
        self.label = title + ': ' + value

        self.data_label = Gtk.Label()
        self.data_label.props.halign = Gtk.Align.START
        self.data_label.props.expand = True
        self.data_label.props.wrap = True
        self.data_label.props.selectable = False
        self.data_label.props.max_width_chars = 32
        self.data_label.props.ellipsize = Pango.EllipsizeMode.END
        self.data_label.props.label = self.label
        if len(self.label) > 32:
            self.data_label.props.has_tooltip = True
            self.data_label.props.tooltip_text = self.label

        self.generate_copy_to_clipboard()

        overlay = Gtk.Overlay()
        overlay.add(self.data_label)
        overlay.add_overlay(self.copy_revealer)
        overlay.add_overlay(self.copied_revealer)

        self.set_size_request(-1, 18)
        self.props.expand = True
        self.add(overlay)
        self.show_all()

        self.connect("enter-notify-event", self.on_hover_datalabel_enter)
        self.connect("leave-notify-event", self.on_hover_datalabel_leave)
        self.connect("button-press-event", self.on_button_pressed)

    def generate_copy_to_clipboard(self):
        copy_button = Gtk.Image().new_from_icon_name("edit-copy-symbolic", Gtk.IconSize.SMALL_TOOLBAR)
        copy_button.props.halign = Gtk.Align.END
        copy_button.get_style_context().add_class("icon-dropshadow")

        self.copy_revealer = Gtk.Revealer()
        self.copy_revealer.add(copy_button)
        self.copy_revealer.props.transition_type = Gtk.RevealerTransitionType.CROSSFADE

        copied_image = Gtk.Image().new_from_icon_name("process-completed", Gtk.IconSize.SMALL_TOOLBAR)
        copied_label = Gtk.Label("copied to clipboard")
        copied_grid = Gtk.Grid()
        copied_grid.props.column_spacing = 2
        copied_grid.props.valign = Gtk.Align.CENTER
        copied_grid.attach(copied_image, 0, 0, 1, 1)
        copied_grid.attach(copied_label, 1, 0, 1, 1)
        copied_grid.props.halign = Gtk.Align.END
        copied_grid.get_style_context().add_class("copied-widget")

        self.copied_revealer = Gtk.Revealer()
        self.copied_revealer.add(copied_grid)
        self.copied_revealer.props.transition_type = Gtk.RevealerTransitionType.CROSSFADE

    def on_hover_datalabel_enter(self, *args):
        self.copy_revealer.set_reveal_child(True)

    def on_hover_datalabel_leave(self, *args):
        self.copy_revealer.set_reveal_child(False)

    def on_button_pressed(self, eventbox, eventbutton):
        if eventbutton.button == 1 and eventbutton.type.value_name == "GDK_BUTTON_PRESS":
            if self.app.utils.copy_to_clipboard(self.label):
                self.copied_revealer.set_reveal_child(True)
                GLib.timeout_add(1000, self.copied_revealer.set_reveal_child, False)
            else:
                self.copied_revealer.get_child().get_children()[1].props.label = "copy failed"
                self.copied_revealer.set_reveal_child(True)
                GLib.timeout_add(1000, self.copied_revealer.set_reveal_child, False)