#!/usr/bin/python

import os
import sys

import itk

import matplotlib.pyplot as plt
from scipy import signal
import numpy as np

# Sampling frequency [Hz]
fs = 30e3

def VisualizeSpectra(rf_files):
    plt.figure(1, figsize=(20, 16))
    for rf_file in rf_files:
        image = itk.imread(rf_file)
        arr = itk.GetArrayViewFromImage(image)
        N = arr.shape[1]
        freq, Pxx = signal.periodogram(arr.transpose(),
                fs,
                window='hamming',
                detrend='linear',
                axis=0)
        Pxx = np.mean(Pxx, 1)
        plt.semilogy(freq, Pxx, label=rf_file)
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('Power spectral density [V**2/Hz]')
    plt.legend(loc='upper right')

    dirname = os.path.dirname(rf_files[0])
    plt.savefig(os.path.join(dirname, 'PowerSpectralDensity.png'), dpi=300)
    # plt.show()



if __name__ == '__main__':
    if len(sys.argv) > 1:
        rf_files = sys.argv[1:]
        VisualizeSpectra(rf_files)
    else:
        print("VisualizeSpectra [rf_file_1] [rf_file_2] [...]")
