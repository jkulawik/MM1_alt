import random
import queue
from models import PacketMM1
from models import PacketEvent
import numpy
from models import Time
from functions import calculate_confidence
from TypeOfEvent import TypeOfEvent
from functions import exp
from functions import draw_plot


# ponizsza f-cja odpowiada za generacje zdarzenia zakonczenia obslugi pakietu przez serwer
def plan_event_finish_service(number_of_packet, time_get_by_server, time_of_service):
    return PacketEvent(TypeOfEvent.END_OF_SERVICE,
                       number_of_packet,
                       time_get_by_server + time_of_service)


# ponizsza f-cja odpowiada za generacje zdarzenia przyjscia kolejnego pakietu
def plan_event_come_next_packet(clock, number_of_packet, time_of_next_packet):
    return PacketEvent(TypeOfEvent.PACKET_ARRIVAL, number_of_packet, clock + time_of_next_packet)


def start_mm1_simulation(LAMBDA, seed, packets_num, confidence_range):
    random.seed(seed)
    print("*************************")
    print("MM1 SIMULATION STARTED!!!")
    print("*************************")
    # sredni czas obslugi pakietu przez serwer
    time_of_service = 0.125
    # sredni odstep pomiedzy pakietami 0.5 - 6
    # LAMBDA = float(input("Input a LAMBDA please (0.5-6)"))
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
    packets_counter = 0
    # tablica wszystkich pakietow ktore braly udzial w symulacji
    packets = []
    # liczba obsluzonych pakietow2
    number_of_serviced_packets = 0
    # liczba pakietow ktora chcemy przesymulowac
    number_of_packets_for_simulation = packets_num

    # wygenerowanie pierwszego pakietu w symulacji
    first_packet = PacketMM1(
        exp(time_of_service),
        exp(average_time_between_packets),
        -1,
        -1,
        packets_counter)
    packets.append(first_packet)
    packets_counter += 1
    # wziecie pierwszego pakietu do obslugi - planowanie zakonczenia obslugi pierwszego pakietu
    list_of_events.append(
        plan_event_finish_service(first_packet.number_of_packet,
                                  first_packet.time_of_arrival,
                                  first_packet.time_of_service,
                                  ))
    # zaplanowanie zdarzenia przyjscia drugiego pakietu
    time_next_packet = exp(average_time_between_packets)
    list_of_events.append(
        plan_event_come_next_packet(clock,
                                    packets_counter,
                                    time_next_packet))
    packets.append(PacketMM1(exp(time_of_service), time_next_packet, -1, -1, packets_counter))

    # sortowanie listy zdarzen po czasie
    list_of_events.sort(key=lambda Event: Event.time_of_event)

    packets_counter += 1

    while number_of_serviced_packets < number_of_packets_for_simulation:
        # przejscie w symulacji do momentu czasu kolejnego zdarzenia
        clock = list_of_events[0].time_of_event
        # przypadek - przyszedl nowy pakiet
        if list_of_events[0].type_of_event.value == 0:
            # warunek aby nie wygenerowac wiecej pakietow niz chcemy dla symulacji
            if packets_counter <= number_of_packets_for_simulation:
                # planujemy przyjscie kolejnego pakietu
                time_next_packet = exp(average_time_between_packets)
                # zdarzenie przyjscia kolejnego pakietu
                list_of_events.append(plan_event_come_next_packet(clock, packets_counter, time_next_packet))
                packets.append(
                    PacketMM1(exp(time_of_service), clock + time_next_packet, -1, -1, packets_counter))
                # dodanie pakietu do listy pakietow
                queue_of_packets.put(packets[packets_counter - 1])
            # jesli serwer jest wolny - bierzemy pakiet do obslugi
            if not is_server_busy:
                is_server_busy = True
                currently_served_packet = queue_of_packets.get()
                # planujemy zdarzenie zakonczenia obslugi danego pakietu - bo bierzemy go do obslugi
                list_of_events.append(plan_event_finish_service(currently_served_packet.number_of_packet,
                                                                clock,
                                                                currently_served_packet.time_of_service))
                packets[currently_served_packet.number_of_packet].time_get_by_server = clock
            packets_counter += 1
        # przypadek - zkonczono obsluge pakietu
        else:
            number_of_serviced_packets += 1
            currently_served_packet = packets[list_of_events[0].number_of_packet]
            packets[currently_served_packet.number_of_packet].time_end_of_service = clock
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

    return calculate_statistics(
        number_of_packets_for_simulation, packets, time_of_service,
        average_time_between_packets, confidence_range)


