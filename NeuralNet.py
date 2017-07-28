import argparse
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
from keras.callbacks import History 

import matplotlib.pyplot as plt

def fitNeuralNet3D( trainPatches, trainLabels, 
                    validationPatches, validationLabels, 
                    testPatches, testLabels  ):

    history = History()
    
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
    return  score


def fitNeuralNet2D( trainPatches, trainLabels, 
                    validationPatches, validationLabels, 
                    testPatches, testLabels  ):

    history = History()
    
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
    
    sgd = optimizers.SGD(lr=0.01, decay=1e-6, momentum=0.66, nesterov=True)
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
    
    model.summary()
    weights = np.sum(trainLabels, axis=0)
    print(weights)
    model.fit( trainPatches, trainLabels, validation_split = 0.0, 
               batch_size = 64, epochs = 10, class_weight = weights, 
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

    return  score



def load_data( basePath, folders ):
    data = []
    labels  = []
    featureNames = []
    for f in folders:
       folder =  path.join( basePath, f)
       labelFile =  glob.glob( path.join( folder, 'ManualLabels') + '/*ManualLabel.mha' )[0]
       patchGenerator = ImagePatches.ImagePatchGenerator()
       patchGenerator.loadFromFolder( folder, labelFile )
       featureNames, patches = patchGenerator.getPatches()
       data.append( patches )
       labels.append( patchGenerator.getLabels() )
    data = np.concatenate( data, axis=0 )
    labels  = np.concatenate( labels,  axis=0 )

    data = data[ labels > 0, ... ]
    labels = labels[ labels > 0 ]
    return (data, labels, featureNames)


def main():
    parser = argparse.ArgumentParser(description='Run Neural Net')
    parser.add_argument('basepath', help="Path to data directory")
    args = parser.parse_args();

    basePath = args.basepath 

    trainFolders = [ 'Chicken1', 'Chicken2', 'Steak1', 'Steak2', 'Pork1', 'Pork2']
    validationFolders = [ 'Chicken3', 'Steak3', 'Pork3' ]
    testFolders = [ 'Chicken4', 'Steak4', 'Pork4' ]


    (trainPatches, trainLabels, featureNames) = load_data(basePath, trainFolders)
    (validationPatches, validationLabels, featureNames) = load_data(basePath, validationFolders)
    (testPatches, testLabels, featureNames) = load_data(basePath, testFolders)

   
    print( trainPatches.shape )
    print( trainLabels.shape )


    results = []

    print( "Neural net of all features 2D conv with channels" )
    res = fitNeuralNet2D( trainPatches, trainLabels, 
                          validationPatches, validationLabels, 
                          testPatches, testLabels)
    res.append("All-2D")
    results.append( res )
    print("")
    print("")

    for i in range( len(featureNames) ):
      print( "Neural net on feature " + featureNames[i] )
      res = fitNeuralNet2D( trainPatches[...,i][...,np.newaxis], trainLabels, 
                            validationPatches[...,i][...,np.newaxis], validationLabels, 
                            testPatches[...,i][...,np.newaxis], testLabels)
      res.append( featureNames[i] )
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
      print( res )
      history = res[2]
      plt.plot(history.history['acc'])
      plt.plot(history.history['val_acc'])
      plt.title('model accuracy ' + res[3] )
      plt.ylabel('accuracy')
      plt.xlabel('epoch')
      plt.legend(['train', 'test'], loc='upper left')
      plt.savefig( 'model-accuracy_' + res[3]  + '.png'  )
      plt.close()

      plt.plot(history.history['loss'])
      plt.plot(history.history['val_loss'])
      plt.title('model loss ' + res[3] )
      plt.ylabel('loss')
      plt.xlabel('epoch')
      plt.legend(['train', 'test'], loc='upper left')
      plt.savefig( 'model-loss_' + res[3]  + '.png'  )
      plt.close()

if __name__ == '__main__':
    main()

