"""
Project 6 Data Visualization
Sharon Steinke
CS 1410

Program reads .dat files, analyzes the data in the files, detects pulses 
in the data, creates .pdf files of smooth and raw data, and records the pulses
and the related area of the pulses to .out files. 

I declare that the following source code was written solely by me. 
I understand that copying any source code, in whole or in part, 
constitutes cheating, and that I will receive a zero on 
this project if I am found in violation of this policy.

"""
import numpy as np
import matplotlib.pyplot as plt
import glob

def get_data(data_file):
    """
    reads a data file and adds data to an array
    """
    array = np.loadtxt(data_file)
    return array

def smooth_data(array):
    """
    smooths data using the formula:
    (yi-3 + 2yi-2 + 3yi + 3yi+1 + 2yi+2 + yi+3 )//15
    where yi is the point to be smoothed.
    """
    len_arr = len(array) 
    smoothed_list = []
    for num in range(len_arr):
        if num <= 2 or num >= (len_arr-3):
            smoothed_list.append(array[num])
        else:
            y1 = array[num-3]
            y2 = 2*array[num-2]
            y3 = 3*array[num-1]
            y4 = 3*array[num]
            y5 = 3*array[num+1]
            y6 = 2*array[num+2]
            y7 = array[num+3]
            smoothed_point = (y1 + y2 + y3 + y4 + y5 + y6 + y7)//15
            smoothed_list.append(smoothed_point)
    smoothed_array = np.array(smoothed_list)
    return smoothed_array

def find_pulse(smoothed_array):
    """
    records the index of the start of a pulse
    if voltage threshold is >= 100
    use yi+2 - yi where yi is the potential start of pulse
    """
    len_smooth = len(smoothed_array)
    pulse_index = []
    previous_rise = 0
    for num in range(len_smooth):
        if num+2 in range(len_smooth):
            y1 = smoothed_array[num]
            y2 = smoothed_array[num+2]
            rise = y2-y1
            if previous_rise >= 100 and rise <= 100:
                previous_rise = rise
            if previous_rise <= 100 and rise >= 100:
                pulse_index.append(num)
                previous_rise = rise
    return pulse_index 
            
def area_pulse(pulse_index, raw_data):
    """
    records the area of a pulse and returns a list of areas
    """
    areas = []

    for ind in range(len(pulse_index)):
        area = 0
        for num in range(len(raw_data)):
            if pulse_index[ind] == num:
                if ind + 1 in range(len(pulse_index)):
                    difference = pulse_index[ind+1]-pulse_index[ind]
                    if difference <= 50:
                        start = pulse_index[ind]
                        end = pulse_index[ind+1]
                        for raw in raw_data[start:end]:
                            area += raw
                        areas.append(area)
                    else:
                        start = pulse_index[ind]
                        end = pulse_index[ind] + 50
                        for raw in raw_data[start:end]:
                            area += raw
                        areas.append(area)
                else:
                    start = pulse_index[ind]
                    end = pulse_index[ind] + 50
                    for raw in raw_data[start:end]:
                        area += raw
                    areas.append(area)
    return areas

def graph_array(raw_data, smooth_data, file_name):
    """
    graphs the raw and smooth data
    and saves as pdf
    """
    fig, ax = plt.subplots(2, 1)
    ax[0].plot(raw_data)
    ax[1].plot(smooth_data)
    ax[0].set(title=f'{file_name}')
    ax[0].set_ylabel('Raw')
    ax[1].set_ylabel('Smooth')
    new_file = file_name.split('.')
    plt.savefig(f'{new_file[0]}.pdf') 

def save_file(pulses, areas, file_name):
    new_file = file_name.split('.')
    file = new_file[0]
    num = 1
    with open(f'{file}.out', 'w') as fout:
        fout.write(f'{file_name}:\n')
        for pulse, area in zip(pulses, areas):
            fout.write(f'Pulse {num}: {round(pulse)} ({round(area)})\n')
            num +=1
def analyze(data_file):
    """
    analyzes data according to various functions used. 
    """
    array = get_data(data_file)
    smoothed_array = smooth_data(array)
    pulse_index = find_pulse(smoothed_array)
    areas = area_pulse(pulse_index, array)
    graph_array(array, smoothed_array, data_file)
    save_file(pulse_index, areas, data_file)

def main(): 
   for fname in glob.glob('*.dat'): 
        analyze(fname) 

if __name__ == "__main__":
    main()