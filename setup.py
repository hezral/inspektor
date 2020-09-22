#!/usr/bin/python3

import glob, os 
from distutils.core import setup

share_path = '/usr/share'
install_path = share_path + '/com.github.hezral.inspektor/inspektor'
icon_path = share_path + '/icons/hicolor/scalable/app'

install_data = [(share_path + '/metainfo', ['data/com.github.hezral.inspektor.appdata.xml']),
                (share_path + '/applications', ['data/com.github.hezral.inspektor.desktop']),
                (share_path + '/contractor', ['data/com.github.hezral.inspektor.contract']),
                (icon_path,['data/com.github.hezral.inspektor.svg']),
                (install_path,['data/style.css']),
                (install_path,['inspektor/application.py']),
                (install_path,['inspektor/window.py']),
                (install_path,['inspektor/parser.py']),
                (install_path,['inspektor/about.py']),
                (install_path,['inspektor/constant.py'])]

setup(  name='inspektor',
        version='1.0.0',
        author='Adi Hezral',
        description='View additional metadata for files',
        url='https://github.com/hezral/inspektor',
        license='GNU GPL3',
        scripts=['com.github.hezral.inspektor'],
        packages=['inspektor'],
        data_files=install_data)
