import random
import math

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