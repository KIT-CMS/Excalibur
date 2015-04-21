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
