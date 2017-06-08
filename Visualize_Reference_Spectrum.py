#!/usr/bin/python

import os

import itk

import matplotlib.pyplot as plt
from scipy import signal
import numpy as np
import argparse

def VisualizeReferenceSpectrum(rf_files, freq_sampling):
    plt.figure(1, figsize=(5, 4))
    handles = []
    labels = []
    for rf_file in rf_files:
        ComponentType = itk.ctype('float')
        Dimension = 2
        ImageType = itk.VectorImage[ComponentType, Dimension]
        reader = itk.ImageFileReader[ImageType].New(FileName=rf_file)
        reader.Update()
        image = reader.GetOutput()
        arr = itk.GetArrayFromImage(image)
        arr /= arr[:,:,arr.shape[2]/10:].max()
        freq = np.linspace(freq_sampling / 2 / arr.shape[2], freq_sampling / 2, arr.shape[2])
        ax = plt.plot(freq, arr[0, 0, :].ravel(), label=rf_file)
        handles.append(ax[0])
        labels.append(rf_file)
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('Power spectral density')
    plt.figlegend(handles, labels, 'upper right')
    plt.ylim(0.0, 1.0)

    dirname = os.path.dirname(rf_files[0])
    plt.savefig(os.path.join(dirname, 'ReferenceSpectrum.png'), dpi=300)
    plt.show()



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Visualize Reference Power Spectrum.')
    parser.add_argument('rf_files', metavar='N', nargs='+', help='rf data files')
    parser.add_argument('--freq-sampling', type=float, default=30e3,
        help='sampling frequency [Hz]')
    args = parser.parse_args()
    VisualizeReferenceSpectrum(args.rf_files, args.freq_sampling)
