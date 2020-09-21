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
from shutil import which, Error
import os
import stat
from constants import tools

class parser(object):
    def __init__(self):
        super().__init__()

        #check if exiftool is installed
        try:
            self.exiftool = which("exiftool")
            #print("Found exiftool installed at", self.exiftool)
        except Error as error:
            print("Shutil: ", error)

        try:
            self.setfattr = which("setfattr")
            #("Found exiftool installed at", self.setfattr)
        except Error as error:
            print("Shutil: ", error)

        try:
            self.getfattr = which("getfattr")
            #print("Found exiftool installed at", self.getfattr)
        except Error as error:
            print("Shutil: ", error)
 

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

    def get_file_comments(self, file):
        run_executable = subprocess.Popen([self.getfattr, '-n', 'user.comment', '--only-values', '--absolute-names', file], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        stdout, stderr = run_executable.communicate()
        file_comments = stdout.decode('utf-8')
        return file_comments

    def set_file_comments(self, file, text):
        run_executable = subprocess.Popen([self.setfattr, '-n', 'user.comment', '-v', text, file], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        run_executable.communicate()
        

    def export_json(self, file):
        outfile = file + '_metadata.json'
        with open(outfile,'wb') as out:
            subprocess.Popen([self.exiftool, '-j', file], stdout=out,stderr=subprocess.DEVNULL)


    def export_csv(self, file):
        outfile = file + '_metadata.csv'
        with open(outfile,'wb') as out:
            subprocess.Popen([self.exiftool, '-csv', file], stdout=out,stderr=subprocess.DEVNULL)

    def export_txt(self, file):
        outfile = file + '_metadata.txt'
        with open(outfile,'wb') as out:
            subprocess.Popen([self.exiftool, file], stdout=out,stderr=subprocess.DEVNULL)

