
import os
import json
from widgets import widgets
from obd import commands as c


class PageConfig():
	""" class managing widget definitions on a single page """

	def __init__(self, config, page_json=None):
		self.config = config
		self.widget_configs = []

		# process each widget definition
		if page_json is not None:
			for w in page_json:
				self.__process_widget(w)


	def __process_widget(self, w):
		if not all(k in w for k in ['sensor', 'type', 'config']):
			print "Config is missing required keys"
			return

		sensor_name = w['sensor'].upper()
		class_name  = w['type'].lower().capitalize()

		if sensor_name not in c.__dict__:
			print "sensor '%s' is not a valid OBD command" % sensor_name
			return

		if class_name not in widgets:
			print "widget '%s' is not a valid Widget type" % class_name
			return

		command = c[sensor_name]

		# construct the default widget for this command
		widget_config = self.add_widget(command)

		# overwrite properties with the user's settings
		widget_config.from_JSON(w['config'], class_name)


	def add_widget(self, command):
		""" constructs a default widgetConfig for the given command """
		
		# try to clone the default config for this command
		if command in defaults:
			widget_config = defaults[command].clone()
		else:
			widget_config = WidgetConfig()

		widget_config.set_command(command)
		self.widget_configs.append(widget_config)
		return widget_config


	def delete_widget(self, widget_config):
		""" deletes a widgetConfig """
		self.widget_configs.remove(widget_config)


	def save(self):
		self.config.save()




class Config():
	""" class managing pages of widgets and the structure of the config file """
	def __init__(self, filename):
		self.filename = filename

		self.port = None
		self.page_adv_pin = 18
		self.demo = False
		self.pages = []

		# read the file
		if os.path.isfile(filename):
			with open(self.filename, 'r') as f:
				config = json.loads(f.read())


		# check for the required root keys
		if not all(k in config for k in ['pages']):
			print "Config is missing the 'pages' array"

		if 'port' in config:
			self.port = config['port']

		if 'page_adv_pin' in config:
			self.page_adv_pin = config['page_adv_pin']

		if 'demo' in config:
			self.demo = config['demo']

		# process each page definition
		for page_json in config['pages']:
			page = PageConfig(self, page_json)
			self.pages.append(page)


	def add_page(self):
		""" constructs a empty page """
		page = PageConfig(self)
		self.pages.append(page)
		return page


	def delete_page(self, page):
		""" deletes a widgetConfig """
		self.pages.remove(page)


	def save(self):
		""" write the config back to the file """
		
		output_pages = []

		for page in self.pages:
			output_page = []
			for w in page.widget_configs:
				output_page.append(w.to_JSON())
			output_pages.append(output_page)

		output = {
			"port": self.port,
			"page_adv_pin": self.page_adv_pin,
			"demo": self.demo,
			"pages": output_pages,
		}

		with open(self.filename, 'w') as f:
			f.write(json.dumps(output, indent=4))
