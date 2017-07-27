from os import listdir, path
import numpy as np
import ImagePatches
import glob
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.layers.convolutional import Conv2D, MaxPooling2D, Conv3D, MaxPooling3D
from keras.utils import to_categorical
from keras import optimizers
from sklearn import metrics

def fitNeuralNet3D( trainPatches, trainLabels, testPatches, testLabels  ):

    trainLabels = np.unique( trainLabels, return_inverse=True )[1]
    trainLabels = to_categorical( trainLabels )
    
    testLabels  = np.unique( testLabels, return_inverse=True )[1]
    testLabels  = to_categorical( testLabels )
  
    print( trainPatches.shape[1:4] )
    model = Sequential()
    model.add( Conv3D(8, (3,3,3), activation='relu', input_shape = trainPatches.shape[1:4] +(1,) ) ) 
    model.add( MaxPooling3D( (2,2,1) ) )
    model.add( Conv3D(8, (3,3,3), activation='relu') )
    model.add( MaxPooling3D( (2,2,2) ) )
    model.add( Flatten() )
    model.add( Dense(trainLabels.shape[1] * 2, activation="sigmoid" ) )
    model.add( Dense(trainLabels.shape[1], activation="softmax") )
    
    sgd = optimizers.SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
    
    model.summary()

    weights = np.sum(trainLabels, axis=0)
    print(weights)
    model.fit( trainPatches, trainLabels, batch_size = 32, epochs = 10, class_weight = weights )    
    test_pred = model.predict_classes( testPatches )
    score = model.evaluate( testPatches, testLabels, batch_size = 32 )
    print("")
    print("Test results:")
    for i in range(len( model.metrics_names)):
        print( model.metrics_names[i] + ": " + str(score[i]) )
  
    
    
    test_pred = to_categorical( test_pred, num_classes = testLabels.shape[1])
    acc = metrics.accuracy_score( testLabels, test_pred )
    print("multilabel subset accuracy: " + str(acc) )

    return ( score, acc )


def fitNeuralNet2D( trainPatches, trainLabels, testPatches, testLabels  ):

    print( trainLabels.shape )
    print( testLabels.shape )
    trainLabels = np.unique( trainLabels, return_inverse=True )[1]
    testLabels  = np.unique( testLabels, return_inverse=True )[1]
    trainLabels = to_categorical( trainLabels )
    print( trainLabels.shape )
    testLabels  = to_categorical( testLabels )
  
    print( trainPatches.shape[1:4] )
    model = Sequential()
    model.add( Conv2D(12, (3,3), activation='relu', input_shape = trainPatches.shape[1:4]) ) 
    model.add( MaxPooling2D( (2,2) ) )
    model.add( Conv2D(24, (3,3), activation='relu') )
    model.add( MaxPooling2D( (2,2) ) )
    model.add( Conv2D(48, (3,3), activation='relu') )
    model.add( MaxPooling2D( (2,2) ) )
    model.add( Flatten() )
    model.add( Dense(trainLabels.shape[1] * 2, activation="sigmoid" ) )
    model.add( Dense(trainLabels.shape[1], activation="softmax") )
    
    sgd = optimizers.SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
    
    model.summary()
    weights = np.sum(trainLabels, axis=0)
    print(weights)
    model.fit( trainPatches, trainLabels, batch_size = 64, epochs = 10, class_weight = weights )
    test_pred = model.predict_classes( testPatches )
    score = model.evaluate( testPatches, testLabels, batch_size = 64 )
    print("")
    print("Test results:")
    for i in range(len( model.metrics_names)):
        print( model.metrics_names[i] + ": " + str(score[i]) )
    
    test_pred = to_categorical( test_pred, num_classes = testLabels.shape[1])
    acc = metrics.accuracy_score( testLabels, test_pred )
    print("multilabel subset accuracy: " + str(acc) )

    #report = metrics.classification_report( testLabels, test_pred )
    #print( report )






def main():
    parser = argparse.ArgumentParser(description='Run Neural Net')
    parser.add_argument('basepath', help="Path to data directory")
    args = parse.parse_args();

    basePath = args.basepath 

    trainFolders = [ 'Chicken1', 'Chicken2', 'Steak1', 'Steak2', 'Pork1', 'Pork2' ]
    trainPatches = []
    trainLabels  = []
    featureNames = []
    for f in trainFolders:
       folder =  path.join( basePath, f)
       labelFile =  glob.glob( path.join( folder, 'ManualLabels') + '/*ManualLabel.mha' )[0]
       patchGenerator = ImagePatches.ImagePatchGenerator()
       patchGenerator.loadFromFolder( folder, labelFile )
       featureNames, patches = patchGenerator.getPatches()
       trainPatches.append( patches )
       trainLabels.append( patchGenerator.getLabels() )
    trainPatches = np.concatenate( trainPatches, axis=0 )
    trainLabels  = np.concatenate( trainLabels,  axis=0 )

    trainPatches = trainPatches[ trainLabels > 0, ... ]
    trainLabels = trainLabels[ trainLabels > 0 ]

   
    print( trainPatches.shape )
    print( trainLabels.shape )

    testFolders = [ 'Chicken3', 'Chicken4', 'Steak3', 'Steak4', 'Pork3', 'Pork4' ]
    testPatches = []
    testLabels  = []
    for f in testFolders:
       folder =  path.join( basePath, f)
       labelFile =  glob.glob( path.join( folder, 'ManualLabels') + '/*ManualLabel.mha' )[0]
       patchGenerator = ImagePatches.ImagePatchGenerator()
       patchGenerator.loadFromFolder( folder, labelFile )
       testPatches.append( patchGenerator.getPatches()[1] )
       testLabels.append( patchGenerator.getLabels() )
    testPatches = np.concatenate( testPatches, axis=0 )
    testLabels  = np.concatenate( testLabels,  axis=0 )
    
    testPatches = testPatches[ testLabels > 0, ... ]
    testLabels = testLabels[ testLabels > 0 ]

    results = []

    print( "Neural net of all features 2D conv with channels" )
    res = fitNeuralNet2D( trainPatches, trainLabels, testPatches, testLabels)
    results.append( res )
    print("")
    print("")

    for i in range( len(featureNames) ):
      print( "Neural net on feature " + featureNames[i] )
      res = fitNeuralNet2D( trainPatches[...,i][...,np.newaxis], trainLabels, testPatches[...,i][...,np.newaxis], testLabels)
      results.append( res )
      print("")
      print("")
  
    print( "Neural net of all features 3D" )
    res = fitNeuralNet3D( trainPatches[...,np.newaxis], trainLabels, testPatches[...,np.newaxis], testLabels)
    results.append( res )
    print("")
    print("")

  
    for res in results:
      print( res )


if __name__ == '__main__':
    main()

