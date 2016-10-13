#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv

import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D


class Algorithm:
    source_file = ""
    label = ""
    color = ""

    def __init__(self, source_file, label, color):
        self.source_file = source_file
        self.label = label
        self.color = color


OUTPUT_FILENAME = 'myplot.pdf'
Y_AXIS_LABEL = "Odsetek wygranych gier"
X_AXIS_LABEL = "Rozegranych gier"
ALGORITHMS = [Algorithm('2cel.csv', '2-Coev', 'purple'),
              Algorithm('2cel-rs.csv', '2-Coev-RS', 'red'),
              Algorithm('cel.csv', '1-Coev', 'black'),
              Algorithm('cel-rs.csv', '1-Coev-RS', 'green'),
              Algorithm('rsel.csv', '1-Evol-RS', 'blue')]


def read_data(filename):
    with open('{filename}'.format(filename=filename), 'rb') as csvfile:
        x, y = [], []
        raw_data = csv.reader(csvfile, delimiter=',', quotechar='|')
        data = list(raw_data)[1:]

        for row in list(data):
            x.append(row[1])
            values = row[2:]

            values = map(float, values)
            y.append(reduce(lambda a, b: a + b, values) / len(values))

        return x[1:], y[1:]


def main():
    for algorithm in ALGORITHMS:
        visualize_algorithm_results(algorithm)

    render_plot()


def visualize_algorithm_results(algorithm):
    x, y = read_data(algorithm.source_file)
    line, = plt.plot(x, y, label=algorithm.label, color=algorithm.color)
    plt.legend(handler_map={line: HandlerLine2D(numpoints=4)})


def render_plot():
    plt.xlabel(X_AXIS_LABEL)
    plt.ylabel(Y_AXIS_LABEL)
    plt.legend(bbox_to_anchor=(1.00, 0), loc=4, borderaxespad=0.)
    plt.xlim([0, 500000])
    plt.savefig(OUTPUT_FILENAME)
    plt.close()


if __name__ == '__main__':
    main()
