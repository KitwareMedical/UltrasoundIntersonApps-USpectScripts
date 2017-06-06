#!/usr/bin/env python

import sys
import os
import itk

def Estimate_USRF_ReferenceSpectrum(input_filepath, side_lines, fft1D_size):

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

    spectra_filter = itk.Spectra1DImageFilter.New(input_RF)
    spectra_filter.SetSupportWindowImage(spectra_window_filter.GetOutput())

    input_dir, input_file = os.path.split(input_filepath)
    output_dir = os.path.join(input_dir, 'ReferenceSpectrum')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    input_filename, input_fileext = os.path.splitext(input_file)
    identifier = '_ReferenceSpectrum_side_lines_{:03d}_fft1d_size_{:03d}.mha'.format(side_lines, fft1D_size)
    output_file = os.path.join(output_dir, input_filename + identifier)

    writer = itk.ImageFileWriter.New(spectra_filter)
    writer.SetFileName(output_file)
    writer.Update()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        input_filepath = sys.argv[1]
        side_lines = 1
        if len(sys.argv) > 2:
            side_lines = int(sys.argv[2])
        fft1D_size = 32
        if len(sys.argv) > 3:
            fft1D_size = int(sys.argv[3])
        Estimate_USRF_ReferenceSpectrum(input_filepath, side_lines, fft1D_size)
    else:
        print("Estimate_USRF_ReferenceSpectrum <input_filepath>")

