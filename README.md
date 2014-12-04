piHud
=====

Configurable heads up display fit for the Raspberry Pi

## Installation

### Setting up your environment

Before you can do anything with this (run the webserver locally, or any of
the scripts) you'll need to setup and activate a python [virtualenv]
(http://pypi.python.org/pypi/virtualenv). Run the following at the command
prompt...

#### On Windows

###Install Pip & PyGal

If you do not have python installed, or are not sure, follow [these steps](http://docs.python-guide.org/en/latest/starting/install/win/) to install/check python.

If you do have pip, go [here](https://pip.pypa.io/en/latest/installing.html) and follw the insturctions to install pip.

If you have pip installed on your machine,

```pip install pygal```

###Install PyQt

[Download the exe,](http://www.riverbankcomputing.com/software/pyqt/download) at the bottom of the page, of PyQt, make sure to have the Py2.7 and correct architecture (32- or 64-bit).

###Install Python-ODB

Clone the [repository](https://github.com/brendanwhitfield/python-OBD/tree/async) and run

```python setup.py install```

###Install PiHud

Clone the [repository](https://github.com/brendanwhitfield/piHud) and run

```python piHud/__main__.py```

#### On Linux/Mac OS X


If you don't have virtualenv installed yet, try:

```$ sudo easy_install virtualenv virtualenvwrapper```

If you're using a distro like Fedora or Ubuntu, you should try this instead::

 Fedora:
 ```$ sudo yum install python-virtualenv!```

 Ubuntu/Debian:
 ```$ sudo apt-get install python-virtualenv```

### Activating your enivronment

```mkvirtualenv pihud```

If you do have virtualenv installed, just run:

```workon pihud```

## Then install the Python dependencies from Pypi

```pip install -r requirements.txt```


### In Fedora:

```sudo yum install PyQt4```

### Dealing with PyQt4 Packaging

yum install PyQt4:
```sudo yum install PyQt4-devel```

symlink the PyQt4 and sip libraries into your virtual environment:

```ln -s /usr/lib64/python2.7/site-packages/PyQt4 /home/$USER/.virtualenvs/pihud/lib/python2.7/```

```ln -s /usr/lib64/python2.7/site-packages/sip.so /home/$USER/.virtualenvs/pihud/lib/python2.7/```


Running
-------

To run, simply execute the following command:

    python piHud/__main__.py
