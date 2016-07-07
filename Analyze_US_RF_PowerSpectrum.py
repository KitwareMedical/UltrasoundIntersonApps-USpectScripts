__author__ = 'hyunjaekang'


import itk
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
import scipy.signal


def Compute_Fit_Coefficient(np_array):
    cols, rows, freqs = np_array.shape

    img_slope              = np.zeros((cols, rows))
    img_intercept          = np.zeros((cols, rows))

    img_Legendre6Deg_coef1 = np.zeros((cols, rows))
    img_Legendre6Deg_coef2 = np.zeros((cols, rows))
    img_Legendre6Deg_coef3 = np.zeros((cols, rows))
    img_Legendre6Deg_coef4 = np.zeros((cols, rows))
    img_Legendre6Deg_coef5 = np.zeros((cols, rows))
    img_Legendre6Deg_coef6 = np.zeros((cols, rows))

    for col in np.arange(cols):
        for row in np.arange(rows):
            temp_rf_pw = np_array[col, row, :]

            log_temp_rf_pw = temp_rf_pw
            slope, intercept, r_value, p_value, std_err = \
                scipy.stats.linregress(np.arange(len(log_temp_rf_pw)), log_temp_rf_pw)

            img_slope[col, row] = slope
            img_intercept[col, row] = intercept

            legendre6Deg_coefs = np.polynomial.legendre.legfit(np.arange(len(log_temp_rf_pw)), log_temp_rf_pw, 3)

            img_Legendre6Deg_coef1[col, row] = legendre6Deg_coefs[0]
            img_Legendre6Deg_coef2[col, row] = legendre6Deg_coefs[1]
            img_Legendre6Deg_coef3[col, row] = legendre6Deg_coefs[2]
            img_Legendre6Deg_coef4[col, row] = legendre6Deg_coefs[3]
            img_Legendre6Deg_coef5[col, row] = legendre6Deg_coefs[4]
            img_Legendre6Deg_coef6[col, row] = legendre6Deg_coefs[5]




def USRF_PWR_Spectrum(input_rf_file_path, N1DFFT, SideLine):

    dim_2D = 2
    dim_3D = 3
    usRF_pixel_type = itk.F

    us_RF2D_Type = itk.Image[usRF_pixel_type, dim_2D]
    us_RF3D_Type = itk.Image[usRF_pixel_type, dim_3D]
    rf_spectra_ImageType = itk.VectorImage[itk.F, dim_2D]
    uchar_2D_ImageType = itk.Image[itk.UC, dim_2D]
    uchar_3D_ImageType = itk.Image[itk.UC, dim_3D]

    ##>>>>>>>>>> Loading
    US_RF3D_Reader = itk.ImageFileReader[us_RF3D_Type].New()
    US_RF3D_Reader.SetFileName(input_rf_file_path)
    US_RF3D_Reader.Update()
    us_rf3D = US_RF3D_Reader.GetOutput()

    ## >>>>>>>>>>  Extract a 2D frame from the loaded 3D volume data
    us_rf3D_region = us_rf3D.GetLargestPossibleRegion()
    us_rf3D_size   = us_rf3D_region.GetSize()
    us_rf3D_frames = us_rf3D_size[2]
    us_rf3D_frames_array = itk.PyBuffer[us_RF3D_Type].GetArrayFromImage(us_rf3D_frames)

    print "RF Data size: ", us_rf3D_size
    print "RF Data size: ", us_rf3D_frames_array.shape

    Extractor  = itk.ExtractImageFilter[us_RF3D_Type,us_RF2D_Type].New()
    Extractor.SetInput(us_rf3D)
    Extractor.SetDirectionCollapseToIdentity()
    extract_size = (int(us_rf3D_size[0]), int(us_rf3D_size[1]),0)
    extract_region = itk.ImageRegion[3]()
    extract_region.SetSize(extract_size)
    extract_Index = extract_region.GetIndex()

    ### Check the following parts
    extract_Index[2] = 0
    extract_region.SetIndex(extract_Index)
    Extractor.SetExtractionRegion(extract_region)
    Extractor.UpdateLargestPossibleRegion()

    extracted_2D = Extractor.GetOutput()

    #############
    ## Build Spectra Window
    side_lines = uchar_2D_ImageType.New()
    side_lines.CopyInformation(extracted_2D)#(us_rf3D)
    side_lines.SetRegions(extracted_2D.GetLargestPossibleRegion())
    side_lines.Allocate()
    side_lines.FillBuffer(SideLine)

    Spectra_window_filter = itk.Spectra1DSupportWindowImageFilter[uchar_2D_ImageType].New()
    Spectra_window_filter.SetInput(side_lines)
    Spectra_window_filter.SetFFT1DSize(N1DFFT)
    Spectra_window_filter.Update()

    ## Build Spectra Filter
    # Create an instance of itk::Spectra1DImageFilter
    Spectra_Filter = itk.Spectra1DImageFilter.IF2IdequeitkIndex22VIF2.New()

    Spectra_Filter.SetInput(Extractor.GetOutput())
    Spectra_Filter.SetSupportWindowImage(Spectra_window_filter.GetOutput())
    Spectra_Filter.UpdateLargestPossibleRegion()

    ## Todo: Save the following data with frame 0
    spectra_Image = Spectra_Filter.GetOutput()

    sum_spectra_Image_arr = itk.PyBuffer[rf_spectra_ImageType].GetArrayFromImage(spectra_Image)
    print "The shape of spectra_Image_arr", sum_spectra_Image_arr.shape

    for frame in np.arange(us_rf3D_frames)[1:]:
        extract_Index[2] = frame
        extract_region.SetIndex(extract_Index)
        Extractor.SetExtractionRegion(extract_region)
        Extractor.UpdateLargestPossibleRegion()

        Spectra_Filter.SetInput(Extractor.GetOutput())
        Spectra_Filter.SetSupportWindowImage(Spectra_window_filter.GetOutput())
        Spectra_Filter.UpdateLargestPossibleRegion()

        ## Todo: Save the following data with frame 0
        spectra_Image = Spectra_Filter.GetOutput()

        temp_spectra_Image_arr = itk.PyBuffer[rf_spectra_ImageType].GetArrayFromImage(spectra_Image)
        sum_spectra_Image_arr += temp_spectra_Image_arr




