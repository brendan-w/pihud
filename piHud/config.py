
from widgets import *
from obd import commands as c


class Config():
	""" the configuration for a single readout """

	def __init__(self, type_=None, min_=None, max_=None, redline_=None):
		self.type    = type_
		self.min     = min_
		self.max     = max_
		self.redline = redline_

		# these defaults are set by the widget at runtime
		self.position = None
		self.dimensions = None


# dict of default configs where key=OBDCommand value=Config
defaults = {
	c.PIDS_A            : Config(),
	c.STATUS            : Config(),
	c.FREEZE_DTC        : Config(),
	c.FUEL_STATUS       : Config(),
	c.ENGINE_LOAD       : Config(),
	c.COOLANT_TEMP      : Config(),
	c.SHORT_FUEL_TRIM_1 : Config(),
	c.LONG_FUEL_TRIM_1  : Config(),
	c.SHORT_FUEL_TRIM_2 : Config(),
	c.LONG_FUEL_TRIM_2  : Config(),
	c.FUEL_PRESSURE     : Config(),
	c.INTAKE_PRESSURE   : Config(),
	c.RPM               : Config(Gauge, 0, 8000, 6750),
	c.SPEED             : Config(),
	c.TIMING_ADVANCE    : Config(),
	c.INTAKE_TEMP       : Config(),
	c.MAF               : Config(),
	c.THROTTLE_POS      : Config(),
	c.AIR_STATUS        : Config(),
	c.O2_SENSORS        : Config(),
	c.O2_B1S1           : Config(),
	c.O2_B1S2           : Config(),
	c.O2_B1S3           : Config(),
	c.O2_B1S4           : Config(),
	c.O2_B2S1           : Config(),
	c.O2_B2S2           : Config(),
	c.O2_B2S3           : Config(),
	c.O2_B2S4           : Config(),
	c.OBD_COMPLIANCE    : Config(),
	c.O2_SENSORS_ALT    : Config(),
	c.AUX_INPUT_STATUS  : Config(),
	c.RUN_TIME          : Config(),
}
