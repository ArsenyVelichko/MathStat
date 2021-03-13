from scipy.stats import norm, cauchy, laplace, poisson, uniform
import numpy as np
import matplotlib.pyplot as plt

def quart(list, p):
    idx = int(np.ceil(len(list) * p))
    return list[idx]

sampleSizes = [20, 100]
distrs = [(norm(0, 1), "normal"),
          (cauchy(0, 1), "cauchy"),
          (laplace(0, 1/np.sqrt(2)), "laplace"),
          (poisson(10), "poisson"),
          (uniform(-np.sqrt(3), 2 * np.sqrt(3)), "uniform")]

for distr in distrs:
    fig, axs = plt.subplots(2)
    for i in range(len(sampleSizes)):
        rvs = distr[0].rvs(sampleSizes[i])
        rvs.sort()
        axs[i].boxplot(rvs, vert=False)
        axs[i].set_ylabel(str(sampleSizes[i]), fontsize=8)

    fig.savefig('Boxplots/' + distr[1] + '.png')

table = open("TablesLab3_1.tex", 'w', encoding="utf-8")
table.writelines("\\begin{table}[h]\n"
                 "\centering\n"
                 "\\begin{tabular}{ |" + "c|" * 2 + " }\n"
                 "\hline\n"
                 "Выборка & Доля выбросов \\\\\n"
                 "\hline\n")
count = 1000;
for distr in distrs:
    for size in sampleSizes:
        outliersPercent = 0
        for i in range(count):
            rvs = distr[0].rvs(size)
            rvs.sort()
            Q1 = quart(rvs, 0.25)
            Q3 = quart(rvs, 0.75)
            X1 = Q1 - 1.5 * (Q3 - Q1)
            X2 = Q3 + 1.5 * (Q3 - Q1)
            outliers = [x for x in rvs if x < X1 or x > X2]
            outliersPercent += len(outliers) / len(rvs)
        outliersPercent /= count

        table.writelines(distr[1] + " $n = " + str(size) +
                         "$ & $" + str(round(outliersPercent, 4)) + "$\\\\\n"
                         "\hline\n")

table.writelines("\\end{tabular}\n"
                     "\caption{Эмпирическая доля выбросов}\n"
                     "\\end{table}\n\n")

table = open("TablesLab3_2.tex", 'w', encoding="utf-8")
table.writelines("\\begin{table}[h]\n"
                 "\centering\n"
                 "\\begin{tabular}{ |" + "c|" * 6 + " }\n"
                 "\hline\n"
                 "Распределение & $Q_1^T$ & $Q_3^T$ & $X_1^T$ & $X_2^T$ & $P^T$\\\\\n"
                 "\hline\n")
for distr in distrs:
    table.writelines(distr[1])

    Q1 = distr[0].ppf(0.25)
    table.writelines("&" + str(round(Q1, 4)))

    Q3 = distr[0].ppf(0.75)
    table.writelines("&" + str(round(Q3, 4)))

    X1 = Q1 - 1.5 * (Q3 - Q1)
    table.writelines("&" + str(round(X1, 4)))

    X2 = Q3 + 1.5 * (Q3 - Q1)
    table.writelines("&" + str(round(X2, 4)))

    P = distr[0].cdf(X1) + (1 - distr[0].cdf(X2))
    table.writelines("&" + str(round(P, 4)))

    table.writelines("\\\\\n\hline\n")

table.writelines("\\end{tabular}\n"
                     "\caption{Теоретическая вероятность выбросов}\n"
                     "\\end{table}\n\n")


