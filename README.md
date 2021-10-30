<div align="center">

![icon](data/icons/128.svg)


[![Get it on AppCenter](https://appcenter.elementary.io/badge.svg)](https://appcenter.elementary.io/com.github.hezral.inspektor) 

<a href="https://www.buymeacoffee.com/hezral" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>
</div>

### Inspektor helps your to view file metadata easily in a window and export it to JSON, CSV or Text file format. 

| ![Screenshot 01](data/screenshot-01.png?raw=true) | ![Screenshot 02](data/screenshot-02.png?raw=true) | ![Screenshot 03](data/screenshot-03.png?raw=true) |
|------------------------------------------|-----------------------------------------|-----------------------------------------|

| ![Screenshot 03](data/screenshot-04.png?raw=true) | ![Screenshot 03](data/screenshot-05.png?raw=true) |
|------------------------------------------|-----------------------------------------|

## Installation

## Build using flatpak
* requires that you have flatpak-builder installed
* flatpak enabled
* flathub remote enabled

```
flatpak-builder --user --force-clean --install build-dir com.github.hezral.inspektor.yml
```

### Build using meson 
Ensure you have these dependencies installed

* python3
* python3-gi
* libgranite-dev
* python3
* libgtk-3-dev
* libimage-exiftool-perl
* attr

Download the updated source [here](https://github.com/hezral/inspektor/archive/master.zip), or use git:
```bash
git clone https://github.com/hezral/inspektor.git
cd inspektor
meson build --prefix=/usr
cd build
ninja build
sudo ninja install
```
The desktop launcher should show up on the application launcher for your desktop environment
if it doesn't, try running
```
com.github.hezral.inspektor
```

## Thanks/Credits
- [ExifTool by Phil Harvey](https://exiftool.org/) Won't work without it. 
- [Extended File Attribues in Linux](https://www.linuxtoday.com/blog/extended-file-attributes-rock.html) Gave me the idea.
- [ElementaryPython](https://github.com/mirkobrombin/ElementaryPython) This started me off on coding with Python and GTK. 
