

from Config import Config
from obd import commands as c


#                         class_name  min  max  redline  color      label_size  title_size  buffer_size
__fallback_default__ = Config("Text",     0,   100, None,    "#53B9E8", 20,         20,         60)


# dict of default configs where key=OBDCommand value=Config
# all 'Nones's will be filled with values from the __fallback_default__
# user settings in the config will override these default values
__defaults__ = {

	# c.PIDS_A            : Config(),
	# c.STATUS            : Config(),
	# c.FREEZE_DTC        : Config(),
	#                            class_name  min   max     redline  color      label_size  title_size  buffer_size
	c.FUEL_STATUS       : Config("Text",     None, None,   None,    None,      50,         None,       None),
	c.ENGINE_LOAD       : Config("Bar_h",    0,    100,    90,      None,      None,       None,       None),
	c.COOLANT_TEMP      : Config("Bar_h",    -40,  215,    None,    None,      None,       None,       None),
	c.SHORT_FUEL_TRIM_1 : Config("Bar_h",    -100, 100,    None,    None,      None,       None,       None),
	c.LONG_FUEL_TRIM_1  : Config("Bar_h",    -100, 100,    None,    None,      None,       None,       None),
	c.SHORT_FUEL_TRIM_2 : Config("Bar_h",    -100, 100,    None,    None,      None,       None,       None),
	c.LONG_FUEL_TRIM_2  : Config("Bar_h",    -100, 100,    None,    None,      None,       None,       None),
	c.FUEL_PRESSURE     : Config("Bar_h",    0,    765,    None,    None,      None,       None,       None),
	c.INTAKE_PRESSURE   : Config("Bar_h",    0,    255,    None,    None,      None,       None,       None),
	c.RPM               : Config("Bar_h",    0,    8000,   6750,    None,      None,       None,       None),
	c.SPEED             : Config("Bar_h",    0,    180,    None,    None,      None,       None,       None),
	c.TIMING_ADVANCE    : Config("Bar_h",    -64,  64,     None,    None,      None,       None,       None),
	c.INTAKE_TEMP       : Config("Bar_h",    -40,  215,    None,    None,      None,       None,       None),
	c.MAF               : Config("Bar_h",    0,    655.35, None,    None,      None,       None,       None),
	c.THROTTLE_POS      : Config("Bar_h",    0,    100,    None,    None,      None,       None,       None),
	c.AIR_STATUS        : Config("Text",     None, None,   None,    None,      50,         None,       None),
	# c.O2_SENSORS        : Config(),
	c.O2_B1S1           : Config("Bar_h",    0,    1.275,  None,    None,      None,       None,       None),
	c.O2_B1S2           : Config("Bar_h",    0,    1.275,  None,    None,      None,       None,       None),
	c.O2_B1S3           : Config("Bar_h",    0,    1.275,  None,    None,      None,       None,       None),
	c.O2_B1S4           : Config("Bar_h",    0,    1.275,  None,    None,      None,       None,       None),
	c.O2_B2S1           : Config("Bar_h",    0,    1.275,  None,    None,      None,       None,       None),
	c.O2_B2S2           : Config("Bar_h",    0,    1.275,  None,    None,      None,       None,       None),
	c.O2_B2S3           : Config("Bar_h",    0,    1.275,  None,    None,      None,       None,       None),
	c.O2_B2S4           : Config("Bar_h",    0,    1.275,  None,    None,      None,       None,       None),
	c.OBD_COMPLIANCE    : Config("Text",     None, None,   None,    None,      50,         None,       None),
	# c.O2_SENSORS_ALT    : Config(),
	# c.AUX_INPUT_STATUS  : Config(),
	c.RUN_TIME          : Config("Text",     None, None,   None,    None,      50,         None,       None),
}


# replace all 'None's with values from the __fallback_default__
for command in __defaults__:
	config = __defaults__[command]

	for key in config:
		if config[key] is None:
			config[key] = __fallback_default__[key]


def new_config(self, command):
	""" function for constructing new config objects based on the desired command """
	if command in __defaults__:
		return __defaults__[command].clone()
	else:
		return __fallback_default__.clone()
