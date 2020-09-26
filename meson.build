# Project name, programming language and version
project (
    'com.github.hezral.inspektor',
    version: '1.0.0'
)

# Listing dependencies
dependencies = [
    dependency ('gtk+-3.0', required: true),
    dependency ('python3', required: true),
    dependency ('pygobject-3.0', required: true),
    dependency ('gobject-introspection-1.0', required: true)
]

subdir ('data')

install_subdir(
  'inspektor',
  install_dir: join_paths(get_option('datadir'), 'com.github.hezral.inspektor'),
  exclude_directories: '__pycache__',
  strip_directory: true
)

install_data(
    'com.github.hezral.inspektor',
    install_dir: get_option('bindir')
)

meson.add_install_script ('post_install.py')
