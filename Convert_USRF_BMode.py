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
    ImageType = itk.Image[InputPixelType, 2]

    reader = itk.ImageFileReader[ImageType].New()
    reader.SetFileName(inputFilePath)

    ## Generate Pre-Scanconversion Data from the RF file
    bMode_Filter = itk.BModeImageFilter[ImageType, ImageType].New()
    bMode_Filter.SetInput(reader.GetOutput())
    bMode_Filter.SetDirection(0)
    bMode_Filter.Update()
    bMode = bMode_Filter.GetOutput()

    outputFilePath = Out_Dir + Input_FileName + '_BMode.mha'

    print(outputFilePath)
    writer = itk.ImageFileWriter[ImageType].New()
    writer.SetFileName(outputFilePath)
    writer.SetInput(bMode)
    writer.SetUseCompression(True)
    writer.Update()

if __name__ == '__main__':
    if len(sys.argv) == 2:
        inputFilePath = sys.argv[1]
        Convert_USRF_BMode(inputFilePath)
    else:
        print("Convert_USRF_BMode inputFilepath")
