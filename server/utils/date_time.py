import datetime
import time


def current_time_sec():
    return int(time.mktime((datetime.datetime.now()).timetuple()))


def calc_exp(exp_sec):
    return current_time_sec() + exp_sec


def check_expired(exp):
    if current_time_sec() < exp:
        return False
    return True
