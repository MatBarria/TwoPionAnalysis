cd ..

mkdir -p bin

g++ -Wall -fPIC -I./include `root-config --cflags` ApplyRcFactor.cpp -o ./bin/ApplyRcFactor  `root-config --glibs` ./include/Integration_Rc.h

g++ -Wall -fPIC -I./include `root-config --cflags` Interpolate_Rc.cpp -o ./bin/Interpolate_Rc `root-config --glibs` ./include/Binning_Rc.h

g++ -Wall -fPIC -I./include `root-config --cflags` Integration_Rc.cpp -o ./bin/Integration_Rc  `root-config --glibs` ./include/Integration_Rc.h

g++ -Wall -fPIC -I./include `root-config --cflags` Broadening_Rc.cpp  -o ./bin/Broadening_Rc  `root-config --glibs` ./include/Broad_Rc.h

g++ -Wall -fPIC -I./include `root-config --cflags` Percentaje_Rc.cpp -o ./bin/Percentaje_Rc  `root-config --glibs` ./include/Broad_Rc.h 

g++ -Wall -fPIC -I./include `root-config --cflags` Pt2Distributions_Rc.cpp -o ./bin/Pt2Distributions_Rc  `root-config --glibs` ./include/Broad_Rc.h

g++ -Wall -fPIC -I./include `root-config --cflags` DivAccRc.cpp -o ./bin/DivAccRc  `root-config --glibs` ./include/Broad_Rc.h

echo "Compilations ended"
cd bin

echo "-----Interpolation-----"
./Interpolate_Rc 
echo "-----Apply Rc factors-----"
./ApplyRcFactor 
echo "-----Integrate histograms-----"
./Integration_Rc
echo "-----Broadening-----"
./Broadening_Rc
#./Percentaje_Rc
echo "-----Pt2Distribution-----"
./Pt2Distributions_Rc
echo "-----Ratio Cpp-----"
./DivAccRc

cd ../MatPlot

echo "-----Plots-----"
python3 Plot_Rc.py
echo "-----Percentaje-----"
#python3 Percentaje_Rc.py
python3 SystematicRc.py
echo "-----Ratio-----"
#python3 AccRcRatio.py
echo "-----Pt2 Distributionsv-----"
python3 Pt2Distribution.py
