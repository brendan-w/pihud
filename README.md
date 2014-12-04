piHud
=====

Configurable heads up display fit for the Raspberry Pi

## Installation

### Setting up your environment

Before you can do anything with this (run the webserver locally, or any of
the scripts) you'll need to setup and activate a python [virtualenv]
(http://pypi.python.org/pypi/virtualenv). Run the following at the command
prompt...

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



Running
-------

To run, simply execute the following command:

    python piHud/__main__.py
