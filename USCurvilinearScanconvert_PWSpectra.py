import itk
import sys
import numpy as np
import matplotlib.pyplot as plt
import skimage.io
import os
import shutil

def GetFileDirNameExt(file_Path):
    file_dir, splt_t = os.path.split(file_Path)
    file_name, file_ext = os.path.splitext(splt_t)
    return file_dir, file_name, file_ext

# def ITKUSCurvilinearScanconvert(itkImg, scan_angle = np.pi/2.0,\
# 	                                    radius_start = 12.4,\
# 	                                    radius_stop = 117.5,\
# 	                                    sz_output = (1108,725),\
# 	                                    spacing_output = (0.15, 0.15, 0.15)):
	
# 	## Retrive the dimension of inputImage
# 	dim                  	   = itkImg.ImageDimension
# 	frames                     = 0 
# 	sz_output                  = (1108,725)
# 	origin_output              = [0.0, 0.0]
	
# 	if dim == 3:
# 		frames                 = int(itk.size(itkImg)[2])
# 		sz_output              = (1108,725, frames)
# 		origin_output          = [0.0, 0.0, 0.0]

	
# 	## Rescale the intensity of Image and cast the type of data from float to char 
# 	# iType_USRFFrame      	   = itk.Image[itk.F, dim]
# 	# iType_CurvilinearImg 	   = itk.CurvilinearArraySpecialCoordinatesImage[itk.UC, dim]
# 	# iFilter_RescaleIntensity = itk.RescaleIntensityImageFilter[iType_USRFFrame,iType_CurvilinearImg].New()
# 	# iFilter_RescaleIntensity.SetInput(itkImg)
# 	# iFilter_RescaleIntensity.UpdateLargestPossibleRegion()

# 	iType_CurvilinearImg 	   = itk.CurvilinearArraySpecialCoordinatesImage[itk.F, dim]
# 	iType_SCUSImg              = itk.Image[itk.F, dim]

# 	iFilterCastImage           = itk.CastImageFilter[iType_SCUSImg, iType_CurvilinearImg].New()

# 	## Put the parameters for curvilinear scan-conversion
# 	#iimg_curvilinear           = itkImg #iFilter_RescaleIntensity.GetOutput()

# 	iimg_curvilinear           = iType_CurvilinearImg.New()
	
# 	help(iimg_curvilinear)

	
# 	iimg_curvilinear.SetInput(itkImg)

# 	exit()
# 	isz_curvilinear            = iimg_curvilinear.GetLargestPossibleRegion().GetSize()

# 	## Computing the parameters of curvilinear sacn-conversion
# 	lateral_angular_separation = scan_angle / (isz_curvilinear[1]-1) 
# 	radius_scan                = (radius_stop - radius_start) / (isz_curvilinear[0]-1)
	
# 	sz_output                  = (1108,725, frames)

# 	origin_output              = [0.0, 0.0, 0.0]
# 	origin_output[0]           = sz_output[0] * spacing_output[0]/ -2.0
# 	origin_output[1]           = radius_start * np.cos(scan_angle/2)

# 	iimg_curvilinear.SetLateralAngularSeparation(lateral_angular_separation)
# 	iimg_curvilinear.SetFirstSampleDistance(radius_start)
# 	iimg_curvilinear.SetRadiusSampleSize(radius_scan)

# 	## Resample Image
# 	#iType_UCharImg             = itk.Image[itk.UC, dim]
# 	iFilter_resample           = itk.ResampleImageFilter[iType_CurvilinearImg, iType_SCUSImg].New()
# 	iFilter_resample.SetInput(iimg_curvilinear)
# 	iFilter_resample.SetSize(sz_output)
# 	iFilter_resample.SetOutputSpacing(spacing_output)
# 	iFilter_resample.SetOutputOrigin(origin_output)
# 	iFilter_resample.UpdateLargestPossibleRegion()

# 	## Return a scan-converted US BMode image
# 	return iFilter_resample.GetOutput()


