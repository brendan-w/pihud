piHud
=====

Configurable heads up display fit for the Raspberry Pi

Warning: This project is still in the very early stages of development.

Turning you Pi into a PiHud
---------------------------

For installation instructions on different platforms, see the `GitHub wiki <https://github.com/brendanwhitfield/piHud/wiki/Installation>`_

First, it is recommended that you start with a clean install of `Raspbian <http://www.raspberrypi.org/downloads/>`_. On first boot, it will prompt you with a setup screen. After you have expanded the filesystem and set your password, enter the listing named

::

	Enable Boot to Desktop/Scratch

In this option, make sure to select the console only option, in order to prevent the Pi from starting its desktop environment on boot

::

	Console Text console, requiring login

You can now click finish, and boot your Pi. After loging in, you will be presented with a terminal. Please install the following dependencies

::

	$ sudo apt-get install python-qt4
	$ sudo apt-get install python-pip
	$ sudo pip install pihud

In order to run PiHud on boot, you will need to tweak a few config files (note: most of the following was taken from `this post <http://www.raspberrypi.org/forums/viewtopic.php?p=344408>`_). Open the file `/etc/rc.local` in a text editor of your choice. Add the following line just before the `exit 0`

::

	su -s /bin/bash -c startx pi &

Now, in order to allow X sessions for all users, run the following command, and choose `Anybody` from the list of options

::

	$ sudo dpkg-reconfigure x11-common

Finally, create an `.xinitrc` file (if you don't have one already), in your home directory

::

	$ touch ~/.xinitrc

Open it in a text editor of your choice, and add the following line:

::

	python -m piHud

Your done! You can now reboot the Pi with:

::

	$ sudo shutdown -r 0


Configuring
-----------

PiHud is configured by modifying a file named `pihud.rc` in your home directory. This file will be created the first time piHud runs. However, a few settings are accessable through the piHud app itself. To move widgets, simply click and drag them around the screen. Right clicking on widgets will tell you which sensor they are tied to, and allow you to delete them. Right clicking on the black background (not on a widget), will let you add widgets or pages to your HUD. To switch pages, simply press the `TAB` key on your keyboard.

All other settings are available in the `pihud.rc` file, which is merely json. A few items of note in this file:

+ Each widget is an object containing a key for `sensor`, `type`, and `config`
+ The `sensor` field is the string name for any sensor your car supports. A full list can be found in the `python-OBD wiki <https://github.com/brendanwhitfield/python-OBD/wiki/Command-Tables>`_
+ All `color` attributes accept CSS color values
+ The `page_adv_pin` setting is used to tie the page cycling to any of the Pi's GPIO pins. Simply wire a button that grounds the set pin while pressed.
+ The `demo` key is used to feed a sin() curve into all widgets. It is used primarily for testing
