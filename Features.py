from os import listdir, path
import numpy as np
import pandas as pd
import itk

class SpectralFeatures:
    
    #def __init__(self):

    def loadFromFolder( self, featureFolder, labelImage ):
        self.featureNames = []
        self.features = []
        for fname in listdir( featureFolder ):
            feature = np.load( path.join( featureFolder, fname) )
            fsplit = fname.split('_');

            self.featureNames.append( fsplit[7].split('.')[0] + "-" + fsplit[2] + "-" + fsplit[4] )
            self.features.append( feature )
            
        
        
        imageType = itk.Image[itk.UC, 3]
        reader = itk.ImageFileReader[imageType].New()
        reader.SetFileName( labelImage )
        reader.Update()

        labelImage = itk.GetArrayFromImage( reader.GetOutput() ).squeeze()
    
        self.labels = np.zeros( self.features[0].shape[0:2] )
        index = 0;
        for i in range(0, labelImage.shape[1], int( labelImage.shape[1] / self.features[0].shape[1] ) ):
            self.labels[:, index] = np.amin( labelImage[:, range(i, i+8)], 1 )
            index = index + 1


    def toPandas(self):
        df = {}
        for i in range(0, len( self.features)):
            for j in range(0, self.features[i].shape[2] ):
                df[ self.featureNames[i] + "-coeff-" + str(j) ] = self.features[i][:,:, j].flatten() 
                
        df["label"] = self.labels.flatten()
        return pd.DataFrame(df)

def main():
    features = SpectralFeatures()
    labelFile = '/home/samuel/Projects/Ultrasound/Spectroscopy/Data/LinearProbe1/Chicken2/ManualLabels/rf_voltage_15_freq_0007500000_2017-5-31_12-50-44_ManualLabel.mha'
    featureFolder = '/home/samuel/Projects/Ultrasound/Spectroscopy/Data/LinearProbe1/Chicken2/SpectraIteration1Features/'
    features.loadFromFolder( featureFolder, labelFile ); 


    df = features.toPandas()

    pass

if __name__ == '__main__':
    main()

