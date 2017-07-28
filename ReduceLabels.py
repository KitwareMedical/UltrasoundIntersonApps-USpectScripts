import os
import argparse
import glob

parser = argparse.ArgumentParser(description='Run Neural Net')
parser.add_argument('basepath', help="Path to data directory")
parser.add_argument('exepath', help="Path ReduceLabelImage executable")
args = parser.parse_args();

folders = os.listdir( args.basePath);

for f in folders:
    try:
      ff = os.path.join( args.basePath, f)
      labelFile =  glob.glob( os.path.join( ff, 'ManualLabels') + '/*ManualLabel.mha' )[0]
      spectraFile =  glob.glob( os.path.join( ff, 'SpectraIteration1') + '/*.mha' )[0]
      os.system(args.exepath + " -s " + spectraFile + " -l " + labelFile)
    except:
      print("Failed on: " + f)

