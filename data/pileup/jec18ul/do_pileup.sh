#!/bin/sh

_excal_data_dir="$CMSSW_BASE/src/Excalibur/data"

year="2018"
config_tag="jec18ul"
data_runs="A B C D ABCD"  # loop through these data run periods below
#data_runs="A"  # loop through these data run periods below
data_tag="12Nov2019_UL2018"

mc_sample="DYJets"
mc_tag="Summer19-madgraphMLM_realistic_v11_L1v1"

#mc_skim_filelist=`pathsub_local_se /storage/gridka-nrg/mhorzela/Skimming/ZJet_DYJetsToLL_Summer19-madgraphMLM_realistic_v11_L1v1-v1/job_48[0..1]_output.root`
mc_skim_filelist=`pathsub_local_grid /storage/gridka-nrg/mhorzela/Skimming/ZJet_DYJetsToLL_Summer19-madgraphMLM_realistic_v11_L1v1-v1/job_*_output.root`


# -- first, calculate data PU profiles for each run period
for data_run in $data_runs; do
    _data_pu_prof_file="$_excal_data_dir/pileup/${config_tag}/PUProfile_Data_${year}_${data_run}_${data_tag}.root"

    _data_run_json_file="$_excal_data_dir/json/Collisions18/Cert_${data_run}_13TeV_Legacy2018_Collisions18_JSON.txt"
    if [[ ! -f ${_data_run_json_file} ]]; then
        echo "[ERROR] Cannot find golden JSON file for data run '${data_run}' at: ${_data_run_json_file}"
        exit 1
    fi

    _data_pu_lumi_file="$_excal_data_dir/pileup/${config_tag}/pileup_latest.txt"
    if [[ ! -f ${_data_pu_lumi_file} ]]; then
        echo "[ERROR] Cannot find PU-per-lumi file at: ${_data_pu_lumi_file}"
        exit 1
    fi

    echo
    mkdir -p `dirname "_data_pu_prof_file"`
    if [[ ! -f ${_data_pu_prof_file} ]]; then
        echo "[INFO] Calculating PU profile for data run: ${data_run}"
        puWeightCalc.py $_data_run_json_file \
            -i $_data_pu_lumi_file \
            -x 69.2 \
            -s \
            -d "$_data_pu_prof_file"
    else
        echo "[INFO] PU profile for data run '${data_run}' exists: skipping..."
    fi
done


# -- next, calculate MC PU profiles from skim filelist
_mc_pu_prof_file="$_excal_data_dir/pileup/${config_tag}/PUProfile_MC_${year}_${mc_sample}_${mc_tag}.root"
if [[ ! -f ${_mc_pu_prof_file} ]]; then
    echo
    echo "[INFO] Calculating PU profile for MC sample: ${mc_sample}_${mc_tag}"
    mkdir -p `dirname "_mc_pu_prof_file"`
    puWeightCalc.py "" $mc_skim_filelist \
        -s \
        -m "$_mc_pu_prof_file"
else
    echo "[INFO] PU profile for MC sample '${mc_sample}_${mc_tag}' exists: skipping..."
fi


# -- finally, calculate MC PU weights for PU profiles in each data run
for data_run in $data_runs; do
    _data_pu_prof_file="$_excal_data_dir/pileup/${config_tag}/PUProfile_Data_${year}_${data_run}_${data_tag}.root"
    _mc_pu_weights_file="$_excal_data_dir/pileup/${config_tag}/PUWeights_${year}_Data_${data_run}_${data_tag}_MC_${mc_tag}.root"
    echo
    if [[ ! -f ${_mc_pu_weights_file} ]]; then
        mkdir -p `dirname "_mc_pu_weights_file"`
        echo "[INFO] Calculating MC PU weights for PU profile in data run: ${data_run}"
        puWeightCalc.py "$_data_pu_prof_file" "$_mc_pu_prof_file" -o "$_mc_pu_weights_file"
    else
        echo "[INFO] MC PU weights for PU profile in data run '${data_run}' exists: skipping..."
    fi
done
