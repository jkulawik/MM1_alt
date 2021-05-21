class Packet:
    def __init__(self, time_of_service, time_of_arrive, time_get_by_server, time_finish_of_service, number_of_packet):
        self.time_of_service = time_of_service
        self.time_of_arrive = time_of_arrive
        self.time_get_by_server = time_get_by_server
        self.time_finish_of_service = time_finish_of_service
        self.number_of_packet = number_of_packet
