from os import listdir, path
import numpy as np
import glob
import itk
from skimage import util

class ImagePatchGenerator:
    
    #def __init__(self):

    def loadFromFolder( self, folder, labelImage, patch_size = (23, 23), step_size = 4 ):
        self.featureNames = []
        self.features = []
        for fname in glob.glob( folder + "/BMode/*.mha" ):
            fsplit = fname.split('_');
            name = "image-" + fsplit[2] + "-" + fsplit[4]
            self.featureNames.append( name )
            
            imageType = itk.Image[itk.F, 3]
            reader = itk.ImageFileReader[imageType].New()
            reader.SetFileName( fname )
            reader.Update()
            image = itk.GetArrayFromImage( reader.GetOutput() ).squeeze()
            image = image -  np.min(image)
            image = image  / np.max(image)
            patches = util.view_as_windows(  image, patch_size, step_size )
            patch_shape = ( patches.shape[0]*patches.shape[1], patches.shape[2], patches.shape[3])
            patches = np.reshape( patches, patch_shape, 'F' )
            print(patches.shape)
            self.features.append( patches )
        
            print( patches.shape )

        self.features = np.stack(self.features, axis=-1)  
        
        
        imageType = itk.Image[itk.UC, 3]
        reader = itk.ImageFileReader[imageType].New()
        reader.SetFileName( labelImage )
        reader.Update()

        labelImage = itk.GetArrayFromImage( reader.GetOutput() ).squeeze() 
        print("label: ")
        print( labelImage.shape )
        patches = util.view_as_windows(  labelImage, patch_size, step_size )
        patch_shape = ( patches.shape[0]*patches.shape[1], patches.shape[2], patches.shape[3])
        patches = np.reshape( patches, patch_shape, 'F' )
        self.labels = np.zeros( patches.shape[0]  )
        for i in range(0, patches.shape[0] ):
            a, b = np.unique( patches[i,].flatten(), return_inverse=True )
            c = np.argmax( np.bincount(b) )
            self.labels[i] = a[c]


    def getPatches(self):
        return (self.featureNames, self.features)

    def getLabels(self):
        return self.labels


def main():
    basePath = '/home/samuel/Projects/Ultrasound/Spectroscopy/Data/LinearProbe1/'
    trainFolders = [ 'PC1' ]
    
    for f in trainFolders:
       folder =  path.join( basePath, f)
       labelFile =  glob.glob( path.join( folder, 'ManualLabels') + '/*ManualLabel.mha' )[0]
       patchGenerator = ImagePatchGenerator()
       patchGenerator.loadFromFolder( folder, labelFile )

    pass

if __name__ == '__main__':
    main()

