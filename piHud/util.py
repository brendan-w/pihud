
def map_value(x, in_min, in_max, out_min, out_max):
	""" maps a value from one range to another """
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

