import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

HISTOGRAM_PATH = "../raw_data/SRR12479080/out.hist"


def load_data(path=HISTOGRAM_PATH):
    tsv = pd.read_csv(path, sep="\t", names=["Lengths", "Counts"], dtype=np.float64)
    return tsv


def plot_contigs_distribution():
    contig_lengths = load_data()
    total = contig_lengths[["Counts"]].sum()

    contig_lengths = contig_lengths.assign(
        wCounts=contig_lengths[["Counts"]] * 100 / total
    )

    mean = contig_lengths[["Lengths"]].T.dot(contig_lengths[["wCounts"]] / 100)
    std = math.sqrt(np.mean([(float(x) - mean) ** 2 for x in contig_lengths["Lengths"] ]))

    sns.histplot(
        contig_lengths,
        x="Lengths",
        weights="wCounts",
        kde=True,
    )
    plt.xlabel("Length (bp)")
    plt.ylabel("Frequency (%)")
    plt.vlines(mean, 0, 100, color="k")
    plt.vlines(mean - std, 0, 100, color="k", ls="--")
    plt.vlines(mean + std, 0, 100, color="k", ls="--")
    plt.grid()
    plt.savefig("../qc_reports/contig_lengths_distributions")


plot_contigs_distribution()
