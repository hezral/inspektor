python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'inspektor.in',
  output: 'com.github.hezral.inspektor',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

inspektor_sources = [
  '__init__.py',
  'main.py',
  'window.py',
  'drop_view.py',
  'base_view.py',
  'constants.py',
  'utils.py',
  'file_inspeck.py',
]

install_data(inspektor_sources, install_dir: moduledir)
