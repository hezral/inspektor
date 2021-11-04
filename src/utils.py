# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2021 Adi Hezral <hezral@gmail.com>

import os
import stat
import json
import subprocess
import cv2

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Gio
 
class HelperUtils():

    def get_jsondata(self, file):
        run_executable = subprocess.Popen(['exiftool', '-j', file], stdout=subprocess.PIPE)
        stdout, stderr = run_executable.communicate()
        jsondata = json.loads(stdout)[0]
        # for key in jsondata:
        #     print(key, ":", jsondata[key])
        return jsondata

    def get_audio_art(self, infile=None, outfile=None):
        audio_art = None
        probe_cmd = 'exiftool -a -G4 "-picture*" {0}'.format(infile)
        run_executable = subprocess.Popen(probe_cmd, shell=True, stdout=subprocess.PIPE)
        stdout, stderr = run_executable.communicate()
        i = 0
        lines = stdout.decode("utf-8").replace(" ","").split("\n")
        for line in lines:
            if "FrontCover" in line:
                image_type =lines[i-1].split(":")[-1].split("/")[-1]
                if image_type == "jpeg":
                    image_type = "jpg"
                outfile = "{0}.{1}".format(outfile, image_type)

                copynum = line.split(":")[0].split("]")[0].split("[")
                
                if copynum[-1] == "":
                    export_cmd = 'exiftool -picture -b {0} > {1}'.format(infile, outfile)
                else:
                    export_cmd = 'exiftool -{0}:picture -b {1} > {2}'.format(copynum[-1], infile, outfile)
                run_executable = subprocess.Popen(export_cmd, shell=True, stdout=subprocess.PIPE)
                stdout, stderr = run_executable.communicate()
                audio_art = outfile
                break                
            i += 1
        return audio_art

    def get_video_frame(self, infile=None, outfile=None):
        video_frame = None
        video_capture = cv2.VideoCapture(infile)
        success, image = video_capture.read()
        count = 0
        frame = 30
        outfile = "{0}.{1}".format(outfile, "png")
        while count <= frame:
            if count == frame:
                cv2.imwrite(outfile, image)
                video_frame = outfile
            success, image = video_capture.read()
            count += 1
        return video_frame

    def get_permission(self, file):
        stmode = os.lstat(file).st_mode
        permissions = stat.filemode(stmode)
        mode = oct(stat.S_IMODE(stmode))
        return permissions

    def get_file_comments(self, file):
        run_executable = subprocess.Popen(['getfattr', '-n', 'user.comment', '--only-values', '--absolute-names', file], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        stdout, stderr = run_executable.communicate()
        file_comments = stdout.decode('utf-8')
        return file_comments

    def set_file_comments(self, file, text):
        run_executable = subprocess.Popen(['setfattr', '-n', 'user.comment', '-v', text, file], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        run_executable.communicate()
        if self.get_file_comments(file) == text:
            return True
        else:
            return False

    def export_json(self, file):
        outfile = file + '_metadata.json'
        with open(outfile,'wb') as out:
            subprocess.Popen(['exiftool', '-j', file], stdout=out,stderr=subprocess.DEVNULL)

    def export_csv(self, file):
        outfile = file + '_metadata.csv'
        with open(outfile,'wb') as out:
            subprocess.Popen(['exiftool', '-csv', file], stdout=out,stderr=subprocess.DEVNULL)

    def export_txt(self, file):
        outfile = file + '_metadata.txt'
        with open(outfile,'wb') as out:
            subprocess.Popen(['exiftool', file], stdout=out,stderr=subprocess.DEVNULL)

    def file_chooser(self, parent):
        file_chooser_dialog = Gtk.FileChooserDialog()
        file_chooser_dialog.add_button("_Open", Gtk.ResponseType.OK)
        file_chooser_dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        file_chooser_dialog.set_default_response(Gtk.ResponseType.OK)
        file_chooser_dialog.set_transient_for(parent)
        file_chooser_dialog.set_destroy_with_parent(False)
        file_chooser_dialog.set_position(Gtk.WindowPosition.MOUSE)
        file_chooser_dialog.set_size_request(320, 480)
        
        response = file_chooser_dialog.run()
        file = None
        if response == Gtk.ResponseType.OK:
            file = file_chooser_dialog.get_file() #return a GLocalFile object
            file_chooser_dialog.destroy()
        else:
            file_chooser_dialog.destroy()
        if file is not None:
            return file

    def copy_to_clipboard(self, text):
        import gi
        gi.require_version('Gtk', '3.0')
        from gi.repository import Gtk, Gdk

        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

        try:
            clipboard.set_text(text, -1)
            return True
        except:
            return False

    def open_file_with_default_app(self, path=None):
        ''' Function to view file using default application via Gio'''
        view_file = Gio.File.new_for_path(path)
        if view_file.query_exists():
            try:
                Gio.AppInfo.launch_default_for_uri(uri=view_file.get_uri(), context=None)
            except:
                import traceback
                print(traceback.format_exc())