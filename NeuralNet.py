import argparse
from os import listdir, path
import numpy as np
import ImagePatches
import glob
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.layers.convolutional import Conv2D, MaxPooling2D, Conv3D, AveragePooling2D, MaxPooling3D
from keras.layers.noise import GaussianNoise
from keras.utils import to_categorical
from keras import optimizers
from sklearn import metrics
from keras.callbacks import History 
import itk
import matplotlib.pyplot as plt

def fitNeuralNet3D( trainPatches, trainLabels, 
                    validationPatches, validationLabels, 
                    testPatches, testLabels  ):

    history = History()
    
    nClasses = int( np.max( trainLabels )+1 )
    trainLabels = np.unique( trainLabels, return_inverse=True )[1]
    validationLabels = np.unique( validationLabels, return_inverse=True )[1]
    testLabels  = np.unique( testLabels, return_inverse=True )[1]
    trainLabels = to_categorical( trainLabels, num_classes=nClasses)
    validationLabels = to_categorical( validationLabels, num_classes=nClasses )
    testLabels  = to_categorical( testLabels, num_classes=nClasses )

    print( trainPatches.shape[1:4] )
    model = Sequential()
    model.add( GaussianNoise(0.2, input_shape = trainPatches.shape[1:4] +(1,) ) )
    model.add( Conv3D(12, (3,3,2), activation='relu' ) )
    model.add( MaxPooling3D( (1,1,1) ) )
    model.add( Conv3D(12, (3,3,1), activation='relu') )
    model.add( MaxPooling3D( (1,1,1) ) )
    #model.add( Conv3D(24, (3,3,1), activation='relu') )
    #model.add( Flatten() )
    #model.add( Dense(trainLabels.shape[1] * 2, activation="sigmoid" ) )
    model.add( Dense(nClasses, activation="softmax") )
    
    sgd = optimizers.SGD(lr=0.005, decay=1e-6, momentum=0.2, nesterov=True)
    model.compile( loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
    
    model.summary()

    weights = np.sum(trainLabels, axis=0)
    print(weights)
    model.fit( trainPatches, trainLabels, validation_split = 0.0, 
               batch_size = 64, epochs = 10, class_weight = weights, 
               callbacks=[history], validation_data = (validationPatches, validationLabels) )    
    test_pred = model.predict_classes( testPatches )
    score = model.evaluate( testPatches, testLabels, batch_size = 32 )
    print("")
    print("Test results:")
    for i in range(len( score) ):
        print( score[i] )
  
    score.append(history)
    score.append( test_pred )
    
    return  score


def fitNeuralNet2D( trainPatches, trainLabels, 
                    validationPatches, validationLabels, 
                    testPatches, testLabels, nInitalFilters = 12 ):

    history = History()
    
    nClasses = int( np.max( trainLabels )+1 )
    trainLabels = np.unique( trainLabels, return_inverse=True )[1]
    validationLabels = np.unique( validationLabels, return_inverse=True )[1]
    testLabels  = np.unique( testLabels, return_inverse=True )[1]
    trainLabels = to_categorical( trainLabels, num_classes=nClasses )
    validationLabels = to_categorical( validationLabels, num_classes=nClasses )
    testLabels  = to_categorical( testLabels, num_classes=nClasses )
  
    print( trainPatches.shape[1:4] )
    model = Sequential()
    #model.add( GaussianNoise(0.5, input_shape = trainPatches.shape[1:4]) )
    model.add( Conv2D(nInitalFilters, (3,3), strides=(1,1), activation='relu', input_shape = trainPatches.shape[1:4]) ) 
    model.add( AveragePooling2D( (2,2) ) )
    model.add( Conv2D(12, (3,3), strides=(1,1), activation='relu') )
    model.add( MaxPooling2D( (2,2) ) )
    model.add( Conv2D(12, (3,3), strides=(1,1), activation='relu') )
    model.add( MaxPooling2D( (2,2) ) )
    #model.add( Conv2D(12, (3,3), strides=(1,1), activation='relu') )
    #model.add( MaxPooling2D( (2,2) ) )    
    #model.add( Conv2D(24, (3,3), strides=(1,1), activation='relu') )
    #model.add( MaxPooling2D( (2,2) ) )
    model.add( Flatten() )
    #model.add( Dense(trainLabels.shape[1] * 2, activation="sigmoid" ) )
    model.add( Dense(nClasses, activation="softmax") )
    
    sgd = optimizers.SGD(lr=0.01, decay=1e-6, momentum=0.05, nesterov=True)
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
    
    model.summary()
    weights = np.sum( trainLabels, axis=0 )
    print(weights)
    model.fit( trainPatches, trainLabels, validation_split = 0.0, 
               batch_size = 64, epochs = 20, class_weight = weights, 
               callbacks=[history], validation_data = (validationPatches, validationLabels)  )
    
    test_pred = model.predict_classes( testPatches )
    score = model.evaluate( testPatches, testLabels, batch_size = 64 )
    print("")
    print("Test results:")
    for i in range(len( model.metrics_names)):
        print( model.metrics_names[i] + ": " + str(score[i]) )
    
    print("Test results:")
    for i in range(len( score) ):
        print( score[i] )
  
    score.append(history)
    score.append( test_pred )

    return  score


def load_data( basePath, folders, patchGenerator):
    data         = []
    dataID       = []
    labels       = []
    featureNames = []
    index        = []
    
    for f in folders:
       folder =  path.join( basePath, f)
       print(folder)
       #labelFile =  glob.glob( path.join( folder, 'ManualLabels') + '/*ManualLabel.mha' )[0]
       labelFile =  glob.glob( path.join( folder, 'BMode') + '/Overlay.mha' )[0]
       patchGenerator.loadFromFolder( folder, labelFile, )
       featureNames, patches = patchGenerator.getPatches() 
       label = patchGenerator.getLabels() 
       ind =  np.where( label > 0)[0] 
       patches   = patches[ ind, ... ]
       print( patches.shape )
       label = label[ ind ]
       data.append( patches )
       dataID.append( np.repeat(f, patches.shape[0] ) ) 
       labels.append( label )
       index.append( ind )
    
    data    = np.concatenate( data  , axis=0 )
    dataID  = np.concatenate( dataID  , axis=0 )
    labels  = np.concatenate( labels, axis=0 )
    index   = np.concatenate( index , axis=0 )
  
    return ( data, labels, featureNames, dataID, index )


def reconstructImages( image_shape, predictions, indexX, indexY, indexLabel, ids, name):
    mid = np.asarray( indexX[0].shape)  / 2 
    mid = mid.astype(int)
    for cid in np.unique( ids ):
        index = np.where( ids == cid )[0]
        lindex = indexLabel[ index ]
        image = np.zeros(image_shape)
        for i in range(len(index)):
            image[ indexX[ lindex[i], mid[0]-2:mid[0]+2, mid[1]-2:mid[1]+2 ].flatten(), 
                   indexY[ lindex[i], mid[0]-2:mid[0]+2, mid[1]-2:mid[1]+2 ].flatten() ] = predictions[ index[i] ] + 1
            
        #itk.imwrite( itk.GetImageFromArray( np.uint8(image) ), name + "_" +  cid + ".mha" )
        imageType = itk.Image[itk.UC, 2]
        writer = itk.ImageFileWriter[imageType].New()
        writer.SetFileName( name + "_" +  path.basename(cid) + ".mha" ) 
        itkImage = itk.GetImageFromArray( np.uint8(image) )
        writer.SetInput( itkImage )
        writer.Update()


def main():
    parser = argparse.ArgumentParser(description='Run Neural Net')
    parser.add_argument('basepath', help="Path to data directory")
    args = parser.parse_args();

    basePath = args.basepath 

    #trainFolders = [ './LinearProbe1/Chicken1', './LinearProbe1/Steak1', './LinearProbe1/Pork1', 
    #                 './LinearProbe1/Chicken2', './LinearProbe1/Steak2', './LinearProbe1/Pork2', 
    #                 './LinearProbe2/Chicken1', './LinearProbe2/Steak1', './LinearProbe2/Pork1', 
    #                 './LinearProbe2/Chicken2', './LinearProbe2/Steak2', './LinearProbe2/Pork2']

    #validationFolders = [ './LinearProbe1/Chicken3', './LinearProbe1/Steak3', './LinearProbe1/Pork3'  ]
    #testFolders = [ './LinearProbe1/Chicken4', './LinearProbe1/Steak4', './LinearProbe1/Pork4' ]

    trainFolders      = [ './2018-02-26_13-07-51', 
                          './2018-02-26_13-08-23', 
                          './2018-02-26_13-09-10' ] 
    validationFolders = [ './2018-02-26_13-10-26' ]
    testFolders       = [ './2018-02-26_13-11-12' ]


    patch_size = (29, 29)

    patchGenerator = ImagePatches.ImagePatchGenerator( patch_size )
    
    ( trainPatches, trainLabels, featureNames, 
      trainIDs, trainIndex ) = load_data(basePath, trainFolders, patchGenerator )
    
    indexX = patchGenerator.getPatchIndexX()
    indexY = patchGenerator.getPatchIndexY()
    reconstructImages( patchGenerator.getImageShape(), trainLabels, indexX, indexY, 
                       trainIndex, trainIDs, "tmp" )

    ( validationPatches, validationLabels, featureNames, 
      validationIDs, validationIndex ) = load_data(basePath, validationFolders, patchGenerator)
    ( testPatches, testLabels, featureNames, 
      testIDs, testIndex ) = load_data(basePath, testFolders, patchGenerator)
   
    print( trainPatches.shape )
    print( trainLabels.shape )
 

    indexX = patchGenerator.getPatchIndexX()
    indexY = patchGenerator.getPatchIndexY()

    results = []
 
    for i in range( len(featureNames) ):
      print( "Neural net on feature " + featureNames[i] )
      res = fitNeuralNet2D( trainPatches[...,i][...,np.newaxis], trainLabels, 
                            validationPatches[...,i][...,np.newaxis], validationLabels, 
                            testPatches[...,i][...,np.newaxis], testLabels, 48)
      res.append( featureNames[i] )
      results.append( res )
      print("")
      print("")
 


    print( "Neural net of all features 2D conv with channels" )
    res = fitNeuralNet2D( trainPatches, trainLabels, 
                          validationPatches, validationLabels, 
                          testPatches, testLabels, 48)
    res.append("All-2D")
    results.append( res )
    print("")
    print("")


    print( "Neural net of all features 3D" )
    res = fitNeuralNet3D( trainPatches[...,np.newaxis], trainLabels,
                          validationPatches[...,np.newaxis], validationLabels, 
                          testPatches[...,np.newaxis], testLabels)
    res.append("All-3D")
    results.append( res )
    print("")
    print("")

  
    for res in results:
      print( res[4] + ": loss = " + str( res[0] ) + ", acc = " + str( res[1] ) )

      history = res[2]
      plt.plot(history.history['acc'])
      plt.plot(history.history['val_acc'])
      plt.title('model accuracy ' + res[4] )
      plt.ylabel('accuracy')
      plt.xlabel('epoch')
      plt.legend(['train', 'test'], loc='upper left')
      plt.savefig( 'model-accuracy_' + res[4]  + '.png'  )
      plt.close()

      plt.plot(history.history['loss'])
      plt.plot(history.history['val_loss'])
      plt.title('model loss ' + res[4] )
      plt.ylabel('loss')
      plt.xlabel('epoch')
      plt.legend(['train', 'test'], loc='upper left')
      plt.savefig( 'model-loss_' + res[4]  + '.png'  )
      plt.close()

      reconstructImages( patchGenerator.getImageShape(), res[3], indexX, indexY, 
                         testIndex, testIDs, res[4] )

if __name__ == '__main__':
    main()

