#!/usr/bin/env python

import sys
import os
import itk

def Estimate_USRF_ReferenceSpectrum(input_filepath, side_lines, fft1D_size,
        subregion_depth_fraction=1.0):

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

    # Look for the peak signal amplitude in a sub-region
    subregion_filter = itk.RegionOfInterestImageFilter.New(input_RF)
    subregion = itk.region(input_RF)
    input_size = itk.size(input_RF)
    input_index = itk.index(input_RF)
    # Skip the initial 10% of the beamline, which is in the nearfield
    subregion_index = itk.Index[Dimension]()
    subregion_index[0] = int(input_size[0] * 0.1)
    subregion_index[1] = input_index[1]
    subregion.SetIndex(subregion_index)
    subregion_size = itk.Size[Dimension]()
    subregion_size[0] = input_size[0] - subregion_index[0]
    subregion_size[0] = subregion_size[0] - int((1. - subregion_depth_fraction) * subregion_size[0])
    subregion_size[1] = input_size[1]
    subregion.SetSize(subregion_size)
    subregion_filter.SetRegionOfInterest(subregion)
    subregion_filter.UpdateLargestPossibleRegion()
    subregion_image = subregion_filter.GetOutput()

    max_calculator = itk.MinimumMaximumImageCalculator.New(subregion_image)
    max_calculator.ComputeMaximum()
    max_index = max_calculator.GetIndexOfMaximum()

    SideLinesPixelType = itk.ctype('unsigned char')
    SideLinesImageType = itk.Image[SideLinesPixelType, Dimension]
    side_lines_image = SideLinesImageType.New()
    side_lines_image.CopyInformation(subregion_image)
    side_lines_image.SetRegions(subregion_image.GetLargestPossibleRegion())
    side_lines_image.Allocate()
    side_lines_image.FillBuffer(side_lines)

    spectra_window_filter = itk.Spectra1DSupportWindowImageFilter.New(side_lines_image)
    spectra_window_filter.SetFFT1DSize(fft1D_size)

    spectra_filter = itk.Spectra1DImageFilter.New(subregion_filter)
    spectra_filter.SetSupportWindowImage(spectra_window_filter.GetOutput())
    spectra_filter.UpdateLargestPossibleRegion()

    reference_spectrum_filter = itk.RegionOfInterestImageFilter.New(spectra_filter)
    reference_spectrum_region = itk.region(spectra_filter.GetOutput())
    reference_spectrum_region.SetIndex(max_index)
    reference_spectrum_size = itk.Size[Dimension]()
    reference_spectrum_size.Fill(1)
    reference_spectrum_region.SetSize(reference_spectrum_size)
    reference_spectrum_filter.SetRegionOfInterest(reference_spectrum_region)

    input_dir, input_file = os.path.split(input_filepath)
    output_dir = os.path.join(input_dir, 'ReferenceSpectrum')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    input_filename, input_fileext = os.path.splitext(input_file)
    identifier = '_ReferenceSpectrum_side_lines_{:02d}_fft1d_size_{:03d}.mha'.format(side_lines, fft1D_size)
    output_file = os.path.join(output_dir, input_filename + identifier)

    writer = itk.ImageFileWriter.New(reference_spectrum_filter)
    writer.SetFileName(output_file)
    writer.SetUseCompression(True)
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
        subregion_depth_fraction = 1.0
        if len(sys.argv) > 4:
            subregion_depth_fraction = float(sys.argv[4])
        Estimate_USRF_ReferenceSpectrum(input_filepath, side_lines, fft1D_size,
                subregion_depth_fraction)
    else:
        print("Estimate_USRF_ReferenceSpectrum <input_filepath> [side_lines] [fft1D_size] [subregion_depth_fraction]")

