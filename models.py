class Event:
    def __init__(self, time, obj, type):
        self.time = time
        self.obj = obj
        self.type = type

    def __str__(self):
        return f'Time: {self.time} Type: {self.type}'


class Packet:
    def __init__(self, time_of_service, time_of_arrival):
        self.time_of_service = time_of_service
        self.time_of_arrival = time_of_arrival
        self.finish_of_service = 0


class CrashOn:
    def __init__(self, duration):
        self.duration = duration
