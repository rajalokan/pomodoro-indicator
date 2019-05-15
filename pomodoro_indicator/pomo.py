import json
import datetime
import calendar
from datetime import timedelta

pomo_file_path = "/tmp/pomo.json"

class Pomo():
    _data = None

    def __init__(self):
        self._data = self._read_pomo_data()

    @property
    def _current_month(self):
        return datetime.datetime.now().strftime('%b').lower()

    @property
    def _current_day(self):
        return str(datetime.datetime.now().day)

    @property
    def today(self):
        return self._data[self._current_month][self._current_day]

    @property
    def yesterday(self):
        date_yesterday = datetime.datetime.today() - timedelta(days=1)
        return self._data[date_yesterday.strftime('%b').lower()][str(date_yesterday.day)]

    def _ensure_consistent_data(self, data):
        if data == None:
            data = {}

        current_month = datetime.datetime.today().month
        for k,v in enumerate(calendar.month_abbr):
            if k == 0:
                continue
            if k <= current_month:
                month = v.lower()
                if not month in data:
                    data[month] = {}

                for day in range(1, calendar.monthrange(2019,k)[1]+1):
                    if k == current_month:
                        if day <= datetime.datetime.today().day:
                            if not str(day) in data[month]:
                                data[month][str(day)] = 0
                    if not str(day) in data[month]:
                        data[month][str(day)] = 0

        return data


    def _read_pomo_data(self):
        try:
            with open(pomo_file_path) as fd:
                data = json.load(fd)
        except FileNotFoundError:
            data = {}

        data = self._ensure_consistent_data(data)
        self._write_pomo_data(data)
        return data

    def _write_pomo_data(self, data):
        with open(pomo_file_path, "w") as fd:
            json.dump(data, fd)

    def update_pomo_counter(self):
        self._data[self._current_month][self._current_day] = self.today + 1
        self._write_pomo_data(self._data)

    def get_pomo_as_string(self):
        if self.today == 0:
            return "No pomos today"
        else:
            return "Today's pomo : %s" % self.today
