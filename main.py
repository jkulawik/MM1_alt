from Mm1CrashSimulator import start_crash_simulation
from Mm1Simulator import start_mm1

debug_values: bool = True


def start_simulation():
    decision = 1
    packets = 200
    repetitions = 2
    confidence_range = 1

    if not debug_values:
        print("************************************")
        decision = input("Prosze wybrac typ symulacji [1] bez awarii, [2] z awaria\n")
        print("************************************")
        packets = int(input("Prosze podac liczbe pakietow\n"))
        print("************************************")
        repetitions = int(input("Prosze podac liczbe replikacji\n"))
        print("************************************")
        confidence_range = float(input("Prosze podac zakres przedzialu ufnosci\n"))
        print("************************************")

    if decision == '1':
        start_mm1(packets_num=packets, repetitions=repetitions, confidence_range=confidence_range)
    if decision == '2':
        start_crash_simulation(packets_num=packets, repetitions=repetitions, confidence_range=confidence_range)


start_simulation()
