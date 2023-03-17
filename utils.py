import time


def current_millis():
    return time.time() * 1000

def convert_seconds_to_minutes_seconds(seconds):
    seconds = int(seconds)
    minutes = seconds // 60
    seconds = seconds % 60
    return minutes, seconds

def convert_seconds_to_time_str(seconds, sep = ' : ', zfill = 2):
    minutes, seconds = convert_seconds_to_minutes_seconds(seconds)
    return str(minutes).zfill(zfill) + sep + str(seconds).zfill(zfill)