
import os
import inspect
from BaseWidget import BaseWidget


# the final dict for storing classes by classname
widgets = {}


# python modules in this directory to exclude
exclude = [
	'__init__',
	'BaseWidget'
]


# find python files in this directory
for f in os.listdir(os.path.dirname(__file__)):
	name, ext = os.path.splitext(f)

	if ext != '.py':
		continue

	if name in exclude:
		continue

	# import the module
	module = __import__(name, locals(), globals())

	# search each modules dict for classes that implement BaseWidget
	for key in module.__dict__:
		e = module.__dict__[key]

		if not inspect.isclass(e):
			continue

		if e == BaseWidget:
			continue

		if issubclass(e, BaseWidget):
			widgets[key] = e

