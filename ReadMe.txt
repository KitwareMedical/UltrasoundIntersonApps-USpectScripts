
#------------------------------------------------------------
# Generate US B-Mode image from US RF data
# Python Code : ConvertRF2BMode_2DImages.py : 3D RF -> Multiple 2D B-Mode images
#               ConvertRF2BMode_3D.py       : 3D RF -> 3D B-Mode image
# Examples:
python ConvertRF2BMode_2DImages.py \
  /300_Project_FAST/90_Data/FAST/2014-11-17-mts/donor1/TrackedImageSequence_CaptureDevice_20141117_210842.mha

python ConvertRF2BMode_3D.py \
  /300_Project_FAST/90_Data/FAST/2014-11-17-mts/donor1/TrackedImageSequence_CaptureDevice_20141117_211023.mha \
  /300_Project_FAST/90_Data/FAST/2014-11-17-mts/donor1/TrackedImageSequence_CaptureDevice_20141117_211023_3DBMode.mha


#------------------------------------------------------------
# Compute super-pixel algorithm
# Python Code : SciKit_SLIC_Folder.py
#
# Example:
python SciKit_SLIC_Folder.py /300_Project_FAST//91_Working_Data/000_Selected_Cadaver_USData

#------------------------------------------------------------
# Compute power spectrum of ultrasound RF data
# Python Code: Get_USRF_PWSpectra.py
# Example:
python Get_USRF_PWSpectra.py 300_Project_FAST/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/BaseLine_P1_F25/BaseLine_P1_F25.mha 9

#------------------------------------------------------------
# Compute normalized power spectrum and coefficient values
# Python Code: Analyze_USRF_PWSpectra_Integrated.py,
#              Analyze_USRF_PWSpectra_Legendre.py,
#              Analyze_USRF_PWSpectra_Chebyshev.py,
#              Analyze_USRF_PWSpectra_LineRegress
# Examples:
python Analyze_USRF_PWSpectra_Integrated.py \
300_Project_FAST/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Liver_P15_F25/Liver_P15_F25.mha \
300_Project_FAST/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/BaseLine_P1_F25/BaseLine_P1_F25.mha

python Analyze_USRF_PWSpectra_Legendre.py \
300_Project_FAST/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Liver_P15_F25/Liver_P15_F25.mha \
300_Project_FAST/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/BaseLine_P1_F25/BaseLine_P1_F25.mha

python Analyze_USRF_PWSpectra_Chebyshev.py \
300_Project_FAST/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Liver_P15_F25/Liver_P15_F25.mha \
300_Project_FAST/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/BaseLine_P1_F25/BaseLine_P1_F25.mha

python Analyze_USRF_PWSpectra_LineRegress.py \
300_Project_FAST/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Liver_P15_F25/Liver_P15_F25.mha \
300_Project_FAST/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/BaseLine_P1_F25/BaseLine_P1_F25.mha

#------------------------------------------------------------
# Generate Curvilinear scan-converted PW spectra coefficient images
# Python Code : USCurvilinearScanconvert_PWSpectra.py
# Examples:
# Integrated
python USCurvilinearScanconvert_PWSpectra.py  \
300_Project_FAST/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Liver_P15_F25/Liver_P15_F25.mha 001

# Chebyshev
python USCurvilinearScanconvert_PWSpectra.py  \
300_Project_FAST/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Liver_P15_F25/Liver_P15_F25.mha 002

# Legendre
python USCurvilinearScanconvert_PWSpectra.py  \
300_Project_FAST/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Liver_P15_F25/Liver_P15_F25.mha 003

# LineRegress
python USCurvilinearScanconvert_PWSpectra.py  \
300_Project_FAST/91_Working_Data/010_Steak-Liver-Blood-Canola-Oil-2015-08-07/Liver_P15_F25/Liver_P15_F25.mha 004