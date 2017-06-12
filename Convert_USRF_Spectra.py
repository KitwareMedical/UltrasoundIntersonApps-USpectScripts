#!/usr/bin/python

import sys

import os
import itk
import numpy as np
import argparse
import glob

def Convert_USRF_Spectra(input_filepath, reference_path, output_path, side_lines=5, fft1D_size=128):

    InputPixelType = itk.ctype('float')
    Dimension = 2
    ImageType = itk.Image[InputPixelType, Dimension]

    reader = itk.ImageFileReader[ImageType].New()
    reader.SetFileName(input_filepath)
    input_RF = reader.GetOutput()
    # Apply missing spacing information
    if 'LinearProbe' in input_filepath:
        change_information = itk.ChangeInformationImageFilter.New(input_RF)
        change_information.SetUseReferenceImage(True)
        change_information.SetChangeSpacing(True)
        output_spacing = [1.0, 1.0]
        size = itk.size(input_RF)
        sos = 1540.
        fs = 30000.
        output_spacing[0] = sos / (2 * fs)
        transducer_width = 30.0
        output_spacing[1] = transducer_width / (size[1] - 1)
        change_information.SetOutputSpacing(output_spacing)
        input_RF = change_information.GetOutput()
    input_RF.UpdateOutputInformation()

    SideLinesPixelType = itk.ctype('unsigned char')
    SideLinesImageType = itk.Image[SideLinesPixelType, Dimension]
    side_lines_image = SideLinesImageType.New()
    side_lines_image.CopyInformation(input_RF)
    side_lines_image.SetRegions(input_RF.GetLargestPossibleRegion())
    side_lines_image.Allocate()
    side_lines_image.FillBuffer(side_lines)

    spectra_window_filter = itk.Spectra1DSupportWindowImageFilter.New(side_lines_image)
    spectra_window_filter.SetFFT1DSize(fft1D_size)
    spectra_window_filter.SetStep(8)
    spectra_window_filter.UpdateLargestPossibleRegion()
    support_window_image = spectra_window_filter.GetOutput()

    SpectraImageType = itk.VectorImage[InputPixelType, Dimension]

    reference_reader = itk.ImageFileReader[SpectraImageType].New()
    basename = os.path.splitext(os.path.basename(input_filepath))[0]
    reference_path = os.path.join(os.path.dirname(input_filepath), reference_path)
    reference_glob = glob.glob(os.path.join(reference_path, basename[:-11] + '*.mha'))
    if len(reference_glob) != 1:
        print('Reference spectra file not found')
        print('Found: ', reference_glob)
        sys.exit(1)
    reference_reader.SetFileName(reference_glob[0])
    reference_reader.UpdateLargestPossibleRegion()

    reference_spectra_image = SpectraImageType.New()
    reference_spectra_image.CopyInformation(support_window_image)
    reference_spectra_image.SetRegions(support_window_image.GetLargestPossibleRegion())
    reference_spectra_image.SetNumberOfComponentsPerPixel(reference_reader.GetOutput().GetNumberOfComponentsPerPixel())
    reference_spectra_image.Allocate()
    reference_index = itk.Index[Dimension]()
    reference_index.Fill(0)
    reference_spectrum = reference_reader.GetOutput().GetPixel(reference_index)
    reference_spectra_image.FillBuffer(reference_spectrum)

    spectra_filter = itk.Spectra1DImageFilter.New(input_RF)
    spectra_filter.SetSupportWindowImage(spectra_window_filter.GetOutput())
    spectra_filter.SetReferenceSpectraImage(reference_spectra_image)
    spectra_filter.UpdateLargestPossibleRegion()

    output_path = os.path.join(os.path.dirname(input_filepath), output_path)
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    identifier = '_Spectra_side_lines_{:02d}_fft1d_size_{:03d}.mha'.format(side_lines, fft1D_size)
    output_filepath = os.path.join(output_path, basename + identifier)
    writer = itk.ImageFileWriter.New(spectra_filter)
    writer.SetFileName(output_filepath)
    writer.Update()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Estimate local corrected spectrum.')
    parser.add_argument('rf_filepath', help='input rf filepath')
    parser.add_argument('reference_path', help='path to folder containing reference spectra relate to rf_filepath dirname')
    parser.add_argument('--output-path', default='SpectraIteration1',
            help='subdirectory relative to rf_filepath dirname to write output spectra images')
    args = parser.parse_args()
    Convert_USRF_Spectra(args.rf_filepath, args.reference_path, args.output_path)
