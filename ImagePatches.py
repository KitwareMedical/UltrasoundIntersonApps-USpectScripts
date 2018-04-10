from os import listdir, path
import numpy as np
import glob
import itk
from skimage import util

class ImagePatchGenerator:
    
    def __init__(self, patch_size = (23, 23), step_size = 4 ):
        self.patch_size = patch_size
        self.step_size = step_size

    def loadFromFolder( self, folder, labelImage ):
        self.featureNames = []
        self.features = []
        #for fname in glob.glob( folder + "/BMode2/rf_voltage_20*.nrrd" ):
        #for fname in glob.glob( folder + "/rf_voltage_20*.nrrd" ):
        for fname in glob.glob( folder + "/rf_voltage_20*filtered.nrrd" ):
            print( fname )
            fsplit = fname.split('_');
            #name = "image-" + fsplit[2] + "-" + fsplit[4]
            name = "image-" + fsplit[3] + "-" + fsplit[5]
            self.featureNames.append( name )
            
            imageType = itk.Image[itk.F, 2]
            reader = itk.ImageFileReader[imageType].New()
            reader.SetFileName( fname )
            reader.Update()
            #itkImage = reader.GetOutput();

            #resampler = itk.ResampleImageFilter[imageType, imageType].New()
            #resampler.SetInput( itkImage )
            #size = itk.size(itkImage);
            #size[1] = 256;
            #resampler.SetSize( size )
            #resampler.Update();


            image = itk.GetArrayViewFromImage( reader.GetOutput() ).squeeze()
            #image = image -  np.min(image)
            #image = image  / np.max(image)
            patches = util.view_as_windows(  image, self.patch_size, self.step_size )
            patch_shape = ( patches.shape[0]*patches.shape[1], patches.shape[2], patches.shape[3])
            patches = np.reshape( patches, patch_shape, 'F' )
            print( patches.shape )
            self.features.append( patches )
        
 
        self.indexX = np.transpose(
                      np.repeat( [np.arange(image.shape[0])], 
                                   image.shape[1], axis=0 ) )
        self.indexY = np.repeat( [np.arange(image.shape[1])], 
                                     image.shape[0], axis=0 ) 

        self.image_shape = image.shape

        self.features = np.stack(self.features, axis=-1)  
        
        
        imageType = itk.Image[itk.UC, 3]
        reader = itk.ImageFileReader[imageType].New()
        reader.SetFileName( labelImage )
        reader.Update()
        
        #resampler = itk.ResampleImageFilter[imageType, imageType].New()
        #resampler.SetInput( reader.GetOutput() )
        #size = itk.size(itkImage);
        #size[1] = 256;
        #resampler.SetSize( size )
        #resampler.SetInterpolator( itk.NearestNeighborInterpolateImageFunction.New() )
        #resampler.Update();

        labelImage = itk.GetArrayViewFromImage( reader.GetOutput() ).squeeze() 
        patches = util.view_as_windows(  labelImage, self.patch_size, self.step_size )
        patch_shape = ( patches.shape[0]*patches.shape[1], patches.shape[2], patches.shape[3])
        patches = np.reshape( patches, patch_shape, 'F' )
        self.labels = np.zeros( patches.shape[0]  )
        for i in range(0, patches.shape[0] ):
            a, b = np.unique( patches[i,].flatten(), return_inverse=True )
            c = np.argmax( np.bincount(b) )
            self.labels[i] = a[c]


    def getPatchIndexX(self):
        print( self.indexX.shape )
        patchesX = util.view_as_windows( np.ascontiguousarray( self.indexX ), 
                                         self.patch_size, self.step_size )
        patch_shape = ( patchesX.shape[0]*patchesX.shape[1], patchesX.shape[2], patchesX.shape[3])
        patchesX = np.reshape( patchesX, patch_shape, 'F' )
        return patchesX

    def getPatchIndexY(self):
        patchesY = util.view_as_windows(  np.ascontiguousarray( self.indexY ), 
                                          self.patch_size, self.step_size )
        patch_shape = ( patchesY.shape[0]*patchesY.shape[1], patchesY.shape[2], patchesY.shape[3])
        patchesY = np.reshape( patchesY, patch_shape, 'F' )
        return patchesY

    def getImageShape(self):
        return self.indexX.shape

    def getPatches(self):
        return (self.featureNames, self.features)

    def getLabels(self):
        return self.labels

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

