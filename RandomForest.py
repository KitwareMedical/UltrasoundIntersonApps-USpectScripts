from os import listdir, path
import numpy as np
import pandas as pd
import itk
from sklearn.ensemble import RandomForestClassifier
from sklearn import preprocessing
import Features
import glob


def main():
    basePath = '/home/samuel/Projects/Ultrasound/Spectroscopy/Data/LinearProbe1/'
    trainFolders = [ 'Chicken1', 'Chicken2', 'Steak1', 'Steak2', 'Pork1', 'Pork2' ]
    
    dfs = []
    for f in trainFolders:
       ff =  path.join( basePath, f)
       labelFile =  glob.glob( path.join( ff, 'ManualLabels') + '/*ManualLabel.mha' )[0]
       featureFolder = path.join(ff, 'SpectraIteration1Features' )
       features = Features.SpectralFeatures()
       features.loadFromFolder( featureFolder, labelFile )
       dfs.append( features.toPandas() )
    traindf = pd.concat(dfs)

    testFolders = [ 'Chicken3', 'Chicken4', 'Steak3', 'Steak4', 'Pork3', 'Pork4' ]
    dfs = []
    for f in testFolders:
       ff =  path.join( basePath, f)
       labelFile =  glob.glob( path.join( ff, 'ManualLabels') + '/*ManualLabel.mha' )[0]
       featureFolder = path.join(ff, 'SpectraIteration1Features' )
       features = Features.SpectralFeatures()
       features.loadFromFolder( featureFolder, labelFile )
       dfs.append( features.toPandas() )
    testdf = pd.concat(dfs)






    #All features
    print( "All Features" )
    print( "------------" )
    rForest = RandomForestClassifier()
    le = preprocessing.LabelEncoder()
    le.fit(traindf['label']) 
    
    labels = np.array( le.transform( traindf['label'] ) ) 
    df = traindf.drop('label', axis=1)
    rForest.fit( df[ (labels > 0) ], labels[ labels > 0 ] ) 

    labels = np.array( le.transform( testdf['label'] ) )
    df = testdf.drop('label', axis=1)  
    score = rForest.score( df[ labels > 0], labels[ labels > 0 ] ) 
 
    print( "Accuracy score: " + str(score) )

    # Print the feature ranking
    importances = rForest.feature_importances_
    indices = np.argsort(importances)[::-1]
    print("Feature ranking:")
    for f in range(10):
      print("%d. %s feature %d (%f)" % (f + 1, df.columns[indices[f]], indices[f], importances[indices[f]]))
    


    #All spectra
    print( "All Spectra" )
    print( "------------" )
    featureNames = []
    for i in range(17):
        featureNames.append("Spectra-10-0007500000"+"-coeff-" + str(i))
        featureNames.append("Spectra-15-0007500000"+"-coeff-" + str(i))
        featureNames.append("Spectra-20-0007500000"+"-coeff-" + str(i))
        featureNames.append("Spectra-10-0005000000"+"-coeff-" + str(i))
        featureNames.append("Spectra-15-0005000000"+"-coeff-" + str(i))
        featureNames.append("Spectra-20-0005000000"+"-coeff-" + str(i))

    rForest = RandomForestClassifier()
    le = preprocessing.LabelEncoder()
    le.fit(traindf['label']) 

    labels = np.array( le.transform( traindf['label'] ) ) 
    df = traindf[featureNames]
    rForest.fit( df[ labels > 0], labels[labels > 0 ] ) 

    labels = np.array( le.transform( testdf['label'] ) ) 
    df = testdf[featureNames]
    score = rForest.score( df[labels > 0 ], labels[ labels > 0 ] )
 
    print( "Accuracy score: " + str(score) )

    # Print the feature ranking
    importances = rForest.feature_importances_
    indices = np.argsort(importances)[::-1]
    print("Feature ranking:")
    for f in range(10):
      print("%d. %s feature %d (%f)" % (f + 1, featureNames[indices[f]], indices[f], importances[indices[f]]))
    



    #Single spectra
    print( "Single Spectra" )
    print( "------------" )
    featureNames = []
    for i in range(17):
        featureNames.append( "Spectra-20-0007500000"+"-coeff-" + str(i) )

    rForest = RandomForestClassifier()
    le = preprocessing.LabelEncoder()
    le.fit(traindf['label']) 

    labels = np.array( le.transform( traindf['label'] ) ) 
    df = traindf[featureNames]
    rForest.fit( df[ labels > 0], labels[labels > 0 ] ) 

    labels = np.array( le.transform( testdf['label'] ) ) 
    df = testdf[featureNames]
    score = rForest.score( df[labels > 0 ], labels[ labels > 0 ] )
 

    print( "Accuracy score: " + str(score) )

    # Print the feature ranking
    importances = rForest.feature_importances_
    indices = np.argsort(importances)[::-1]
    print("Feature ranking:")
    for f in range(10):
      print("%d. %s feature %d (%f)" % (f + 1, featureNames[indices[f]], indices[f], importances[indices[f]]))
    



if __name__ == '__main__':
    main()

