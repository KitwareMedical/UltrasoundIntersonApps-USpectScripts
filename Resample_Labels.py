#!/usr/bin/env python

import argparse
import os
import glob

import itk

def Resample_Labels(labels_filepath, reference_path, output_path):

    PixelType = itk.ctype('unsigned char')
    Dimension = 2
    ImageType = itk.Image[PixelType, Dimension]

    basename = os.path.basename(labels_filepath).split('_ManualLabel')[0]

    labels_reader = itk.ImageFileReader[ImageType].New()
    labels_reader.SetFileName(labels_filepath)
    labels_reader.UpdateLargestPossibleRegion()

    reference_filepath_glob = os.path.join(os.path.dirname(labels_filepath),
            reference_path, basename + '*')
    reference_filepath = glob.glob(reference_filepath_glob)[0]
    reference_reader = itk.ImageFileReader[ImageType].New()
    reference_reader.SetFileName(reference_filepath)
    reference_reader.UpdateLargestPossibleRegion()

    resampler = itk.ResampleImageFilter[ImageType, ImageType].New()
    resampler.SetInput(labels_reader.GetOutput())
    resampler.SetReferenceImage(reference_reader.GetOutput())
    resampler.SetUseReferenceImage(True)
    resampler.UpdateLargestPossibleRegion()

    output_path = os.path.join(os.path.dirname(labels_filepath), output_path)
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    writer = itk.ImageFileWriter.New(resampler.GetOutput())
    writer.SetFileName(os.path.join(output_path, basename + '_ManualLabelResampled.mha'))
    writer.Update()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Resample labels to sampling grid in a feature image.')
    parser.add_argument('labels_filepath', help='input manual labels image filepath')
    parser.add_argument('reference_path', default='../SpectraIteration1',
            help='subdirectory relative to labels_filepath to find the corresponding reference spectra image')
    parser.add_argument('output_path', default='../ManualLabelsResampled',
            help='subdirectory relative to labels_filepath dirname to write output resampled label images')
    args = parser.parse_args()
    Resample_Labels(args.labels_filepath, args.reference_path, args.output_path)
