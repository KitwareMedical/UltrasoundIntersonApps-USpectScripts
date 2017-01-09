__author__ = 'hyunjaekang'

import sys
sys.path.append('/home/ubuntu/src/ITK-Release/Wrapping/Generators/Python')
sys.path.append('/home/ubuntu/src/ITK-Release/lib')

import numpy as np
import matplotlib.pyplot as plt
import os
import scipy.stats
import scipy.signal
import itk
import skimage.io

def GetFileDirNameExt(file_Path):
    file_dir, splt_t = os.path.split(file_Path)
    file_name, file_ext = os.path.splitext(splt_t)
    return file_dir, file_name, file_ext

def Analyze_USRF_PWSpectra(target_pw_file, base_pw_file):
    T_Dir, T_FileName, T_FileExt = GetFileDirNameExt(target_pw_file)

    TargetDir = T_Dir+'/Features/'
    if not os.path.exists(TargetDir):
        os.makedirs(TargetDir)

    B_Dir, B_FileName, B_FileExt = GetFileDirNameExt(base_pw_file)

    print "target_pw_file: ", target_pw_file
    frame_target = np.load(target_pw_file)
    frame_base   = np.load((base_pw_file))

    print "frame_target.shape:", frame_target.shape
    cols, rows, freqs = frame_target.shape

    tar_col = frame_base[0,0]
    tar_row = frame_base[1,0]
    win_1   = max(frame_base[2,0], 0)
    win_2   = min(frame_base[3,0]+1, freqs)
    base_pw = frame_base[4,0]

    ## Save Log 
    log_file_path = T_Dir + 'LogFile.txt'
    log_file = open(log_file_path, 'w')
    log_file.write("input target file: \n")
    log_file.write("%s \n" % target_pw_file)
    log_file.write("input base pw file: \n")
    log_file.write("%s \n" % base_pw_file)
    log_file.write("base pw position (col, row):\n")
    log_file.write("%d, %d \n" % (tar_col, tar_row))
    log_file.write("windos index (win1, win2)\n")
    log_file.write("%d, %d \n" % (win_1, win_2))
    log_file.close()
    

    ## Save Base PW Line
    output_filepath = T_Dir+B_FileName+B_FileExt
    np.save(output_filepath,frame_base)

    # Prep images
    cheb_dim_img_z = 7
    cheb_img_fit = np.zeros([cheb_dim_img_z, cols, rows], dtype = np.float32)

    line_dim_img_z = 2
    line_img_fit = np.zeros([line_dim_img_z, cols, rows], dtype = np.float32)

    legn_dim_img_z = 7
    legn_img_fit = np.zeros([legn_dim_img_z, cols, rows], dtype = np.float32)

    intg_dim_img_z = 1
    intg_img_fit = np.zeros([intg_dim_img_z, cols, rows], dtype = np.float32)

    for col in np.arange(cols):
        print "Column ", col, " of ", cols
        for row in np.arange(rows):
            temp_rf_pw = frame_target[col, row, :]
            temp_rf_pw_norm = temp_rf_pw / base_pw
            temp_rf_pw_norm_win = temp_rf_pw_norm[int(win_1):int(win_2)]
            cheb_coefs = np.polynomial.chebyshev.Chebyshev.fit(
                np.arange(len(temp_rf_pw_norm_win)), temp_rf_pw_norm_win,
                    cheb_dim_img_z-1)
            #line_slope, line_intercept, line_r, line_p, line_stderr = \
            line_coefs = scipy.stats.linregress(
                np.arange(len(temp_rf_pw_norm_win)), temp_rf_pw_norm_win)
            legn_coefs = np.polynomial.legendre.legfit(
                np.arange(len(temp_rf_pw_norm_win)), temp_rf_pw_norm_win,
                    legn_dim_img_z-1)
            intg_coefs = np.sum(temp_rf_pw_norm_win)

            for dz in np.arange(cheb_dim_img_z):
                cheb_img_fit[dz, col, row] = cheb_coefs.coef[dz]

            for dz in np.arange(line_dim_img_z):
                line_img_fit[dz, col, row] = line_coefs[dz]

            for dz in np.arange(legn_dim_img_z):
                legn_img_fit[dz, col, row] = legn_coefs[dz]

            intg_img_fit[0, col, row] = intg_coefs

    ## Save *.NP

    # Cheb
    OutputFile = TargetDir + T_FileName + '_Chebyshev.npy'
    np.save(OutputFile, cheb_img_fit)

    # Line
    OutputFile = TargetDir + T_FileName + '_Line.npy'
    np.save(OutputFile, line_img_fit)

    # Legendre
    OutputFile = TargetDir + T_FileName + '_Legendre.npy'
    np.save(OutputFile, legn_img_fit)

    # Intg
    OutputFile = TargetDir + T_FileName + '_Integration.npy'
    np.save(OutputFile, intg_img_fit)


    ## Save 2D Files
    dim_2D = 2
    usRF_pixel_type = itk.F
    us_RF2D_Type = itk.Image[usRF_pixel_type, dim_2D]

    # Cheb
    for z in np.arange(cheb_dim_img_z):
        Gimg_filepath = output_filepath = TargetDir + T_FileName + \
            '_Cheb_Coef_%03d.mha' % z
        us_pw2d = itk.PyBuffer[us_RF2D_Type].GetImageFromArray(
            cheb_img_fit[z,:,:])
    
        FileWriter2D = itk.ImageFileWriter[us_RF2D_Type].New()
        FileWriter2D.SetUseCompression( True )
        FileWriter2D.SetFileName(Gimg_filepath)
        FileWriter2D.SetInput(us_pw2d)
        FileWriter2D.Update()

    # Line
    for z in np.arange(line_dim_img_z):
        Gimg_filepath = output_filepath = TargetDir + T_FileName + \
            '_Line_Coef_%03d.mha' % z
        us_pw2d = itk.PyBuffer[us_RF2D_Type].GetImageFromArray(
            line_img_fit[z,:,:])
    
        FileWriter2D = itk.ImageFileWriter[us_RF2D_Type].New()
        FileWriter2D.SetUseCompression( True )
        FileWriter2D.SetFileName(Gimg_filepath)
        FileWriter2D.SetInput(us_pw2d)
        FileWriter2D.Update()

    # Legendre
    for z in np.arange(legn_dim_img_z):
        Gimg_filepath = output_filepath = TargetDir + T_FileName + \
            '_Legn_Coef_%03d.mha' % z
        us_pw2d = itk.PyBuffer[us_RF2D_Type].GetImageFromArray(
            legn_img_fit[z,:,:])
    
        FileWriter2D = itk.ImageFileWriter[us_RF2D_Type].New()
        FileWriter2D.SetUseCompression( True )
        FileWriter2D.SetFileName(Gimg_filepath)
        FileWriter2D.SetInput(us_pw2d)
        FileWriter2D.Update()

    # Integration
    Gimg_filepath = output_filepath = TargetDir + T_FileName + \
        '_Legn_Coef_000.mha'
    us_pw2d = itk.PyBuffer[us_RF2D_Type].GetImageFromArray(
        intg_img_fit[0,:,:])
  
    FileWriter2D = itk.ImageFileWriter[us_RF2D_Type].New()
    FileWriter2D.SetUseCompression( True )
    FileWriter2D.SetFileName(Gimg_filepath)
    FileWriter2D.SetInput(us_pw2d)
    FileWriter2D.Update()


    ## Save *.mha
    dim_3D = 3
    us_RF3D_Type = itk.Image[usRF_pixel_type, dim_3D]

    # Cheb
    output_filepath = TargetDir + T_FileName + '_Chebyshev.mha'
    us_pw3d = itk.PyBuffer[us_RF3D_Type].GetImageFromArray(cheb_img_fit)

    FileWriter3D = itk.ImageFileWriter[us_RF3D_Type].New()
    FileWriter3D.SetFileName(output_filepath)
    FileWriter3D.SetUseCompression( True )
    FileWriter3D.SetInput(us_pw3d)
    FileWriter3D.Update()

    # Line
    output_filepath = TargetDir + T_FileName + '_Line.mha'
    us_pw3d = itk.PyBuffer[us_RF3D_Type].GetImageFromArray(line_img_fit)

    FileWriter3D = itk.ImageFileWriter[us_RF3D_Type].New()
    FileWriter3D.SetFileName(output_filepath)
    FileWriter3D.SetUseCompression( True )
    FileWriter3D.SetInput(us_pw3d)
    FileWriter3D.Update()

    # Legendre
    output_filepath = TargetDir + T_FileName + '_Legendre.mha'
    us_pw3d = itk.PyBuffer[us_RF3D_Type].GetImageFromArray(legn_img_fit)

    FileWriter3D = itk.ImageFileWriter[us_RF3D_Type].New()
    FileWriter3D.SetFileName(output_filepath)
    FileWriter3D.SetUseCompression( True )
    FileWriter3D.SetInput(us_pw3d)
    FileWriter3D.Update()

    # Integration
    output_filepath = TargetDir + T_FileName + '_Integration.mha'
    us_pw3d = itk.PyBuffer[us_RF3D_Type].GetImageFromArray(intg_img_fit)

    FileWriter3D = itk.ImageFileWriter[us_RF3D_Type].New()
    FileWriter3D.SetFileName(output_filepath)
    FileWriter3D.SetUseCompression( True )
    FileWriter3D.SetInput(us_pw3d)
    FileWriter3D.Update()


