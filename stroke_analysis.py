import pandas as pd
import numpy as np
from scipy.signal import find_peaks

from constants import COLUMN_NAMES
from constants import MINIMUM_DISTANCE_BETWEEN_PEAKS

from helpers import read_data
from helpers import get_peaks


class StrokeAnalysis:
    def __init__(self, file_path) -> None:
        self.data = read_data(file_path)

        self.selected_data = None
        self.peaks = None
        self.water_entries = None
        self.exits = None
        self.air_entries = None

    def get_peaks(self):

        self.peaks = get_peaks()

    def get_water_entries(self):

        if self.selected_data is None:

            entries_index = get_entry_points_index(self.peaks, data)
            self.water_entries = data.iloc[entries_index].reset_index(
                drop=True)
