
import json
from collections import OrderedDict


class Config():
    """ the configuration for a single readout or command """

    # this constructor is only for defining defaults
    def __init__(self,
                 _class_name     = None,
                 _min            = None,
                 _max            = None,
                 _redline        = None,
                 _buffer_size    = None):

        # ordered to make the JSON prettier
        self.data = OrderedDict([
            ("sensor",      ""          ),
            ("type",        _class_name ),
            ("title",       ""          ),
            ("x",           0           ),
            ("y",           0           ),
            ("w",           None        ), # default sizes are set by each widget's sizeHint()
            ("h",           None        ),
            ("min",         _min        ),
            ("max",         _max        ),
            ("redline",     _redline    ),
            ("buffer_size", _buffer_size),
        ])

        self.global_config = None


    def clone(self):
        c = Config()
        c.data = OrderedDict(self.data) # copy the data
        return c


    def __getitem__(self, key):
        if key in self.data:
            return self.data[key]
        elif key in self.global_config:
            return self.global_config[key]
        else:
            raise KeyError("'%s' is not a valid config key" % key)


    def __setitem__(self, key, value):
        if key in self.data:
            self.data[key] = value
        else:
            raise KeyError("'%s' is not a valid config key" % key)


    def __contains__(self, key):
        return key in self.data


    def __iter__(self):
        for key in self.data:
            yield key
