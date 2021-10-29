# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2021 Adi Hezral <hezral@gmail.com>

import json
import subprocess
from shutil import which, Error
import os
import stat
from .constants import tools

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
            #print("Found setfattr installed at", self.setfattr)
        except Error as error:
            print("Shutil: ", error)

        try:
            self.getfattr = which("getfattr")
            #print("Found getfattr installed at", self.getfattr)
        except Error as error:
            print("Shutil: ", error)
 

    def get_jsondata(self, file):
        run_executable = subprocess.Popen([self.exiftool, '-j', file], stdout=subprocess.PIPE)
        stdout, stderr = run_executable.communicate()
        jsondata = json.loads(stdout)[0]

        for key in jsondata:
            print(key, ":", jsondata[key])

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

