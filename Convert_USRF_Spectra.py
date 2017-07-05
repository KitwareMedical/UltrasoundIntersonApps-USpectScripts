#!/usr/bin/python

import sys
#sys.path.append('/home/ubuntu/src/ITK-Release/Wrapping/Generators/Python')
#sys.path.append('/home/ubuntu/src/ITK-Release/lib')

import os
import itk
import numpy as np

def Convert_USRF_Spectra_File(input_rf_file_path, N1DFFT, side_line, targetframe=9999, save_ITK_vector=0):

    i_side_line = int(side_line)
    i_N1DFFT   = int(N1DFFT)
    b_Target   = False

    if targetframe != 9999:
        print( "Target Frame:"  + str(targetframe) )
        b_Target = True
        print( "b_Target: " + str(b_Target) )

    file_dir, splt_t = os.path.split(input_rf_file_path)
    file_name, file_ext = os.path.splitext(splt_t)

    ###############
    out_dir = file_dir +'/RF_PWSpectra/'
    if not os.path.exists(out_dir):
        print( 'Create Dir' )
        os.makedirs(out_dir)

    out_dir = out_dir + '%03dSLine' %i_side_line +'-%03dNFFT/' %i_N1DFFT
    if not os.path.exists(out_dir):
        print( 'Create Dir' )
        os.makedirs(out_dir)


    print( "File_Dir:" + str(  file_dir ))
    print( "File_Name:" + str( file_name ))
    print( "File_Ext:" + str(  file_ext ))

    print( "Out_Dir: " + str(  out_dir ))
    print( "N1DFFT: " + str(   N1DFFT ))
    print( "SideLine: " + str( side_line ))

    new_file_name_prefix = file_name +'-%03dSLine' %i_side_line +'-%03dNFFT' %i_N1DFFT
    print( "new_file_name_prefix: " + str( new_file_name_prefix))

    ##############################
    dim_2D               = 2
    dim_3D               = 3
    usRF_pixel_type      = itk.F

    us_RF2D_Type         = itk.Image[usRF_pixel_type, dim_2D]
    us_RF3D_Type         = itk.Image[usRF_pixel_type, dim_3D]
    rf_spectra_ImageType = itk.VectorImage[itk.F, dim_2D]
    uchar_2D_ImageType   = itk.Image[itk.UC, dim_2D]
    uchar_3D_ImageType   = itk.Image[itk.UC, dim_3D]

    ##>>>>>>>>>> Loading
    US_RF3D_Reader       = itk.ImageFileReader[us_RF3D_Type].New()
    US_RF3D_Reader.SetFileName(input_rf_file_path)
    US_RF3D_Reader.Update()
    us_rf3D              = US_RF3D_Reader.GetOutput()

    ## >>>>>>>>>>  Extract a 2D frame from the loaded 3D volume data
    us_rf3D_region       = us_rf3D.GetLargestPossibleRegion()
    us_rf3D_size         = us_rf3D_region.GetSize()


    us_rf3D_frames_array = itk.PyBuffer[us_RF3D_Type].GetArrayFromImage(us_rf3D)

    print( "RF Data size: " + str( us_rf3D_size) )
    print( "RF Data size: " + str( us_rf3D_frames_array.shape) )

    us_rf3D_rows         = us_rf3D_size[0]
    us_rf3D_cols         = us_rf3D_size[1]
    us_rf3D_frames       = us_rf3D_size[2]

    print( "us_rf3D_rows: " + str( us_rf3D_rows ))
    print( "us_rf3D_cols: " + str( us_rf3D_cols ))
    print( "us_rf3D_frames: " + str( us_rf3D_frames ))
    ##### Extract 2D from 3D
    Extractor            = itk.ExtractImageFilter[us_RF3D_Type,us_RF2D_Type].New()
    Extractor.SetInput(us_rf3D)
    Extractor.SetDirectionCollapseToIdentity()
    # extract_size         = (int(us_rf3D_size[0]), int(us_rf3D_size[1]),0)
    extract_size         = (int(us_rf3D_rows), int(us_rf3D_cols),0)
    extract_region       = itk.ImageRegion[3]()
    extract_region.SetSize(extract_size)
    extract_Index        = extract_region.GetIndex()

    ### Check the following parts
    extract_Index[2]     = 0
    extract_region.SetIndex(extract_Index)
    Extractor.SetExtractionRegion(extract_region)
    Extractor.UpdateLargestPossibleRegion()
    extracted_2D         = Extractor.GetOutput()

    #############
    ## Build Spectra Window
    side_lines = uchar_2D_ImageType.New()
    side_lines.CopyInformation(extracted_2D)#(us_rf3D)
    side_lines.SetRegions(extracted_2D.GetLargestPossibleRegion())
    side_lines.Allocate()
    side_lines.FillBuffer(i_side_line)

    Spectra_window_filter = itk.Spectra1DSupportWindowImageFilter[uchar_2D_ImageType].New()
    Spectra_window_filter.SetInput(side_lines)
    Spectra_window_filter.SetFFT1DSize(i_N1DFFT)
    Spectra_window_filter.Update()

    ## Build Spectra Filter
    # Create an instance of itk::Spectra1DImageFilter
    Spectra_Filter = itk.Spectra1DImageFilter.IF2IdequeitkIndex22VIF2.New()

    ITKWriter_Spectra = itk.ImageFileWriter[rf_spectra_ImageType].New()

    Spectra_Filter.SetInput(Extractor.GetOutput())
    Spectra_Filter.SetSupportWindowImage(Spectra_window_filter.GetOutput())
    Spectra_Filter.UpdateLargestPossibleRegion() 

    ## Todo: Save the following data with frame 0
    spectra_Image = Spectra_Filter.GetOutput()

    Vec2D_Dir = out_dir+new_file_name_prefix+'_2D_ImgVectors/'
    print( "Vec2D_Dir : " + str( Vec2D_Dir))

    if save_ITK_vector > 0:
        if not os.path.exists(Vec2D_Dir):
            print( 'Create Dir' )
            os.makedirs(Vec2D_Dir)

        Vec2D_Nam = "frame_%05d.mha" % 0
        print( "Vec2D_Nam : " + str( Vec2D_Nam))
        ITKWriter_Spectra.SetInput(spectra_Image)
        ITKWriter_Spectra.SetFileName(Vec2D_Dir+Vec2D_Nam)
        ITKWriter_Spectra.Update()

    temp_spectra_Image_arr = itk.PyBuffer[rf_spectra_ImageType].GetArrayFromImage(spectra_Image)
    print( "The shape of spectra_Image_arr" + str( temp_spectra_Image_arr.shape))

    sz_Freq = temp_spectra_Image_arr.shape[2]
    print( "sz_Freq: " + str( sz_Freq))

    NPArr_3DRF_PWSpectra = np.zeros((us_rf3D_frames, us_rf3D_cols, us_rf3D_rows, sz_Freq))
    NPArr_3DRF_PWSpectra[0, :, :, :] = temp_spectra_Image_arr

    sum_spectra_Image_arr = temp_spectra_Image_arr


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

        if save_ITK_vector > 0:
            Vec2D_Nam = "frame_%05d.mha" % frame
            print( "Vec2D_Nam : " + str( Vec2D_Nam))
            ITKWriter_Spectra.SetInput(spectra_Image)
            ITKWriter_Spectra.SetFileName(Vec2D_Dir+Vec2D_Nam)
            ITKWriter_Spectra.Update()

        temp_spectra_Image_arr = itk.PyBuffer[rf_spectra_ImageType].GetArrayFromImage(spectra_Image)
        NPArr_3DRF_PWSpectra[frame, :, :, :] = temp_spectra_Image_arr
        sum_spectra_Image_arr += temp_spectra_Image_arr

        if b_Target == True:
            if targetframe == frame:
                print( "Targeted Frame: %d, current frame: %d" %(targetframe, frame) )
                FilePathFrame     = out_dir + new_file_name_prefix +'_frame_%05d.npy' % frame
                np.save(FilePathFrame, temp_spectra_Image_arr)

                Vec2D_Nam = new_file_name_prefix + "_2DVector_frame_%05d.mha" % frame
                print( "Vec2D_Nam : " + str( Vec2D_Nam))
                ITKWriter_Spectra.SetInput(spectra_Image)
                ITKWriter_Spectra.SetFileName(out_dir+Vec2D_Nam)
                ITKWriter_Spectra.Update()


    NPArr_3DRF_PWSpectra_Avg = sum_spectra_Image_arr / us_rf3D_frames
    FilePath3DAvg  = out_dir + new_file_name_prefix +'-Avg.npy'
    np.save(FilePath3DAvg, NPArr_3DRF_PWSpectra_Avg)

    if b_Target == False:
        FilePath3D     = out_dir + new_file_name_prefix +'.npy'
        np.save(FilePath3D, NPArr_3DRF_PWSpectra)


def Convert_USRF_Spectra(input_file, target_frame=9999, save_ITK_vector=0):
    N1DFFT_R = [1048]#32,64]
    side_line_R = [2]
    for nsfft in N1DFFT_R:
        for szline in side_line_R:
            print( "N1DFFT: %d, SideLine: %d" %(nsfft,szline ))
            Convert_USRF_Spectra_File(input_file, nsfft, szline,
                target_frame, save_ITK_vector)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        input_file         = sys.argv[1]
        Convert_USRF_Spectra(input_file)
    elif len(sys.argv) == 3:
        input_file         = sys.argv[1]
        target_frame       = int(sys.argv[2])
        Convert_USRF_Spectra(input_file, target_frame)
    elif len(sys.argv) == 4:
        input_file         = sys.argv[1]
        target_frame       = int(sys.argv[2])
        save_ITK_vector    = sys.argv[3]
        Convert_USRF_Spectra( input_rf_file_path, target_frame, 
            save_ITK_vector )
    else:
        print( "Convert_USRF_Spectra <input_file> [target_frame [save_ITK_vector]]" )
