import dash_html_components as html
import numpy as np
import sys
sys.path.insert(1, '/Users/kehuiyao/Desktop/coral_sampling')
from Simulation import Simulation
import shapely.geometry as sg
from pyproj import Proj


# generate table
def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])


# estimate the rough density based on the sites in the selected region
def estimate_density_based_on_selected_sites(selected_data, data):
    if not selected_data:
        return 0



    points = selected_data['points']
    points_ind = [x['pointIndex'] for x in points]

    # if no points within range
    if not points:
        mapbox = selected_data['range']['mapbox']
        center = [(mapbox[0][0] + mapbox[1][0]) / 2, (mapbox[0][1] + mapbox[1][1]) / 2]

        # if the center is too far from historical sites, just return a default value
        if center[0] > max(data['Longitude']) or center[0] < min(data['Longitude']) or center[1] > max(data['Latitude']) or center[1] < min(data['Latitude']):
            return 0.03  # a default value


        # otherwise, use 10 nearest sites to estimate the prop cover
        x = data['Longitude']
        y = data['Latitude']
        res = {}
        for ind, pair in enumerate(zip(x,y)):
            res[ind] = (center[0] - pair[0])**2 + (center[1] - pair[1])**2

        print(res)
        # first 10 ind
        points_ind = [k for k,v in sorted(res.items(), key=lambda item: item[1])[:10]]

        print({k:v for k,v in sorted(res.items(), key=lambda item: item[1])[:10]})






    # calculate the total number of corals in all the selected coral sites
    total_corals = data['count'].iloc[points_ind].sum()

    # considering each coral site has the same area, calculate the rough density estimate of the coral
    single_site_area = 1600
    total_area = single_site_area * len(points_ind)
    prop_cover = total_corals / total_area
    return prop_cover


# generate simulation setting
def generate_setting(dropdown_select_process, prop_cover,
                     disease_prevalence, n_toolkits, fun_lambda, parent_prop,
                     parent_range, strauss_beta, strauss_gamma, strauss_R, selected_data,
                     toolkit_length,
                     toolkit_width,
                     line_intercept_ratio,
                     coral_size,
                     coral_size_sd
                     ):
    # specify some constants
    # coral_size=np.mean(np.array([109, 72, 42, 50])) / 100 ** 2
    # coral_size_sd=0.001
    # toolkit_length = 25
    # toolkit_width = 6
    #line_intercept_ratio = 1 / 6

    # project the lat and lon of the boundary of the selected region to meters
    if 'range' in selected_data.keys():
        temp = selected_data['range']['mapbox']
        data = []

        # Florida projection, record location
        p = Proj('epsg:2337', preserve_units=False)
        data.append(p(temp[0][0], temp[0][1]))
        data.append(p(temp[1][0], temp[1][1]))
        center = ((data[0][0] + data[1][0]) / 2, (data[1][0] + data[1][1]) / 2)
        left_down = (min(data[0][0], data[1][0]), min(data[0][1], data[1][1]))
        left_up = (min(data[0][0], data[1][0]), max(data[0][1], data[1][1]))
        right_down = (max(data[0][0], data[1][0]), min(data[0][1], data[1][1]))
        right_up = (max(data[0][0], data[1][0]), max(data[0][1], data[1][1]))
        boundary = [left_down, left_up, right_up, right_down]
        area = sg.Polygon(boundary)


    #     if area.area < 10000 or area.area > 40000:
    #
    #         # if the area is to small, raise error
    #         if area.area < 10000:
    #             print("The selected region is too small!")
    #             print("the square meters are the selected area is %d" % area.area)
    #             print("Automatically select a region containing your selected region")
    #
    #         else:
    #             print("The selected region is too large!")
    #             print("the square meters are the selected area is %d" % area.area)
    #             print("Automatically select a region within your selected region")
    #
    #         left_down = [(center[0] - 50), (center[1] - 50)]
    #         left_up = [(center[0] - 50), (center[1] + 50)]
    #         right_down = [(center[0] + 50), (center[1] - 50)]
    #         right_up = [(center[0] + 50), (center[1] + 50)]
    #         boundary = [left_down, left_up, right_up, right_down]
    #         area = sg.Polygon(boundary)
    #
    #
    #     #print("area bounds=", area.bounds)
    #
    #
    # else:
    #     # use a constant area
    #     area = sg.Polygon([(0, 0), (0, 100), (100, 100), (100, 0)])

    # core simulation function
    if dropdown_select_process == 1:
        # setting
        setting = Simulation(area, dropdown_select_process, disease_prevalence, coral_size, coral_size_sd, n_toolkits,
                             toolkit_length, toolkit_width, line_intercept_ratio, prop_cover)


    elif dropdown_select_process == 2:
        # deal with the input lambda_fun
        f = eval('lambda x,y: ' + fun_lambda)
        setting = Simulation(area, dropdown_select_process, disease_prevalence, coral_size, coral_size_sd, n_toolkits,
                             toolkit_length, toolkit_width, line_intercept_ratio, fun_lambda=f)

    elif dropdown_select_process == 3:
        setting = Simulation(area, dropdown_select_process, disease_prevalence, coral_size, coral_size_sd, n_toolkits,
                             toolkit_length, toolkit_width, line_intercept_ratio, prop_cover=prop_cover,
                             parent_prop=parent_prop,
                             parent_range=parent_range)

    elif dropdown_select_process == 4:
        setting = Simulation(area, dropdown_select_process, disease_prevalence, coral_size, coral_size_sd, n_toolkits,
                             toolkit_length, toolkit_width, line_intercept_ratio, strauss_beta=strauss_beta,
                             strauss_gamma=strauss_gamma, strauss_R=strauss_R)

    return setting, area, p

