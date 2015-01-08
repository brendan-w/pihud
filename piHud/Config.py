

class Config():
	""" the configuration for a single readout or command """

	# constructor for defining defaults
	def __init__(self,
	             class_name_      = None,
	             min_             = None,
	             max_             = None,
	             redline_         = None,
	             color_           = None,
	             label_font_size_ = None,
	             title_font_size_ = None,
	             buffer_size_     = None):

		# user definable properties:
		self.command         = None
		self.title           = None
		self.class_name      = class_name_
		self.min             = min_
		self.max             = max_
		self.redline         = redline_
		self.color           = color_
		self.label_font_size = label_font_size_
		self.title_font_size = title_font_size_
		self.buffer_size     = buffer_size_
		# these defaults may be set by the widget at runtime:
		self.position        = None
		self.dimensions      = None

		# private properties
		self.__global_config   = None


	def set_global_config(self, config_file):
		self.__global_config = config_file


	def clone(self):
		clone = Config()
		# note: this clone is SHALLOW
		for key in self:
			clone[key] = self[key]
		return clone


	def save(self):
		self.__global_config.save();


	def delete(self):
		pass
		# self.__global_config.delete_config(self)


	def __getitem__(self, key):
		return getattr(self, key, None)


	def __setitem__(self, key, value):
		if key in self:
			setattr(self, key, value);


	def __contains__(self, key):
		""" tests whether the given key is a valid attribute of the config """

		if not isinstance(key, basestring):
			return False

		if len(key) <= 0:
			return False

		if len(key) >= 1 and key[0] == '_':
			return False

		if key not in dir(self):
			return False

		if hasattr(self[key], '__call__'):
			return False

		return True


	def __iter__(self):
		""" iterate over attribute names """
		for key in dir(self):
			if key in self: # skip keys that aren't config properties
				yield key
