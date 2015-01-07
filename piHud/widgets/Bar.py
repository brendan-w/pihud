
from BaseWidget import BaseWidget


class Bar_v(BaseWidget):
    def __init__(self, parent, config):
        super(Bar_v, self).__init__(parent, config)


    def default_dimensions(self):
        """ override default size, called by superclass """
        super(Bar_v, self).setFixedWidth(180)
        super(Bar_v, self).setFixedHeight(400)


    def render(self, response):
        """ function called by python-OBD with new data to be rendered """
        pass



class Bar_h(BaseWidget):
    def __init__(self, parent, config):
        super(Bar_h, self).__init__(parent, config)


    def default_dimensions(self):
        """ override default size, called by superclass """
        super(Bar_h, self).setFixedWidth(400)
        super(Bar_h, self).setFixedHeight(100)


    def render(self, response):
        """ function called by python-OBD with new data to be rendered """
        pass