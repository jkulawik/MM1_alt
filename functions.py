import random
import math
import matplotlib.pyplot as plt
import scipy.stats as st
import numpy


# ponizsza funkcja generuje liczbe rozkladu wykladniczego na podstawie zadanej sredniej
def exp(mean):
    # random generuje liczbe pseudolosowa z przedzialu [0.0, 1.0)
    losowa = random.random()
    # random.random losuje liczbe z przedzialu [0.0, 1.0),
    # dla 0 dostaniemy -inf wiec tak nie moze byc - losujemy ponownie
    while losowa == 0:
        losowa = random.random()
    # na podstawie wzoru odwrotnej dystrybuanty rozkladu wykladniczego tzn.
    # F^(-1)(u)=(-1/Lambda)*ln(w), gdzie w - liczba z przedzialu (0,1) (losowa) o rozkladzie jednostajnym
    return float(-1.0) * float(mean) * math.log(losowa)


def draw_plot(x, practical, teoretical, confidence_avg, confidence_min, confidence_max, LAMBDA):
    plt.plot(x, practical, label='practical')
    plt.plot(x, teoretical, label='teoretical')
    plt.plot(x, confidence_avg, label='srednia przedzialu ufnosci')
    plt.plot(x, confidence_min, label='minimum przedzialu ufnosci')
    plt.plot(x, confidence_max, label='maksimum przedzialu ufnosci')
    plt.xlabel("Lambda 0.5 - "+str(LAMBDA)+".0 [1/s]")
    plt.ylabel("Sredni czas oczekowania E[T]")
    plt.legend()
    plt.show()


def write_output_to_file(real_list, theo_list, l, avg_practical_delay):
    with open('output.txt', 'a+') as f:
        f.write(' \n \n \n LAMBDA {}'.format(l))
        f.write('\n REAL: \n')
        f.write(str(real_list))
        f.write('\n THEORETICAL: \n')
        f.write(str(theo_list))

        f.write(' \n MEAN : \n')
        f.write(avg_practical_delay)


def calculate_confidence(opoznienia, range):
    confidence = st.norm.interval(alpha=range, loc=numpy.mean(opoznienia), scale=st.sem(opoznienia))
    confidence_delays = []
    for i in opoznienia:
        if confidence[0] <= i <= confidence[1]:
            confidence_delays.append(i)
    average_confidance_delay = 0
    for i in confidence_delays:
        average_confidance_delay += i
    average_confidance_delay /= len(confidence_delays)
    print("AVERAGE CONFIDENCE DELAY: " + str(average_confidance_delay))
    return average_confidance_delay, confidence[0], confidence[1]
