/* Copyright (c) 2014 - All Rights Reserved
 *   Dominik Haitz <dhaitz@cern.ch>
 */

#include <boost/algorithm/string.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <boost/property_tree/ptree.hpp>

#include <TFile.h>

#include "Artus/Configuration/interface/ArtusConfig.h"
#include "Artus/Configuration/interface/RootEnvironment.h"

#include "Excalibur/Compile/interface/ZJetTypes.h"
#include "Excalibur/Compile/interface/ZJetEventProvider.h"
#include "Excalibur/Compile/interface/ZJetFactory.h"

int main(int argc, char** argv)
{
    // parse the command line and load the
    std::unique_ptr<ArtusConfig> myConfig = std::make_unique<ArtusConfig>(argc, argv);
    // ArtusConfig myConfig(argc, argv);

    // load the global settings from the config file
    ZJetSettings settings = myConfig->GetSettings<ZJetSettings>();

    // create the output root environment, automatically saves the config into
    // the root file
    RootEnvironment rootEnv(*myConfig);

    FileInterface2 fileInterface(myConfig->GetInputFiles());
    ZJetEventProvider evtProvider(fileInterface, (settings.GetInputIsData() ? DataInput : McInput));
    evtProvider.WireEvent(settings);

    // the pipeline initializer will setup the pipeline, with
    // all the attached Producer, Filer and Consumer
    ZJetPipelineInitializer pInit;
    ZJetFactory factory;
    ZJetPipelineRunner runner;

    // load the pipeline with their configuration from the config file
    myConfig->LoadConfiguration(pInit, runner, factory, rootEnv.GetRootFile());

    // run all the configured pipelines and all their attached
    // consumers
    runner.RunPipelines(evtProvider, settings);

    // close output root file
    rootEnv.Close();

    return 0;
}
