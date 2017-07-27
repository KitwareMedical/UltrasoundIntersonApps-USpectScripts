from os import listdir, path
import numpy as np
import pandas as pd
import glob
import itk

class SpectralFeatures:
    
    #def __init__(self):

    def loadFromFolder( self, featureFolder, labelImageFile, windowSize = 128 ):
        self.featureNames = []
        self.features = []
        for fname in listdir( featureFolder ):
            feature = np.load( path.join( featureFolder, fname) )
            fsplit = fname.split('_');
            name = fsplit[7].split('.')[0] + "-" + fsplit[2] + "-" + fsplit[4]
            self.featureNames.append( name )
            self.features.append( feature )
            print( name + str( feature.shape ) )
             
        
        
        imageType = itk.Image[itk.UC, 2]
        reader = itk.ImageFileReader[imageType].New()
        reader.SetFileName( labelImageFile )
        reader.Update()
        self.labels = itk.GetArrayFromImage( reader.GetOutput() );
        print(self.labels.shape) 

    def toPandas(self):
        df = {}
        for i in range(0, len( self.features)):
            for j in range(0, self.features[i].shape[2] ):
                df[ self.featureNames[i] + "-coeff-" + str(j) ] = self.features[i][:,:, j].flatten() 
                
        df["label"] = self.labels.flatten()
        print( np.max( df["label"]) )
        return pd.DataFrame(df)

def main():
    basePath = '/home/samuel/Projects/Ultrasound/Spectroscopy/Data/LinearProbe1/'
    trainFolders = [ 'PC1' ]
    
    dfs = []
    for f in trainFolders:
       ff =  path.join( basePath, f)
       labelFile =  glob.glob( path.join( ff, 'ManualLabels') + '/*ManualLabel-reduced.mha' )[0]
       featureFolder = path.join(ff, 'SpectraIteration1Features' )
       features = SpectralFeatures()
       features.loadFromFolder( featureFolder, labelFile )
       dfs.append( features.toPandas() )
    traindf = pd.concat(dfs)

    traindf.to_csv("data-pc1.csv")  
    pass

if __name__ == '__main__':
    main()

