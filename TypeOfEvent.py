import enum


class TypeOfEvent(enum.Enum):
    PACKET_ARRIVAL = 0
    END_OF_SERVICE = 1
    BEGIN_CRASH = 2
    END_CRASH = 3


