from Mm1CrashSimulator import start_crash_simulation
from Mm1Simulator import start_mm1


def start_simulation():
    print("************************************")
    decision = input("Prosze wybrac typ symulacji [1] bez awarii, [2] z awaria")
    print("************************************")
    packets = int(input("Prosze podac liczbe pakietow"))
    print("************************************")
    replicates = int(input("Prosze podac liczbe replikacji"))
    print("************************************")
    confidence_range = float(input("Prosze podac zakres przedzialu ufnosci"))
    print("************************************")
    if decision == '1':
        start_mm1(packets_num=packets, replicates=replicates, confidence_range=confidence_range)
    if decision == '2':
        start_crash_simulation(packets_num=packets, replicates=replicates, confidence_range=confidence_range)


start_simulation()