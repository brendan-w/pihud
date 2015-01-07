

class Config():
	""" the configuration for a single readout or command """

	def __init__(self,
	             class_name_,
	             min_,
	             max_,
	             redline_,
	             color_,
	             label_font_size_,
	             title_font_size_,
	             buffer_size_):

		# specially handled by ConfigStore
		self.command    = None
		self.class_name = class_name_
		self.title      = "No title specified"

		# user definable properties
		self.min             = min_
		self.max             = max_
		self.redline         = redline_
		self.color           = color_
		self.label_font_size = label_font_size_
		self.title_font_size = title_font_size_
		self.buffer_size     = buffer_size_

		# these defaults are set by the widget at runtime
		self.position = None
		self.dimensions = None


	def clone(self):
		clone = Config()
		# note: this clone is SHALLOW
		for key in self:
			clone[key] = self[key]
		return clone


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

		if len(key) >= 2 and key[-2:] == '__':
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
