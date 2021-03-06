import scipy.stats as stats
import matplotlib.pyplot as plt
import numpy as np

def least_squares(x, y):
    xy = np.array([x[i] * y[i] for i in range(len(x))])
    x_2 = np.array([x[i] * x[i] for i in range(len(x))])
    b_1 = (np.mean(xy) - np.mean(x) * np.mean(y)) / (np.mean(x_2) - np.mean(x) ** 2)
    b_0 = np.mean(y) - np.mean(x) * b_1
    return b_1, b_0

def quantile(sample, p):
    pn = p * sample.size
    if (pn == int(pn)):
        return sample[int(pn)]
    return sample[int(pn) + 1]


def least_modules(x, y):
    k = 1.491
    n = len(x)
    q_y = (quantile(y, 3 / 4) - quantile(y, 1 / 4)) / k
    q_x = (quantile(x, 3 / 4) - quantile(x, 1 / 4)) / k
    r_q = 0
    med_x = np.median(x)
    med_y = np.median(y)
    for i in range(n):
        r_q += np.sign(x[i] - med_x) * np.sign(y[i] - med_y)
    r_q /= n
    b_1 = r_q * q_y / q_x
    b_0 = med_y - b_1 * med_x
    return b_1, b_0


x = np.linspace(-1.8, 2, 20)
e = stats.norm.rvs(0, 1, size=20)
y = 2 * x + 2
y_1 = y + e
e = stats.norm.rvs(0, 1, size=20)
y_2 = y + e
y_2[0] += 10
y_2[-1] -= 10

a_1, b_1 = least_squares(x, y_1)
a_2, b_2 = least_modules(x, y_1)
l_1 = a_1 * x + b_1
l_2 = a_2 * x + b_2
fig, axis = plt.subplots()
axis.scatter(x, y_1, color='k', facecolor='none', label='Выборка')
axis.plot(x, y, 'r', label='Модель$')
axis.plot(x, l_1, 'b', label='МНК')
axis.plot(x, l_2, 'g', label='МНМ')
axis.legend(loc='upper left')
fig.savefig('Regression/straight')
file = open('coefs.txt', 'w')
file.write('a_1 = ' + str(a_1) + ', b_1 = ' + str(b_1))
file.write('\na_2 = ' + str(a_2) + ', b_2 = ' + str(b_2))

a_1, b_1 = least_squares(x, y_2)
a_2, b_2 = least_modules(x, y_2)
l_1 = a_1 * x + b_1
l_2 = a_2 * x + b_2
fig, axis = plt.subplots()
axis.scatter(x, y_2, color='k', facecolor='none', label='Выборка')
axis.plot(x, y, 'r', label='Модель$')
axis.plot(x, l_1, 'b', label='МНК')
axis.plot(x, l_2, 'g', label='МНМ')
axis.legend(loc='upper left')
fig.savefig('Regression/perm')
file.write('\n\na_1 = ' + str(a_1) + ', b_1 = ' + str(b_1))
file.write('\na_2 = ' + str(a_2) + ', b_2 = ' + str(b_2))
file.close()

plt.show()