#!/bin/bash

set -x -e

script_dir=$(cd $(dirname $0) || exit 1; pwd)

#python ./ApplyPyToFolder.py ./Convert_USRF_Spectra.py ./2016-09-09-MeatPhantom/${1}
#python ./ApplyPyToFolder.py ./Analyze_USRF_Spectra.py ./2016-09-09-MeatPhantom/${1} ./2016-09-09-MeatPhantom/Baseline


#python ./ApplyPyToFolder.py ./Convert_USRF_BMode.py ~/data/2017.05.31-FourProbes-PlanarNormalization-Meat-Liver/

glob='*[12][05]_freq_000[75][05]00000_*.nrrd'

#python ${script_dir}/ApplyPyToFolder.py \
  #--glob '*[12][05]_freq_000[75][05]00000_*.nrrd' \
  #${script_dir}/Estimate_USRF_ReferenceSpectrum.py \
  #./LinearProbe1/PlanarReflector1
#python ${script_dir}/ApplyPyToFolder.py \
  #--glob '*[12][05]_freq_000[75][05]00000_*.nrrd' \
  #${script_dir}/Estimate_USRF_ReferenceSpectrum.py \
  #./LinearProbe2/PlanarReflector1

LinearProbe1DataSets=(
  Chicken1/
  Chicken2/
  Chicken3/
  Chicken4/
  CS1/
  CS2/
  CS3/
  CS4/
  PC1/
  PC2/
  PC3/
  PC4/
  PC5/
  Pork1/
  Pork2/
  Pork3/
  Pork4/
  PS1/
  PS2/
  PS3/
  PS4/
  SC1/
  SC2/
  SC3/
  SC4/
  Steak1/
  Steak2/
  Steak3/
  Steak4/
  )
#for dataset in ${LinearProbe1DataSets[@]}; do
  #python ${script_dir}/ApplyPyToFolder.py \
    #--glob "${glob}" \
    #${script_dir}/Convert_USRF_Spectra.py \
    #./LinearProbe1/${dataset} \
    #'../PlanarReflector1/ReferenceSpectrum/' \
    #'SpectraIteration1'
  #echo ''
#done

for dataset in ${LinearProbe1DataSets[@]}; do
  python ${script_dir}/ApplyPyToFolder.py \
    --glob "*Spectra*.mha" \
    ${script_dir}/Analyze_USRF_Spectra.py \
    ./LinearProbe1/${dataset}/SpectraIteration1/ \
    '../SpectraIteration1Features'
  echo ''
done


LinearProbe2DataSets=(
  Chicken1/
  Chicken2/
  CS1/
  CS2/
  Pork1/
  Pork2/
  Steak1/
  Steak2/
  )

#for dataset in ${LinearProbe2DataSets[@]}; do
  #python ${script_dir}/ApplyPyToFolder.py \
    #--glob "${glob}" \
    #${script_dir}/Convert_USRF_Spectra.py \
    #./LinearProbe2/${dataset} \
    #'../PlanarReflector1/ReferenceSpectrum/' \
    #'SpectraIteration1'
  #echo ''
#done
