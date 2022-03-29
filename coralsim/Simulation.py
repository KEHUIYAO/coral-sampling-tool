import re
import shapely.geometry as sg
import matplotlib
matplotlib.use('Agg')
import plotly.graph_objects as go
import numpy as np;  # NumPy package for arrays, random number generation, etc
import matplotlib.pyplot as plt  # For plotting
from CoralGenerator import CoralGenerator
from SamplingPlanner import SamplingPlanner


class Simulation:
    def __init__(self, area, point_process_type, disease_prevalence, coral_size, coral_size_sd, n_toolkits,
                 length, width, line_intercept_ratio, prop_cover=None, fun_lambda=None, parent_prop=None,
                 parent_range=None, strauss_beta=None, strauss_gamma=None, strauss_R=None):

        self.area = area
        self.disease_prevalence = disease_prevalence
        self.n_toolkits = n_toolkits
        self.line_intercept_ratio = line_intercept_ratio
        self.point_process_type = point_process_type
        self.coral_size = coral_size
        self.coral_size_sd = coral_size_sd
        self.prop_cover = prop_cover
        self.fun_lambda = fun_lambda
        self.parent_prop = parent_prop
        self.parent_range = parent_range
        self.length = length
        self.width = width
        self.line_intercept_ratio = line_intercept_ratio
        self.strauss_beta = strauss_beta
        self.strauss_gamma = strauss_gamma
        self.strauss_R = strauss_R

        self.sampling_planner = None

    def change_toolkit_number(self, n):
        """
        change the exsiting number of toolkits n in this setting
        """
        self.n_toolkits = n

    def simulate(self):
        """
        simulate coral in the whole region first and place the toolkits
        """
        n_toolkits = self.n_toolkits
        length = self.length
        width = self.width
        line_intercept_ratio = self.line_intercept_ratio
        point_process_type = self.point_process_type
        disease_prevalence = self.disease_prevalence
        coral_generator = CoralGenerator(area)
        coral_size = self.coral_size
        coral_size_sd = self.coral_size_sd
        prop_cover = self.prop_cover
        fun_lambda = self.fun_lambda
        parent_prop = self.parent_prop
        parent_range = self.parent_range
        strauss_beta = self.strauss_beta
        strauss_gamma = self.strauss_gamma
        strauss_R = self.strauss_R

        #  set the type of point process, optional choices are 1.homogeneous poisson process, 2.inhomogeneous poisson process
        if point_process_type == 1:
            coral_generator.generate_coral_from_homogeneous_poisson_process(disease_prevalence, coral_size,
                                                                     coral_size_sd, prop_cover)
        elif point_process_type == 2:
            coral_generator.generate_coral_from_inhomogeneous_poisson_process(disease_prevalence, coral_size,

                                                                              coral_size_sd, fun_lambda)
        elif point_process_type == 3:
            coral_generator.generate_coral_from_poisson_cluster_process(disease_prevalence, coral_size,
                                                                        coral_size_sd, prop_cover, parent_prop,
                                                                        parent_range)
        elif point_process_type == 4:
            coral_generator.generate_coral_from_strauss_process(disease_prevalence, coral_size, coral_size_sd,
                                                                strauss_beta, strauss_gamma, strauss_R)


        self.coral_list = coral_generator.corals
        self.sampling_planner = SamplingPlanner()
        self.sampling_planner.random_toolkit_placement(area, n_toolkits, length, width, line_intercept_ratio)

    def efficient_simulate(self):
        """
        place the toolkits first and simulate coral inside the toolkits
        """
        area = self.area
        n_toolkits = self.n_toolkits
        length = self.length
        width = self.width
        line_intercept_ratio = self.line_intercept_ratio
        point_process_type = self.point_process_type
        disease_prevalence = self.disease_prevalence
        coral_size = self.coral_size
        coral_size_sd = self.coral_size_sd
        prop_cover = self.prop_cover
        fun_lambda = self.fun_lambda
        parent_prop = self.parent_prop
        parent_range = self.parent_range
        strauss_beta = self.strauss_beta
        strauss_gamma = self.strauss_gamma
        strauss_R = self.strauss_R

        self.sampling_planner = SamplingPlanner()
        self.sampling_planner.random_toolkit_placement(area, n_toolkits, length, width, line_intercept_ratio)
        self.coral_list = []
        for toolkit in self.sampling_planner.toolkit_list:
            cur_region = toolkit.sampling_region
            coral_generator = CoralGenerator(cur_region)
            if point_process_type == 1:
                coral_generator.generate_coral_from_homogeneous_poisson_process(disease_prevalence, coral_size,
                                                                                coral_size_sd, prop_cover)
            elif point_process_type == 2:
                coral_generator.generate_coral_from_inhomogeneous_poisson_process(disease_prevalence, coral_size,
                                                                                  coral_size_sd, fun_lambda)
            elif point_process_type == 3:
                coral_generator.generate_coral_from_poisson_cluster_process(disease_prevalence, coral_size,
                                                                            coral_size_sd, prop_cover, parent_prop,
                                                                            parent_range)
            elif point_process_type == 4:
                coral_generator.generate_coral_from_strauss_process(disease_prevalence, coral_size, coral_size_sd,
                                                                    strauss_beta, strauss_gamma, strauss_R)
            self.coral_list = self.coral_list + coral_generator.corals

    def plot(self, dpi=None, *args, **kwargs):
        """
        plot the simulation with a given aspect ratio
        """
        if dpi:
            plt.rcParams['figure.dpi'] = dpi  # 分辨率


        fig, ax = plt.subplots(figsize = (3,2))
        polygon_area = matplotlib.patches.Polygon(self.area.exterior.coords, color='k', *args, **kwargs)
        ax.add_patch(polygon_area)
        num_color_mapping = {0: 'g', 1: 'r'}

        for i in self.coral_list:
            i.plot(ax)

        self.sampling_planner.plot_placed_toolkits(ax)
        ax.plot()
        plt.show()
        return fig

    def plot_with_plotly(self, dpi=None, *args, **kwargs):
        """
        plot the simulation using plotly
        """
        ############### TODO ##############
        fig = go.Figure()
        # add boarder
        svg = self.area._repr_svg_()
        pattern = r'.*d="(.*)z.*'
        svg_for_plotly = re.search(pattern, svg).group(1)
        fig.add_shape(type='path', path=svg_for_plotly)
        fig.update_xaxes(range=[self.area.bounds[0], self.area.bounds[2]])
        fig.update_yaxes(range=[self.area.bounds[1], self.area.bounds[3]])
        # # add corals, this is slow
        # for i in self.coral_list:
        #     i.plot_with_plotly(fig)

        # add corals in an efficient way
        print(len(self.coral_list))
        x = [i.x for i in self.coral_list]
        y = [i.y for i in self.coral_list]
        radius = [i.radius for i in self.coral_list]
        # x0 = [x[i]-radius[i] for i in range(len(x))]
        # y0 = [y[i]-radius[i] for i in range(len(x))]
        # x1 = [x[i]+radius[i] for i in range(len(x))]
        # y1 = [y[i]+radius[i] for i in range(len(x))]
        num_color_mapping = {0: 'blue', 1: 'pink'}
        condition = [num_color_mapping[i.health_condition] for i in self.coral_list]
        fig.add_trace(go.Scatter(x=x, y=y, mode='markers', marker=dict(color=condition, opacity=0.5)))
        # for i in range(len(x)):
        #     fig.add_shape(type='circle', x0=x0[i], y0=y0[i], x1=x1[i], y1=y1[i], fillcolor=condition[i], opacity=0.5)

        # add toolkits
        self.sampling_planner.plot_placed_toolkits_with_plotly(fig)
        # fig.show()
        return fig


        ###################################

    def estimate_prevalence(self):
        """
        estimate the prevalence, together with the std and CI
        """
        coral_list = self.coral_list
        total_coral = 0
        total_infected_coral = 0
        total_line_intercept_coral = 0
        total_estimated_coral = 0

        for i in self.sampling_planner.toolkit_list:
            a, b, c, d = i.count_corals(coral_list)
            total_coral += a
            total_infected_coral += b
            total_line_intercept_coral += c
            total_estimated_coral += d

        average_total_coral = total_coral / self.n_toolkits
        average_total_infected_coral = total_infected_coral / self.n_toolkits
        average_total_line_intercept_coral = total_line_intercept_coral / self.n_toolkits
        average_total_estimated_coral = total_estimated_coral / self.n_toolkits

        if average_total_estimated_coral == 0:
            print("The prevalence cannot be estimated")
            return 0, 0, (0, 0)

        prevalence = average_total_infected_coral / average_total_estimated_coral
        # define some notations for variance calculation
        x = average_total_infected_coral
        n = average_total_line_intercept_coral
        N = average_total_estimated_coral
        q = self.line_intercept_ratio
        p = x / N
        # calculate the standard error based on CLT, delta's method and Goodman's (1960) formula
        var_prevalence = (p * (1 - p) + p ** 2 * (1 - q) / q ** 2) / (n / q) / self.n_toolkits
        sd_prevalence = np.sqrt(var_prevalence)
        ci_lower = max(prevalence - 1.96 * sd_prevalence, 0)
        ci_upper = prevalence + 1.96 * sd_prevalence
        print(
            "The estimated prevalence is %.4f,the standard deviation of this estimator is %.4f, the confidence interval is (%.2f, %.2f)." % (
                prevalence, sd_prevalence, ci_lower, ci_upper))

        return prevalence, sd_prevalence, (ci_lower, ci_upper)

    def n_corals(self):
        """
        calculate the total number of corals in this simulation
        """
        print("The total number of corals we sampled are %d" % len(self.coral_list))
        return len(self.coral_list)

    def cover_true_disease_prevalence(self):
        """
        return True if the prevalence CI covers the true disease prevalence rate
        """
        _, _, ci = self.estimate_prevalence()
        if ci[0] <= self.disease_prevalence and ci[1] >= self.disease_prevalence:
            # print("cover")
            return True
        else:
            # print("do not cover")
            return False
    def cover_true_prop_cover(self):
        "return True if the prop cover CI covers the true prop cover"
        _, _, ci = self.estimate_prop_cover()
        if ci[0] <= self.prop_cover and ci[1] >= self.prop_cover:
            # print("cover")
            return True
        else:
            # print("do not cover")
            return False

    def estimate_prop_cover(self):
        """
        use bootstrap method, consider each transect as an independent sample
        """

        prop_cover_list = []

        for toolkit in self.sampling_planner.toolkit_list:
            prop_cover_list.append(toolkit.line_intercept_method(self.coral_list))


        prop_cover_mean = np.mean(prop_cover_list)
        prop_cover_sd = np.std(prop_cover_list)

        # lower bound is 0
        ci_lower = max(0, prop_cover_mean - 1.96 * prop_cover_sd)
        ci_upper = prop_cover_mean + 1.96 * prop_cover_sd
        return prop_cover_mean, prop_cover_sd, (ci_lower, ci_upper)



