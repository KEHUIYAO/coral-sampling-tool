import dash_core_components as dcc
import dash_html_components as html
import base64

def add_static_image(image_filename, height_ratio='50%', width_ratio='50%'):
    encoded_image = base64.b64encode(open(image_filename, 'rb').read())
    return html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), style={'height': height_ratio, 'width': width_ratio})

def generate_introduction_tab():
    return html.Div([html.Br(),
                     generate_introduction(),
                     #html.Img(src='https://i.imgur.com/eZLreAj.jpg')
                     add_static_image('assets/transect_line.jpeg', height_ratio='20%', width_ratio='20%'),
                     add_static_image('assets/transect_visualization.png', '27%', '27%'),
                     generate_basic_usage()

                     ])

# def generate_introduction():
#     "return a Div containing the introduction of the app"
#     # introduction text
#     return  dcc.Markdown('''
#
# #### Introduction
# This is an interactive simulation tool that helps with coral sampling. There are two purposes of this tool: 1. Assess the power using line intercept method to estimate the proportion cover of corals within a region. 2. Assess the level of effort required to estimate the prevalence of lesions on corals with a desired precision.  The tool let the users simulate corals following customizable spatial point process in a selected region on the map, then let them decide how many resources should be assigned by using some coral disease survey methods to estimate the parameters of interest such as coral proportion cover and coral disease prevalence.
#
# The main workflow of the tool is: 1. Select a region where your survey is conducted. 2. Specify how the corals are distributed in the region. 3. Determine how many resources should be put to conduct the survey. 4. Obtain the estimation power and accuracy and sampling plans.
#
# Next, we briefly describe the coral survey methods used in the tool.
#
# ** Line intercept method **
#
# Line intercept method is mainly used to estimate the proportion cover of the corals. This method requires a diver to lay out a 10-25 m line. At intervals, substrate is characterized as 'coral', 'sand', 'algae', 'rubble'. For Point intercept, substrate is recorded at each 10 cm interval. For the Line intercept, substrate is recorded at length intervals (e.g. 0-5 cm-'coral'; 5-13 cm-'Sand', 13-28 cm-'coral', etc.). Point intercepts are faster to do than line, (important consideration when air is limiting).
#
# ** Disease prevalence estimation using an extended plot **
#
# To estimate the disease prevalence,  the survey design first involves conducting coral colony counts along a transect of length 25 m and width 1 m. Then the 1 x 25 m transect is extended an additional 5 m in width and become a 6 x 25 m plot and all the corals with disease(lesions) are enumerated in the plot. The prevalence of disease is then estimated as the number of diseased corals / 6 x the number of counted corals in the transect.
#
# Threre are two figures below. The left one shows how the diver count the coral colonies; For the right figure, the pink region of the right figure is the 6 x 25 m study plot. the blue line inside the region is the 1 x 25m transect, and these dots are corals. In the survey, we count all the corals within the 1 x 25 m transect, and count all the diseased corals (leisons) in the 6 x 25 m plot.
#
#
# ''',
#                      className='col-sm-12')
#                      # style={'height': '400px',
#                      #        'overflow': 'scroll'})

def generate_brief_introduction_tab():
    return html.Div([html.Br(),
                     generate_brief_introduction_1(),
                     add_static_image('assets/transect_line.jpeg', height_ratio='20%', width_ratio='20%'),
                     add_static_image('assets/transect_visualization.png', '27%', '27%'),
                     generate_brief_introduction_2(),
                     add_static_image('assets/point_process.jpg'),
                     generate_brief_introduction_3()
                     ])


def generate_brief_introduction_1():
    return dcc.Markdown('''
#### Overview

This tool let the users simulate corals on a landscape to characterize coral distribution in a selected region on the map. Based on this distribution, it then guides you on how many transects should be assigned during a survey to estimate percent coral cover and disease prevalence.  The use of this tool is predicated on the following survey method:

** Percent Coral cover: **

This is estimated using line intercept (e.g. substrate categorized at length intervals such as 0-5 cm-'coral'; 5-13 cm-'Sand', 13-28 cm-'coral', etc.).

** Coral composition: **

A 25 m line is deployed and coral colonies categorized as to genus (or species) and size class (1-5cm, 6-10cm, 11-20cm, 21-40cm, 41-80cm, 81-160, > 160 cm).

** Disease prevalence: **

A 6 m band (3 m to each side of the line) is surveyed and corals with lesions unmerated (genus or species and size class as above).  Prevalence of disease is estimated as No, lesioned corals divided by extrapolated of colony count from 1 m band to 25 X 6 m area.
    
    
    ''')

def generate_brief_introduction_2():
    return dcc.Markdown('''

The tool will ask you to enter an estimate of the following parameters for a given survey site:

1)	Your estimate of the distribution pattern of corals is on a site.

    ''')

