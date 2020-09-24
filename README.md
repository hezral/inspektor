<div align="center">

![icon](data/icons/com.github.hezral.inspektor.svg)

# Inspektor

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

### From .setup.py
Download the updated source [here](https://gitlab.com/hezral/inspektor/archive/master.zip), or use git:

```bash
git clone https://gitlab.com/hezral/inspektor.git
cd inspektor
sudo python3 setup.py install
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
