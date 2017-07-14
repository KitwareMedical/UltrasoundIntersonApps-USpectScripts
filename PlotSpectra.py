from os import listdir, path
import numpy as np
import glob
import matplotlib.pyplot as plt
import itk

def main():
    featureFiles = glob.glob('/home/samuel/Projects/Ultrasound/Spectroscopy/Data/LinearProbe1/Chicken2/SpectraIteration1Features/*Spectra.npy')

    labelFile = '/home/samuel/Projects/Ultrasound/Spectroscopy/Data/LinearProbe1/Chicken2/ManualLabels/rf_voltage_15_freq_0007500000_2017-5-31_12-50-44_ManualLabel.mha'

    features = []
    for ff in featureFiles:
        features.append( np.load(ff) )
    
    imageType = itk.Image[itk.UC, 3]
    reader = itk.ImageFileReader[imageType].New()
    reader.SetFileName( labelFile )
    reader.Update()
    labelImage = itk.GetArrayFromImage( reader.GetOutput() ).squeeze()
    
    print( ff )
    for i in range(0, 256, 10):
      fig = plt.figure(1)
      plt.subplot(211)
      plt.imshow(labelImage)
      plt.plot( [ i * 8 - 56, i * 8 + 56], [55, 55], color="red")

      plt.subplot(212)
      plt.plot( features[0][55, i, :], color="C0" )
      plt.plot( features[1][55, i, :], color="C1" )
      plt.plot( features[2][55, i, :], color="C2" )
      plt.plot( features[3][55, i, :], color="C3" )
      plt.plot( features[4][55, i, :], color="C4" )
      plt.plot( features[5][55, i, :], color="C5" )
      
      fig.savefig( "fig-" + str(i) + ".png" )
      plt.show()

if __name__ == '__main__':
    main()

