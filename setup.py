#!/usr/bin/env python3

from distutils.core import setup

project_name = 'com.github.hezral.inspektor'
share_path = '/usr/share'
install_path = share_path + '/com.github.hezral.inspektor/'
icon_scalable = share_path + '/icons/hicolor/scalable/apps'
icon_16 = share_path + '/icons/hicolor/16x16/apps'
icon_24 = share_path + '/icons/hicolor/24x24/apps'
icon_32 = share_path + '/icons/hicolor/32x32/apps'
icon_48 = share_path + '/icons/hicolor/48x48/apps'
icon_64 = share_path + '/icons/hicolor/64x64/apps'
icon_128 = share_path + '/icons/hicolor/128x128/apps'

install_data = [(share_path + '/metainfo', ['data/com.github.hezral.inspektor.appdata.xml']),
                (share_path + '/applications', ['data/com.github.hezral.inspektor.desktop']),
                (share_path + '/contractor', ['data/com.github.hezral.inspektor.contract']),
                (icon_scalable,['data/icons/com.github.hezral.inspektor.svg']),
                (icon_16,['data/icons/16/com.github.hezral.inspektor.svg']),
                (icon_24,['data/icons/24/com.github.hezral.inspektor.svg']),
                (icon_32,['data/icons/32/com.github.hezral.inspektor.svg']),
                (icon_48,['data/icons/48/com.github.hezral.inspektor.svg']),
                (icon_64,['data/icons/64/com.github.hezral.inspektor.svg']),
                (icon_128,['data/icons/128/com.github.hezral.inspektor.svg']),
                (install_path,['inspektor/application.py']),
                (install_path,['inspektor/window.py']),
                (install_path,['inspektor/parser.py']),
                (install_path,['inspektor/about.py']),
                (install_path,['inspektor/constants.py'])]

setup(  name='inspektor',
        version='1.0.0',
        author='Adi Hezral',
        description='View additional metadata for files',
        url='https://github.com/hezral/inspektor',
        license='GNU GPL3',
        scripts=['com.github.hezral.inspektor'],
        data_files=install_data)
