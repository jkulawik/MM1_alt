from main import mm1_with_crash


real_list = []
theo_list = []
lambdas = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4]

for l in lambdas:
    real_list= []
    theo_list= []
    print("L NOW: " + str(l))
    for c in range(0,40):
        print("C NOW: " + str(c))
        a, b = mm1_with_crash(c, l, 100000)
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



print(real_list)
print(theo_list)
test = sum(real_list)
print(test/len(real_list))
