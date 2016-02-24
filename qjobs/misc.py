"""miscellaneous functions"""

from . import constants
from datetime import datetime, timedelta


def rm_brackets(string):
    """remove [ ] if at 1st and last char"""

    if string and string[0] == '[':
        string = string[1:]
    if string and string[-1] == ']':
        string = string[:-1]

    return string


def itmfilter(string, allow_caps=False):
    """remove undefined items from an ITEMS string"""
    return ''.join((itm for itm in string
                    if (itm in constants.itms or
                        itm.lower() in constants.itms and allow_caps)))


class ElapsedTime(timedelta):
    """timedelta with custom str conversion"""
    fmt = ''

    def __str__(self):
        """str conversion made according to the
        user-defined format"""
        dct = {}
        dct['d'] = self.days
        dct['h'], rmd = divmod(self.seconds, 3600)
        dct['m'], dct['s'] = divmod(rmd, 60)
        dct['S'] = 86400 * self.days + self.seconds
        dct['M'] = dct['S'] // 60
        dct['H'] = dct['S'] // 3600
        dct['D'] = dct['S'] / 86400.
        return self.fmt.format(**dct)

    def __format__(self, fmt_spec):
        """formatting conversion"""
        return self.__str__().__format__(fmt_spec)


class StartTime(datetime):
    """datetime with custom str conversion"""
    fmt = ''

    def __str__(self):
        """str conversion made according to the
        user-defined format"""
        return self.strftime(self.fmt)

    def __format__(self, fmt_spec):
        """formatting conversion"""
        return self.__str__().__format__(fmt_spec)


def time_handler(start_time, start_fmt, elaps_fmt, today):
    """return StartTime, ElapsedTime tuple using
    start/sub time string"""
    start_time = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S')
    start_time = StartTime(start_time.year, start_time.month,
                           start_time.day, start_time.hour,
                           start_time.minute, start_time.second)
    start_time.fmt = start_fmt

    delta = today - start_time
    delta = ElapsedTime(delta.days, delta.seconds, 0)
    delta.fmt = elaps_fmt

    return start_time, delta
