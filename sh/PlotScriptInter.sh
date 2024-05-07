#!/bin/bash
cd ..
mkdir -p bin
cd Cpp

g++ -Wall -fPIC -I../include `root-config --cflags` Integration.cpp -o ../bin/Integration  `root-config --glibs` ../include/Pt2Processing2.h
g++ -Wall -fPIC -I../include `root-config --cflags` Broadening.cpp  -o ../bin/Broadening  `root-config --glibs` ../include/Broad.h
#g++ -Wall -fPIC -I../include `root-config --cflags` Interpolate_Acc_EmptySimpler.cpp -o ../bin/Interpolate_Acc_Empty `root-config --glibs` ../include/Binning.h
g++ -Wall -fPIC -I../include `root-config --cflags` Interpolate_Acc_Empty2.cpp -o ../bin/Interpolate_Acc_Empty `root-config --glibs` ../include/Binning.h


cd ../bin

./Interpolate_Acc_Empty
./Integration
./Broadening

cd ../MatPlot

python3 Broadening.py
