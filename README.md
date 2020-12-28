<div align="center">

![icon](data/icons/com.github.hezral.inspektor.svg)

# Inspektor

[![Get it on AppCenter](https://appcenter.elementary.io/badge.svg)](https://appcenter.elementary.io/com.github.hezral.inspektor)

If you like what i make, it would really be nice to have someone

<a href="https://www.buymeacoffee.com/hezral" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>

## Inspektor helps your to view file metadata easily in a window and export it to JSON, CSV or Text file format. 

</div>
<div align="center">

![Screenshot 01](data/screenshot-01.png?raw=true)
![Screenshot 02](data/screenshot-02.png?raw=true)
![Screenshot 03](data/screenshot-03.png?raw=true)

</div>

## Installation

# Install it from source

You can of course download and install this app from source.

## Dependencies

Ensure you have these dependencies installed. 
Except for ExifTool, your Linux distribution may/may not have this already installed. 

* python3
* libgtk-3-dev
* exiftool
* setfattr
* getfattr

## Installation

Download the updated source [here](https://gitlab.com/hezral/inspektor/archive/master.zip), or use git:
```bash
git clone https://gitlab.com/hezral/inspektor.git
cd inspektor
```

### From .setup.py
In the inspektor file directory:
```bash
sudo python3 setup.py install --prefix=/usr --install-data prefix/share --install-purelib prefix/share
```

## Uninstallation
This will output all the installed files.
```bash
sudo python3 setup.py install --prefix=/usr --install-data prefix/share --record files.txt
```
Then when you want to uninstall it simply run; be careful with the 'sudo'
```bash
cat files.txt | xargs sudo rm -rf
```

## How to run from command line
```bash
com.github.hezral.inspektor
```

## How to run in elementary OS
Right click on a file and select File Inspektor
![](data/action.gif)

## Thanks/Credits

- [ExifTool by Phil Harvey](https://exiftool.org/) Won't work without it. 
- [Extended File Attribues in Linux](https://www.linuxtoday.com/blog/extended-file-attributes-rock.html) Gave me the idea.
- [ElementaryPython](https://github.com/mirkobrombin/ElementaryPython) This started me off on coding with Python and GTK. 
