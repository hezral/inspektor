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

class parser(object):
    def __init__(self, file):
        super().__init__()

        self.executable = "exiftool"
        if shutil.which(self.executable):
            jsondata = self.get_json(file)

        self.get_basedata(jsondata)

    def get_json(self, file):
        run_executable = subprocess.Popen(['exiftool', '-j', file], stdout=subprocess.PIPE)
        stdout, stderr = run_executable.communicate()

        for data in json.loads(stdout):
            for key in data:
                print(key, ':', data[key])

        jsondata = json.loads(stdout)[0]
        return jsondata

    def get_basedata(self, json):
        base_filename = json['FileName']
        base_directory = json['Directory']
        base_filesize = json['FileSize']
        base_filemodifydate = json['FileModifyDate']
        base_fileaccessdate = json['FileAccessDate']
        base_filechangedate = json['FileInodeChangeDate']
        base_filepermissions = json['FilePermissions']
        basedata = ( \
            base_filename, \
            base_directory, \
            base_filesize, \
            base_filemodifydate,\
            base_fileaccessdate,\
            base_filechangedate,\
            base_filepermissions \
        )
        #print(basicdata)
        return basedata

    def get_extendeddata_file(self, json):
        ext_filetype = json['FileType']
        ext_fileextension = json['FileTypeExtension']
        ext_filemimetype = json['MIMEType']
        extendeddata_file = ( \
            ext_filetype, \
            ext_fileextension, \
            ext_filemimetype \
        )
        return extendeddata_file

    def get_extendeddata_office(self, json):
        pass

    def get_extendeddata_video(self, json):
        pass
    
    def get_extendeddata_audio(self, json):
        pass

    def get_extendeddata_image(self, json):
        pass




