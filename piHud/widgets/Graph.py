
from BaseWidget import BaseWidget


class Graph(BaseWidget):
    def __init__(self, parent, config):
        super(Graph, self).__init__(parent, config)

        # initialize an empty buffer 
        self.buffer = [0] * config.buffer_size


    def default_dimensions(self):
        """ override default size, called by superclass """
        super(Graph, self).setFixedWidth(400)
        super(Graph, self).setFixedHeight(300)


    def render(self, response):
        """ function called by python-OBD with new data to be rendered """
        pass


