import enum


class TypeOfEvent(enum.Enum):
    COME_OF_PACKET = 0
    FINISH_OF_SERVICE = 1
    BEGIN_CRASH = 2
    CRASH_FINISH = 3


