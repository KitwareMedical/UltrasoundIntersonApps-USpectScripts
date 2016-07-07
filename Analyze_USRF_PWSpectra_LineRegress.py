__author__ = 'hyunjaekang'

import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import scipy.stats
import scipy.signal
import itk
import skimage.io

def GetFileDirNameExt(file_Path):
    file_dir, splt_t = os.path.split(file_Path)
    file_name, file_ext = os.path.splitext(splt_t)
    return file_dir, file_name, file_ext

def ComputeLineRegress(target_pw_file, base_pw_file):
    T_Dir, T_FileName, T_FileExt = GetFileDirNameExt(target_pw_file)

    TargetDir = T_Dir+'/LineRegress/'
    if not os.path.exists(TargetDir):
        os.makedirs(TargetDir)

    B_Dir, B_FileName, B_FileExt = GetFileDirNameExt(base_pw_file)

    output_filepath = TargetDir + T_FileName + '_Line.mha'

    if os.path.isfile(output_filepath):
        print "Computed"
    else:
        frame_target = np.load(target_pw_file)
        frame_base   = np.load((base_pw_file))

        cols, rows, freqs = frame_target.shape
        print "Cols: %d, Rows %d, NumOfFreqs: %d" %(cols,rows,freqs)

        tar_col = frame_base[0,0]
        tar_row = frame_base[1,0]
        win_1   = max(frame_base[2,0], 0)
        win_2   = min(frame_base[3,0]+1, freqs)
        base_pw = frame_base[4,0]

        ## Save Log 
        log_file_path = TargetDir + 'LogFile.txt'
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
        output_filepath = TargetDir+B_FileName+B_FileExt
        np.save(output_filepath,frame_base)

        dim_img_z = 2
        img_fit = np.zeros([dim_img_z, cols, rows], dtype = np.float32)

        for col in np.arange(cols):
            for row in np.arange(rows):
                temp_rf_pw = frame_target[col, row, :]
                temp_rf_pw_norm = temp_rf_pw / base_pw
                temp_rf_pw_norm_win = temp_rf_pw_norm[win_1:win_2]
                slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(np.arange(len(temp_rf_pw_norm_win)), temp_rf_pw_norm_win)

                img_fit[0, col, row] = intercept
                img_fit[1, col, row] = slope

        ## Save Base PW Line
        output_filepath = TargetDir+B_FileName+B_FileExt
        np.save(output_filepath,frame_base)

        ## Save *.NP
        OutputFile = TargetDir + T_FileName + '_Line.npy'
        np.save(OutputFile, img_fit)

        ## Save PNG Files
        for z in np.arange(dim_img_z):
            Gimg_filepath = output_filepath = TargetDir + T_FileName + '_G_Coef_%03d.png' % z
            gcmap = plt.get_cmap('gray')
            g_img = gcmap(img_fit[z,:,:])
            skimage.io.imsave(Gimg_filepath, g_img)

            Himg_filepath = output_filepath = TargetDir + T_FileName + '_H_Coef_%03d.png' % z
            hcmap = plt.get_cmap('hot')
            h_img = hcmap(img_fit[z,:,:])
            skimage.io.imsave(Himg_filepath, h_img)

        ## Save *.mha
        output_filepath = TargetDir + T_FileName + '_Line.mha'
        dim_3D = 3
        usRF_pixel_type = itk.F
        us_RF3D_Type = itk.Image[usRF_pixel_type, dim_3D]
        us_pw3d = itk.PyBuffer[us_RF3D_Type].GetImageFromArray(img_fit)

        FileWriter3D = itk.ImageFileWriter[us_RF3D_Type].New()
        FileWriter3D.SetFileName(output_filepath)
        FileWriter3D.SetInput(us_pw3d)
        FileWriter3D.Update()



