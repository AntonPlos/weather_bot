import parser_weather_gis
import render_graphics
import os

from weather_data import WeatherData


def save_graphics_today(file_path):
    data = parser_weather_gis.get_today_weather()
    render_graphics.print_graphic(data, file_path, 23)


def save_graphics_two_day(file_path):
    today = parser_weather_gis.get_today_weather()
    next_day = parser_weather_gis.get_tomorrow_weather()
    union_data = WeatherData()
    union_data.set_times(today.get_times() + __add_next_day_times(next_day.get_times()))
    union_data.set_precipitation(today.get_precipitation() + next_day.get_precipitation())
    union_data.set_temperature(today.get_temperature() + next_day.get_temperature())
    render_graphics.print_graphic(union_data, file_path, 47)


def has_current_day_graph(file_path):
    return os.path.exists(file_path)


def __add_next_day_times(array):
    out = []
    for t in array:
        out.append(t + 24)
    return out


save_graphics_two_day('test_png//two_day.png')
print(has_current_day_graph('test_png//two_day.png'))
