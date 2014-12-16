piHud
=====

Configurable heads up display fit for the Raspberry Pi

## Turning you Pi into a PiHud

For installation instructions on different platforms, see the [GitHub wiki](https://github.com/brendanwhitfield/piHud/wiki/Installation)

First, it is recommended that you start with a clean install of [Raspbian](http://www.raspberrypi.org/downloads/). On first boot, it will prompt you with a setup screen. After you have expanded the filesystem and set your password, enter the listing named:

	Enable Boot to Desktop/Scratch

In this option, make sure to select the console only option, in order to prevent the Pi from starting its desktop environment on boot.

	Console Text console, requiring login

You can now click finish, and boot your Pi. After loging in, you will be presented with a terminal. Please install the following dependencies:

	$ sudo apt-get install python-qt4
	$ sudo apt-get install python-pip
	$ sudo pip install pihud

In order to run PiHud on boot, you will need to tweak a few config files

