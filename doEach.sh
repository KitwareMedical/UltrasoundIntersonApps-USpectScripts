#!/bin/sh

./Code/ApplyPyToFolder.py ./Code/Convert_USRF_Spectra.py ./2016-09-09-MeatPhantom/${1}
./Code/ApplyPyToFolder.py ./Code/Analyze_USRF_Spectra.py ./2016-09-09-MeatPhantom/${1} ./2016-09-09-MeatPhantom/Baseline
./Code/ApplyPyToFolder.py ./Code/Convert_USRF_BMode.py ./2016-09-09-MeatPhantom/${1}
