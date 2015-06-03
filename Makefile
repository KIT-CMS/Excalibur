# Makefile for excalibur:artus (c) 2013
# Joram Berger <joram.berger@cern.ch>
# Dominik Haitz <dhaitz@cern.ch>
# usage: make help

ROOTCFLAGS     = $(shell root-config --cflags)
ROOTLDFLAGS    = $(shell root-config --ldflags --libs)

PROJECT        = Excalibur
EXECUTABLE     = artus
CXX            = g++
FLAGS          = -O2 -pedantic -Wfatal-errors -lprofiler -ltcmalloc -Wall -Wno-unused-local-typedefs -c -std=c++11 -g -fPIC
CFLAGS         = $(FLAGS)\
 -Isrc/ -Iexternal/OfflineCorrection/ -Iexternal/ -I../\
 $(ROOTCFLAGS) -I$(BOOSTPATH)/include/ -I$(KAPPATOOLSPATH)/../
LDFLAGS        = $(ROOTLDFLAGS) -lGenVector -lTMVA\
 -L$(BOOSTPATH)/lib/ -lboost_regex\
 -L../Artus/ -lartus_configuration -lartus_consumer -lartus_core -lartus_filter -lartus_provider -lartus_utility -lartus_kappaanalysis -lartus_externalcorr\
 -L$(KAPPAPATH)/lib/ -L$(KAPPATOOLSPATH)/lib/ -lKappa -lKRootTools -lKToolbox

OBJECTS = $(patsubst %.cc,%.o,$(wildcard src/*.cc src/*/*.cc))

HEADERS = $(wildcard src/*.h src/*/*.h)

$(EXECUTABLE): $(OBJECTS) $(HEADERS)
	@echo `git branch | sed -n '/\* /s///p'` &> version.log
	@echo "Linking" $(EXECUTABLE)":"
	@echo $(CXX) LDFLAGS $(OBJECTS)
	@$(CXX) $(LDFLAGS) $(OBJECTS) -o scripts/$@
	@echo $(EXECUTABLE) "built successfully."

.cc.o:
	@echo $(CXX) $(FLAGS) $<
	@$(CXX) $(CFLAGS) $< -o $@

clean:
	rm -f $(OBJECTS) $(EXECUTABLE)

purge: clean
	rm -f src/*.cc.formatted src/*/*.cc.formatted
	rm -f plotting/*.pyc plotting/*/*.pyc cfg/artus/*.pyc scripts/*.pyc
	rm -f cfg/artus/*.py.json

check:
	@echo -e "checking COMPILER...     \c" && which $(CXX)
	@echo -e "checking ROOT...         \c" && root-config --version
	@echo -e "checking BOOST...        \c" && ls $(BOOSTPATH) -d
	@echo -e "checking KAPPA...        \c" && ls $(KAPPAPATH) -d
	@echo -e "checking KAPPATOOLS...   \c" && ls $(KAPPATOOLSPATH) -d
	@echo -e "checking OFFLINE JEC...  \c" && ls ../CondFormats -d
	@echo -e "checking ARTUS...        \c" && ls ../Artus -d
	@echo -e "checking PYTHON...       \c" && python --version || echo "  Python is not needed for compiling"
	@echo -e "checking GRID-CONTROL... \c" && which go.py 2> /dev/null || echo "not found, grid-control is not needed for compiling"
	@echo -e "checking EXECUTABLE...   \c" && ls scripts/$(EXECUTABLE) 2> /dev/null || echo $(EXECUTABLE) "not yet built"
	@echo $(PROJECT) "is ok."

project:
	@test -f ../Makefile || ln -s Excalibur/Makefile.project ../Makefile
	make -C ..

#TODO: version	path
#NN=`ls /wlcg/sw/boost/current/lib/libboost_regex.so.*` && echo ${NN/*so./}
#&& git --git-dir=$(KAPPAPATH)/../.git log -1 | grep Date

doc:
	@echo "Make" $(EXECUTABLE) "documentation in future"

help:
	@echo "The" $(PROJECT) "Makefile"
	@echo " " $(PROJECT) version $(shell git describe)
	@echo "  see DOCUMENTATION.md for more help and COPYING for the licence."
	@echo "make check          check for build requirements"
	@echo "make [-j 4] [-B]    build" $(EXECUTABLE) "[on 4 cores] [rebuild everything]"
	@echo "make clean          clean up object files and executable"
	@echo "make purge          clean up .pyc and .py.json files additionally"
	@echo "make help           show this help message"