def ComputeLegendre(target_pw_file, base_pw_file):
    T_Dir, T_FileName, T_FileExt = GetFileDirNameExt(target_pw_file)

    TargetDir = T_Dir+'/Legendre/'
    if not os.path.exists(TargetDir):
        os.makedirs(TargetDir)

    B_Dir, B_FileName, B_FileExt = GetFileDirNameExt(base_pw_file)

    frame_target = np.load(target_pw_file)
    frame_base   = np.load((base_pw_file))

    cols, rows, freqs = frame_target.shape
    print "Cols: %d, Rows %d, NumOfFreqs: %d" %(cols,rows,freqs)

    tar_col = frame_base[0,0]
    tar_row = frame_base[1,0]
    win_1   = max(frame_base[2,0], 0)
    win_2   = min(frame_base[3,0]+1, freqs)
    base_pw = frame_base[4,0]

    dim_img_z = 7
    img_fit = np.zeros([dim_img_z, cols, rows], dtype = np.float32)

    for col in np.arange(cols):
        for row in np.arange(rows):
            temp_rf_pw = frame_target[col, row, :]
            temp_rf_pw_norm = temp_rf_pw / base_pw
            temp_rf_pw_norm_win = temp_rf_pw_norm[win_1:win_2]
            coefs = np.polynomial.legendre.legfit(np.arange(len(temp_rf_pw_norm_win)), temp_rf_pw_norm_win, dim_img_z-1)

            for dz in np.arange(dim_img_z):
                img_fit[dz, col, row] = coefs[dz]


    ## Save Base PW Line
    output_filepath = TargetDir+B_FileName+B_FileExt
    np.save(output_filepath,frame_base)

    ## Save *.NP
    OutputFile = TargetDir + T_FileName + '_Legendre.npy'
    np.save(OutputFile, img_fit)

    ## Save PNG Files
    for z in np.arange(dim_img_z):
        Gimg_filepath = output_filepath = TargetDir + T_FileName + '_G_Coef_%03d.png' % z
        gcmap = plt.get_cmap('gray')
        g_img = gcmap(img_fit[z,:,:])
        skimage.io.imsave(Gimg_filepath, g_img)

        Himg_filepath = output_filepath = TargetDir + T_FileName + '_H_Coef_%03d.png' % z
        hcmap = plt.get_cmap('hot')
        h_img = hcmap(img_fit[z,:,:])
        skimage.io.imsave(Himg_filepath, h_img)

    ## Save *.mha
    output_filepath = TargetDir + T_FileName + '_Legendre.mha'
    dim_3D = 3
    usRF_pixel_type = itk.F
    us_RF3D_Type = itk.Image[usRF_pixel_type, dim_3D]
    us_pw3d = itk.PyBuffer[us_RF3D_Type].GetImageFromArray(img_fit)

    FileWriter3D = itk.ImageFileWriter[us_RF3D_Type].New()
    FileWriter3D.SetFileName(output_filepath)
    FileWriter3D.SetInput(us_pw3d)
    FileWriter3D.Update()



