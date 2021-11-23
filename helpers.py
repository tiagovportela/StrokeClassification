import pandas as pd
from scipy.signal import find_peaks

from constants import COLUMN_NAMES


def read_data(file_path):
    """ 
    Read csv with data
    -------------------
    Return pandas DataFrame

    """
    return pd.read_csv(file_path, names=COLUMN_NAMES)


def select_data_interval(data, start, end):
    """
    Select data between a interval
    -------------------------------
    return pandas DataFrame
    """
    mask = (data.time >= start) & (data.time <= end)
    return data[mask].reset_index(drop=True).copy()


def get_acceleration_peaks_index(data):
    """
    Calculate peaks in acceleration
    -------------------------------------
    return index of peak
    """
    peak_index, _ = find_peaks(data.ax, distance=30)

    return peak_index


def get_entry_points_index(peaks, data):
    """
    Calculate the entry point of stroke
    ------------------------------------
    Return index of entry points
    """
    local_minimum_index = data.ax[(start_data.ax.shift(1) > data.ax) & (
        data.ax.shift(-1) > data.ax) & (data.ax < 0)].index
    local_minimum = data.iloc[local_minimum_index]

    entry_point_index = list()
    for index, row in peaks.iterrows():
        mask = (local_minimum.time < row.time)
        aux_df = local_minimum[mask]
        aux_df.sort_values(by='time')
        try:
            point_index = aux_df.tail(1).index.values[0]
        except IndexError:
            point_index = index

        entry_point_index.append(point_index)
    return entry_point_index


def get_peaks(data):
    """
    Calculate de peak point
    --------------------------
    Return pandas Dataframe with PEAK points
    """
    peaks_index = get_acceleration_peaks_index(data)
    return data.iloc[peaks_index]


def get_entry_points(data):
    """
    Calculate de entry point
    --------------------------
    Return pandas Dataframe with ENTRY points
    """
    peaks_index = get_entry_points_index(data)
    return data.iloc[peaks_index]
