# coral-sampling-tool
This repository contains the source code of a dash app for coral sampling. An online version of this tool is hosted on
[heroku](https://coral-sampling.herokuapp.com/).

## Prerequisites
- **Conda** (Miniconda or Anaconda) - [Download here](https://docs.conda.io/en/latest/miniconda.html)
- **Git** (to clone the repository)
- **Python 3.7** (will be installed via conda)

## Quick Start 

1. Clone or download this repository
2. Navigate to the project directory
3. Run the automated setup script:
```console
$ chmod +x setup.sh
$ ./setup.sh
```
4. Activate the environment and run the app:
```console
$ conda activate coral-sampling
$ python app.py
```
5. Click the link that appears in the terminal to open the app in your browser.


## What is a coral sampling tool
### Overview
This tool let the users simulate corals on a landscape to characterize coral distribution in a selected region on the map. Based on this distribution, it then guides you on how many transects should be assigned during a survey to estimate percent coral cover and disease prevalence.  The use of this tool is predicated on the following survey method:

- Percent Coral cover:  This is estimated using line intercept (e.g. substrate categorized at length intervals such as 0-5 cm-'coral'; 5-13 cm-'Sand', 13-28 cm-'coral', etc.).
- Coral composition:  A 25 m line is deployed and coral colonies categorized as to genus (or species) and size class (1-5cm, 6-10cm, 11-20cm, 21-40cm, 41-80cm, 81-160, > 160 cm).
- Disease prevalence: A 6 m band (3 m to each side of the line) is surveyed and corals with lesions unmerated (genus or species and size class as above).  Prevalence of disease is estimated as No, lesioned corals divided by extrapolated of colony count from 1 m band to 25 X 6 m area.
  
The tool will ask you to enter an estimate of the following parameters for a given survey site:
- Your estimate of the distribution pattern of corals is on a site. 
- A rough estimate of coral cover (eyeballing the habitat) (0-20%, 21-40%, 41-60%, 61-80%, >80%).
- A rough estimate of prevalence of disease (eyeballing the habitat) (<1%, 2-5%, 6-10%, 11-20%, 21-40%, >40%)
- Number and orientation of transects to survey.
- If data exists for a particular site (or if you wish to upload data for a site), you can opt to do so and entries 1-3 will be automatically filled in.