def ComputeChebyshev(target_pw_file, base_pw_file):
    T_Dir, T_FileName, T_FileExt = GetFileDirNameExt(target_pw_file)

    TargetDir = T_Dir+'/Chebyshev/'
    if not os.path.exists(TargetDir):
        os.makedirs(TargetDir)

    B_Dir, B_FileName, B_FileExt = GetFileDirNameExt(base_pw_file)

    frame_target = np.load(target_pw_file)
    frame_base   = np.load((base_pw_file))

    cols, rows, freqs = frame_target.shape
    print "Cols: %d, Rows %d, NumOfFreqs: %d" %(cols,rows,freqs)

    tar_col = frame_base[0,0]
    tar_row = frame_base[1,0]
    win_1   = max(frame_base[2,0], 0)
    win_2   = min(frame_base[3,0]+1, freqs)
    base_pw = frame_base[4,0]

    dim_img_z = 7
    img_fit = np.zeros([dim_img_z, cols, rows], dtype = np.float32)

    for col in np.arange(cols):
        for row in np.arange(rows):
            temp_rf_pw = frame_target[col, row, :]
            temp_rf_pw_norm = temp_rf_pw / base_pw
            temp_rf_pw_norm_win = temp_rf_pw_norm[win_1:win_2]
            coefs = np.polynomial.chebyshev.Chebyshev.fit(np.arange(len(temp_rf_pw_norm_win)), temp_rf_pw_norm_win, dim_img_z-1)

            for dz in np.arange(dim_img_z):
                img_fit[dz, col, row] = coefs[dz]


    ## Save Base PW Line
    output_filepath = TargetDir+B_FileName+B_FileExt
    np.save(output_filepath,frame_base)

    ## Save *.NP
    OutputFile = TargetDir + T_FileName + '_Chebyshev.npy'
    np.save(OutputFile, img_fit)

    ## Save PNG Files
    for z in np.arange(dim_img_z):
        Gimg_filepath = output_filepath = TargetDir + T_FileName + '_G_Coef_%03d.png' % z
        gcmap = plt.get_cmap('gray')
        g_img = gcmap(img_fit[z,:,:])
        skimage.io.imsave(Gimg_filepath, g_img)

        Himg_filepath = output_filepath = TargetDir + T_FileName + '_H_Coef_%03d.png' % z
        hcmap = plt.get_cmap('hot')
        h_img = hcmap(img_fit[z,:,:])
        skimage.io.imsave(Himg_filepath, h_img)

    ## Save *.mha
    output_filepath = TargetDir + T_FileName + '_Chebyshev.mha'
    dim_3D = 3
    usRF_pixel_type = itk.F
    us_RF3D_Type = itk.Image[usRF_pixel_type, dim_3D]
    us_pw3d = itk.PyBuffer[us_RF3D_Type].GetImageFromArray(img_fit)

    FileWriter3D = itk.ImageFileWriter[us_RF3D_Type].New()
    FileWriter3D.SetFileName(output_filepath)
    FileWriter3D.SetInput(us_pw3d)
    FileWriter3D.Update()



def ComputeIntegrated(target_pw_file, base_pw_file):
    T_Dir, T_FileName, T_FileExt = GetFileDirNameExt(target_pw_file)

    TargetDir = T_Dir+'/Integrated/'
    if not os.path.exists(TargetDir):
        os.makedirs(TargetDir)

    B_Dir, B_FileName, B_FileExt = GetFileDirNameExt(base_pw_file)

    frame_target = np.load(target_pw_file)
    frame_base   = np.load((base_pw_file))

    cols, rows, freqs = frame_target.shape
    print "Cols: %d, Rows %d, NumOfFreqs: %d" %(cols,rows,freqs)

    tar_col = frame_base[0,0]
    tar_row = frame_base[1,0]
    win_1   = max(frame_base[2,0], 0)
    win_2   = min(frame_base[3,0]+1, freqs)
    base_pw = frame_base[4,0]


    img_fit = np.zeros([cols, rows], dtype = np.float32)

    for col in np.arange(cols):
        for row in np.arange(rows):
            temp_rf_pw = frame_target[col, row, :]
            temp_rf_pw_norm = temp_rf_pw / base_pw
            temp_rf_pw_norm_win = temp_rf_pw_norm[win_1:win_2]
            img_fit[col, row] = np.sum(temp_rf_pw_norm_win)


    ## Save Base PW Line
    output_filepath = TargetDir+B_FileName+B_FileExt
    np.save(output_filepath,frame_base)

    ## Save *.NP
    OutputFile = TargetDir + T_FileName + '_Integrated.npy'
    np.save(OutputFile, img_fit)

    ## Save PNG Files

    Gimg_filepath = output_filepath = TargetDir + T_FileName + '_G_Coef_.png'
    gcmap = plt.get_cmap('gray')
    g_img = gcmap(img_fit[:,:])
    skimage.io.imsave(Gimg_filepath, g_img)

    Himg_filepath = output_filepath = TargetDir + T_FileName + '_H_Coef_.png'
    hcmap = plt.get_cmap('hot')
    h_img = hcmap(img_fit[:,:])
    skimage.io.imsave(Himg_filepath, h_img)

    ## Save *.mha
    output_filepath = TargetDir + T_FileName + '_Integrated.mha'
    dim_3D = 2
    usRF_pixel_type = itk.F
    us_RF3D_Type = itk.Image[usRF_pixel_type, dim_3D]
    us_pw3d = itk.PyBuffer[us_RF3D_Type].GetImageFromArray(img_fit)

    FileWriter3D = itk.ImageFileWriter[us_RF3D_Type].New()
    FileWriter3D.SetFileName(output_filepath)
    FileWriter3D.SetInput(us_pw3d)
    FileWriter3D.Update()

