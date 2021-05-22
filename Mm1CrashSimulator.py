from functions import exp
import random
from models import Event, Packet, CrashOn
from functions import write_output_to_file
from functions import draw_plot
from functions import calculate_confidence


def start_crash_simulation(packets_num, replicates, confidence_range):
    real_list = []
    theo_list = []
    lambdas = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4]
    #lambdas = [1, 2, 3, 4]
    theoretical = []
    practical = []
    confidence = []

    for l in lambdas:
        real_list = []
        theo_list = []
        conf_list = []
        print("L NOW: " + str(l))
        for c in range(0, replicates):
            print("C NOW: " + str(c))
            a, b, delay = mm1_with_crash(c, l, packets_num)
            real_list.append(a)
            theo_list.append(b)
            conf_list.append(calculate_confidence(delay, confidence_range))
        test = sum(real_list)
        avg_practical_delay = str(test / len(real_list))
        write_output_to_file(real_list=real_list, theo_list=theo_list, l=l, avg_practical_delay=avg_practical_delay)
        theoretical.append(theo_list[0])
        practical.append(test / len(real_list))
        confidence.append(sum(conf_list)/len(conf_list))
    print(real_list)
    print(theo_list)
    test = sum(real_list)
    print(test/len(real_list))

    draw_plot(x=lambdas, practical=practical, teoretical=theoretical, confidence=confidence, LAMBDA=4)


def mm1_with_crash(seed, lambda_in, max_packets):
    random.seed(seed)
    # sredni czas obslugi pakietu przez serwer
    time_of_service = 0.125
    # sredni odstep pomiedzy pakietami 0.5 - 4
    LAMBDA = lambda_in
    average_time_between_packets = 1 / LAMBDA
    # czy serwer jest zajety
    is_server_busy = True
    # czy serwer ma awarie
    is_server_dead = False
    # sredni czas dzialania serwera = 40
    c_on = 40
    # sredni czas NIE dzialania serwera = 35
    c_off = 35
    event_list = []
    clock = 0
    # licznik pakieto - ktory pakiet obslugujemy
    packetsCounter = 0
    # tablica wszystkich pakietow ktore braly udzial w symulacji
    packets = []
    packets_buffor = []
    # liczba obsluzonych pakietow
    number_of_serviced_packets = 0
    # liczba pakietow ktora chcemy przesymulowac
    number_of_packets_for_simulation = max_packets

    first_packet = Packet(time_of_service=exp(time_of_service), time_of_arrival=exp(average_time_between_packets))
    packets.append(first_packet)
    packets_buffor.append(first_packet)
    # wziecie pierwszego pakietu do obslugi - planowanie zakonczenia obslugi pierwszego pakietu
    packet_end_event = Event(time=exp(time_of_service), obj=first_packet, type='end_packet')
    # zaplanowanie zdarzenia przyjscia drugiego pakietu
    event_list.append(packet_end_event)
    time_next_packet = exp(average_time_between_packets)
    next_packet = Packet(time_of_arrival=time_next_packet, time_of_service=exp(time_of_service))
    event_list.append(Event(time=time_next_packet, obj=next_packet, type='new_packet'))
    packets.append(next_packet)
    # zaplanowanie pierwszej awarii
    crash_duration1 = exp(c_off)
    crash = CrashOn(crash_duration1)
    event_list.append(Event(time=exp(c_on), obj=crash, type='crash_on'))
    # sortowanie listy zdarzen po czasie
    event_list.sort(key=lambda Event: Event.time)
    crash_list = []
    packet_delay_list = []
    time_of_service_list = []
    buffer_size_list = []

    packetsCounter += 1

    while number_of_serviced_packets < number_of_packets_for_simulation:
        if number_of_serviced_packets % 10000 == 0:
            # print(f'{100*number_of_serviced_packets/number_of_packets_for_simulation} %')
            pass
        event_list.sort(key=lambda Event: Event.time)
        event = event_list.pop(0)
        clock = event.time
        #print(f'TIME: {clock} EVENT: {event.type}')
        if event.type == 'end_packet':
            number_of_serviced_packets += 1
            curr_p = event.obj
            curr_p.finish_of_service = clock
            # print(f'PROCESSED ARRIVE: {curr_p.time_of_arrival} AT: {curr_p.finish_of_service}')
            #print(f'END PACKET {curr_p.time_of_arrival}')
            if len(packets_buffor) == 0:
                is_server_busy = False
            elif not is_server_dead:
                is_server_busy = True
                curr_p = packets_buffor.pop(0)
                event_list.append(Event(time=clock + curr_p.time_of_service, type='end_packet', obj=curr_p))
        elif event.type == 'new_packet':
            # print('NEW PACKET')
            # obecny pakiet trafia na bufor
            packets_buffor.append(event.obj)
            buffer_size_list.append(len(packets_buffor))
            # nastepny pakiet
            t_delay = exp(average_time_between_packets)
            packet_delay_list.append(t_delay)
            tof_temp = exp(time_of_service)
            time_of_service_list.append(tof_temp)
            next_p = Packet(time_of_arrival=clock + t_delay, time_of_service=tof_temp)
            event_list.append(Event(time=next_p.time_of_arrival, obj=next_p, type='new_packet'))
            packets.append(next_p)
            # jesli wszystko ok to przetwarzamy najstarszy pakiet
            if not is_server_busy and not is_server_dead:
                curr_p = packets_buffor.pop(0)
                event_list.append(Event(time=clock + curr_p.time_of_service, type='end_packet', obj=curr_p))
        elif event.type == 'crash_on':

            is_server_dead = True
            curr_crash = event.obj
            #print(f'CRASH ON {clock} FOR {curr_crash.duration}')
            event_list.append(Event(time=clock + curr_crash.duration, type='crash_off', obj=None))
            crash_list.append(curr_crash.duration)
            for a in event_list:
                if a.type == 'end_packet':
                    a.time += curr_crash.duration
        elif event.type == 'crash_off':
            #print(f'CRASH OFF {clock}')
            is_server_dead = False
            crash_duration = exp(c_off)
            curr_crash = CrashOn(crash_duration)
            event_list.append(Event(time=exp(c_on) + clock, obj=curr_crash, type='crash_on'))

    sum_time = 0
    sum_processed = 0
    delays_list = []
    packets_less = packets[round(len(packets)*0.1):]
    for p in packets:
        if p.finish_of_service != 0:
            sum_time += (p.finish_of_service - p.time_of_arrival)
            delays_list.append((p.finish_of_service - p.time_of_arrival))
            sum_processed += 1
    average = sum_time/sum_processed

    propability_off = c_off / (c_off + c_on)
    propability_on = c_on / (c_off + c_on)

    LAMBDA = 1 / average_time_between_packets
    #u - intensywnosc obslugi klientow - odwrotnosc czasu obslugi klienta
    u = 1 / time_of_service
    # p - srednie obciazenie systemu = LAMBDA/U
    p = LAMBDA / (u*propability_on)
    if p != 1:
        # Sredni czas oczekiwania w systemie - kalkulacje teoretyczne
        teoretical_average_delay = (p + LAMBDA*c_off*propability_off) / (LAMBDA * (1 - p))
        return average, teoretical_average_delay, delays_list
    else:
        return average, None, None




