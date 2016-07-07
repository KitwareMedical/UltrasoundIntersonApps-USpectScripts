#!/bin/sh

python SciKit_SLIC_Folder.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/000_Selected_Cadaver_USData


# BaseLine_P1_F25   Liver_P15_F50_2   Steak_P15_F25_3   Steak_P30_F25_3
# BaseLine_P1_F35   Liver_P30_F25     Steak_P15_F35     Steak_P30_F35
# BaseLine_P1_F50   Liver_P30_F25_2   Steak_P15_F35_2   Steak_P30_F35_2
# BaseLine_P1_F50_2 Liver_P30_F35     Steak_P15_F35_3   Steak_P30_F35_3
# Liver_P15_F25     Liver_P30_F35_2   Steak_P15_F50     Steak_P30_F50
# Liver_P15_F25_2   Liver_P30_F50     Steak_P15_F50_2   Steak_P30_F50_2
# Liver_P15_F35     Liver_P30_F50_2   Steak_P15_F50_3   Steak_P30_F50_3
# Liver_P15_F35_2   Steak_P15_F25     Steak_P30_F25
# Liver_P15_F50     Steak_P15_F25_2   Steak_P30_F25_2
             

### Convert 3D BMode
# python ConvertRF2BMode_3D.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/BaseLine_P1_F25/BaseLine_P1_F25.mha /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/BaseLine_P1_F25/BaseLine_P1_F25_3DMbode.mha

# python ConvertRF2BMode_3D.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/BaseLine_P1_F25/BaseLine_P1_F25.mha /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/BaseLine_P1_F25/BaseLine_P1_F25_3DBMode.mha
# python ConvertRF2BMode_3D.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Liver_P15_F50_2/Liver_P15_F50_2.mha /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Liver_P15_F50_2/Liver_P15_F50_2_3DBMode.mha
# python ConvertRF2BMode_3D.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Steak_P15_F25_3/Steak_P15_F25_3.mha /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Steak_P15_F25_3/Steak_P15_F25_3_3DBMode.mha
# python ConvertRF2BMode_3D.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Steak_P30_F25_3/Steak_P30_F25_3.mha /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Steak_P30_F25_3/Steak_P30_F25_3_3DBMode.mha

# python ConvertRF2BMode_3D.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/BaseLine_P1_F35/BaseLine_P1_F35.mha /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/BaseLine_P1_F35/BaseLine_P1_F35_3DBMode.mha
# python ConvertRF2BMode_3D.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Liver_P30_F25/Liver_P30_F25.mha /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Liver_P30_F25/Liver_P30_F25_3DBmode.mha
# python ConvertRF2BMode_3D.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Steak_P15_F35/Steak_P15_F35.mha /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Steak_P15_F35/Steak_P15_F35_3DBMode.mha
# python ConvertRF2BMode_3D.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Steak_P30_F35/Steak_P30_F35.mha /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Steak_P30_F35/Steak_P30_F35_3DBMode.mha

# python ConvertRF2BMode_3D.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/BaseLine_P1_F50/BaseLine_P1_F50.mha /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/BaseLine_P1_F50/BaseLine_P1_F50_3DBMode.mha 
# python ConvertRF2BMode_3D.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Liver_P30_F25_2/Liver_P30_F25_2.mha /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Liver_P30_F25_2/Liver_P30_F25_2_3DBMode.mha
# python ConvertRF2BMode_3D.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Steak_P15_F35_2/Steak_P15_F35_2.mha /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Steak_P15_F35_2/Steak_P15_F35_2_3DBMode.mha
# python ConvertRF2BMode_3D.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Steak_P30_F35_2/Steak_P30_F35_2.mha /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Steak_P30_F35_2/Steak_P30_F35_2_3DBMode.mha

