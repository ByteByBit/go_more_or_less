import re
from datetime import datetime, date


class Parameters:
    ''' Parameter parser class.'''

    num_seats = None
    from_city = None
    to_city = None
    from_date = None
    to_date = None

    def __init__(self, args: list) -> None:

        self.args = args

    def set_cities(self, city: str) -> None:

        if self.from_city:
            self.to_city = city
        else:
            self.from_city = city

    def set_dates(self, date_txt: str) -> None:

        date = self.date_converter(date_txt=date_txt)

        if self.from_date:
            self.to_date = date
        else:
            self.from_date = date

    def date_converter(self, date_txt: str) -> date:
        ''' Convert date string to date obj.'''

        return datetime.strptime(date_txt, '%Y-%m-%d').date()

    def parse(self) -> None:
        ''' Parsing args by regex.'''

        for  arg in self.args:

            if re.search('^[a-zA-Z]+(?:[\s-][a-zA-Z]+)*$', arg):
                self.set_cities(city=arg)

            elif re.search('\d{4}[-]\d{2}[-]\d{2}', arg):
                self.set_dates(date_txt=arg)
                
            elif re.search('\d+', arg):
                self.num_seats = int(arg)
