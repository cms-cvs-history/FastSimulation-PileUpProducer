#include "PluginManager/ModuleDef.h"
#include "FWCore/Framework/interface/InputSourceMacros.h"
#include "FWCore/Framework/interface/VectorInputSourceMacros.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FastSimulation/PileUpProducer/interface/PUSource.h"

using edm::PUSource;
DEFINE_SEAL_MODULE();
DEFINE_ANOTHER_FWK_INPUT_SOURCE(PUSource);
DEFINE_ANOTHER_FWK_VECTOR_INPUT_SOURCE(PUSource);
