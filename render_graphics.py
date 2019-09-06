import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

from scipy.interpolate import interp1d
from weather_data import WeatherData


def print_graphic(data: WeatherData, path):
    if data.is_valid():
        x = data.get_times()
        new_x = np.linspace(0, 21, num=100, endpoint=True)

        fig, axs = plt.subplots(2, 1, sharex=True, sharey=False, gridspec_kw={'height_ratios': [3, 1]})

        t = data.get_temperature()
        interpolation_t = interp1d(x, t, kind='cubic')
        points_t = np.array([new_x, interpolation_t(new_x)]).T.reshape(-1, 1, 2)
        segments_t = np.concatenate([points_t[:-1], points_t[1:]], axis=1)
        norm_t = plt.Normalize(-1, 10)
        line_collect_t = LineCollection(segments_t, cmap='cividis', norm=norm_t)
        line_collect_t.set_array(interpolation_t(new_x))
        line_collect_t.set_linewidth(3)
        line_t = axs[0].add_collection(line_collect_t)
        fig.colorbar(line_t, ax=axs[0])

        p = data.get_precipitation()
        interpolation_p = interp1d(x, p, kind='cubic')
        points_p = np.array([new_x, interpolation_p(new_x)]).T.reshape(-1, 1, 2)
        segments_p = np.concatenate([points_p[:-1], points_p[1:]], axis=1)
        norm_p = plt.Normalize(0, 0.3)
        line_collect_p = LineCollection(segments_p, cmap='Greens', norm=norm_p)
        line_collect_p.set_array(interpolation_p(new_x))
        line_collect_p.set_linewidth(3)
        line_p = axs[1].add_collection(line_collect_p)
        fig.colorbar(line_p, ax=axs[1])

        axs[0].set_xlim(0, 21)
        axs[0].set_ylim(0 if min(t) > 1 else min(t) - 1, 0 if max(t) < -1 else max(t) + 1)
        axs[1].set_ylim(0, 1 if max(p) < 0.8 else max(p) + 0.5)
        plt.show()
        #plt.savefig(path, dpi=150)

