#!/usr/bin/python

import sys
import os
import itk

def Convert_USRF_BMode(inputFilePath):

    Input_Dir, Input_File = os.path.split(inputFilePath)
    Input_FileName, Input_FileExt = os.path.splitext(Input_File)

    ## Set Output Dir
    Out_Dir = Input_Dir +'/BMode/'
    if not os.path.exists(Out_Dir):
        os.makedirs(Out_Dir)

    ## Load RF data
    InputPixelType = itk.F
    Dimension = 2
    ImageType = itk.Image[InputPixelType, Dimension]
    direction = 0

    reader = itk.ImageFileReader[ImageType].New()
    reader.SetFileName(inputFilePath)

    # Remove low frequency artifacts on the Interson array probe
    filterFunction = itk.ButterworthBandpass1DFilterFunction.New()
    # < 2 MHz
    filterFunction.SetLowerFrequency( 0.12 )
    filterFunction.SetOrder( 7 )
    ComplexPixelType = itk.complex[InputPixelType]
    ComplexImageType = itk.Image[ComplexPixelType, Dimension]
    frequencyFilter = itk.FrequencyDomain1DImageFilter[ComplexImageType,
            ComplexImageType].New()
    frequencyFilter.SetDirection(direction)
    filterFunctionBase = itk.FrequencyDomain1DFilterFunction.New()
    frequencyFilter.SetFilterFunction(filterFunctionBase.cast(filterFunction))

    ## Generate Pre-Scanconversion Data from the RF file
    bMode_Filter = itk.BModeImageFilter[ImageType, ImageType].New()
    bMode_Filter.SetInput(reader.GetOutput())
    bMode_Filter.SetDirection(direction)
    bMode_Filter.SetFrequencyFilter(frequencyFilter)
    bMode_Filter.Update()
    bMode = bMode_Filter.GetOutput()

    writerInput = bMode
    # Apply missing spacing information
    if 'LinearProbe' in inputFilePath:
        changeInformation = itk.ChangeInformationImageFilter.New(bMode)
        changeInformation.SetUseReferenceImage(True)
        changeInformation.SetChangeSpacing(True)
        output_spacing = [1.0, 1.0]
        size = itk.size(bMode)
        sos = 1540.
        fs = 30000.
        output_spacing[0] = sos / (2 * fs)
        transducer_width = 30.0
        output_spacing[1] = transducer_width / (size[1] - 1)
        changeInformation.SetOutputSpacing(output_spacing)
        writerInput = changeInformation.GetOutput()

    outputFilePath = Out_Dir + Input_FileName + '_BMode.mha'
    print(outputFilePath)
    writer = itk.ImageFileWriter[ImageType].New()
    writer.SetFileName(outputFilePath)
    writer.SetInput(writerInput)
    writer.SetUseCompression(True)
    writer.Update()

if __name__ == '__main__':
    if len(sys.argv) == 2:
        inputFilePath = sys.argv[1]
        Convert_USRF_BMode(inputFilePath)
    else:
        print("Convert_USRF_BMode inputFilepath")
