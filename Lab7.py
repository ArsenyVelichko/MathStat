import numpy as np
import scipy.stats as stats
from TableWriter import TableWriter


def accurate_vals(sample):
    mu = np.mean(sample)
    sigma = np.std(sample)
    return mu, sigma


def intervals(sample):
    number = int(np.ceil(1.72 * len(sample) ** (1 / 3)))
    inters = []
    a_0 = -1.1
    a_n = 1.1
    inters.append((float('-inf'), a_0))
    a_k = a_0
    step = (a_n - a_0) / (number - 2)
    for i in range(1, number - 1):
        inters.append((a_k, a_k + step))
        a_k += step
    inters.append((a_k, float('inf')))
    return inters


def chi_2(F, sample):
    inters = intervals(sample)
    print('k = ', len(inters))
    mu, sigma = accurate_vals(sample)
    print('mu = ', mu, ' sigma = ', sigma)
    chi = [0 for i in range(len(inters))]
    p = chi.copy()
    n = p.copy()
    for i in range(len(inters)):
        p[i] = F.cdf(inters[i][1], loc=mu, scale=sigma) - F.cdf(inters[i][0], loc=mu, scale=sigma)
        n[i] = len([val for val in sample if inters[i][0] <= val < inters[i][1]])
        chi[i] = (n[i] - len(sample) * p[i]) ** 2 / (len(sample) * p[i])
    return inters, n, p, chi


def print_table(inters, n, p, chi, name):
    writer = TableWriter(name + ".tex")
    writer.begin(7)

    writer.append("$i$")
    writer.append("$\\Delta_i$")
    writer.append("$n_i$")
    writer.append("$p_i$")
    writer.append("$np_i$")
    writer.append("$n_i-np_i$")
    writer.append("$\\dfrac{(n_i-np_i)^2}{np_i}$")

    for i in range(len(inters)):
        a = str(round(inters[i][0], 2)) if inters[i][0] > -np.inf else '\\infty'
        b = str(round(inters[i][1], 2)) if inters[i][1] < np.inf else '\\infty'

        writer.append(str(i + 1))
        writer.append('$(' + a + ',\\;' +  b + ')$')
        writer.append(str(n[i]))
        writer.append(str(round(p[i], 4)))
        writer.append(str(round(sum(n) * p[i], 2)))
        writer.append(str(round(n[i] - sum(n) * p[i], 2)))
        writer.append(str(round(chi[i], 4)))

    writer.append("$\\Sigma$")
    writer.append("$--$")
    writer.append(str(sum(n)))
    writer.append(str(round(sum(p), 1)))
    writer.append(str(round(sum(n) * sum(p), 1)))
    writer.append("0")
    writer.append("$" + str(round(sum(chi), 2)) + "=\\chi^2_B$")

    writer.end("Проверка гипотезы $H_0$ на нормальной выборке")


#sample = stats.norm.rvs(size=100)
#sample = stats.uniform.rvs(scale=2 * np.sqrt(3), loc=-np.sqrt(3), size=20)
sample = stats.laplace.rvs(loc=0, scale= 1 / np.sqrt(2), size=20)
inters, n, p, chi = chi_2(stats.norm, sample)
print_table(inters, n, p, chi, 'laplace')
