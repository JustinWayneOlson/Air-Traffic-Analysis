import numpy as np


def mean_data(indp_var, delay_time):

    start_day_index = 0
    curr_day = indp_var[0]
    mean_day = []
    indp_axis = []

    for index in range(0, len(indp_var)):
        if(curr_day != indp_var[index]):
            mean_day.append(np.mean(delay_time[start_day_index:index]))
            indp_axis.append(curr_day)
            curr_day = indp_var[index]
            start_day_index = index

    if(start_day_index == index):
        mean_day.append(delay_time[index])

    else:
        mean_day.append(np.mean(delay_time[start_day_index:index]))

    indp_axis.append(indp_var[index])

    return mean_day




