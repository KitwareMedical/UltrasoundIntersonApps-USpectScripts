#!/usr/bin/python

import sys

import numpy as np
import matplotlib.pyplot as plt
import os
import scipy.stats
import scipy.signal
import itk
import skimage.io
import argparse

def Analyze_USRF_Spectra(spectra_filepath, output_path, spectra_start_idx=4,
        spectra_stop_idx=21):

    ComponentType = itk.ctype('float')
    Dimension = 2
    ImageType = itk.VectorImage[ComponentType, Dimension]

    reader = itk.ImageFileReader[ImageType].New()
    reader.SetFileName(spectra_filepath)
    reader.UpdateLargestPossibleRegion()
    spectra_image = reader.GetOutput()
    # lateral x axial x spectral component
    spectra_array = itk.GetArrayFromImage(spectra_image)

    # Look at low noise bandwidth of interest
    spectra_bandwidth = spectra_array[..., spectra_start_idx:spectra_stop_idx]

    # Work with spectra in dB
    spectra = 10 * np.log10(spectra_bandwidth)

    output_path = os.path.join(os.path.dirname(spectra_filepath), output_path)
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    basename = os.path.basename(spectra_filepath).split('_Spectra')[0]

    def save_output(arr, identifier):
        output_filepath = os.path.join(output_path, basename + identifier)
        np.save(output_filepath + '.npy', arr)

    save_output(spectra, '_Spectra')


    # Prep images
    num_lateral = spectra.shape[0]
    num_axial = spectra.shape[1]

    chebyshev_num_features = 7
    chebyshev_image = np.zeros([num_lateral, num_axial, chebyshev_num_features], dtype=np.float32)

    line_num_features = 2
    line_image = np.zeros([num_lateral, num_axial, line_num_features], dtype=np.float32)

    legendre_num_features = 7
    legendre_image = np.zeros([num_lateral, num_axial, legendre_num_features], dtype=np.float32)

    integrated_num_features = 1
    integrated_image = np.zeros([num_lateral, num_axial, integrated_num_features], dtype=np.float32)

    for lateral in np.arange(num_lateral):
        print "Line ", lateral, " of ", num_lateral
        for axial in np.arange(num_axial):
            spectrum = spectra[lateral, axial, :].ravel()

            cheb_coefs = np.polynomial.chebyshev.Chebyshev.fit(
                np.arange(len(spectrum)), spectrum, chebyshev_num_features-1)
            chebyshev_image[lateral, axial, :] = cheb_coefs.coef

            line_coefs = scipy.stats.linregress(
                np.arange(len(spectrum)), spectrum)
            line_image[lateral, axial, 0] = line_coefs.slope
            line_image[lateral, axial, 1] = line_coefs.intercept

            legn_coefs = np.polynomial.legendre.legfit(
                np.arange(len(spectrum)), spectrum, legendre_num_features-1)
            legendre_image[lateral, axial, :] = legn_coefs

            intg_coefs = np.sum(spectrum)
            integrated_image[lateral, axial, 0] = intg_coefs

    save_output(chebyshev_image, '_Chebyshev')
    save_output(line_image, '_Line')
    save_output(legendre_image, '_Legendre')
    save_output(integrated_image, '_Integrated')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compute features from the spectra image.')
    parser.add_argument('spectra_filepath', help='input spectra filepath')
    parser.add_argument('--output-path', default='../SpectraIteration1Features',
            help='subdirectory relative to spectra_filepath dirname to write output spectra feature images')
    args = parser.parse_args()
    Analyze_USRF_Spectra(args.spectra_filepath, args.output_path)
