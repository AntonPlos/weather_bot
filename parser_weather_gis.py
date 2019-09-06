import requests
import bs4

import lxml

from weather_data import WeatherData

BASE_URL = "https://www.gismeteo.ru/weather-moscow-4368/"
NEXT_URL = "tomorrow/"
HEADERS = {'User-Agent': 'Mozilla/6.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2171.95 Safari/537.36'}


def __get_widget_container(content):
    widget_list = content.find_all('div', class_='widget__container')
    if widget_list is None:
        return None
    for _widget in widget_list:
        return _widget
    return None


def __get_widget_precipitation(_widget):
    output_data = []
    content_list = _widget.find_all('div', class_="widget__row widget__row_table widget__row_precipitation")
    if content_list is None:
        print('ERROR: _get_widget_precipitation - content_list is None')
        return None
    for content in content_list:
        prec__without = content.find_all('div', class_="w_prec__without")
        if len(prec__without) == 1:
            if prec__without[0].getText() == 'Без осадков':
                output_data = [0, 0, 0, 0, 0, 0, 0, 0]
        else:
            values = content.find_all('div', class_="w_prec__value")
            if values is None:
                print('ERROR: _get_widget_precipitation - w_prec__value is None')
                return None
            for value in values:
                try:
                    precipitation = value.getText().strip().replace(',', '.')
                    output_data.append(precipitation)
                except Exception as ex:
                    print("ERROR: _get_widget_precipitation value.getText().strip()")
                    print(ex)
    return output_data


def __get_list_of_temperature(_widget):
    output_data = []
    content_list = _widget.find_all('div', class_="templine w_temperature")
    if content_list is None:
        print('ERROR: _get_list_of_temperature - templine w_temperature is None')
        return None
    for content in content_list:
        values = content.find_all('div', class_="value")
        if values is None:
            print('ERROR: _get_list_of_temperature - value is None')
            return None
        for value in values:
            try:
                temp = value.find('span').get_text()
                output_data.append(temp)
            except Exception as ex:
                print("ERROR: _get_list_of_temperature value.find('span').get_text()")
                print(ex)
    return output_data


def __get_list_of_time(_widget):
    output_data = []
    content_list = _widget.find_all('div', class_="widget__row widget__row_time")
    if content_list is None:
        print('ERROR: _get_list_of_time - widget__row widget__row_time is None')
        return None
    for content in content_list:
        values = content.find_all('div', class_="w_time")
        if values is None:
            print('ERROR: _get_list_of_time - w_time is None')
            return None
        for value in values:
            try:
                temp = value.find('span').get_text()
                output_data.append(temp)
            except Exception as ex:
                print("ERROR: _get_list_of_time value.find('span').get_text()")
                print(ex)
    return output_data


def get_today_weather():
    data = WeatherData()
    session = requests.session()
    r = session.get(BASE_URL, headers=HEADERS, timeout = 5)
    soup = bs4.BeautifulSoup(r.content, "lxml")
    widget = __get_widget_container(soup)
    data.set_temperature(__get_list_of_temperature(widget))
    data.set_times(__get_list_of_time(widget))
    data.set_precipitation(__get_widget_precipitation(widget))
    return data


def get_tomorrow_weather():
    data = WeatherData()
    session = requests.session()
    r = session.get(BASE_URL + NEXT_URL, headers=HEADERS, timeout = 5)
    soup = bs4.BeautifulSoup(r.content, "lxml")
    widget = __get_widget_container(soup)
    data.set_temperature(__get_list_of_temperature(widget))
    data.set_times(__get_list_of_time(widget))
    data.set_precipitation(__get_widget_precipitation(widget))
    return data
