

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
		for key in self.__dict__:
			clone.__dict__[key] = self.__dict__[key]
		return clone
