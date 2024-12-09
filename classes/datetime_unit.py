from math import inf

class DatetimeUnit:

    def __init__(self, name, default_value, min_value=-inf, max_value=inf):
        self.name = name
        self.default_value = default_value
        self.min_value = min_value
        self.max_value = max_value

    def get_default_value(self):
        return self.default_value

    def get_name(self):
        return self.name
    
    def get_min_value(self):
        return self.min_value
    
    def get_max_value(self):
        return self.max_value

    def is_valid(self, value):
        try:
            value_int = int(value)
            return value_int >= self.min_value and value_int <= self.max_value
        except ValueError:
            return False
