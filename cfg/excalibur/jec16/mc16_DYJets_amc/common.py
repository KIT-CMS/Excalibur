JEC_BASE = 'Summer16_07Aug2017'
# JEC_VERSION = 'V15'
JEC_VERSION = 'V11'

#JER = 'Summer16_25nsV1'  # set this to 'None' to turn JER smearing off
JER = None

SE_PATH_PREFIXES = dict(
    srm_gridka_nrg="srm://cmssrm-kit.gridka.de:8443/srm/managerv2?SFN=/pnfs/gridka.de/cms/disk-only/store/user",
    srm_desy_dcache="srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2/store/user",
    local_gridka_nrg="/storage/gridka-nrg",
    local_desy_dcache="/pnfs/desy.de/cms/tier2/store/user",
    xrootd_gridka_nrg="root://cmsxrootd-redirectors.gridka.de//store/user"
)
