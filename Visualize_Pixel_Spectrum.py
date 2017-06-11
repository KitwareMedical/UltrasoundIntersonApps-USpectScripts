#!/usr/bin/python

import os

import itk

import matplotlib.pyplot as plt
from scipy import signal
import numpy as np
import argparse

def VisualizePixelSpectrum(spectra_file, freq_sampling, index):
    plt.figure(1, figsize=(5, 4))
    handles = []
    labels = []
    ComponentType = itk.ctype('float')
    Dimension = 2
    ImageType = itk.VectorImage[ComponentType, Dimension]
    reader = itk.ImageFileReader[ImageType].New(FileName=spectra_file)
    reader.Update()
    image = reader.GetOutput()
    arr = itk.GetArrayFromImage(image)
    freq = np.linspace(freq_sampling / 2 / arr.shape[2], freq_sampling / 2, arr.shape[2])
    ax = plt.plot(freq, arr[index[1], index[0], :].ravel(), label=spectra_file)
    handles.append(ax[0])
    labels.append(spectra_file)
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Power spectral density')
    plt.figlegend(handles, labels, 'upper right')
    # plt.ylim(0.0, 1.0)

    dirname = os.path.dirname(spectra_file)
    # plt.savefig(os.path.join(dirname, 'PixelSpectrum.png'), dpi=300)
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Visualize Pixel Power Spectrum.')
    parser.add_argument('spectra_file', help='spectra data file')
    parser.add_argument('--freq-sampling', type=float, default=30e3,
        help='sampling frequency [Hz]')
    parser.add_argument('--index', help='comma delimited index of the pixel to investigate', default='0,0')
    args = parser.parse_args()
    index = [int(component) for component in args.index.split(',')]
    VisualizePixelSpectrum(args.spectra_file, args.freq_sampling, index)
