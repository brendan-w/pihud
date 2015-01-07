
import os
import json
from collections import OrderedDict

import obd
from widgets import widgets
from defaults import new_config


class ConfigFile():
	""" manages the structure of the config file """
	def __init__(self, filename):
		self.filename = filename
		self.load()


	def load(self):
		""" reads a config from a file """
		self.port = None
		self.page_adv_pin = 18
		self.debug = False
		self.pages = []

		required_keys = ['pages']
		optional_keys = ['debug', 'port', 'page_adv_pin']

		json_file = {}

		# read the file
		if os.path.isfile(self.filename):
			with open(self.filename, 'r') as f:
				json_file = json.loads(f.read())

		# check for the required root keys
		if not all(k in json_file for k in ['pages']):
			print "Config is missing the 'pages' array"

		# load optional keys
		for key in optional_keys:
			if key in json_file:
				setattr(self, key, json_file[key])

		# process each page definition
		for page_json in json_file['pages']:
			page = []

			for json_config in page_json:
				config = self.__json_to_config(json_config)

				if config is None:
					print "Skipping invalid widget"
				else:
					page.append(config)


			self.pages.append(page)


	def save(self):
		""" write the config back to the file """
		
		json_pages = []

		for page in self.pages:
			json_page =  []
			for config in page:
				json_config = self.__config_to_json(config)
				json_page.append(json_config)
			json_pages.append(json_page)

		output = OrderedDict([
			('debug', self.debug),
			('port', self.port),
			('page_adv_pin', self.page_adv_pin),
			('pages', json_pages),
		])

		with open(self.filename, 'w') as f:
			f.write(json.dumps(output, indent=4))


	def __json_to_config(self, json_):
		""" Constructs a Config out of a JSON structure """

		if not all((k in json_) for k in ['sensor', 'type', 'config']):
			print "Config is missing required keys"
			return None

		sensor_name = json_['sensor'].upper()
		class_name  = json_['type']
		json_config = json_['config']

		if sensor_name not in obd.commands.__dict__:
			print "sensor '%s' is not a valid OBD command" % sensor_name
			return None

		if class_name not in widgets:
			print "widget '%s' is not a valid Widget type" % class_name
			return None

		# Make a default config for this command
		config = new_config(obd.commands[sensor_name],
		                    class_name)

		# Overwrite default values with user values
		for key in json_config:

			# prevent the 'config' section from overriding keys with special handling
			if key in ['command', 'class_name']:
				continue

			# overwrite the default config with the user's settings
			if key in config:
				config[key] = json_config[key]

		return config


	def __config_to_json(self, config):
		""" Constructs a JSON output structure for an existing Config """
		
		json_config = {}

		# copy all the keys except for the command and class name		
		for key in config:
			if key not in ['command', 'class_name']:
				json_config[key] = config[key]

		return OrderedDict([
			('sensor', config.command.name),
			('type',   config.class_name),
			('config', json_config)
		])
