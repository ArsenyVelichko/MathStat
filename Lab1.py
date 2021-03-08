from scipy.stats import norm, cauchy, laplace, poisson, uniform
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb

def drawNorm(size):
    fn = norm(0, 1)
    x = np.linspace(fn.ppf(0.01), fn.ppf(0.99), 1000)
    plt.plot(x, fn.pdf(x), 'k', lw=2)

    bins = fn.rvs(size=size)
    plt.tight_layout()
    sb.histplot(bins, stat="density", alpha=0.5, color="red")


def drawCauchy(size):
    fc = cauchy(0, 1)
    x = np.linspace(fc.ppf(0.01), fc.ppf(0.99), 1000)
    plt.plot(x, fc.pdf(x), 'k', lw=2)

    bins = fc.rvs(size=size)
    plt.tight_layout()
    sb.histplot(bins, stat="density", alpha=0.5, color="blue")


def drawLaplace(size):
    fl = laplace(0, 1 / np.sqrt(2))
    x = np.linspace(fl.ppf(0.01), fl.ppf(0.99), 1000)
    plt.plot(x, fl.pdf(x), 'k', lw=2)

    bins = fl.rvs(size=size)
    plt.tight_layout()
    sb.histplot(bins, stat="density", alpha=0.5, color="green")


def drawPoisson(size):
    fp = poisson(10)
    x = np.arange(fp.ppf(0.01), fp.ppf(0.99))
    plt.plot(x, fp.pmf(x), 'ok', lw=2)

    bins = fp.rvs(size=size)
    plt.tight_layout()
    sb.histplot(bins, stat="density", alpha=0.5, color="yellow")


def drawUniform(size):
    fu = uniform(-np.sqrt(3), np.sqrt(3))
    x = np.linspace(fu.ppf(0.01), fu.ppf(0.99), 1000)
    plt.plot(x, fu.pdf(x), 'k', lw=2)

    bins = fu.rvs(size=size)
    plt.tight_layout()
    sb.histplot(bins, stat="density", alpha=0.5, color="orange", label="density")


sampleSizes = [10, 50, 1000]
distrPlots = [[drawNorm, "normal"],
              [drawCauchy, "cauchy"],
              [drawLaplace, "laplace"],
              [drawPoisson, "poisson"],
              [drawUniform, "uniform"]]

for plot in distrPlots:
    fig = plt.figure()

    for i in range(len(sampleSizes)):
        axes = fig.add_subplot(len(sampleSizes), 1, i + 1)
        axes.set_title('Samples number: ' + str(sampleSizes[i]))
        axes.set_ylabel('Density')
        plot[0](sampleSizes[i])
        plt.savefig('Graphics/' + plot[1] + '.png')