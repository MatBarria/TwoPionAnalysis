SHELL = /bin/bash

.DELETE_ON_ERROR:

.PHONY: all clean


ROOTCONFIG  := root-config
ROOTCFLAGS  := $(shell $(ROOTCONFIG) --cflags)
ROOTLDFLAGS := $(shell $(ROOTCONFIG) --ldflags)
ROOTLIBS    := $(shell $(ROOTCONFIG) --libs)
CERNLIBS    := -lpdflib804 -lmathlib -lphtools -lpacklib -lkernlib -lpawlib

CXX       := g++
CXXFLAGS  += -std=c++11 -O2 -Wall -fPIC $(ROOTCFLAGS)
# CXXFLAGS  += -std=c++0x -O2 -Wall -fPIC $(ROOTCFLAGS)
LD        = gfortran
LDFLAGS   = -O2 $(ROOTLDFLAGS) -lgfortran -Wl,-rpath,$(HAPRAD_CPP)/slib

INCLUDES  := -I$(HAPRAD_CPP) -I/home/matias/proyecto/TwoPionAnalysis/RCFactor/include
#LIBS      := -L/$(HAPRAD_CPP)/slib -lTRadCor $(ROOTLIBS) -lMathMore -L/usr/lib64/cernlib/2006/lib/ $(CERNLIBS)
LIBS      := -lstdc++ -L$(HAPRAD_CPP)/slib -lTRadCor $(ROOTLIBS) -lMathMore -L/home/matias/software/cernlib/2005/lib $(CERNLIBS) /home/matias/proyecto/TwoPionAnalysis/RCFactor/include/Binning_Rc.h

all: genRC

genRC:genRC.o
	$(LD) $(LDFLAGS) $^ $(LIBS) -o $@

genRC.o:genRC.cpp
	$(CXX) $(CXXFLAGS) $(INCLUDES) -c $< -o $@

clean:
	@rm -rf genRC genRC.o
