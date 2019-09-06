import parser_weather_gis
import render_graphics


def save_graphics_today(path):
    data = parser_weather_gis.get_today_weather()
    render_graphics.print_graphic(data, path)


save_graphics_today('test_png//today.png')
