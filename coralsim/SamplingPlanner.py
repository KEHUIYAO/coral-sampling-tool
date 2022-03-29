import shapely.geometry as sg
import numpy as np;  # NumPy package for arrays, random number generation, etc
from ToolKit import ToolKit


class SamplingPlanner:
    def __init__(self):
        self.toolkit_list = None

        # the final location of each toolkit
        self.placement = []

    def random_toolkit_placement(self, area, n_toolkits, length, width, line_intercept_ratio):
        """
        place n toolkits inside the area and make sure they do not overlap
        :param area: sg.Polygon, in which our toolkits are placed
        :param n_toolkits: number of toolkits
        :param lenght: length of each toolkit
        :param width: width of each toolkit
        :param line_intercept_ratio: line intercept width / toolkit width
        :return: a list, each element is a ToolKit object
        """
        count = 0
        toolkit_list = []
        minx, miny, maxx, maxy = area.bounds
        while count < n_toolkits:
            # generate a point that is almost inside the study area
            p = sg.Point(np.random.uniform(minx, maxx), np.random.uniform(miny, maxy))
            # test whethre the centroid of the toolkit is within the sampling region
            if area.contains(p):
                random_rotation = np.random.randint(0, 360)
                toolkit = ToolKit(length, width, line_intercept_ratio)
                toolkit.place(p.x, p.y, random_rotation)
                # test whether the sampling area contains the toolkit after rotation
                if area.contains(toolkit.sampling_region):
                    flag = True

                    for i in toolkit_list:
                        # the current toolkit should not intersect with other toolkits already placed in the sampling area
                        if i.sampling_region.intersects(toolkit.sampling_region):
                            flag = False
                            break

                    if flag:
                        toolkit_list.append(toolkit)
                        self.placement.append([p.x, p.y, random_rotation])
                        count += 1

        self.toolkit_list = toolkit_list

        return toolkit_list


    def manually_toolkit_placement(self,area, center_position_list, length, width, line_intercept_ratio):
        """
        manually place the toolkit by click and drag
        :param area: sg.Polygon, in which our toolkits are placed
        :param center_position_list: a two dimensional list, describes the centroid position of each toolkit
        :param lenght: length of each toolkit
        :param width: width of each toolkit
        :param line_intercept_ratio: line intercept width / toolkit width
        :return: a list, each element is a ToolKit object
        """
        ################## TODO ####################
        pass
        ############################################

    def plot_placed_toolkits(self, ax):
        "plot the placement of toolkits"
        for i in self.toolkit_list:
            i.plot(ax)

    def plot_placed_toolkits_with_plotly(self, fig):
        "plot the placement of toolkits in plotly"
        for i in self.toolkit_list:
            i.plot_with_plotly(fig)