from main import mm1_with_crash
import matplotlib.pylab as plt
import numpy as np

real_list = []
theo_list = []
#lambdas = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4]
lambdas = np.arange(0.5, 4, 0.1)
real_mean_list = []
theo_end_list = []

for l in lambdas:
    real_list= []
    theo_list= []
    print("L NOW: " + str(l))
    for c in range(0,20):
        print("C NOW: " + str(c))
        a, b = mm1_with_crash(c, l, 1000000)
        real_list.append(a)
        theo_list.append(b)
        #print(real_list)
        #print(theo_list)
    with open('output.txt', 'a+') as f:
        f.write(' \n \n \n LAMBDA {}'.format(l))
        f.write('\n REAL: \n')
        f.write(str(real_list))
        f.write('\n THEORETICAL: \n')
        f.write(str(theo_list))
        test = sum(real_list)
        f.write(' \n MEAN : \n')
        f.write(str(test / len(real_list)))
        real_mean_list.append(test/len(real_list))
        theo_end_list.append(theo_list[0])


plt.plot(lambdas, real_mean_list, label='practical')
plt.plot(lambdas, theo_end_list, label='teoretical')
plt.xlabel("Lambda 0.5 - 4 [1/s]")
plt.ylabel("Sredni czas oczekowania E[T]")
plt.legend()
plt.show()

