from os import listdir, path
import numpy as np
import pandas as pd
import itk
from sklearn.ensemble import RandomForestClassifier
from sklearn import preprocessing
import Features
import glob
import argparse


def fitForest(name, featureNames, labelEncoder, traindf, testdf):
    rForest = RandomForestClassifier()
    
    print( "" )
    labels = np.array( labelEncoder.transform( traindf['label'] ) ) 
    print( "Train label counts:" )
    print( np.bincount(labels) )

    if len(featureNames) == 0:
       df = traindf.drop('label', axis=1)
    else:
       df = traindf[featureNames]
    rForest.fit( df[ (labels > 0) ], labels[ labels > 0 ] ) 

    labels = np.array( labelEncoder.transform( testdf['label'] ) )
    print( "Test label counts:" )
    print( np.bincount(labels) )
    if len(featureNames) == 0:
       df = testdf.drop('label', axis=1)
    else:
       df = testdf[featureNames]
 
    score = rForest.score( df[ labels > 0], labels[ labels > 0 ] ) 
 
    print( "" )
    print( name )
    print( "------------" )
    print( "Accuracy score: " + str(score) )

    # Print the feature ranking
    importances = rForest.feature_importances_
    indices = np.argsort(importances)[::-1]
    print("Feature ranking:")
    for f in range( min(df.shape[1], 10) ):
        print( "%d. %s feature %d (%f)" % (f + 1, df.columns[indices[f]], indices[f], importances[indices[f]]))


def main():
    parser = argparse.ArgumentParser(description='Run Neural Net')
    parser.add_argument('basepath', help="Path to data directory")
    args = parser.parse_args();

    basePath = args.basepath
    trainFolders = [ 'Chicken1', 'Chicken2', 'Steak1', 'Steak2', 'Pork1', 'Pork2' ]
    
    dfs = []
    for f in trainFolders:
       ff =  path.join( basePath, f)
       labelFile =  glob.glob( path.join( ff, 'ManualLabels') + '/*ManualLabel-reduced.mha' )[0]
       featureFolder = path.join(ff, 'SpectraIteration1Features' )
       features = Features.SpectralFeatures()
       features.loadFromFolder( featureFolder, labelFile )
       dfs.append( features.toPandas() )
    traindf = pd.concat(dfs)

    testFolders = [ 'Chicken3', 'Chicken4', 'Steak3', 'Steak4', 'Pork3', 'Pork4' ]
    dfs = []
    for f in testFolders:
       ff =  path.join( basePath, f)
       labelFile =  glob.glob( path.join( ff, 'ManualLabels') + '/*ManualLabel-reduced.mha' )[0]
       featureFolder = path.join(ff, 'SpectraIteration1Features' )
       features = Features.SpectralFeatures()
       features.loadFromFolder( featureFolder, labelFile )
       dfs.append( features.toPandas() )
    testdf = pd.concat(dfs)






    #All features
    le = preprocessing.LabelEncoder()
    le.fit(traindf['label'])
    print( le.classes_ )
   
    fitForest("All Features", [], le, traindf, testdf)
    
    #All spectra
    featureNames = []
    for i in range(17):
        featureNames.append("Spectra-10-0007500000"+"-coeff-" + str(i))
        featureNames.append("Spectra-15-0007500000"+"-coeff-" + str(i))
        featureNames.append("Spectra-20-0007500000"+"-coeff-" + str(i))
        featureNames.append("Spectra-10-0005000000"+"-coeff-" + str(i))
        featureNames.append("Spectra-15-0005000000"+"-coeff-" + str(i))
        featureNames.append("Spectra-20-0005000000"+"-coeff-" + str(i))

    fitForest("All Spectra", featureNames, le, traindf, testdf)


    #Single spectra
    featureNames = []
    for i in range(17):
        featureNames.append( "Spectra-20-0007500000"+"-coeff-" + str(i) )
    
    fitForest("Single Spectrum", featureNames, le, traindf, testdf)

    #All chebyshev
    featureNames = []
    for i in range(7):
        featureNames.append("Chebyshev-10-0007500000"+"-coeff-" + str(i))
        featureNames.append("Chebyshev-15-0007500000"+"-coeff-" + str(i))
        featureNames.append("Chebyshev-20-0007500000"+"-coeff-" + str(i))
        featureNames.append("Chebyshev-10-0005000000"+"-coeff-" + str(i))
        featureNames.append("Chebyshev-15-0005000000"+"-coeff-" + str(i))
        featureNames.append("Chebyshev-20-0005000000"+"-coeff-" + str(i))

    fitForest("All Chebyshev", featureNames, le, traindf, testdf)
   
    #Single chebyshev
    featureNames = []
    for i in range(7):
        featureNames.append("Chebyshev-20-0007500000"+"-coeff-" + str(i))

    fitForest("Single Chebyshev", featureNames, le, traindf, testdf)

    #All chebyshev
    featureNames = []
    for i in range(2):
        featureNames.append("Line-10-0007500000"+"-coeff-" + str(i))
        featureNames.append("Line-15-0007500000"+"-coeff-" + str(i))
        featureNames.append("Line-20-0007500000"+"-coeff-" + str(i))
        featureNames.append("Line-10-0005000000"+"-coeff-" + str(i))
        featureNames.append("Line-15-0005000000"+"-coeff-" + str(i))
        featureNames.append("Line-20-0005000000"+"-coeff-" + str(i))

    fitForest("All Line", featureNames, le, traindf, testdf)
   
    #Single chebyshev
    featureNames = []
    for i in range(2):
        featureNames.append("Line-20-0007500000"+"-coeff-" + str(i))

    fitForest("Single Line", featureNames, le, traindf, testdf)
if __name__ == '__main__':
    main()

