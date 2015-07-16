#source HarryPlotter ini script
source $ARTUSPATH/HarryPlotter/scripts/ini_harry.sh

export PYTHONCONFIGS=$EXCALIBURPATH/Plotting/plot-configs/python-configs
export JSONCONFIGS=$EXCALIBURPATH/Plotting/plot-configs/json-configs

export PYTHONPATH=$PYTHONCONFIGS:$PYTHONPATH

export PYTHONLINKDIR=$EXCALIBURPATH/../python-links
export PATH=$EXCALIBURPATH/Plotting/scripts:$PATH
if [ -d "$PYTHONLINKDIR" ]; then
    export PYTHONPATH=$PYTHONLINKDIR:$PYTHONPATH
fi

# This function creates a folder with links to python directories, like SCRAM
# TODO enable merlin standalone usage without reinventing SCRAM ...
standalone_merlin(){
    for j in Artus Excalibur; do
        # base dirs
        mkdir -p $PYTHONLINKDIR/$j
        touch $PYTHONLINKDIR/$j/__init__.py
        for i in `ls -d $(dirname $EXCALIBURPATH)/$j/*/python/`; do
            # create links to python dirs
            if [ ! -d $PYTHONLINKDIR/$j/$(basename $(dirname $i)) ]; then
                ln -s $(dirname $i)/python $PYTHONLINKDIR/$j/$(basename $(dirname $i))
            fi
            # create __init__.py in dirs and subdirs
            for k in `find $PYTHONLINKDIR/$j/*/ -type d`; do
                touch $k/__init__.py
            done
        done
    done
}

# get the weights for a simple reweighting in npv. weight string is printed as output
# Usage: get_weights data.root mc.root
get_weights(){
	ALGO=ak4PFJetsCHS
	QUANTITY=npv
	BINNING="30,0.5,30.5"
	echo "(npv=="`merlin.py -x $QUANTITY -i $1 $2 --zjetf nocuts --corr L1L2L3 --algo $ALGO --analy NormalizeToFirstHisto Ratio --nicks-white ratio --log-l debug --x-bins $BINNING --y-lims 0 1 | grep fSumw | cut -d "=" -f 2 | cut -d "," -f 1 | while read i; do echo ")*${i}+(npv=="; done | nl | sed 's/ //g' | sed 's/\t//g' ` | sed 's/ //g' | sed 's/.\{7\}$//'
}
