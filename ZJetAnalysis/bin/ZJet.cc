/* Copyright (c) 2014 - All Rights Reserved
 *   Dominik Haitz <dhaitz@cern.ch>
 */

#include <boost/algorithm/string.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <boost/property_tree/ptree.hpp>

#include <TFile.h>

#include "Artus/Configuration/interface/ArtusConfig.h"
#include "Artus/Configuration/interface/RootEnvironment.h"

#include "ZJet/ZJetAnalysis/interface/ZJetTypes.h"
#include "ZJet/ZJetAnalysis/interface/ZJetEventProvider.h"
#include "ZJet/ZJetAnalysis/interface/ZJetFactory.h"


int main(int argc, char** argv) {

	// parse the command line and load the
	ArtusConfig myConfig(argc, argv);
	
	// load the global settings from the config file
	ZJetGlobalSettings globalsettings = myConfig.GetGlobalSettings<ZJetGlobalSettings>();

	// create the output root environment, automatically saves the config into the root file
	RootEnvironment rootEnv(myConfig);


	FileInterface2 fileInterface(myConfig.GetInputFiles());
	ZJetEventProvider evtProvider(fileInterface, (globalsettings.GetInputIsData() ? DataInput : McInput));
	evtProvider.WireEvent( globalsettings );

	// the pipeline initializer will setup the pipeline, with
	// all the attached Producer, Filer and Consumer
	ZJetPipelineInitializer pInit;
	ZJetFactory factory;
	ZJetPipelineRunner runner;

	// load the pipeline with their configuration from the config file
	myConfig.LoadConfiguration( pInit, runner, factory, rootEnv.GetRootFile());

	// run all the configured pipelines and all their attached
	// consumers
	runner.RunPipelines(evtProvider, globalsettings);

	// close output root file
	rootEnv.Close();

	return 0;
}
