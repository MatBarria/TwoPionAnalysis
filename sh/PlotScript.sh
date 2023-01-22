#!/bin/bash
cd ..
mkdir -p bin
cd Cpp

g++ -Wall -fPIC -I../include `root-config --cflags` Integration.cpp -o ../bin/Integration  `root-config --glibs` ../include/Pt2Processing.h
g++ -Wall -fPIC -I../include `root-config --cflags` Broadening.cpp  -o ../bin/Broadening  `root-config --glibs` ../include/Broad.h


cd ../bin

./Integration
./Broadening

cd ../MatPlot

python3 Broadening.py
