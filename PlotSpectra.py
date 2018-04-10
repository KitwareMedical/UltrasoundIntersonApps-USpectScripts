from os import listdir, path
import numpy as np
import glob
import matplotlib.pyplot as plt
import matplotlib as mpl
import itk
import Features
import argparse
from statsmodels.graphics import functional

def main():
    parser = argparse.ArgumentParser(description='Run Neural Net')
    parser.add_argument('basepath', help="Path to data directory")
    args = parser.parse_args();

    basePath = args.basepath
    trainFolders = [ 'Chicken1', 'Chicken2', 'Steak1', 'Steak2', 'Pork1', 'Pork2' ]
    
    dfs = []
    for f in trainFolders:
       ff = path.join( basePath, f)
       labelFile =  glob.glob( path.join( ff, 'ManualLabels') + '/*ManualLabel-reduced.mha' )[0]
       featureFolder = path.join(ff, 'SpectraIteration1Features' )
       features = Features.SpectralFeatures()
       features.loadFromFolder( featureFolder, labelFile )
       df = features.toPandas()
       df = df.loc[ df['label'] > 0 ]
       dfs.append( df )

    spectraNames = ["Spectra-10-0005000000-coeff-",
                    "Spectra-15-0005000000-coeff-",
                    "Spectra-20-0005000000-coeff-",
                    "Spectra-10-0007500000-coeff-",
                    "Spectra-15-0007500000-coeff-",
                    "Spectra-20-0007500000-coeff-" ]

    colors = ["xkcd:orangey red", 
              "xkcd:pumpkin", 
              "xkcd:orange yellow",
              "xkcd:light navy",
              "xkcd:cerulean blue",
              "xkcd:faded blue"]
    colors1 = [ mpl.colors.to_rgba(x, 0.75) for x in colors]
    colors2 = [ mpl.colors.to_rgba(x, 0.5) for x in colors]
    print(colors1)

    mean = []
    std = []
    smple = []
    for df in dfs:
        mean.append([])
        std.append([])
        smple.append([])

    for s in spectraNames:
        cols = []
        for i in range(17):
            cols.append( s + str(i) )
        for k in range( len( dfs ) ):
            sel = dfs[k][cols]
            smple[k].append( sel.sample(n=5) );
            #res = functional.fboxplot( sel.sample(n=100), wfactor=5,
            #        plot_opts ={ "c_inner":colors1[k], 
            #                     "c_median":colors[k], 
            #                     "c_outer":colors2[k]}
            #        )
            #plt.show()

            mean[k].append( sel.mean( axis = 0 ) )
            std[k].append( sel.std( axis=0 ) )


    for k in range( len(mean) ):
        for i in range( len( mean[k] ) ):
          
          #plt.plot( np.arange(len(mean[k][i])), smple[k][i].as_matrix().transpose(), 
          #          color=colors2[i] )
          plt.errorbar( x=np.arange(len(mean[k][i]) )+i/10, y=mean[k][i], 
                        yerr=3*std[k][i], color=colors[i] ) 

        plt.title( trainFolders[k] )
        #plt.show()
        plt.savefig( trainFolders[k] + "-spectra.png")
        plt.close()
    

if __name__ == '__main__':
    main()

