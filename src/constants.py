# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2021 Adi Hezral <hezral@gmail.com>

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

class data:
    basedata = [
        ('FileName','Name'),
        ('Directory','Directory'),
        ('FileSize','Size'),
        ('FileAccessDate','Last Accessed'),
        ('FileModifyDate','Content Modified'),
        ('FileInodeChangeDate','Properties Changed'),
        ('FilePermissions','Permissions'),
        ('FileTypeExtension','Extension'),
        ('MIMEType','Type')
        ]
    mindata = [
        ('FileName','Name'),
        ('Directory','Directory'),
        ('FileSize','Size'),
        ('FileModifyDate','Modified'),
        ('FileAccessDate','Last Accessed'),
        ('FileInodeChangeDate','Changed'),
        ('FilePermissions','Permissions')
        ]