import shapely.geometry as sg
import matplotlib.pyplot as plt
import plotly.graph_objects as go


class Coral:
    def __init__(self, x, y, radius, health_condition):
        """
        Core coral object
        :param x: x coordinate of the coral
        :param y: y coordinate of the coral
        :param radius: the radius of the coral
        :param health_condition: 1 means the coral is infected, 0 means the coral is healthy
        """
        # location of the coral
        self.x = x
        self.y = y

        # some properties of the coral
        self.radius = radius
        self.health_condition = health_condition

    def create_circle_buffer(self):
        """
        create a circle with radius = radius, centered at (x,y)
        """
        return sg.Point(self.x, self.y).buffer(self.radius)

    def plot(self, ax):
        "plot a coral on the ax"
        num_color_mapping = {0: 'blue', 1: 'pink'}
        ax.add_artist(plt.Circle((self.x, self.y), self.radius, color=num_color_mapping[self.health_condition]))


    def plot_with_plotly(self, fig):
        "plot a coral on a fig with plotly"
        num_color_mapping = {0: 'blue', 1: 'pink'}
        fig.add_shape(type='circle', x0=self.x - self.radius, y0=self.y - self.radius, x1=self.x + self.radius, y1=self.y + self.radius,
                      fillcolor=num_color_mapping[self.health_condition])
