
from BaseWidget import BaseWidget


class Gauge(BaseWidget):
    def __init__(self, parent, config):
        super(Gauge, self).__init__(parent, config)


    def default_dimensions(self):
        """ override default size, called by superclass """
        super(Gauge, self).setFixedWidth(360)
        super(Gauge, self).setFixedHeight(400)


    def render(self, response):
        """ function called by python-OBD with new data to be rendered """
        pass