def ITKUSCurvilinearScanconvert_File(input_filepath,\
									 dim =3,\
									 scan_angle = np.pi/2.0,\
	                                 radius_start = 12.4,\
	                                 radius_stop = 117.5,\
	                                 sz_output = (1108,725),\
	                                 spacing_output = (0.15, 0.15, 0.15)):
	
	## Retrive the dimension of inputImage
	#dim                  	   = itkImg.ImageDimension
	frames                     = 0 
	sz_output                  = (1108,725)
	origin_output              = [0.0, 0.0]
	

	iType_CurvilinearImg 	   = itk.CurvilinearArraySpecialCoordinatesImage[itk.F, dim]
	iType_SCUSImg              = itk.Image[itk.F, dim]

	iFileReaderUSRF            = itk.ImageFileReader[iType_CurvilinearImg].New()
	iFileReaderUSRF.SetFileName(input_filepath)
	iFileReaderUSRF.UpdateOutputInformation()
	iimg_curvilinear           = iFileReaderUSRF.GetOutput()

	
	if dim == 3:
		frames                 = int(itk.size(iimg_curvilinear)[2])
		sz_output              = (1108,725, frames)
		origin_output          = [0.0, 0.0, 0.0]
		spacing_output         = (0.15, 0.15, 0.15)
	else:
		sz_output              = (1108,725)
		origin_output          = [0.0, 0.0]
		spacing_output         = (0.15, 0.15)

	isz_curvilinear            = iimg_curvilinear.GetLargestPossibleRegion().GetSize()

	## Computing the parameters of curvilinear sacn-conversion
	lateral_angular_separation = scan_angle / (isz_curvilinear[1]-1) 
	radius_scan                = (radius_stop - radius_start) / (isz_curvilinear[0]-1)
	
	# sz_output                  = (1108,725, frames)
	# origin_output              = [0.0, 0.0, 0.0]
	origin_output[0]           = sz_output[0] * spacing_output[0]/ -2.0
	origin_output[1]           = radius_start * np.cos(scan_angle/2)

	iimg_curvilinear.SetLateralAngularSeparation(lateral_angular_separation)
	iimg_curvilinear.SetFirstSampleDistance(radius_start)
	iimg_curvilinear.SetRadiusSampleSize(radius_scan)

	## Resample Image
	#iType_UCharImg             = itk.Image[itk.UC, dim]
	iFilter_resample           = itk.ResampleImageFilter[iType_CurvilinearImg, iType_SCUSImg].New()
	iFilter_resample.SetInput(iimg_curvilinear)
	iFilter_resample.SetSize(sz_output)
	iFilter_resample.SetOutputSpacing(spacing_output)
	iFilter_resample.SetOutputOrigin(origin_output)
	iFilter_resample.UpdateLargestPossibleRegion()

	## Return a scan-converted US BMode image
	return iFilter_resample.GetOutput()


