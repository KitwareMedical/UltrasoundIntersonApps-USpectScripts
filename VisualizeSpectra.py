#!/usr/bin/python

import os

import itk

import matplotlib.pyplot as plt
from scipy import signal
import numpy as np
import argparse

def VisualizeSpectra(rf_files, freq_sampling):
    plt.figure(1, figsize=(20, 16))
    for rf_file in rf_files:
        image = itk.imread(rf_file)
        arr = itk.GetArrayViewFromImage(image)
        freq, Pxx = signal.periodogram(arr.transpose(),
                freq_sampling,
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
    plt.show()



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Visualize Power Spectra.')
    parser.add_argument('rf_files', metavar='N', nargs='+', help='rf data files')
    parser.add_argument('--freq-sampling', type=float, default=30e3,
        help='sampling frequency [Hz]')
    args = parser.parse_args()
    VisualizeSpectra(args.rf_files, args.freq_sampling)