# funkcja odpowiedzialna za obliczenie wymaganych statystyk
def calculate_statistics(number_of_packets_for_simulation, packets, time_of_service,
                         average_time_between_packets, confidence_range):
    print("**********************")
    print("CALCULATING STATISTICS")
    print("**********************")
    # l - LAMBDA - intensywnosc naplywu klientow
    LAMBDA = 1 / average_time_between_packets
    # u - intensywnosc obslugi klientow - odwrotnosc czasu obslugi klienta
    u = 1 / time_of_service
    # p - srednie obciazenie systemu = LAMBDA/U
    p = LAMBDA / u
    teoretical_average_delay = 0
    if p != 1:
        # Sredni czas oczekiwania w systemie - kalkulacje teoretyczne
        teoretical_average_delay = p/(LAMBDA * (1 - p))
        print("AVERAGE TEORETICAL TIME OF WAITING IN QUEUE: ", teoretical_average_delay)
    else:
        print("AVERAGE TEORETICAL TIME OF WAITING IN QUEUE: INF")

    print("PRACTICAL CALCULATIONS")
    # rozbieg
    # packets_less = packets[round(len(packets) * 0.1):]
    # Sredni czas oczekiwania w kolejce - kalkulacje praktyczne
    practical_average_time_of_delay = 0
    for i in packets:
        delay = i.time_end_of_service - i.time_of_arrival
        if delay > 0:
            practical_average_time_of_delay += delay
    practical_average_time_of_delay /= (number_of_packets_for_simulation - 1)
    print("AVERAGE PRACTICAL TIME OF WAITING IN SYSTEM ", practical_average_time_of_delay)
    delays = []
    for i in packets:
        delay = i.time_end_of_service - i.time_of_arrival
        if delay > 0:
            delays.append(i.time_end_of_service - i.time_of_arrival)
    confidence_delay, min_delay, max_delay = calculate_confidence(delays, confidence_range)
    return Time(practical_average_time_of_delay, teoretical_average_delay, confidence_delay, min_delay, max_delay)


def start_mm1(packets_num, repetitions, confidence_range):
    # lista elementow od 0.5 do 6.0 z krokiem 0.1
    lambdas = numpy.arange(0.5, 6.1, 0.5)
    theoretical = []
    practical = []
    confidence_avg = []
    confidence_minimal = []
    confidence_maksimal = []

    for i in lambdas:
        real_list = []
        theo_list = []
        conf_list = []
        conf_list_min = []
        conf_list_max = []
        print("L NOW: " + str(i))
        for j in range(0, repetitions):
            print("C NOW: " + str(j))
            temp = start_mm1_simulation(LAMBDA=i, seed=j, packets_num=packets_num, confidence_range=confidence_range)
            real_list.append(temp.practical)
            theo_list.append(temp.theoretical)
            conf_list.append(temp.confidence_interval)
            conf_list_min.append(temp.confidence_min)
            conf_list_max.append(temp.confidence_max)
        test = sum(real_list)
        # avg_practical_delay = str(test / len(real_list))
        theoretical.append(theo_list[0])
        practical.append(test / len(real_list))
        confidence_avg.append(sum(conf_list) / len(conf_list))
        confidence_minimal.append(sum(conf_list_min) / len(conf_list_min))
        confidence_maksimal.append(sum(conf_list_max) / len(conf_list_max))
    test = sum(real_list)
    print(test / len(real_list))
    draw_plot(x=lambdas, practical=practical, teoretical=theoretical, confidence_avg=confidence_avg,
              confidence_min=confidence_minimal, confidence_max=confidence_maksimal, LAMBDA=6)