def ScanConvert_ComputedFiles(input_filepath, PWCoef_method):
	
	print ">>>>>>>>>>>>> ScanConvert_ComputedFiles"
	print input_filepath
	print "<<<<<<<<<<<<< ScanConvert_ComputedFiles"

	###
	T_file_dir, T_file_name, T_file_ext = GetFileDirNameExt(input_filepath)
	T_PWSpectSC_Dir = T_file_dir + '/Scanconverted/'

	if not os.path.exists(T_PWSpectSC_Dir):
		os.makedirs(T_PWSpectSC_Dir)   ## Create a new Folder
	else:
		shutil.rmtree(T_PWSpectSC_Dir) ## Delete an existing Folder
		os.makedirs(T_PWSpectSC_Dir)   ## Create a new Folder

	itype  = itk.Image[itk.F, 2]
	iFileWriterPWSpCSC = itk.ImageFileWriter[itype].New()

	#T_PWSpectSC_Dir = T_PWSpectSC_Dir + '/'
    ## Laod a targeted image with input_filepath
	dim                        = 2
	
	if PWCoef_method != 1:
		dim = 3


	iimage_PWSPectraCoefSC     = ITKUSCurvilinearScanconvert_File(input_filepath, dim)

	## Save the 
	## Save the Scanconverted Data as mutiple 2D mha files
	iType_SCUS2DImg            = itk.Image[itk.F, 2]
	iType_SCUS3DImg            = itk.Image[itk.F, 3]

	print '+++++++++Saving'
	print 'dim', dim
	if dim == 2:
		filepath_output        = T_PWSpectSC_Dir+T_file_name+'_SC.mha'
		iFileWriterPWSpCSC.SetFileName(filepath_output)
		iFileWriterPWSpCSC.SetInput(iimage_PWSPectraCoefSC)
		iFileWriterPWSpCSC.Update()
	else:
		region_SCImg           = iimage_PWSPectraCoefSC.GetLargestPossibleRegion()
		sz_SCImg               = region_SCImg.GetSize()
		frames                 = sz_SCImg[2]
		
		iExtractor_2DSCImg     = itk.ExtractImageFilter[iType_SCUS3DImg, iType_SCUS2DImg].New()
		iExtractor_2DSCImg.SetInput(iimage_PWSPectraCoefSC)
		iExtractor_2DSCImg.SetDirectionCollapseToIdentity()
		sz_Extract             = (int(sz_SCImg[0]), int(sz_SCImg[1]), 0)
		region_Extract         = itk.ImageRegion[3]()
		region_Extract.SetSize(sz_Extract)
		idx_Extract            = region_Extract.GetIndex()
		for frame in np.arange(frames):
			idx_Extract[2]     = frame
			region_Extract.SetIndex(idx_Extract)
			iExtractor_2DSCImg.SetExtractionRegion(region_Extract)
			iExtractor_2DSCImg.UpdateLargestPossibleRegion()

			filepath_output        = T_PWSpectSC_Dir+T_file_name+'_SC_Coef_%d.mha'%frame
			iFileWriterPWSpCSC.SetFileName(filepath_output)
			iFileWriterPWSpCSC.SetInput(iExtractor_2DSCImg.GetOutput())
			iFileWriterPWSpCSC.Update()


## Generate file path
def Pre_ScanConvert_ComputedFiles(rf_filepath, PWCoef_method =1):
	
	## Retrive the method for computing Power Spectrum Coefficient
	map_PWCoef_method = { 1:'Integrated', 2:'Chebyshev',
	                      3:'Legendre',   4:'LineRegress' }
	method_PWCoef     = map_PWCoef_method[PWCoef_method]

	T_file_dir, T_file_name, T_file_ext = GetFileDirNameExt(root_target_rf_file)
	T_PWSpect_Dir = T_file_dir + '/RF_PWSpectra/'

	N1DFFT_R = [32,64] #[32,64,128]
	SideLine_R = [2]#[1,2,4,8,16,32]

	method  = method_PWCoef
	if PWCoef_method == 4:
		method = 'Line'

	print method

	for nsfft  in N1DFFT_R:
		for szline in SideLine_R:
			Target_Dir        = T_PWSpect_Dir + 'SLine_%03d' %szline +'_NFFT_%03d' %nsfft +'/' + method_PWCoef +'/'
			Target_File_F     = T_file_name +'_SLine_%03d' %szline +'_NFFT_%03d' %nsfft + '_frame_00009_' + method + '.mha' 
			Target_FilePath_F = Target_Dir+Target_File_F
			print Target_FilePath_F
			ScanConvert_ComputedFiles(Target_FilePath_F, PWCoef_method)

			# Target_File_A     = T_file_name +'_SLine_%03d' %szline +'_NFFT_%03d' %nsfft + '_Avg_' + method + '.mha' 
			# Target_FilePath_A = Target_Dir+Target_File_A
			# print Target_FilePath_A
			# ScanConvert_ComputedFiles(Target_FilePath_A, PWCoef_method)



if __name__ == "__main__":
	if len(sys.argv) == 3:
		print 'input 3'
		root_target_rf_file = sys.argv[1]
		pwcoefmethod        = int(sys.argv[2])
		
		Pre_ScanConvert_ComputedFiles(root_target_rf_file, pwcoefmethod)
