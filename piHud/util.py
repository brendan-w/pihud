
from math import ceil, floor, log10


def map_value(x, in_min, in_max, out_min, out_max):
    """ maps a value from one range to another """
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min



def scale(_min, _max):

    # handle inverse ranges
    if _max < _min:
        return scale(_max, _min)[::-1]

    # handle null ranges
    if _max == _min:
        return [ float(_min) ]

    # choose a smart scale step
    scale_len = _max - _min

    scale_step  = 10 ** floor(log10(scale_len))
    scale_ticks = int(scale_len // scale_step)

    # if there are less than 5 ticks, try the next power down.
    # if there are more than 10 ticks, try doubling the step.
    # ensures that there will be between 5-10 ticks in the result
    while (scale_ticks + 2) <= 5:
        scale_step /= 10
        scale_ticks = int(scale_len // scale_step)

    while (scale_ticks + 2) >= 11:
        scale_step *= 2
        scale_ticks = int(scale_len // scale_step)

    output = []
    start = _min

    # if the starting value is NOT perfectly divided by the scale step
    if bool(_min % scale_step):

        # the first value will be the minimum
        output += [ float(_min) ]

        # compute the nearest interval of the scale step
        start = ceil(_min / scale_step) * scale_step


    output += [ (start + (scale_step * x)) for x in range(scale_ticks) ]
    output += [ float(_max) ]

    return output