def Analyze_USRF_PWSpectra(target_pw_file, base_pw_file):

    # ComputeChebyshev(target_pw_file, base_pw_file)
    # ComputeLegendre(target_pw_file, base_pw_file)
    ComputeLineRegress(target_pw_file, base_pw_file)
    # ComputeIntegrated(target_pw_file, base_pw_file)

def Pre_Analyze_USRF_PWSpectra(root_target_rf_file, root_base_rf_file):

    T_file_dir, T_file_name, T_file_ext = GetFileDirNameExt(root_target_rf_file)
    T_PWSpect_Dir = T_file_dir +'/RF_PWSpectra/'

    B_file_dir, B_file_name, B_file_ext = GetFileDirNameExt(root_base_rf_file)
    B_PWSpect_Dir = B_file_dir +'/RF_PWSpectra/'

    N1DFFT_R = [32,64,128]

    SideLine_R = [1,2,4,8,16,32]
    for nsfft  in N1DFFT_R:
        for szline in SideLine_R:
            # Target File
            Target_Dir      = T_PWSpect_Dir + 'SLine_%03d' %szline +'_NFFT_%03d/' %nsfft
            Target_File     = T_file_name +'_SLine_%03d' %szline +'_NFFT_%03d' %nsfft +'_frame_00009.npy'
            Target_FilePath = Target_Dir+Target_File
            print Target_FilePath

            # BaseLine File
            Base_Dir        = B_PWSpect_Dir + 'SLine_%03d' %szline +'_NFFT_%03d/' %nsfft
            Base_File       = B_file_name +'_SLine_%03d' %szline +'_NFFT_%03d' %nsfft +'_Avg_BL.npy'
            Base_FilePath   = Base_Dir+Base_File
            print Base_FilePath

            Analyze_USRF_PWSpectra(Target_FilePath, Base_FilePath)

            # Target File
            Target_Dir      = T_PWSpect_Dir + 'SLine_%03d' %szline +'_NFFT_%03d/' %nsfft
            Target_File     = T_file_name +'_SLine_%03d' %szline +'_NFFT_%03d' %nsfft +'_Avg.npy'
            Target_FilePath = Target_Dir+Target_File
            print Target_FilePath

            # BaseLine File
            Base_Dir        = B_PWSpect_Dir + 'SLine_%03d' %szline +'_NFFT_%03d/' %nsfft
            Base_File       = B_file_name +'_SLine_%03d' %szline +'_NFFT_%03d' %nsfft +'_Avg_BL.npy'
            Base_FilePath   = Base_Dir+Base_File
            print Base_FilePath

            Analyze_USRF_PWSpectra(Target_FilePath, Base_FilePath)






if __name__ == '__main__':
    if len(sys.argv) == 3:
        print 'input 3'
        #input_file = sys.argv[1]
        #input_file = '/Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/BaseLine_P1_F25/RF_PWSpectra/SLine_001_NFFT_032/BaseLine_P1_F25_SLine_001_NFFT_032_Avg.npy'
        #Select_Ref_Baseline_Windows(input_file)
        root_target_rf_file = sys.argv[1]
        root_base_rf_file = sys.argv[2]
        Pre_Analyze_USRF_PWSpectra(root_target_rf_file, root_base_rf_file)