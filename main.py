from Mm1CrashSimulator import start_crash_simulation
from Mm1Simulator import start_mm1


def start_simulation():
    print("************************************")
    print("************************************")
    decision = input("Prosze wybrac typ symulacji [1] bez awarii, [2] z awaria")
    print("************************************")
    print("************************************")
    if decision == '1':
        start_mm1()
    if decision == '2':
        start_crash_simulation()


start_simulation()