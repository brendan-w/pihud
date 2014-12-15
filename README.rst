piHud
=====

Configurable heads up display fit for the Raspberry Pi

Installation
------------

On Windows
^^^^^^^^^^

Install PyQt
~~~~~~~~~~~~

`Download the
exe, <http://www.riverbankcomputing.com/software/pyqt/download>`__ at
the bottom of the page, of PyQt, make sure to have the Py2.7 and correct
architecture (32- or 64-bit).

On Linux/Mac OS X
^^^^^^^^^^^^^^^^^

In Ubuntu/Debian:
~~~~~~~~~~~~~~~~~

``sudo apt-get install python-qt4``

In Fedora:
~~~~~~~~~~

``sudo yum install PyQt4``

Dealing with PyQt4 Packaging
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

yum install PyQt4: ``sudo yum install PyQt4-devel``

symlink the PyQt4 and sip libraries into your virtual environment:

``ln -s /usr/lib64/python2.7/site-packages/PyQt4 /home/$USER/.virtualenvs/pihud/lib/python2.7/``

``ln -s /usr/lib64/python2.7/site-packages/sip.so /home/$USER/.virtualenvs/pihud/lib/python2.7/``

Running
-------

To run, simply execute the following command:

::

    python piHud/__main__.py

License
-------
GNU LGPL v2.1

Enjoy and Drive Safely!