def Pre_Analyze_USRF_PWSpectra(root_target_rf_file, root_base_rf_file):

    T_file_dir, T_file_name, T_file_ext = GetFileDirNameExt(root_target_rf_file)
    T_PWSpect_Dir = T_file_dir +'/RF_PWSpectra/'

    B_file_dir, B_file_name, B_file_ext = GetFileDirNameExt(root_base_rf_file)
    B_PWSpect_Dir = B_file_dir +'/'

    N1DFFT_R = [32,64]
    SideLine_R = [2]

    for nsfft  in N1DFFT_R:
        for szline in SideLine_R:
            # Target File
            Target_Dir = T_PWSpect_Dir + 'SLine_%03d' %szline + \
                '_NFFT_%03d/' %nsfft
            Target_File = T_file_name +'_SLine_%03d' %szline + \
                '_NFFT_%03d' %nsfft +'_Avg.npy'
            Target_FilePath = Target_Dir+Target_File
            print "Target file = ", Target_FilePath

            # BaseLine File
            Base_Dir = B_PWSpect_Dir 
            Base_File = B_file_name +'_SLine_%03d' %szline + \
                '_NFFT_%03d' %nsfft +'_Avg_BL.npy'
            Base_FilePath   = Base_Dir+Base_File
            print "Baseline file - ", Base_FilePath

            Analyze_USRF_PWSpectra(Target_FilePath, Base_FilePath)


if __name__ == '__main__':
    if len(sys.argv) == 3:
        print 'input 3'
        root_target_rf_file = sys.argv[1]
        root_base_rf_file = sys.argv[2]
        Pre_Analyze_USRF_PWSpectra(root_target_rf_file, root_base_rf_file)
