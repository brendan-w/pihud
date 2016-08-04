
from math import ceil, floor, log10


def scale(_min, _max, step=None):

    # handle inverse ranges
    if _max < _min:
        return scale(_max, _min)[::-1]

    # handle null ranges
    if _max == _min:
        return [ float(_min) ]

    size = _max - _min

    if step is None:
        # auto scale step

        step  = 10 ** floor(log10(size))
        ticks = int(size // step)

        # if there are less than 5 ticks, try the next power down.
        # if there are more than 10 ticks, try doubling the step.
        # ensures that there will be between 5-10 ticks in the result
        while (ticks + 2) <= 5:
            step /= 10
            ticks = int(size // step)

        # while (ticks + 2) >= 11:
        #     step *= 2
        #     ticks = int(size // step)

    else:
        # use the user-defined scale
        ticks = int(size // step)


    start = _min + step

    # if the starting value is NOT perfectly divided by the scale step
    if bool(_min % step):

        # compute the nearest interval of the scale step
        start = ceil(float(_min) / step) * step


    output  = [ float(_min) ]
    output += [ (start + (step * x)) for x in range(ticks) ]
    output += [ float(_max) ]

    # if the ends of the scale are two cramped (within a half step)
    # then ditch the 2nd and/or 2nd-to-last values
    if len(output) >= 4:
        diff = output[1] - output[0]
        if diff < (step / 2):
            output.pop(1)

        diff = output[-1] - output[-2]
        if diff < (step / 2):
            output.pop(-2)

    return output


def map_value(x, in_min, in_max, out_min, out_max):
    """ maps a value from one range to another """
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def map_scale(s, out_min, out_max):
    in_min = s[0]
    in_max = s[-1]
    return [map_value(x, in_min, in_max, out_min, out_max) for x in s]


def avg_power(s):
    return sum([1 if x == 0 else floor(log10(abs(x))) for x in s]) / len(s)


def str_scale(s, multiplier=None):
    if multiplier is None:
        multiplier = 10 ** floor(avg_power(s))
    return ([str(int(x/multiplier)) for x in s], int(multiplier))


# [10, 20, 30, 50]   --->   [0, 10, 10, 20]
def scale_offsets(s):
    return [0] + [(b-a) for a, b in zip(s, s[1:])]

# tests that value is in range (a, b)
#                    NOTE: not [a, b]
def in_range(v, _min, _max):
    return ((_min < v) and (v < _max))
