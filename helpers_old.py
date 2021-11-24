def get_all_peaks_and_hollows(data):

    # ,threshold=0.04)
    peaks, _ = find_peaks(data.ax, distance=25, prominence=1)
    local_peaks = data.ax.iloc[peaks]
    data['max'] = local_peaks[local_peaks > 1]
    data['min'] = data.ax[(data.ax.shift(1) > data.ax) & (
        data.ax.shift(-1) > data.ax) & (data.ax < 0)]
    data_peaks = data[~(data['max'].isna())].copy()
    data_hollow = data[~(data['min'].isna())].copy()
    return data_peaks, data_hollow


def get_peaks_and_hollows(data):

    data_peaks, data_hollow = get_all_peaks_and_hollows(data)

    pk = data_peaks.copy()

    index_begin_stroke = list()
    loop_iteration = 0
    for index, row in data_peaks.iterrows():
        if loop_iteration == 0:
            time_peak = row.time
            crop = data_hollow[(data_hollow.time < time_peak)].copy()
            try:
                index_nearts_hollow = crop.time.index[-1]
                index_begin_stroke.append(index_nearts_hollow)
                last_Time = time_peak
            except IndexError:
                last_Time = time_peak
                continue
        else:
            time_peak = row.time
            crop = data_hollow[(data_hollow.time > last_Time) & (
                data_hollow.time < time_peak)].copy()

            #min_acc = crop.ax.argmin()
            #index_nearts_hollow = crop.Time.index[min_acc]
            try:
                index_nearts_hollow = crop.time.index[-1]
                index_begin_stroke.append(index_nearts_hollow)
                last_Time = time_peak
            except IndexError:
                last_Time = time_peak
                continue

        loop_iteration += 1
    hl = data.iloc[index_begin_stroke]
    hl = hl.reset_index(drop=True)
    pk = pk.reset_index(drop=True)
    return pk, hl


def get_exits(data, strokes):
    exits = data.copy()
    exits = exits.drop(index=exits.index)
    for stk in strokes:
        peak, index = get_peaks(stk)
        exitpoint = stk.iloc[[index]]
        exits = pd.concat([exits, exitpoint])
        exits = exits.sort_values(by='time', ascending=True)
        exits = exits.reset_index(drop=True)
    return exits


def get_stroke_list(data):

    stroke_list = list()

    peaks, hollows = get_peaks_and_hollows(data)
    #exits = get_exits(data, hollows)
    #data = pd.concat([data, exits])
    for index, row in hollows.iterrows():
        if index == 0:
            mask = (data.time >= row.time)
            crop = data[mask].reset_index(drop=True).copy()
            stroke_list.append(crop)
        else:
            mask = (data.time >=
                    hollows.iloc[index - 1].time) & (data.time <= row.time)
            crop = data[mask].reset_index(drop=True).copy()
            stroke_list.append(crop)
    stroke_list = stroke_list[1:]
    exits = get_exits(data, stroke_list)
    return stroke_list, exits


def get_peaks(data):
    # peaks = find_peaks_cwt(data.ax, data.Time)#, height=0)

    index_max_ax = data.ax.argmax()
    # print(index_max_ax)
    acc_ax = data.ax.iloc[index_max_ax:].copy()

    peaks = list()
    lowest_peak_value = 99999
    lowest_peak_index = 0
    for index, ax in zip(acc_ax.index, acc_ax):
        #print("Index: {} Acc: {}".format(index,ax))
        if index == index_max_ax:
            continue
        elif index == index_max_ax + len(acc_ax) - 1:
            continue
        else:
            if ax > acc_ax[index - 1] and ax > acc_ax[index + 1]:
                if abs(ax) < lowest_peak_value:
                    lowest_peak_value = ax
                    lowest_peak_index = index
    if lowest_peak_value == 99999:
        lowest_peak_index = acc_ax.abs().argmin() + index_max_ax
        #print("Lowest Index: ", lowest_peak_index)
        # rint(acc_ax)
        lowest_peak_value = acc_ax[lowest_peak_index]

        return lowest_peak_value, lowest_peak_index
    return lowest_peak_value, lowest_peak_index
