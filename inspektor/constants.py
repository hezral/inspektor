#!/usr/bin/env python3

'''
   Copyright 2020 Adi Hezral (hezral@gmail.com)

   This file is part of inspektor.

    inspektor is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    inspektor is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with inspektor.  If not, see <http://www.gnu.org/licenses/>.
'''

import gi
import os
import locale
import gettext
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class app:
    application_shortname = "inspektor"
    application_id = "com.github.hezral.inspektor"
    application_name = "Inspektor"
    application_description = "View additional metadata for files"
    application_version = None
    app_years = None
    main_url = "https://github.com/hezral/inspektor"
    bug_url = "https://github.com/hezral/inspektor/issues/labels/bug"
    help_url = "https://github.com/hezral/inspektor/wiki"
    translate_url = "https://github.com/hezral/inspektor/blob/master/CONTRIBUTING.md"
    about_authors = None 
    about_documenters = None
    about_comments = application_description
    about_license_type = Gtk.License.GPL_3_0

class data:
    basedata = ('Directory','FileSize','FileModifyDate','FileAccessDate','FileInodeChangeDate','FilePermissions','FileType','FileTypeExtension','MIMEType')


class colors:
    primary_color = None
    primary_text_color = None
    primary_text_shadow_color = None

