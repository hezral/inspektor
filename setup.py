#!/usr/bin/python3

import glob, os 
from distutils.core import setup

install_data = [('share/applications', ['data/com.github.hezral.inspektor.desktop']),
                ('share/metainfo', ['data/com.github.hezral.inspektorappdata.xml']),
                ('share/icons/hicolor/128x128/apps',['data/com.github.hezral.inspektorsvg']),
                ('bin/inspektor',['inspektor/constants.py']),
                ('bin/inspektor',['inspektor/headerbar.py']),
                ('bin/inspektor',['inspektor/main.py']),
                ('bin/inspektor',['inspektor/welcome.py']),
                ('bin/inspektor',['inspektor/window.py']),
                ('bin/inspektor',['inspektor/__init__.py']),
                ('bin/inspektor/locale/it_IT/LC_MESSAGES',
                    ['inspektor/locale/it_IT/LC_MESSAGES/inspektor.mo']),
                ('bin/inspektor/locale/it_IT/LC_MESSAGES',
                    ['inspektor/locale/it_IT/LC_MESSAGES/inspektor.po'])]

setup(  name='inspektor',
        version='1.0.0',
        author='Adi Hezral',
        description='An application for viewing additional file information, designed for elementary OS',
        url='https://github.com/hezral/inspektor',
        license='GNU GPL3',
        scripts=['com.github.hezral.inspektor'],
        packages=['inspektor'],
        data_files=install_data)
