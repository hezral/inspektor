#!/usr/bin/env python3

import glob, os
from os import environ, path
from subprocess import call
from distutils.core import setup
from setuptools.command.install import install

project_name = 'com.github.hezral.inspektor'
share_path = '/usr/share'
install_path = share_path + '/com.github.hezral.inspektor/inspektor'
icon_scalable = share_path + '/icons/hicolor/scalable/app'
icon_16 = share_path + '/icons/hicolor/16x16/app'
icon_24 = share_path + '/icons/hicolor/24x24/app'
icon_32 = share_path + '/icons/hicolor/32x32/app'
icon_48 = share_path + '/icons/hicolor/48x48/app'
icon_64 = share_path + '/icons/hicolor/64x64/app'
icon_128 = share_path + '/icons/hicolor/128x128/app'

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

class PostInstall(install):
    prefix = environ.get('MESON_INSTALL_PREFIX', '/usr')
    datadir = path.join(prefix, 'share')
    destdir = environ.get('DESTDIR', '')

    if not destdir:
        print('Updating icon cache...')
        call(['gtk-update-icon-cache', '-qtf', path.join(datadir, 'icons', 'hicolor')])
        # print("Installing new Schemas")
        # call(['glib-compile-schemas', path.join(datadir, 'glib-2.0/schemas')])

setup(  name='inspektor',
        version='1.0.0',
        author='Adi Hezral',
        description='View additional metadata for files',
        url='https://github.com/hezral/inspektor',
        license='GNU GPL3',
        scripts=['com.github.hezral.inspektor'],
        packages=['inspektor'],
        data_files=install_data,
        cmdclass={'install': PostInstall})
