import re
import shapely
import shapely.geometry as sg
import matplotlib
import plotly.graph_objects as go


class ToolKit:
    def __init__(self, length, width, line_intercept_ratio):
        self.sampling_region = None
        self.line_intercept = None
        self.sampling_region_width = width
        self.sampling_region_length = length
        self.line_intercept_width = line_intercept_ratio * width
        self.line_intercept_length = length
        self.line_intercept_ratio = line_intercept_ratio

    def place(self, center_location_x, center_location_y, degree_of_rotation):
        """
        place the ToolKit at a given location and rotate it with a given degree
        :param center_location_x: the x coordinate of the center of the polygon
        :param center_location_y: the y coordinate of the center of the polygon
        :param degree_of_rotation: rotate the polygon clockwise
        :return: None
        """

        # create the frame
        point1 = (
            center_location_x - 0.5 * self.sampling_region_length, center_location_y - 0.5 * self.sampling_region_width)
        point2 = (
            center_location_x - 0.5 * self.sampling_region_length, center_location_y + 0.5 * self.sampling_region_width)
        point3 = (
            center_location_x + 0.5 * self.sampling_region_length, center_location_y + 0.5 * self.sampling_region_width)
        point4 = (
            center_location_x + 0.5 * self.sampling_region_length, center_location_y - 0.5 * self.sampling_region_width)
        obj = sg.Polygon([point1, point2, point3, point4])

        # create the intercept
        point1 = (
            center_location_x - 0.5 * self.line_intercept_length, center_location_y - 0.5 * self.line_intercept_width)
        point2 = (
            center_location_x - 0.5 * self.line_intercept_length, center_location_y + 0.5 * self.line_intercept_width)
        point3 = (
            center_location_x + 0.5 * self.line_intercept_length, center_location_y + 0.5 * self.line_intercept_width)
        point4 = (
            center_location_x + 0.5 * self.line_intercept_length, center_location_y - 0.5 * self.line_intercept_width)
        inner_obj = sg.Polygon([point1, point2, point3, point4])

        # a line
        line = sg.LineString([(center_location_x - 0.5 * self.line_intercept_length, center_location_y),
                                                    (center_location_x + 0.5 * self.line_intercept_length, center_location_y)])

        # rotate the frame and the intercept
        self.sampling_region = shapely.affinity.rotate(obj, degree_of_rotation, 'center')
        self.line_intercept = shapely.affinity.rotate(inner_obj, degree_of_rotation, 'center')

        self.line = shapely.affinity.rotate(line, degree_of_rotation, 'center')



    def count_corals(self, coral_list):
        """
        count how many coral there are in the sampling region
        count how many infected corals are detected within the sampling_region
        count how many corals are detected using the line intercept and use this to estimate how many corals there are in the sampling region
        :param coral_list: a list, each element is a coral object
        :return: (total corals, total infected corals, corals counted using the line intercept, estimated total corals)
        """
        total_coral = 0
        total_infected_coral = 0
        total_line_intercept_coral = 0

        for i in coral_list:
            cur_coral = i.create_circle_buffer()
            if self.sampling_region.intersects(cur_coral):
                total_coral += 1
                if i.health_condition == 1:
                    total_infected_coral += 1

            if self.line_intercept.intersects(cur_coral):
                total_line_intercept_coral += 1

        estimated_total_coral = total_line_intercept_coral / self.line_intercept_ratio

        return (total_coral, total_infected_coral, total_line_intercept_coral, estimated_total_coral)

    def line_intercept_method(self, coral_list):
        "estimate the prop cover based on the line intercept method"
        total_length = 0
        for i in coral_list:
            cur_coral = i.create_circle_buffer()
            temp = cur_coral.intersection(self.line)
            total_length += temp.length

        return total_length / self.line_intercept_length









    def plot(self, ax):
        "plot the toolkit"
        patch_sampling_region = matplotlib.patches.Polygon(self.sampling_region.exterior.coords, color='yellow')
        patch_line_intercept = matplotlib.patches.Polygon(self.line_intercept.exterior.coords, color='blue')
        ax.add_patch(patch_sampling_region)
        ax.add_patch(patch_line_intercept)
        # ax.plot()

    def plot_with_plotly(self, fig):
        "plot the toolkit using plotly"
        # sampling region
        svg = self.sampling_region._repr_svg_()
        pattern = r'.*d="(.*)z.*'
        svg_for_plotly = re.search(pattern, svg).group(1)
        fig.add_shape(type='path', path=svg_for_plotly, fillcolor='LightPink', opacity=0.5)

        # intercept
        svg = self.line_intercept._repr_svg_()
        pattern = r'.*d="(.*)z.*'
        svg_for_plotly = re.search(pattern, svg).group(1)
        fig.add_shape(type='path', path=svg_for_plotly, fillcolor='PaleTurquoise', opacity=0.7)

