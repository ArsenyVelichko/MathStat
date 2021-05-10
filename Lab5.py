import scipy.stats as stats
import matplotlib.pyplot as plt
import numpy as np
from TableWriter import TableWriter
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms


def calc_pirson(selection):
    return stats.pearsonr(selection[:, 0], selection[:, 1])[0]


def calc_spirman(selection):
    return stats.spearmanr(selection)[0]


def calc_square(selection):
    count = 0
    mean_point = np.median(selection, axis=0)
    for point in selection:
        translated = point - mean_point
        if translated[0] * translated[1] > 0:
            count += 1
        else:
            count -= 1
    return count / len(selection)


def get_2d_selection(size, weight):
    return stats.multivariate_normal(cov=[[1, weight], [weight, 1]]).rvs(size)


def get_mix_selection(size):
    first_selection = stats.multivariate_normal(cov=[[1, 0.9], [0.9, 1]]).rvs(size)
    second_selection = stats.multivariate_normal(cov=[[10, -0.9], [-0.9, 10]]).rvs(size)
    return 0.9 * first_selection + 0.1 * second_selection


def mean_str(arr):
    mean_val = round(np.mean(arr), 4)
    return str(mean_val)


def square_mean_str(arr):
    square_arr = np.array([val * val for val in arr])
    return mean_str(square_arr)


def dispersion_str(arr):
    dispersion = round(np.var(arr), 4)
    return str(dispersion)


def confidence_ellipse(x, y, ax, n_std=3.0):
    cov = np.cov(x, y)
    pearson = cov[0, 1]/np.sqrt(cov[0, 0] * cov[1, 1])

    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    ellipse = Ellipse((0, 0),
                      width=ell_radius_x * 2,
                      height=ell_radius_y * 2,
                      facecolor='none',
                      edgecolor='k',
                      linestyle='--')

    scale_x = np.sqrt(cov[0, 0]) * n_std
    mean_x = np.mean(x)

    scale_y = np.sqrt(cov[1, 1]) * n_std
    mean_y = np.mean(y)

    transf = transforms.Affine2D() \
        .rotate_deg(45) \
        .scale(scale_x, scale_y) \
        .translate(mean_x, mean_y)

    ellipse.set_transform(transf + ax.transData)
    ax.scatter(x, y)
    return ax.add_patch(ellipse)


def write_2d_selection(sizes, iters, weights, writer):
    for size in sizes:
        writer.begin(4)

        fig, axes = plt.subplots(1, len(weights))

        for i in range(len(weights)):
            writer.append("$\\rho = " + str(weights[i]) + " $")

            writer.append("$ r $")
            writer.append("$ r_S $")
            writer.append("$ r_Q $")

            pirson_arr = np.zeros(iters)
            spirman_arr = np.zeros(iters)
            square_arr = np.zeros(iters)

            for j in range(iters):
                selection = get_2d_selection(size, weights[i])

                pirson_arr[j] = calc_pirson(selection)
                spirman_arr[j] = calc_spirman(selection)
                square_arr[j] = calc_square(selection)

            writer.append("$ E(z) $")
            writer.append(mean_str(pirson_arr))
            writer.append(mean_str(spirman_arr))
            writer.append(mean_str(square_arr))

            writer.append("$ E(z^2) $")
            writer.append(square_mean_str(pirson_arr))
            writer.append(square_mean_str(spirman_arr))
            writer.append(square_mean_str(square_arr))

            writer.append("$ D(z) $")
            writer.append(dispersion_str(pirson_arr))
            writer.append(dispersion_str(spirman_arr))
            writer.append(dispersion_str(square_arr))

            if i != len(weights) - 1:
                writer.next_line()

            confidence_ellipse(selection[:, 0], selection[:, 1], axes[i])
            axes[i].set_title("$ \\rho = " + str(weights[i]) + " $")

        fig.savefig("Ellipses/" + str(size))
        writer.end("Двумерное нормальное распределение, $ n = " + str(size) + " $")


def write_mix_selection(sizes, iters, writer):
    writer.begin(4)

    for size in sizes:
        writer.append("$ n = " + str(size) + " $")

        writer.append("$ r $")
        writer.append("$ r_S $")
        writer.append("$ r_Q $")

        pirson_arr = np.zeros(iters)
        spirman_arr = np.zeros(iters)
        square_arr = np.zeros(iters)

        for i in range(iters):
            selection = get_mix_selection(size)

            pirson_arr[i] = calc_pirson(selection)
            spirman_arr[i] = calc_spirman(selection)
            square_arr[i] = calc_square(selection)

        writer.append("$ E(z) $")
        writer.append(mean_str(pirson_arr))
        writer.append(mean_str(spirman_arr))
        writer.append(mean_str(square_arr))

        writer.append("$ E(z^2) $")
        writer.append(square_mean_str(pirson_arr))
        writer.append(square_mean_str(spirman_arr))
        writer.append(square_mean_str(square_arr))

        writer.append("$ D(z) $")
        writer.append(dispersion_str(pirson_arr))
        writer.append(dispersion_str(spirman_arr))
        writer.append(dispersion_str(square_arr))

        if size != sizes[-1]:
            writer.next_line()

    writer.end("Смесь нормальных распределений")


if __name__ == '__main__':
    writer = TableWriter("Lab5Results.tex")

    sizes = [20, 60, 100]
    weights = [0, 0.5, 0.9]
    iters = 1000

    write_2d_selection(sizes, iters, weights, writer)
    write_mix_selection(sizes, iters, writer)



