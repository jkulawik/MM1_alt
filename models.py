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
    def __init__(self, practical, theoretical, confidence_interval, confidence_min, confidence_max):
        self.practical = practical
        self.theoretical = theoretical
        self.confidence_interval = confidence_interval
        self.confidence_min = confidence_min
        self.confidence_max = confidence_max

    def __str__(self): return f'theoretical: {self.theoretical} practical {self.practical} confidence {self.confidence_interval}'


class PacketMM1:
    def __init__(self, time_of_service, time_of_arrival, time_get_by_server, time_end_of_service, number_of_packet):
        self.time_of_service = time_of_service
        self.time_of_arrival = time_of_arrival
        self.time_get_by_server = time_get_by_server
        self.time_end_of_service = time_end_of_service
        self.number_of_packet = number_of_packet


class PacketEvent:
    def __init__(self, type_of_event, number_of_packet, time_of_event):
        self.type_of_event = type_of_event
        self.time_of_event = time_of_event
        self.number_of_packet = number_of_packet
