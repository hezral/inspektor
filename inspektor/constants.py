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
    app_name = "inspektor"
    app_id = "com.github.hezral.inspektor"
    app_name = "Inspektor"
    app_description = "View additional metadata for files"
    app_version = '1.0'

    about_authors = ["hezral@gmail.com"]
    about_comments = app_description
    about_license_type = Gtk.License.GPL_3_0
    about_logo_icon_name = "com.github.hezral.inspektor"
    about_program_name = app_name
    about_version = app_version
    about_website = "https://github.com/hezral/inspektor"
    about_website_label = "Feedback/Report Bugs at Github"
    about_copyright = "Copyright © 2020 Adi Hezral"
    about_license = '''
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

class data:
    basedata = ('FileName','Directory','FileSize','FileModifyDate','FileAccessDate','FileInodeChangeDate','FilePermissions','FileType','FileTypeExtension','MIMEType')
    mindata = ('FileName','Directory','FileSize','FileModifyDate','FileAccessDate','FileInodeChangeDate','FilePermissions')


class tools:
    tools = ('exiftool','setfattr','getfattr')



