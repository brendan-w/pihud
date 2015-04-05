

from Config import Config
from obd import commands as c


#                         class_name  min  max  redline  scale_step  scale_mult  buffer_size
fallback_default = Config("Text",     0,   100, None,    None,       1,          60)



# dict of default configs where key=OBDCommand value=Config
# all 'Nones's will be filled with values from fallback_default
# user settings in the config file will override these default values
defaults = {

    # c.PIDS_A            : Config(),
    # c.STATUS            : Config(),
    # c.FREEZE_DTC        : Config(),
    #                            class_name           min   max     redline  scale_step  scale_mult  buffer_size
    c.FUEL_STATUS       : Config("Text",              None, None,   None,    None,       None,       None),
    c.ENGINE_LOAD       : Config("Bar_Horizontal",    0,    100,    90,      None,       None,       None),
    c.COOLANT_TEMP      : Config("Bar_Horizontal",    -40,  215,    None,    50,         None,       None),
    c.SHORT_FUEL_TRIM_1 : Config("Bar_Horizontal",    -100, 100,    None,    None,       None,       None),
    c.LONG_FUEL_TRIM_1  : Config("Bar_Horizontal",    -100, 100,    None,    None,       None,       None),
    c.SHORT_FUEL_TRIM_2 : Config("Bar_Horizontal",    -100, 100,    None,    None,       None,       None),
    c.LONG_FUEL_TRIM_2  : Config("Bar_Horizontal",    -100, 100,    None,    None,       None,       None),
    c.FUEL_PRESSURE     : Config("Bar_Horizontal",    0,    765,    None,    None,       None,       None),
    c.INTAKE_PRESSURE   : Config("Bar_Horizontal",    0,    255,    None,    None,       None,       None),
    c.RPM               : Config("Gauge",             0,    8000,   6750,    1000,       1000,       None),
    c.SPEED             : Config("Gauge",             0,    180,    120,     20,         1,          None),
    c.TIMING_ADVANCE    : Config("Bar_Horizontal",    -64,  64,     None,    None,       None,       None),
    c.INTAKE_TEMP       : Config("Bar_Horizontal",    -40,  215,    None,    None,       None,       None),
    c.MAF               : Config("Bar_Horizontal",    0,    655.35, None,    None,       None,       None),
    c.THROTTLE_POS      : Config("Bar_Horizontal",    0,    100,    None,    None,       None,       None),
    c.AIR_STATUS        : Config("Text",              None, None,   None,    None,       None,       None),
    # c.O2_SENSORS        : Config(),
    c.O2_B1S1           : Config("Bar_Horizontal",    0,    1.275,  None,    None,       None,       None),
    c.O2_B1S2           : Config("Bar_Horizontal",    0,    1.275,  None,    None,       None,       None),
    c.O2_B1S3           : Config("Bar_Horizontal",    0,    1.275,  None,    None,       None,       None),
    c.O2_B1S4           : Config("Bar_Horizontal",    0,    1.275,  None,    None,       None,       None),
    c.O2_B2S1           : Config("Bar_Horizontal",    0,    1.275,  None,    None,       None,       None),
    c.O2_B2S2           : Config("Bar_Horizontal",    0,    1.275,  None,    None,       None,       None),
    c.O2_B2S3           : Config("Bar_Horizontal",    0,    1.275,  None,    None,       None,       None),
    c.O2_B2S4           : Config("Bar_Horizontal",    0,    1.275,  None,    None,       None,       None),
    c.OBD_COMPLIANCE    : Config("Text",              None, None,   None,    None,       None,       None),
    # c.O2_SENSORS_ALT    : Config(),
    # c.AUX_INPUT_STATUS  : Config(),
    c.RUN_TIME          : Config("Text",              None, None,   None,    None,       None,       None),
}


# replace all 'None's with values from the fallback_default
for command in defaults:
    config = defaults[command]

    for key in config:
        if config[key] is None:
            config[key] = fallback_default[key]


# accessor for creating configs based on the defaults listed above
def default_for(command):

    if command in defaults:
        config = defaults[command].clone()
    else:
        config = fallback_default.clone()

    config["sensor"] = command.name
    config["title"]  = command.desc

    return config
