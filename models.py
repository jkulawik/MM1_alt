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


class Time:
    def __init__(self, practical, teoretical, confidence_interval):
        self.practical = practical
        self.teoretical = teoretical
        self.confidence_interval = confidence_interval

    def __str__(self): return f'teoretical: {self.teoretical} practical {self.practical} confidence {self.confidence_interval}'


class PacketMM1:
    def __init__(self, time_of_service, time_of_arrive, time_get_by_server, time_finish_of_service, number_of_packet):
        self.time_of_service = time_of_service
        self.time_of_arrive = time_of_arrive
        self.time_get_by_server = time_get_by_server
        self.time_finish_of_service = time_finish_of_service
        self.number_of_packet = number_of_packet


class PacketEvent:
    def __init__(self, type_of_event, number_of_packet, time_of_event):
        self.type_of_event = type_of_event
        self.time_of_event = time_of_event
        self.number_of_packet = number_of_packet
