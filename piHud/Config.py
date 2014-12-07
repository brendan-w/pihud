
import json
import widgets
from obd import commands as c



class WidgetConfig():
	""" the configuration for a single readout or command """

	def __init__(self, class_name="Gauge", min_=0, max_=100, redline_=None):

		self.command    = None
		self.class_name = class_name

		# user definable in 'config' dict
		self.title   = "No title specified"
		self.min     = min_
		self.max     = max_
		self.redline = redline_
		self.color   = "#53B9E8"
		self.label_font_size = 25
		self.title_font_size = 25

		# these defaults are set by the widget at runtime
		self.position = None
		self.dimensions = None


	def clone(self):
		clone = WidgetConfig()
		for key in self.__dict__:
			clone.__dict__[key] = self.__dict__[key]
		return clone


	def set_command(self, command):
		self.command = command
		self.title = command.name


	def from_JSON(self, config_props, class_name):

		for key in config_props:
			if self.__dict__.has_key(key):
				self.__dict__[key] = config_props[key]

		self.class_name = class_name


	def to_JSON(self):

		# copy all the keys except for the command and class name
		props = self.__dict__.keys()
		props.remove('command')
		props.remove('class_name')

		config = {}
		for key in props:
			config[key] = self.__dict__[key]

		return {
			"sensor": self.command.name,
			"type": self.class_name,
			"config": config
		}



# dict of default configs where key=OBDCommand value=Config
# user settings in the config will override these default values
defaults = {
	c.PIDS_A            : WidgetConfig(),
	c.STATUS            : WidgetConfig(),
	c.FREEZE_DTC        : WidgetConfig(),
	c.FUEL_STATUS       : WidgetConfig(),
	c.ENGINE_LOAD       : WidgetConfig("Gauge", 0, 100, 90),
	c.COOLANT_TEMP      : WidgetConfig(),
	c.SHORT_FUEL_TRIM_1 : WidgetConfig(),
	c.LONG_FUEL_TRIM_1  : WidgetConfig(),
	c.SHORT_FUEL_TRIM_2 : WidgetConfig(),
	c.LONG_FUEL_TRIM_2  : WidgetConfig(),
	c.FUEL_PRESSURE     : WidgetConfig(),
	c.INTAKE_PRESSURE   : WidgetConfig(),
	c.RPM               : WidgetConfig("Gauge", 0, 8000, 6750),
	c.SPEED             : WidgetConfig("Gauge", 0, 180),
	c.TIMING_ADVANCE    : WidgetConfig(),
	c.INTAKE_TEMP       : WidgetConfig(),
	c.MAF               : WidgetConfig(),
	c.THROTTLE_POS      : WidgetConfig("Bar", 0, 100),
	c.AIR_STATUS        : WidgetConfig(),
	c.O2_SENSORS        : WidgetConfig(),
	c.O2_B1S1           : WidgetConfig(),
	c.O2_B1S2           : WidgetConfig(),
	c.O2_B1S3           : WidgetConfig(),
	c.O2_B1S4           : WidgetConfig(),
	c.O2_B2S1           : WidgetConfig(),
	c.O2_B2S2           : WidgetConfig(),
	c.O2_B2S3           : WidgetConfig(),
	c.O2_B2S4           : WidgetConfig(),
	c.OBD_COMPLIANCE    : WidgetConfig(),
	c.O2_SENSORS_ALT    : WidgetConfig(),
	c.AUX_INPUT_STATUS  : WidgetConfig(),
	c.RUN_TIME          : WidgetConfig(),
}



class Config():
	""" class managing widget definitions and the structure of the config file """
	def __init__(self, filename):
		self.filename = filename
		self.load()


	def load(self):
		self.port = None
		self.widget_configs = []

		# read the file
		config = {}
		with open(self.filename, 'r') as f:
			config = json.loads(f.read())

		# check for the required root keys
		if not all(k in config for k in ['widgets']):
			print "Config is missing the 'widgets' array"

		# process each widget definition
		for w in config['widgets']:

			if not all(k in w for k in ['sensor', 'type', 'config']):
				print "Config is missing required keys"
				continue

			sensor_name = w['sensor'].upper()
			class_name  = w['type'].lower().capitalize()

			if sensor_name not in c.__dict__:
				print "sensor '%s' is not a valid OBD command" % sensor_name
				continue

			if class_name not in widgets.__dict__:
				print "widget '%s' is not a valid Widget type" % class_name
				continue

			command = c[sensor_name]

			# construct the default widget for this command
			widget_config = self.add_widget(command)

			# overwrite properties with the user's settings
			widget_config.from_JSON(w['config'], class_name)


	def add_widget(self, command):
		""" constructs a default widgetConfig for the given command """
		# clone the default config for this command
		widget_config = defaults[command].clone()
		widget_config.set_command(command)
		self.widget_configs.append(widget_config)
		return widget_config


	def delete_widget(self, widget_config):
		""" deletes a widgetConfig """
		self.widget_configs.remove(widget_config)


	def save(self):
		output = {
			"port": self.port,
			"widgets": [],
		}
		
		for w in self.widget_configs:
			output['widgets'].append(w.to_JSON())

		with open(self.filename, 'w') as f:
			f.write(json.dumps(output, indent=4))
