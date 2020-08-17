global_awaiting_time = 0


def to_minute(sec):
    return sec / 60


def to_timestamp(min):
    return min * 60


class OrderLog:
    def __init__(self, order_id, user_id, order_date, expected_arrive, expected_trip_time):
        self.id = order_id
        self.user_id = user_id
        self.date = order_date
        self.expected_arrive = expected_arrive
        self.expected_trip_time = expected_trip_time
        self.type = 'ordered'

    def expected_trip_finished(self):
        return self.date + \
               to_timestamp(self.expected_arrive) + \
               to_timestamp(global_awaiting_time) + \
               to_timestamp(self.expected_trip_time)


class TimeLog:
    def __init__(self, type, order_id, time):
        self.id = order_id
        self.time = time
        self.type = type


class Trip:
    order_log = None
    arrived_log = None
    start_log = None
    finish_log = None

    def set_log(self, log):
        if log.type == 'ordered':
            self.order_log = log
        if log.type == 'arrived':
            self.arrived_log = log
        if log.type == 'started':
            self.start_log = log
        if log.type == 'finished':
            self.finish_log = log

    def _should_ignore(self):
        return (
                self.order_log is None
                or self.arrived_log is None
                or self.start_log is None
                or self.finish_log is None
        )

    def is_passenger_late(self):
        return to_minute(self.start_log.time - self.arrived_log.time) > global_awaiting_time

    def is_coming_to_pass_in_time(self):
        return self.order_log.date + to_timestamp(self.order_log.expected_arrive) >= self.arrived_log.time

    def compute_late_diff(self):
        if self._should_ignore():
            return -1

        if self.is_passenger_late():
            return -1

        expected_finished = self.order_log.expected_trip_finished()
        actual_finished = self.finish_log.time

        return actual_finished - expected_finished


def parse_log(log):
    arr = log.split()
    if arr[0] == 'ordered':
        return OrderLog(arr[1], arr[2], int(arr[3]), int(arr[4]), int(arr[5]))

    return TimeLog(arr[0], arr[1], int(arr[2]))


def solve(raw_logs):
    parsed_logs = map(parse_log, raw_logs)
    trip_dict = dict()

    for parsed_log in parsed_logs:
        log_id = parsed_log.id
        trip = None

        if log_id in trip_dict:
            trip = trip_dict[log_id]
        else:
            trip = Trip()
            trip_dict[log_id] = trip

        trip.set_log(parsed_log)

    user_dict = dict()
    for trip in trip_dict.values():
        diff = trip.compute_late_diff()
        if diff <= 0:
            continue
        user_id = trip.order_log.user_id
        if user_id in user_dict:
            user_dict[user_id] += diff
        else:
            user_dict[user_id] = diff

    sorted2 = sorted(user_dict.items(), key=lambda item: (-item[1], item[0]))
    return list(map(
        lambda x: x[0],
        sorted2
    ))


n = int(input())

for i in range(n):
    logs_amount, top_users, awaiting_time = input().split()
    global_awaiting_time = int(awaiting_time)
    logs = []
    for j in range(int(logs_amount)):
        logs.append(input())

    result = solve(logs)
    if len(result) == 0:
        print('-')
    else:
        print(' '.join(result))
