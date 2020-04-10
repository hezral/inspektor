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
    def __init__(self):
        super().__init__()

        self.executable = "exiftool"

        self.basedata = ('FileName','Directory','FileSize','FileModifyDate','FileAccessDate','FileInodeChangeDate','FilePermissions','FileType','FileTypeExtension','MIMEType')

        try:
            shutil.which(self.executable)
        except shutil.Error as error:
            print('Shutil: ', error)

    def get_jsondata(self, file):
        run_executable = subprocess.Popen([self.executable, '-j', file], stdout=subprocess.PIPE)
        stdout, stderr = run_executable.communicate()
        
        jsondata = json.loads(stdout)[0]
        
        return jsondata

        
    def get_basedata(self, jsondata):
        base_filename = jsondata['FileName']
        base_directory = jsondata['Directory']
        base_filesize = jsondata['FileSize']
        base_filemodifydate = jsondata['FileModifyDate']
        base_fileaccessdate = jsondata['FileAccessDate']
        base_filechangedate = jsondata['FileInodeChangeDate']
        base_filepermissions = jsondata['FilePermissions']
        base_filetype = jsondata['FileType']
        base_fileextension = jsondata['FileTypeExtension']
        base_filemimetype = jsondata['MIMEType']
        basedata = ( \
            base_filename, \
            base_filetype, \
            base_fileextension, \
            base_filemimetype, \
            base_directory, \
            base_filesize, \
            base_filemodifydate,\
            base_fileaccessdate,\
            base_filechangedate,\
            base_filepermissions 
        )
        return basedata

    def get_extendeddata_photo(self, jsondata):
        extended_photo = jsondata['Height']
        pass

    def get_extendeddata_image(self, jsondata):
        pass

    def get_extendeddata_office(self, jsondata):
        pass

    def get_extendeddata_video(self, jsondata):
        # extended_video
        # Duration
        # ImageWidth
        # ImageHeight
        # VideoFrameRate
        # AudioChannels
        # AudioBitsPerSample
        # AudioSampleRate
        # ImageSize
        # Megapixels
        pass
    
    def get_extendeddata_audio(self, jsondata):
        pass