def generate_brief_introduction_3():
    return dcc.Markdown('''
2)	A rough estimate of coral cover (eyeballing the habitat) (0-20%, 21-40%, 41-60%, 61-80%, >80%)

3)	A rough estimate of prevalence of disease (eyeballing the habitat) (<1%, 2-5%, 6-10%, 11-20%, 21-40%, >40%)

4)	Number and orientation of transects to survey

5)	If data exists for a particular site (or if you wish to upload data for a site), you can opt to do so and entries 1-3 will be automatically filled in. 

Based on those entries, the program will spit out the proportion of the confidence interval of your estimates of coral cover and disease prevalence that covers the true parameters.

    ''')

def generate_introduction():
    "return a Div containing the introduction of the app"
    # introduction text
    return  dcc.Markdown(''' 
#### Overview

This is an interactive simulation tool to inform design of surveys for estimating density and diseases of coral reefs. Specifically, this tool: 1) Estimates the proportion cover of corals and associated precision using line intercept method within a region. 2) Assess the level of effort required to estimate the prevalence of lesions on corals with a desired precision. 3) Calculates the power of a given survey design using the coverage probability of confidence intervals (i.e., the probability the true simulation value fell within the confidence interval bounds) of the estimated cover proportion or prevalence.  
To achieve this functionality, the tool let the users simulate corals on a landscape following customizable spatial point process to characterize coral distribution in a selected region on the map. It then  allows them to decide how many transects should be assigned during a survey to estimate coral proportion cover and coral disease prevalence.

#### Workflow

The main workflow of the tool is: 1) Select a region where your survey is conducted. 2) Specify how the corals are distributed in the region. 3) Determine how many transect should be used during a survey. 4. Obtain the estimated power and accuracy and sampling plans. There are three tabs under the title: Introduction, Map corals and Simulation. The Introduction panel describes the goal of this sampling tool and what functionalities it provides. The Point Process Introduction focuses on different spatial point processes, under which the coral can be generated in a 2D space. This can be used to create coral distributions of interest. The Simulation tab contains the user-interface for controlling the coral simulation, survey design and calculating the power of the survey. 

#### Survey Methods   
** Line intercept method **
    
Intercept methods are used to estimate the proportion cover of coral within a region of interest. These methods require a diver to lay out a transect (e.g., 10–25 m long), and along the transect characterize substrate as 'coral', 'sand', 'algae', 'rubble', etc. For the Line intercept, substrate is recorded at length intervals (e.g. 0-5 cm-'coral'; 5-13 cm-'Sand', 13-28 cm-'coral', etc.).
    
** Disease prevalence estimation using an extended plot **

To estimate the disease prevalence, the survey design first involves conducting coral colony counts along a transect of length 25 m and width 1 m. Then the 1 m x 25 m transect is extended an additional 5 m in width and becomes a 6 m x 25 m plot and all the corals with signs of disease are enumerated in the plot. The prevalence of disease is then estimated as the number of diseased corals / 6 x the number of counted corals in the transect.
The figures below demonstrate survey methods. The left one shows how diver count the coral colonies.  The right figure depicts in the pink region the 6 m x 25 m study plot. The blue line inside the region is the 1m x 25m transect, and the dots represent individual coral colonies, and different colors represent whether the coral is healthy or diseased. 

''',
                         className='col-sm-12')
    # style={'height': '400px',
    #        'overflow': 'scroll'})

# def generate_basic_usage():
#     return dcc.Markdown('''
# #### How to use?
# There are three tabs under the title: Introduction, Point Process Introduction and Simulation. The **Introduction** panel basically introduces the goal of this sampling tool and what functionalities it provides. The **Point Process Introduction** focuses on different spatial point processes, under which the coral can be generated in a 2D space. The **Simulation** tab contains the user-interface for controlling the coral simulation and resource allocation. More detailed information are described after you entered the tab.
#
#     ''')

def generate_basic_usage():
    return dcc.Markdown('''
#### Coral distribution
                
** Homogeneous poisson process **              
A homogeneous poisson process, with intensity lambda, is the basic 'reference' or 'benchmark' model of a point process to generate a distribution of coral colonies on the landscape.  It is sometimes called complete spatial randomness (CSR). Its basic properties are: 1) the number of coral colonies falling in any region A has a Poisson distribution with mean = lambda x area(A); 2) given that there are n colonies inside region A, the locations of these colonies are independent and uniformly distributed inside A; and 3) the contents of two disjoint regions A and B are independent.
                
** Inhomogeneous poisson process **

In general, the intensity of an inhomogeneous Poisson process will vary based on local conditions, so the expected number of coral colonies falling within a small region of area depends on the intensity rate at that region, which is characterized by a spatially varying intensity function. Other properties follow the same as the homogeneous poisson process.
    
** Poisson clustering process ** 

In a Poisson cluster process, we begin with a Poisson process Y of 'parent' coral colonies. Each parent colony then givens rise to a finite set of 'offspring' colonies according to some stochastic mechanism.  This tool uses a Matern cluster process to generate offspring colonies with the parent colonies come from a homogeneous Poisson process with intensity k, and each parent having a Poisson(u) number of offspring, that are independently and uniformly distributed in a disc of radius r centered around the parent. Here, we provide an interactive plot of the Matern cluster process, one can input different parent intensity rates and offspring intensity rates to see how the distribution of coral colonies changes.

    ''')