# python ConvertRF2BMode_3D.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/BaseLine_P1_F50_2/BaseLine_P1_F50_2.mha /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/BaseLine_P1_F50_2/BaseLine_P1_F50_2_3DBMode.mha 
# python ConvertRF2BMode_3D.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Liver_P30_F35/Liver_P30_F35.mha /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Liver_P30_F35/Liver_P30_F35_3DBMode.mha
# python ConvertRF2BMode_3D.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Steak_P15_F35_3/Steak_P15_F35_3.mha /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Steak_P15_F35_3/Steak_P15_F35_3_3DBMode.mha
# python ConvertRF2BMode_3D.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Steak_P30_F35_3/Steak_P30_F35_3.mha /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Steak_P30_F35_3/Steak_P30_F35_3_3DBMode.mha

# python ConvertRF2BMode_3D.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Liver_P15_F25/Liver_P15_F25.mha /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Liver_P15_F25/Liver_P15_F25_3DBMode.mha
# python ConvertRF2BMode_3D.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Liver_P30_F35_2/Liver_P30_F35_2.mha /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Liver_P30_F35_2/Liver_P30_F35_2_3DBMode.mha
# python ConvertRF2BMode_3D.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Steak_P15_F50/Steak_P15_F50.mha /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Steak_P15_F50/Steak_P15_F50_3DBmode.mha
# python ConvertRF2BMode_3D.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Steak_P30_F50/Steak_P30_F50.mha /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Steak_P30_F50/Steak_P30_F50_3DBMode.mha

# python ConvertRF2BMode_3D.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Liver_P15_F25_2/Liver_P15_F25_2.mha /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Liver_P15_F25_2/Liver_P15_F25_2_3DBMode.mha
# python ConvertRF2BMode_3D.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Liver_P30_F50/Liver_P30_F50.mha /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Liver_P30_F50/Liver_P30_F50_3DBMode.mha
# python ConvertRF2BMode_3D.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Steak_P15_F50_2/Steak_P15_F50_2.mha /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Steak_P15_F50_2/Steak_P15_F50_2_3DBMode.mha
# python ConvertRF2BMode_3D.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Steak_P30_F50_2/Steak_P30_F50_2.mha /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Steak_P30_F50_2/Steak_P30_F50_2_3DBMode.mha

# python ConvertRF2BMode_3D.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Liver_P15_F35/Liver_P15_F35.mha /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Liver_P15_F35/Liver_P15_F35_3DBMode.mha
# python ConvertRF2BMode_3D.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Liver_P30_F50_2/Liver_P30_F50_2.mha /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Liver_P30_F50_2/Liver_P30_F50_2_3DBMode.mha
# python ConvertRF2BMode_3D.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Steak_P15_F50_3/Steak_P15_F50_3.mha /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Steak_P15_F50_3/Steak_P15_F50_3_3DBMode.mha
# python ConvertRF2BMode_3D.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Steak_P30_F50_3/Steak_P30_F50_3.mha /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Steak_P30_F50_3/Steak_P30_F50_3_3DBMode.mha

# python ConvertRF2BMode_3D.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Liver_P15_F35_2/Liver_P15_F35_2.mha /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Liver_P15_F35_2/Liver_P15_F35_2_3DBMode.mha
# python ConvertRF2BMode_3D.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Steak_P15_F25/Steak_P15_F25.mha /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Steak_P15_F25/Steak_P15_F25_3DBMode.mha
# python ConvertRF2BMode_3D.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Steak_P30_F25/Steak_P30_F25.mha /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Steak_P30_F25/Steak_P30_F25_3DBMode.mha

# python ConvertRF2BMode_3D.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Liver_P15_F50/Liver_P15_F50.mha /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Liver_P15_F50/Liver_P15_F50_3DBMode.mha
# python ConvertRF2BMode_3D.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Steak_P15_F25_2/Steak_P15_F25_2.mha /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Steak_P15_F25_2/Steak_P15_F25_2_3DBMode.mha
# python ConvertRF2BMode_3D.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Steak_P30_F25_2/Steak_P30_F25_2.mha /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Steak_P30_F25_2/Steak_P30_F25_2_3DBMode.mha

