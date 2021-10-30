# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2021 Adi Hezral <hezral@gmail.com>

import os
import stat
import json
import subprocess

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
 
class HelperUtils():

    def get_jsondata(self, file):
        run_executable = subprocess.Popen(['exiftool', '-j', file], stdout=subprocess.PIPE)
        stdout, stderr = run_executable.communicate()
        jsondata = json.loads(stdout)[0]
        # for key in jsondata:
        #     print(key, ":", jsondata[key])
        return jsondata

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
