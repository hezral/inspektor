# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2021 Adi Hezral <hezral@gmail.com>

import re
import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gio, Pango

class ExtendedView(Gtk.Grid):

    def __init__(self, app, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.app = app

        self.props.halign = Gtk.Align.FILL
        self.props.valign = Gtk.Align.FILL
        self.props.expand = True
        self.props.margin = 4
        self.props.column_spacing = 6
        self.props.row_spacing = 6

        self.extended_scrolledview = Gtk.ScrolledWindow()
        self.extended_scrolledview.add(self)
        self.extended_scrolledview.props.shadow_type = Gtk.ShadowType(3)
        self.extended_scrolledview.props.vscrollbar_policy = Gtk.PolicyType(1)

        # base grid for stack
        extended_grid = Gtk.Grid()
        extended_grid.props.expand = True
        extended_grid.props.margin = 24
        extended_grid.props.column_spacing = 6
        extended_grid.props.row_spacing = 6
        extended_grid.attach(self.extended_scrolledview, 0, 1, 1, 1)
