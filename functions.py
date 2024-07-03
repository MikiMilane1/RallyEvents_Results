import datetime
import datetime as dt
import math
import logging
from models.event_entry import ResultModel
from models.ss import SSModel
from models.event import EventModel


def add_time(*args):
    """
    Takes datetime.time objects as args and return their sum
    :param args: datetime.time objects
    :return: the sum of all args in the form of a datetime.time object
    """
    total_hours = 0
    total_minutes = 0
    total_seconds = 0
    total_microseconds = 0
    for arg in args:
        total_hours += arg.hour
        total_minutes += arg.minute
        total_seconds += arg.second
        total_microseconds += arg.microsecond

    if total_microseconds >= pow(10, 6):
        total_seconds += math.floor(total_microseconds / pow(10, 6))
        total_microseconds = total_microseconds % pow(10, 6)

    if total_seconds >= 60:
        total_minutes += math.floor(total_seconds / 60)
        total_seconds = total_seconds % 60

    if total_minutes >= 60:
        total_hours += math.floor(total_minutes / 60)
        total_minutes = total_minutes % 60

    sum_time = dt.time(hour=total_hours, minute=total_minutes, second=total_seconds, microsecond=total_microseconds)
    return sum_time


def place_drivers(event):
    num_of_ss = event.ss_num

    ss_sorted_dict = {}
    for ss in range(1, num_of_ss+1):
        ss_list = SSModel.query.filter(SSModel.event == event, SSModel.ss_num == ss).all()
        ss_list_sorted = sorted(ss_list, key=lambda x: x.time, reverse=False)
        ss_sorted_dict[f'ss{ss}_sorted'] = ss_list_sorted

    return ss_sorted_dict
