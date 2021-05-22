import random
import queue
from models import PacketMM1
from models import PacketEvent
import numpy
from models import Time
import scipy.stats as st
import TypeOfEvent
from functions import exp
from functions import draw_plot


# ponizsza f-cja odpowiada za generacje zdarzenia zakonczenia obslugi pakietu przez serwer
def plan_event_finish_service(number_of_packet, time_get_by_server, time_of_service):
    return PacketEvent(TypeOfEvent.TypeOfEvent.FINISH_OF_SERVICE,
                                   number_of_packet,
                                   time_get_by_server + time_of_service)


# ponizsza f-cja odpowiada za generacje zdarzenia przyjscia kolejnego pakietu
def plan_event_come_next_packet(clock, number_of_packet, time_of_next_packet):
    return PacketEvent(TypeOfEvent.TypeOfEvent.COME_OF_PACKET, number_of_packet, clock + time_of_next_packet)


def start_mm1_simulation(LAMBDA,seed):
    random.seed(seed)
    print("*************************")
    print("MM1 SIMULATION STARTED!!!")
    print("*************************")
    # sredni czas obslugi pakietu przez serwer
    time_of_service = 0.125
    # sredni odstep pomiedzy pakietami 0.5 - 6
    #LAMBDA = float(input("Input a LAMBDA please (0.5-6)"))
    average_time_between_packets = 1/LAMBDA
    # czy serwer jest zajety
    is_server_busy = True
    # kolejka pakietow
    queue_of_packets = queue.Queue()
    # tablica zdarzen w symulacji
    list_of_events = []
    # czas symulacji
    clock = 0
    # licznik pakieto - ktory pakiet obslugujemy
    packetsCounter = 0
    # tablica wszystkich pakietow ktore braly udzial w symulacji
    packets = []
    # liczba obsluzonych pakietow2
    number_of_serviced_packets = 0
    # liczba pakietow ktora chcemy przesymulowac
    number_of_packets_for_simulation = 1000000

    # wygenerowanie pierwszego pakietu w symulacji
    first_packet = PacketMM1(
        exp(time_of_service),
        exp(average_time_between_packets),
        -1,
        -1,
        packetsCounter)
    packets.append(first_packet)
    packetsCounter += 1
    # wziecie pierwszego pakietu do obslugi - planowanie zakonczenia obslugi pierwszego pakietu
    list_of_events.append(
        plan_event_finish_service(first_packet.number_of_packet,
                                  first_packet.time_of_arrive,
                                  first_packet.time_of_service,
                                  ))
    # zaplanowanie zdarzenia przyjscia drugiego pakietu
    time_next_packet = exp(average_time_between_packets)
    list_of_events.append(
        plan_event_come_next_packet(clock,
                                    packetsCounter,
                                    time_next_packet))
    packets.append(PacketMM1(exp(time_of_service), time_next_packet, -1, -1, packetsCounter))

    # sortowanie listy zdarzen po czasie
    list_of_events.sort(key=lambda Event: Event.time_of_event)

    packetsCounter += 1

    while number_of_serviced_packets < number_of_packets_for_simulation:
        # przejscie w symulacji do momentu czasu kolejnego zdarzenia
        clock = list_of_events[0].time_of_event
        # przypadek - przyszedl nowy pakiet
        if list_of_events[0].type_of_event.value == 0:
            # warunek aby nie wygenerowac wiecej pakietow niz chcemy dla symulacji
            if packetsCounter <= number_of_packets_for_simulation:
                # planujemy przyjscie kolejnego pakietu
                time_next_packet = exp(average_time_between_packets)
                # zdarzenie przyjscia kolejnego pakietu
                list_of_events.append(plan_event_come_next_packet(clock, packetsCounter, time_next_packet))
                packets.append(
                    PacketMM1(exp(time_of_service), clock + time_next_packet, -1, -1, packetsCounter))
                # dodanie pakietu do listy pakietow
                queue_of_packets.put(packets[packetsCounter - 1])
            # jesli serwer jest wolny - bierzemy pakiet do obslugi
            if not is_server_busy:
                is_server_busy = True
                currently_served_packet = queue_of_packets.get()
                # planujemy zdarzenie zakonczenia obslugi danego pakietu - bo bierzemy go do obslugi
                list_of_events.append(plan_event_finish_service(currently_served_packet.number_of_packet,
                                                                clock,
                                                                currently_served_packet.time_of_service))
                packets[currently_served_packet.number_of_packet].time_get_by_server = clock
            packetsCounter += 1
        # przypadek - zkonczono obsluge pakietu
        else:
            number_of_serviced_packets += 1
            currently_served_packet = packets[list_of_events[0].number_of_packet]
            packets[currently_served_packet.number_of_packet].time_finish_of_service = clock
            # przypadek w ktorym nie mamy pakietow w kolejce - ustawiamy stan serwera na wolny
            if queue_of_packets.empty():
                is_server_busy = False
            # przypadek w ktorym kolejka nie jest pusta - bierzemy kolejny pakiet do obslugi
            else:
                is_server_busy = True
                currently_served_packet = queue_of_packets.get()
                packets[currently_served_packet.number_of_packet].time_get_by_server = clock
                # planujemy zdarzenie zakonczenia obslugi kolejnego pakietu
                list_of_events.append(plan_event_finish_service(
                    currently_served_packet.number_of_packet,
                    currently_served_packet.time_get_by_server,
                    currently_served_packet.time_of_service))
        # zdejmujemy obsluzone zdarzenie z listy
        list_of_events.pop(0)
        # sortowanie listy zdarzen po czasie
        list_of_events.sort(key=lambda Event: Event.time_of_event)

    return calculate_statistics(number_of_packets_for_simulation, packets, time_of_service, average_time_between_packets
                                )


