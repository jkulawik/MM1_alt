class PacketEvent:
    def __init__(self, type_of_event, number_of_packet, time_of_event):
        self.type_of_event = type_of_event
        self.time_of_event = time_of_event
        self.number_of_packet = number_of_packet
