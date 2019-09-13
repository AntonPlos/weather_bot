import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

from scipy.interpolate import interp1d
from weather_data import WeatherData


def print_graphic(data: WeatherData, path, count):
    if data.is_valid():
        x = data.get_times()
        new_x = np.linspace(0, count - 2, num=100, endpoint=True)

        fig, axs = plt.subplots(2,
                                1,
                                sharex=True,
                                sharey=False,
                                gridspec_kw={'height_ratios': [1, 3]},
                                figsize=(10,  5))

        labels_x = []
        for lx in x:
            if lx > 24:
                labels_x.append(lx - 24)
            else:
                labels_x.append(lx)
        plt.xticks(np.arange(min(x), max(x) + 1, 3.0), labels_x)

        __print_labels(data)

        t = data.get_temperature()
        interpolation_t = interp1d(x, t, kind='cubic')
        points_t = np.array([new_x, interpolation_t(new_x)]).T.reshape(-1, 1, 2)
        segments_t = np.concatenate([points_t[:-1], points_t[1:]], axis=1)
        norm_t = plt.Normalize(-15, 18)
        line_collect_t = LineCollection(segments_t, cmap='cividis', norm=norm_t)
        line_collect_t.set_array(interpolation_t(new_x))
        line_collect_t.set_linewidth(3)
        axs[1].add_collection(line_collect_t)
        axs[1].set_xlabel('Температура')
        axs[0].set_xlabel('Количество осадков')

        p = data.get_precipitation()
        interpolation_p = interp1d(x, p, kind='cubic')
        points_p = np.array([new_x, interpolation_p(new_x)]).T.reshape(-1, 1, 2)
        segments_p = np.concatenate([points_p[:-1], points_p[1:]], axis=1)
        norm_p = plt.Normalize(0, 0.3)
        line_collect_p = LineCollection(segments_p, cmap='Greens', norm=norm_p)
        line_collect_p.set_array(interpolation_p(new_x))
        line_collect_p.set_linewidth(3)
        axs[0].add_collection(line_collect_p)

        axs[0].set_xlim(0, count)
        axs[1].set_ylim(0 if min(t) > 1 else min(t) - 1, 0 if max(t) < -1 else max(t) + 1)
        axs[0].set_ylim(0, 1 if max(p) < 0.8 else max(p) + 0.5)
        plt.savefig(path, dpi=150)


def __print_labels(data: WeatherData):
    for i in range(len(data.get_times())):
        current_time = data.get_times()[i]
        current_t = data.get_temperature()[i]
        plt.annotate(current_t if current_t < 0 else '+' + str(current_t), xy=(current_time, current_t), color='green')


