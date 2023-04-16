#!/bin/bash
cd ..
mkdir -p bin
cd Cpp

g++ -Wall -fPIC -I../include `root-config --cflags` ApplyACFactors.cpp -o ../bin/ApplyACFactors `root-config --glibs` ../include/Binning.h
g++ -Wall -fPIC -I../include `root-config --cflags` Integration.cpp -o ../bin/Integration  `root-config --glibs` ../include/Pt2Processing.h
g++ -Wall -fPIC -I../include `root-config --cflags` Broadening.cpp  -o ../bin/Broadening  `root-config --glibs` ../include/Broad.h
g++ -Wall -fPIC -I../include `root-config --cflags` AccEventTuple.cpp -o ../bin/AccEventTuple  `root-config --glibs` ../include/Binning.h


cd ../bin

#./AccEventTuple
./ApplyACFactors
#./Integration
#./Broadening

cd ../MatPlot

#python3 Broadening.py