# funkcja odpowiedzialna za obliczenie wymaganych statystyk
def calculate_statistics(number_of_packets_for_simulation, packets, time_of_service,
                         average_time_between_packets):
    print("**********************")
    print("CALCULATING STATISTICS")
    print("**********************")
    # l - LAMBDA - intensywnosc naplywu klientow
    LAMBDA = 1 / average_time_between_packets
    # u - intensywnosc obslugi klientow - odwrotnosc czasu obslugi klienta
    u = 1 / time_of_service
    # p - srednie obciazenie systemu = LAMBDA/U
    p = LAMBDA / u
    if p != 1:
        # Sredni czas oczekiwania w systemie - kalkulacje teoretyczne
        teoretical_average_delay = p/(LAMBDA * (1 - p))
        print("AVERAGE TEORETICAL TIME OF WAITING IN QUEUE: ", teoretical_average_delay)
    else:
        print("AVERAGE TEORETICAL TIME OF WAITING IN QUEUE: INF")

    print("PRACTICAL CALCULATIONS")
    # Sredni czas oczekiwania w kolejce - kalkulacje praktyczne
    practical_average_time_of_delay = 0
    for i in range(0, number_of_packets_for_simulation - 1):
        practical_average_time_of_delay += (packets[i].time_finish_of_service -
                                  packets[i].time_of_arrive) / (number_of_packets_for_simulation - 1)
    print("AVERAGE PRACTICAL TIME OF WAITING IN SYSTEM ", practical_average_time_of_delay)
    confidance_delay = calculate_delays(packets)

    return Time(practical_average_time_of_delay, teoretical_average_delay, confidance_delay)


def calculate_delays(packets):
    opoznienia = []
    for i in packets:
        opoznienia.append(i.time_finish_of_service - i.time_of_arrive)
    confidence = st.norm.interval(alpha=0.95, loc=numpy.mean(opoznienia), scale=st.sem(opoznienia))
    confidence_delays = []
    for i in opoznienia:
        if confidence[0] <= i <=confidence[1]:
            confidence_delays.append(i)
    average_confidance_delay = 0
    for i in confidence_delays:
        average_confidance_delay += i
    average_confidance_delay /= len(confidence_delays)
    print("AVERAGE CONFIDENCE DELAY: " + str(average_confidance_delay))
    return average_confidance_delay

def start_mm1():
    #lista elementow od 0.5 do 6.0 z krokiem 0.1
    test_mm1 = numpy.arange(0.5, 6.1, 0.5)
    results1 = []
    for i in test_mm1:
        results1.append(start_mm1_simulation(i, 5))
    practical = []
    teoretical = []
    confidence = []
    for i in results1:
        practical.append(i.practical)
    for i in results1:
        teoretical.append(i.teoretical)
    for i in results1:
        confidence.append(i.confidence_interval)
    draw_plot(test_mm1, practical, teoretical, confidence, 6)



