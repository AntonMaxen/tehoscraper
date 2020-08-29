import datetime
from writefile import get_content


def is_wanted_hour(wanted_hour, FILENAME):
    bool_wanted_hour = False
    hour = get_content(FILENAME)
    if len(hour) > 0:
        last_hour = int(hour[0])
    else:
        last_hour = -1

    time_date = datetime.datetime.now()
    hour = time_date.hour
    if hour != last_hour:
        print("This is a new hour")
        last_hour = hour
        time_file = open(FILENAME, 'w', encoding='utf-8')
        time_file.write(str(last_hour))
        time_file.close()
        if last_hour % wanted_hour == 0:
            print(f'{last_hour}: is a wanted hour')
            bool_wanted_hour = True
    else:
        print("This hour has already happened")

    return bool_wanted_hour


if __name__ == '__main__':
    is_wanted_hour(18)
