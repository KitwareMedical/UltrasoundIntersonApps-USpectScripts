#!/bin/sh

# python SciKit_SLIC_Folder.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/000_Selected_Cadaver_USData


# # BaseLine_P1_F25   Liver_P15_F50_2   Steak_P15_F25_3   Steak_P30_F25_3
# # BaseLine_P1_F35   Liver_P30_F25     Steak_P15_F35     Steak_P30_F35
# # BaseLine_P1_F50   Liver_P30_F25_2   Steak_P15_F35_2   Steak_P30_F35_2
# # BaseLine_P1_F50_2 Liver_P30_F35     Steak_P15_F35_3   Steak_P30_F35_3
# # Liver_P15_F25     Liver_P30_F35_2   Steak_P15_F50     Steak_P30_F50
# # Liver_P15_F25_2   Liver_P30_F50     Steak_P15_F50_2   Steak_P30_F50_2
# # Liver_P15_F35     Liver_P30_F50_2   Steak_P15_F50_3   Steak_P30_F50_3
# # Liver_P15_F35_2   Steak_P15_F25     Steak_P30_F25
# # Liver_P15_F50     Steak_P15_F25_2   Steak_P30_F25_2


### Convert 3D BMode
python ConvertRF2BMode_2DImages.py \
  /Volumes/KHJ_WD_2T/900_Data/300_Project_FAST/90_Data/FAST/2014-11-17-mts/donor1/TrackedImageSequence_CaptureDevice_20141117_210842.mha

python ConvertRF2BMode_2DImages.py \
  /Volumes/KHJ_WD_2T/900_Data/300_Project_FAST/90_Data/FAST/2014-11-17-mts/donor1/TrackedImageSequence_CaptureDevice_20141117_210923.mha

python ConvertRF2BMode_2DImages.py \
  /Volumes/KHJ_WD_2T/900_Data/300_Project_FAST/90_Data/FAST/2014-11-17-mts/donor1/TrackedImageSequence_CaptureDevice_20141117_211023.mha

python ConvertRF2BMode_2DImages.py \
  /Volumes/KHJ_WD_2T/900_Data/300_Project_FAST/90_Data/FAST/2014-11-17-mts/donor1/TrackedImageSequence_CaptureDevice_20141117_211827.mha


### Convert 2D BMode


echo 'Done'
exit 0


