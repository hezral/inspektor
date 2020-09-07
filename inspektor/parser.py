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

import json
import subprocess
import shutil
import os
import stat

class parser(object):
    def __init__(self, exif_path):
        super().__init__()

        self.exiftool = exif_path
        self.basedata = ('FileName','Directory','FileSize','FileModifyDate','FileAccessDate','FileInodeChangeDate','FilePermissions','FileType','FileTypeExtension','MIMEType')

    def get_jsondata(self, file):
        run_executable = subprocess.Popen([self.exiftool, '-j', file], stdout=subprocess.PIPE)
        stdout, stderr = run_executable.communicate()
        jsondata = json.loads(stdout)[0]
        return jsondata

    def get_permission(self, file):
        stmode = os.lstat(file).st_mode
        permissions = stat.filemode(stmode)
        mode = oct(stat.S_IMODE(stmode))
        return permissions