if __name__ == "__main__":
    area = sg.Polygon([(0, 0), (0, 100), (100, 100), (100, 0)])
    # area = sg.Polygon([(-1,-1),(-1,1),(1,1),(1,-1)])
    # coral_generator = CoralGenerator(area)
    # # use homogeneous poisson process, prop_cover = 0.03, prevalence = 0.1, coral_size = 1, sd = 0.5
    # generated_corals = coral_generator.generate_coral_from_homogeneous_poisson(0.03,0.1,1,0.5)
    # print(generated_corals)
    #
    # kit = ToolKit(20,20,0.2)
    # kit.place(50,50,90)
    #
    # print(kit.count_corals(generated_corals))
    #
    #
    # sampling_planner = SamplingPlanner()
    # sampling_planner.random_toolkit_placement(area,10,10,10,0.2)
    #
    # fig,ax = plt.subplots()
    # coral_generator.plot(ax)
    # #kit.plot(ax,alpha = 0.1)
    #
    # sampling_planner.plot_placed_toolkits(ax)
    #
    # plt.show()

    # setting 1
    setting1 = Simulation(area, 1, 0.1, 0.5, 0.1, 4, 25, 6, 0.2, prop_cover=0.03)
    # setting1.simulate()
    setting1.efficient_simulate()

    #print(setting1.estimate_prop_cover())

    temp = setting1.plot(dpi=200, alpha=0.1)
    temp.savefig('temp')
    #setting1.plot_with_plotly()
    #setting1.estimate_prevalence()
    #setting1.n_corals()

    # # setting 2
    # def fun_lambda(x, y):
    #     return 0.1 * np.exp(-(((x - 50) / 50) ** 2 + ((y - 50) / 50) ** 2) / 0.5 ** 2);  # intensity function
    #
    # setting2 = Simulation(area, 2, 0.1, 0.5, 0.1, 3, 20, 20, 0.2, fun_lambda=fun_lambda)
    # #setting2.simulate()
    # setting2.efficient_simulate()
    # setting2.plot(alpha = 0.1)
    # setting2.estimate_prevalence()
    # setting2.n_corals()

    # # setting 3
    # setting3 = Simulation(area,3,0.1,0.5,0.1,5,20,20,0.2,prop_cover= 0.03,parent_prop=0.1,parent_range=5)
    # setting3.efficient_simulate()
    # setting3.plot(alpha = 0.1)

    # # setting 4
    # # hard core process
    # setting4 = Simulation(area, 4, 0.1, 0.5, 0.1, 5, 20, 6, 0.2,strauss_beta=2,strauss_gamma=0,strauss_R=0.7)
    # setting4.efficient_simulate()
    # setting4.plot(alpha=0.1)
