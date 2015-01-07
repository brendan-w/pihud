
import os
import sys
import shutil
from PiHud import PiHud
from PyQt4 import QtGui
from ConfigFile import ConfigFile


running_dir         = os.path.dirname(os.path.realpath(__file__))
default_config_path = os.path.join(running_dir, 'default.rc')
config_path         = os.path.join(os.path.expanduser('~'), 'pihud.rc')


def main():
	""" entry point """

	if not os.path.isfile(config_path):
		# copy the default config
		if not os.path.isfile(default_config_path):
			print "[piHud] Fatal: Missing default config file. Try reinstalling"
			sys.exit(1)
		else:
			shutil.copyfile(default_config_path, config_path)

	global_config = ConfigFile(config_path)

	# Start QT application, exit upon return
	'''
	app = QtGui.QApplication(sys.argv)
	pihud = PiHud()
	sys.exit(app.exec_())
	'''



if __name__ == "__main__":
	main()
