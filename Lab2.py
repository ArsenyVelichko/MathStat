from scipy.stats import norm, cauchy, laplace, poisson, uniform
import numpy as np


def extrHalfSum(list):
    return (list[0] + list[-1]) / 2


def quart(list, p):
    idx = int(np.ceil(len(list) * p))
    return list[idx]


def quartHalfSum(list):
    return (quart(list, 0.25) + quart(list, 0.75)) / 2


def cutMean(list):
    n = len(list)
    r = int(n / 4)
    sum = np.sum(np.split(list, [r + 1, n - r + 1])[1])
    return sum / (n - 2 * r)


n = 1000
sampleSizes = [10, 100, 1000]
distrs = [(norm(0, 1), 'Нормальное распределение'),
          (cauchy(0, 1), 'Распределение Коши'),
          (laplace(0, 1/np.sqrt(2)), 'Распределение Лапласа'),
          (poisson(10), 'Распределение Пуассона'),
          (uniform(-np.sqrt(3), np.sqrt(3)), 'Равномерное распределение')]

table = open("Tables.tex", 'w', encoding="utf-8")
for distr in distrs:

    table.writelines("\\begin{table}[h]\n"
                     "\centering\n"
                     "\\begin{tabular}{ |" + "c|" * 6 + " }\n"
                     "\hline\n"
                     "& $\overline{x}$ & $med\, x$ & $z_R$ & $z_Q$ & $z_{tr}$ \\\\\n"
                     "\hline\n")

    for size in sampleSizes:
        table.writelines("n = " + str(size) + " & & & & &\\\\\n"
                         "\hline\n")

        statValues = [([], np.mean),
                      ([], np.median),
                      ([], extrHalfSum),
                      ([], quartHalfSum),
                      ([], cutMean)]

        for i in range(n):
            sample = distr[0].rvs(size)
            sample.sort()

            for statValue in statValues:
                statValue[0].append(statValue[1](sample))

        EList = [np.mean(pair[0]) for pair in statValues]
        ERecord = "$E(z)$"
        for value in EList:
            ERecord += " & $" + str(round(value, 6)) + "$"
        ERecord += "\\\\\n\hline\n"
        table.writelines(ERecord)

        DList = [np.std(pair[0]) ** 2 for pair in statValues]
        DRecord = "$D(z)$"
        for value in DList:
            DRecord += " & $" + str(round(value, 6)) + "$"
        DRecord += "\\\\\n\hline\n"
        table.writelines(DRecord)

    table.writelines("\\end{tabular}\n"
                     "\caption{" + distr[1] +"}\n"
                     "\\end{table}\n\n")