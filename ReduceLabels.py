import os
import glob

basePath = '/home/samuel/Projects/Ultrasound/Spectroscopy/Data/LinearProbe1/'
folders = os.listdir(basePath);

for f in folders:
    try:
      ff = os.path.join(basePath, f)
      labelFile =  glob.glob( os.path.join( ff, 'ManualLabels') + '/*ManualLabel.mha' )[0]
      spectraFile =  glob.glob( os.path.join( ff, 'SpectraIteration1') + '/*.mha' )[0]
      os.system("~/Projects/Ultrasound/Spectroscopy/UltrasoundSpectroscopyScripts-build/ReduceLabelImage -s " + spectraFile + " -l " + labelFile)
    except:
      print("Failed on: " + f)

