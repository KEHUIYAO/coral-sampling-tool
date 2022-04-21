from Simulation import Simulation
import shapely.geometry as sg
import numpy as np
from .utility import calculate_coverage_probability
from .utility import power_comparison_using_different_number_of_toolkits


# simulation setting's parameters that need to be specified
area = sg.Polygon([(0, 0), (0, 200), (200, 200), (200, 0)])
coral_size = np.mean(np.array([109,72,42,50])) / 100**2
coral_size_sd = 0.001
point_process_type = 3
disease_prevalence = 0.1
toolkit_length = 25
toolkit_width = 6
line_intercept_ratio = 1/6

prop_cover = 0.03
parent_prop = 0.1
parent_range = 5

#n_toolkit_candidate = [3,4,5,6,7,8,9,10]
#n_toolkit_candidate = [10,20]
n_toolkit_candidate = [1,3,5]
repeat = 10



mysim = Simulation(area,point_process_type,disease_prevalence,coral_size,coral_size_sd,n_toolkit_candidate[0],toolkit_length,toolkit_width,line_intercept_ratio,prop_cover = prop_cover, parent_prop = parent_prop, parent_range=parent_range)

power_comparison_using_different_number_of_toolkits(mysim,n_toolkit_candidate,repeat,write_to_csv=True)

