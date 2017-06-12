#!/bin/sh

set -x -e

script_dir=$(cd $(dirname $0) || exit 1; pwd)

#python ./ApplyPyToFolder.py ./Convert_USRF_Spectra.py ./2016-09-09-MeatPhantom/${1}
#python ./ApplyPyToFolder.py ./Analyze_USRF_Spectra.py ./2016-09-09-MeatPhantom/${1} ./2016-09-09-MeatPhantom/Baseline


#python ./ApplyPyToFolder.py ./Convert_USRF_BMode.py ~/data/2017.05.31-FourProbes-PlanarNormalization-Meat-Liver/

python ${script_dir}/ApplyPyToFolder.py \
  --glob '*[12][05]_freq_000[75][05]00000_*.nrrd' \
  ${script_dir}/Estimate_USRF_ReferenceSpectrum.py \
  ./LinearProbe1/PlanarReflector1
python ${script_dir}/ApplyPyToFolder.py \
  --glob '*[12][05]_freq_000[75][05]00000_*.nrrd' \
  ${script_dir}/Estimate_USRF_ReferenceSpectrum.py \
  ./LinearProbe2/PlanarReflector1