# ### Convert Multiple 2D Image
# python ConvertRF2BMode_2DImages.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/BaseLine_P1_F25/BaseLine_P1_F25.mha
# python ConvertRF2BMode_2DImages.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Liver_P15_F50_2/Liver_P15_F50_2.mha
# python ConvertRF2BMode_2DImages.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Steak_P15_F25_3/Steak_P15_F25_3.mha
# python ConvertRF2BMode_2DImages.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Steak_P30_F25_3/Steak_P30_F25_3.mha

# python ConvertRF2BMode_2DImages.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/BaseLine_P1_F35/BaseLine_P1_F35.mha
# python ConvertRF2BMode_2DImages.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Liver_P30_F25/Liver_P30_F25.mha
# python ConvertRF2BMode_2DImages.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Steak_P15_F35/Steak_P15_F35.mha
# python ConvertRF2BMode_2DImages.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Steak_P30_F35/Steak_P30_F35.mha

# python ConvertRF2BMode_2DImages.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/BaseLine_P1_F50/BaseLine_P1_F50.mha
# python ConvertRF2BMode_2DImages.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Liver_P30_F25_2/Liver_P30_F25_2.mha
# python ConvertRF2BMode_2DImages.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Steak_P15_F35_2/Steak_P15_F35_2.mha
# python ConvertRF2BMode_2DImages.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Steak_P30_F35_2/Steak_P30_F35_2.mha

# python ConvertRF2BMode_2DImages.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/BaseLine_P1_F50_2/BaseLine_P1_F50_2.mha
# python ConvertRF2BMode_2DImages.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Liver_P30_F35/Liver_P30_F35.mha
# python ConvertRF2BMode_2DImages.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Steak_P15_F35_3/Steak_P15_F35_3.mha
# python ConvertRF2BMode_2DImages.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Steak_P30_F35_3/Steak_P30_F35_3.mha

# python ConvertRF2BMode_2DImages.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Liver_P15_F25/Liver_P15_F25.mha
# python ConvertRF2BMode_2DImages.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Liver_P30_F35_2/Liver_P30_F35_2.mha
# python ConvertRF2BMode_2DImages.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Steak_P15_F50/Steak_P15_F50.mha
# python ConvertRF2BMode_2DImages.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Steak_P30_F50/Steak_P30_F50.mha

# python ConvertRF2BMode_2DImages.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Liver_P15_F25_2/Liver_P15_F25_2.mha
# python ConvertRF2BMode_2DImages.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Liver_P30_F50/Liver_P30_F50.mha
# python ConvertRF2BMode_2DImages.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Steak_P15_F50_2/Steak_P15_F50_2.mha
# python ConvertRF2BMode_2DImages.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Steak_P30_F50_2/Steak_P30_F50_2.mha

# python ConvertRF2BMode_2DImages.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Liver_P15_F35/Liver_P15_F35.mha
# python ConvertRF2BMode_2DImages.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Liver_P30_F50_2/Liver_P30_F50_2.mha
# python ConvertRF2BMode_2DImages.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Steak_P15_F50_3/Steak_P15_F50_3.mha
# python ConvertRF2BMode_2DImages.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Steak_P30_F50_3/Steak_P30_F50_3.mha

# python ConvertRF2BMode_2DImages.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Liver_P15_F35_2/Liver_P15_F35_2.mha
# python ConvertRF2BMode_2DImages.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Steak_P15_F25/Steak_P15_F25.mha
# python ConvertRF2BMode_2DImages.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Steak_P30_F25/Steak_P30_F25.mha

# python ConvertRF2BMode_2DImages.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Liver_P15_F50/Liver_P15_F50.mha
# python ConvertRF2BMode_2DImages.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Steak_P15_F25_2/Steak_P15_F25_2.mha
# python ConvertRF2BMode_2DImages.py /Users/hyunjaekang/100_Kitware_Working/300_Fast/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Steak_P30_F25_2/Steak_P30_F25_2.mha


echo 'Done'
exit 0


