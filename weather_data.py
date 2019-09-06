class WeatherData:
    __times = []
    __temperature = []
    __precipitation = []

    def set_times(self, data):
        if data is not None:
            self.__times = data

    def set_temperature(self, data):
        if data is not None:
            self.__temperature = data

    def set_precipitation(self, data):
        if data is not None:
            self.__precipitation = data

    def get_times(self):
        return self.__times

    def get_temperature(self):
        return self.__temperature

    def get_precipitation(self):
        return self.__precipitation

    def is_valid(self):
        return (len(self.__times) == len(self.__precipitation)) & (len(self.__times) == len(self.__temperature))

    def __str__(self):
        out_string = 'Time '
        for t in self.__times:
            out_string += '{0:5.0f}'.format(float(t))
        out_string += '\nT    '
        for t in self.__temperature:
            out_string += '{0:5.0f}'.format(float(t))
        out_string += '\nPrec '
        for t in self.__precipitation:
            out_string += '{0:5.1f}'.format(float(t))
        return out_string


