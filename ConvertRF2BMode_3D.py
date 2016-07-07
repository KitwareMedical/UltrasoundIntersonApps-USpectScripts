#!/usr/bin/python

import itk
import numpy as np
import sys

def ConvertRF2BMode(inputFilePath, outputFilePath):

    ## Check
    print inputFilePath
    print outputFilePath
    ## Initialize
    Dimension = 3

    ## Load RF data
    InputPixelType = itk.F
    ImageType = itk.Image[InputPixelType, Dimension]
    reader = itk.ImageFileReader[ImageType].New()
    reader.SetFileName(inputFilePath)
    # reader.Update()


    ## Generate Pre-Scanconversion Data from the RF file
    PreSc_BMode_Filter = itk.BModeImageFilter[ImageType, ImageType].New()
    PreSc_BMode_Filter.SetInput(reader.GetOutput())
    PreSc_BMode_Filter.SetDirection(1)
    # PreSc_BMode_Filter.Update()
    PreSc_BMode = PreSc_BMode_Filter.GetOutput()


    InputRF_Size = itk.size(PreSc_BMode)
    print '----------------'
    print InputRF_Size[0]
    print InputRF_Size[1]
    print InputRF_Size[2]

    RF_Sz_Z = InputRF_Size[2]

    # output_size = (1108, 725, RF_Sz_Z)
    #
    # print "---- Before ----"
    # print "The type of RF_Sz_Z: %s" % type(RF_Sz_Z)
    # print "The type of output_size: %s" % type(output_size)
    #
    # print "---- After -----"
    # RF_Sz_Z_Int = int(RF_Sz_Z)
    # output_size_Int = (1108, 725, RF_Sz_Z_Int)
    # print "The type of RF_Sz_Z_Int: %s" % type(RF_Sz_Z_Int)
    # print "The type of output_size_Int: %s" % type(output_size_Int)


    ## Scanconversion
    #01. Rescale the image's intensity
    CurvilinearImageType = itk.CurvilinearArraySpecialCoordinatesImage[itk.UC, Dimension]
    rescale_filter = itk.RescaleIntensityImageFilter[ImageType, CurvilinearImageType].New()
    #rescale_filter.SetInput(PreSc_BMode)#(bmode_filter.GetOutput())
    rescale_filter.SetInput(PreSc_BMode_Filter.GetOutput())
    rescale_filter.UpdateLargestPossibleRegion()
    curvilinear = rescale_filter.GetOutput()

    # writer = itk.ImageFileWriter[CurvilinearImageType].New()
    # writer.SetFileName(outputFilePath)
    # writer.SetInput(curvilinear)
    # writer.Update()


    #02. Scanconversion
    curvilinear_size = curvilinear.GetLargestPossibleRegion().GetSize()

    #lateral_angular_separation = (np.pi / 2.0 + np.pi / 4.0) / (curvilinear_size[1] - 1)
    lateral_angular_separation = (np.pi / 2.0 ) / (curvilinear_size[1] - 1)
    radius_start = 12.4
    radius_stop = 117.5

    curvilinear.SetLateralAngularSeparation(lateral_angular_separation)
    curvilinear.SetFirstSampleDistance(radius_start)
    curvilinear.SetRadiusSampleSize((radius_stop - radius_start) / (curvilinear_size[0] - 1))

    #output_size = (800, 800)
    #output_size = (1108, 725)
    output_size = (int(1108), int(725), int(RF_Sz_Z))

    print output_size

    output_spacing = (float(0.15), float(0.15), float(0.15))
    output_origin = [float(0.0), float(0.0), float(0.0)]
    output_origin[0] = float(output_size[0] * output_spacing[0] / -2.0)
    output_origin[1] = float(radius_start * np.cos(np.pi / 4.0))

    UCharImageType = itk.Image[itk.UC, Dimension]
    resample_filter = itk.ResampleImageFilter[CurvilinearImageType, UCharImageType].New()
    resample_filter.SetInput(curvilinear)
    resample_filter.SetSize(output_size)
    resample_filter.SetOutputSpacing(output_spacing)
    resample_filter.SetOutputOrigin(output_origin)
    resample_filter.UpdateLargestPossibleRegion()

    bmode_image2 = resample_filter.GetOutput()
    bmode_image2.DisconnectPipeline()

    writer = itk.ImageFileWriter[UCharImageType].New()
    writer.SetFileName(outputFilePath)
    writer.SetInput(bmode_image2)
    writer.Update()


    print '------------------------'
    print 'Done'


if __name__ == '__main__':
    if len(sys.argv) == 3:
        inputFilePath = sys.argv[1]
        outputFilePath = sys.argv[2]
        ConvertRF2BMode(inputFilePath, outputFilePath)
    else:
        print "ConvertRF2BMode inputFilepath outputFilePath"

