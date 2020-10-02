# Install icons
icon_sizes = ['16', '24', '32', '48', '64', '128']

foreach i : icon_sizes
    install_data (
        join_paths ('icons', i, meson.project_name () + '.svg'),
        install_dir: join_paths (get_option ('datadir'), 'icons', 'hicolor', i + 'x' + i, 'apps')
    )
    install_data (
        join_paths ('icons', i, meson.project_name () + '.svg'),
        install_dir: join_paths (get_option ('datadir'), 'icons', 'hicolor', i + 'x' + i + '@2', 'apps')
    )
endforeach

# Install scaralable app icon
install_data(
    meson.project_name() + '.svg',
    install_dir: join_paths (get_option ('datadir'), 'icons', 'hicolor', 'scalable', 'apps')
)

# Install Contractor menu
install_data(
    meson.project_name() + '.contract',
    install_dir: join_paths(get_option('prefix'), 'share', 'contractor')
)

# Install Application menu
install_data(
    meson.project_name() + '.desktop',
    install_dir: join_paths(get_option('prefix'), 'share', 'applications')
)

# Install Appdata
install_data(
    meson.project_name() + '.appdata.xml',
    install_dir: join_paths(get_option('prefix'), 'share', 'metainfo')
)
