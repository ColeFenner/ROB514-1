#!/usr/bin/env python3

#--------------- Fit a line to the middle part of the finger 1 motor positions ----------------------

# It might be helpful to look at the instruction/background slides before tackling this
#
# https://docs.google.com/presentation/d/1IoiD43zjp_XOEH0soCZGMBN4b13KWVndoHAxoUJMQoM/edit?usp=sharing

# Doing the imports for you
import numpy as np
import json as json
from scipy.stats import linregress
import matplotlib.pyplot as plt

# BEGIN SOLUTION NO PROMPT
# Read in the processed data

data_successful = np.loadtxt("Data/week3_Motor position f1_successful.csv", dtype="float", delimiter=",")
data_failed = np.loadtxt("Data/week3_Motor position f1_failed.csv", dtype="float", delimiter=",")

# END SOLUTION

""" # BEGIN PROMPT
# Read in week3_Motor position f1_success and failed .csv files
data_successful = ...  # week3_Motor position f1_successful.csv
data_failed = ...  # week3_Motor position f1_failed.csv
# END PROMPT"""


# -------------------------------- Fit a line to the middle points -----------------------------

# Doing this as a function so you can use it twice
#  Some decisions
#   1) Pass in the data as two arrays, the t and y values
#         Use this function to pull out the "middle" bit
#   2) Returns the points of intersection with the min/max values (rather than slope and intercept) because in the
#         long run that's what we care about (where the motor started and stopped)
#   3) The eps is a "fudge factor" so that you can clip out data above/below a threshhold
#
#  Two ways to do this:
#     Clip with a fudge factor, use np.logical_and
#          fudge factor should be d_y = eps * (y_max - y_min), take all points y_min + d_y < y < y_max - dy
#     Use np.where to find the first index > y_min + d_y (or < y_max - d_y)
#          np.where returns an array of arrays; use index[0][0] to get the value out
#          Then use start:end to get the values out of ts, ys
#
# Implementation steps (suggested)
#   Start with just fitting the entire data and drawing the resulting line
#        Use y = mx + b equation to find start/stop points from slope/intercept
#        Find max/min y values, and plug those into the equation
#   You should get something that goes roughly from the bottom left to the top right of the original data
#   Step 2: Clip just the y_max values by using boolean indexing to keep just part of the array
#       Alternate: Use np.where to find the max value, extract the ending index, and use 0:end_index
#   Step 3: Clip both ends at the same time (change the boolean indexing to use a logical_and)
#       Alternate: Use np.where a second time to find the min value, extract the starting index
def fit_line_to_middle_bit(ts, ys, eps=1e-2):
    """ Fit a line to the sloped middle bit of the data
      Return the line as a pair of points, one where the fitted line crosses the y min value, one where the line crosses
      the y max value (see slides for picture)
      Reminder; Use & to do an AND of two boolean conditions
    @param ts - the time values for the data (x-axis)
    @param ys - the function values (y-axis)
    @param eps - a fudge factor for clipping the middle bit
    @returns (x_min, y_min), (x_max, y_max)  (two tuples)"""

    # BEGIN SOLUTION NO PROMPT

    y_max = np.max(ys)
    y_min = np.min(ys)
    delta_y = eps * (y_max - y_min)

    find_vals = np.logical_and(ys > (y_min + delta_y), ys < (y_max - delta_y))
    res_clip = linregress(ts[find_vals], ys[find_vals])

    index_start = np.where(ys > y_min + delta_y)
    index_end = np.where(ys > y_max - delta_y)
    res_bounds = linregress(ts[index_start[0][0]:index_end[0][0]], ys[index_start[0][0]:index_end[0][0]])

    # print(f"Result, clipping: {res_clip}")
    # print(f"Result, bounds: {res_bounds}")

    x_min = (y_min - res_clip.intercept) /res_clip.slope
    x_max = (y_max - res_clip.intercept) /res_clip.slope
    # END SOLUTION

    """ # BEGIN PROMPT
    # Indices 8-12 should be True for first row successful
    # Slope should be 654.xxx, intercept 162.xxx for first row successful
    y_min = ...
    y_max = ...
    x_min = ...
    x_max = ...
    # END PROMPT"""
    return (x_min, y_min), (x_max, y_max)

# -------------------------------- Plot -----------------------------
n_rows = 1
n_cols = 2
fig, axs = plt.subplots(n_rows, n_cols)

# BEGIN_SOLUTION NO_PROMPT
# Know time step
time_step = 1/30
ts = np.arange(start=0, stop=data_successful.shape[1] * time_step, step=time_step)

pt_start, pt_end = fit_line_to_middle_bit(ts, data_successful[0])
axs[0].plot(ts, data_successful[0], '-b', label=f"Motor position f1")
axs[0].plot([pt_start[0], pt_end[0]], [pt_start[1], pt_end[1]], ':k', label="fitted line")
axs[0].plot([pt_start[0], pt_end[0]], [pt_start[1], pt_end[1]], 'Xr')
axs[0].set_title(f"Succesful t={pt_end[0]}")
axs[0].legend()

pt_start, pt_end = fit_line_to_middle_bit(ts, data_failed[0])
axs[1].plot(ts, data_successful[0], '-b', label=f"Motor position f1")
axs[1].plot([pt_start[0], pt_end[0]], [pt_start[1], pt_end[1]], ':k', label="fitted line")
axs[1].plot([pt_start[0], pt_end[0]], [pt_start[1], pt_end[1]], 'Xr')
axs[1].set_title(f"Failed t={pt_end[0]}")
axs[1].legend()

# END_SOLUTION

""" # BEGIN PROMPT
# Create t values with appropriate step size
ts = ...
# Plot original data and fitted line (see slides)
#   Put the end time value in the title
# END PROMPT"""
plt.tight_layout()
plt.close(fig)
