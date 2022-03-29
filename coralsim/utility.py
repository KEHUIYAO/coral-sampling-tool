from Simulation import Simulation
import pandas as pd
def calculate_coverage_probability(x:Simulation,n_rep):
    "calculate the coverage probability of prevalence estimation"

    count = 0
    for i in range(n_rep):
        x.efficient_simulate()
        x.n_corals()
        if x.cover_true_disease_prevalence():
            count += 1
    return count / n_rep

def calculate_coverage_probability_2(x:Simulation,n_rep):
    "calculate the coverage probability of both prop cover estimation and prevalence estimation"

    count_1 = 0
    count_2 = 0
    for i in range(n_rep):
        x.efficient_simulate()
        x.n_corals()
        if x.cover_true_prop_cover():
            count_1 += 1
        if x.cover_true_disease_prevalence():
            count_2 += 1
    return count_1 / n_rep, count_2 / n_rep


def power_comparison_using_different_number_of_toolkits(x:Simulation,number_of_toolkit_candidates,n_rep,write_to_csv = False, return_table=False):
    "compare the power of prevalence estimation using different number of transects"

    res = []
    for i in number_of_toolkit_candidates:
        print("---------- Using %d toolkits ----------" % i)
        x.change_toolkit_number(i)
        res.append(calculate_coverage_probability(x,n_rep))

    print("---------- Power for different number of toolkits ----------")

    for i in range(len(number_of_toolkit_candidates)):
        print("Using %d transects under %d reptitions, the power is %f" %(number_of_toolkit_candidates[i],n_rep,res[i]))

    d = {"Number_of_transects": number_of_toolkit_candidates, "Coverage_probability": res}
    df = pd.DataFrame(data=d)

    if write_to_csv:
        df.to_csv("result.csv",index = False)

    if return_table:
        return df
    else:
        return res



def power_comparison_using_different_number_of_toolkits_2(x:Simulation,number_of_toolkit_candidates,n_rep,write_to_csv = False, return_table=False):
    "compare the power of both prop cover and the prevalence estimation using different number of transects"

    res_1 = []
    res_2 = []
    for i in number_of_toolkit_candidates:
        print("---------- Using %d toolkits ----------" % i)
        x.change_toolkit_number(i)
        prop_cover_coverage, prevalence_coverage = calculate_coverage_probability_2(x, n_rep)
        res_1.append(prop_cover_coverage)
        res_2.append(prevalence_coverage)

    print("---------- Power for different number of toolkits ----------")

    for i in range(len(number_of_toolkit_candidates)):
        print("Using %d transects under %d reptitions, the power for prop cover is %f, the power for prevalence is %f" %(number_of_toolkit_candidates[i],n_rep,res_1[i], res_2[i]))

    d = {"Number_of_transects": number_of_toolkit_candidates, "Coverage_probability_proportion_cover": res_1, 'Coverage_propbability_prevalence_rate':res_2}
    df = pd.DataFrame(data=d)

    if write_to_csv:
        df.to_csv("result.csv",index = False)

    if return_table:
        return df
    else:
        return res_1, res_2
