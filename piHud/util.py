
from math import ceil, floor, log10


def scale(_min, _max):

    # handle inverse ranges
    if _max < _min:
        return scale(_max, _min)[::-1]

    # handle null ranges
    if _max == _min:
        return [ float(_min) ]

    # choose a smart scale step
    size = _max - _min

    step  = 10 ** floor(log10(size))
    ticks = int(size // step)

    # if there are less than 5 ticks, try the next power down.
    # if there are more than 10 ticks, try doubling the step.
    # ensures that there will be between 5-10 ticks in the result
    while (ticks + 2) <= 5:
        step /= 10
        ticks = int(size // step)

    while (ticks + 2) >= 11:
        step *= 2
        ticks = int(size // step)

    output = []
    start = _min

    # if the starting value is NOT perfectly divided by the scale step
    if bool(_min % step):

        # the first value will be the minimum
        output += [ float(_min) ]

        # compute the nearest interval of the scale step
        start = ceil(_min / step) * step


    output += [ (start + (step * x)) for x in range(ticks) ]
    output += [ float(_max) ]

    return output


def map_value(x, in_min, in_max, out_min, out_max):
    """ maps a value from one range to another """
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def map_scale(s, out_min, out_max):
    in_min = s[0]
    in_max = s[-1]
    return [map_value(x, in_min, in_max, out_min, out_max) for x in s]


def avg_power(s):
    return sum([1 if x == 0 else floor(log10(x)) for x in s]) / len(s)


def str_scale(s):
    divisor = 10 ** ceil(avg_power(s)) # ceil(): always tend towards fewer decimals
    return ([str(int(x/divisor)) for x in s], int(divisor))


# [10, 20, 30, 50]   --->   [0, 10, 10, 20]
def scale_offsets(s):
    return [0] + [(b-a) for a, b in zip(s, s[1:])]
