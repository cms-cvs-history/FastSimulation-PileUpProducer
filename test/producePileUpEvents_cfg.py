import FWCore.ParameterSet.Config as cms

process = cms.Process("PileUp")

# The number of events to be generated
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(10000)
)

# Initialize the random number generator service
process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService",
    # This is to initialize the random engine of the source
    theSource = cms.PSet(
        initialSeed = cms.untracked.uint32(123456),
        engineName = cms.untracked.string('TRandom3')
    )
)

# Pythia
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.source = cms.Source(
    "PythiaSource",
    pythiaPylistVerbosity = cms.untracked.int32(0),
    # put here the efficiency of your filter (1. if no filter) dummy
    filterEfficiency = cms.untracked.double(1.0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    # put here the cross section of your process (in pb) dummy
    crossSection = cms.untracked.double(55000000000.0),
    maxEventsToPrint = cms.untracked.int32(2),
    PythiaParameters = cms.PSet(
        parameterSets = cms.vstring(
            'pythiaUESettings', 
            'pythiaMinBias', 
            'myParameters'
        ),
        # UE settings were taken from Configuration/Sprin08Production/python/PythiaUESetting_cfi.py
        pythiaUESettings = cms.vstring(
            'MSTJ(11)=3     ! Choice of the fragmentation function', 
            'MSTJ(22)=2     ! Decay those unstable particles', 
            'PARJ(71)=10 .  ! for which ctau  10 mm', 
            'MSTP(2)=1      ! which order running alphaS', 
            'MSTP(33)=0     ! no K factors in hard cross sections', 
            'MSTP(51)=10042     ! CTEQ6L1 structure function chosen', 
            'MSTP(52)=2     ! work with LHAPDF', 
            'MSTP(81)=1     ! multiple parton interactions 1 is Pythia default', 
            'MSTP(82)=4     ! Defines the multi-parton model', 
            'MSTU(21)=1     ! Check on possible errors during program execution', 
            'PARP(82)=1.8387   ! pt cutoff for multiparton interactions', 
            'PARP(89)=1960. ! sqrts for which PARP82 is set', 
            'PARP(83)=0.5   ! Multiple interactions: matter distrbn parameter', 
            'PARP(84)=0.4   ! Multiple interactions: matter distribution parameter', 
            'PARP(90)=0.16  ! Multiple interactions: rescaling power', 
            'PARP(67)=2.5    ! amount of initial-state radiation', 
            'PARP(85)=1.0  ! gluon prod. mechanism in MI', 
            'PARP(86)=1.0  ! gluon prod. mechanism in MI', 
            'PARP(62)=1.25   ! ', 
            'PARP(64)=0.2    ! ', 
            'MSTP(91)=1     !', 
            'PARP(91)=2.1   ! kt distribution', 
            'PARP(93)=15.0  ! '
        ),
        # The processes open for minimum bias events
        pythiaMinBias = cms.vstring(
            'MSEL=0         ! User defined processes', 
            'MSUB(11)=1     ! Min bias process', 
            'MSUB(12)=1     ! Min bias process', 
            'MSUB(13)=1     ! Min bias process', 
            'MSUB(28)=1     ! Min bias process', 
            'MSUB(53)=1     ! Min bias process', 
            'MSUB(68)=1     ! Min bias process', 
            'MSUB(92)=1     ! Min bias process, single diffractive', 
            'MSUB(93)=1     ! Min bias process, single diffractive', 
            'MSUB(94)=1     ! Min bias process, double diffractive', 
            'MSUB(95)=1     ! Min bias process'),
        #    Disable the ctau check : particles are not decayed
        myParameters = cms.vstring('PARJ(71) = -1.')
        # This is a vector of ParameterSet names to be read, in this order
        # The first two are minbias-event configuration
        # The last one are simply my additional parameters
    )
)

# The module to produce events
process.prodPU = cms.EDFilter(
    "producePileUpEvents",
    PUParticleFilter = cms.PSet(
        # Particles with |eta| > etaMax (momentum direction at primary vertex) 
        # are not simulated - 7.0 includes CASTOR (which goes to 6.6) 
        etaMax = cms.double(7.0),
        # Charged particles with pT < pTMin (GeV/c) are not simulated
        pTMin = cms.double(0.0),
        # Particles with energy smaller than EMin (GeV) are not simulated
        EMin = cms.double(0.0),
        # Protons with energy larger than EProton (GeV) are all kept
        EProton = cms.double(5000.0)
    ),
    PUEventFile = cms.untracked.string('MinBiasEvents_001.root'),
    SavePileUpEvents = cms.bool(True),
    BunchPileUpEventSize = cms.uint32(1000)
)

# The path
process.p = cms.Path(process.prodPU)


