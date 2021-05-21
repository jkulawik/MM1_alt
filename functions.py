import random
import math
import matplotlib.pyplot as plt


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


def draw_plot(x, practical, teoretical, confidence, LAMBDA):
    plt.plot(x, practical, label='practical')
    plt.plot(x, teoretical, label='teoretical')
    plt.plot(x, confidence, label='srednia przedzialu ufnosci')
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
