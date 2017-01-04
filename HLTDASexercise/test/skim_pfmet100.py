import FWCore.ParameterSet.Config as cms

process = cms.Process('SKIM')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff")

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

# Input source
process.source = cms.Source("PoolSource",
   fileNames = cms.untracked.vstring(
       '/store/data/Run2016G/SingleElectron/MINIAOD/23Sep2016-v1/100000/004A7893-A990-E611-B29F-002590E7DE36.root',
       '/store/data/Run2016G/SingleElectron/MINIAOD/23Sep2016-v1/100000/004A7893-A990-E611-B29F-002590E7DE36.root,'
       '/store/data/Run2016G/SingleElectron/MINIAOD/23Sep2016-v1/100000/0083C5D5-968F-E611-B630-7845C4FC35CF.root,'
       '/store/data/Run2016G/SingleElectron/MINIAOD/23Sep2016-v1/100000/02A99D82-C590-E611-9030-002590E7E02E.root,'
       '/store/data/Run2016G/SingleElectron/MINIAOD/23Sep2016-v1/100000/02B11FAD-1B90-E611-B564-002590E7DEBE.root,'
       '/store/data/Run2016G/SingleElectron/MINIAOD/23Sep2016-v1/100000/043C2F15-E990-E611-8B0C-002590D0AF50.root,'
       '/store/data/Run2016G/SingleElectron/MINIAOD/23Sep2016-v1/100000/04D0C318-9491-E611-8A52-001E67E6F53F.root,'
       '/store/data/Run2016G/SingleElectron/MINIAOD/23Sep2016-v1/100000/04D4E6A2-7B8F-E611-A853-0090FAA581F4.root,'
       '/store/data/Run2016G/SingleElectron/MINIAOD/23Sep2016-v1/100000/06BAD5AC-9E90-E611-B55B-7845C4FC3B8A.root,'
       '/store/data/Run2016G/SingleElectron/MINIAOD/23Sep2016-v1/100000/085E96CE-C88D-E611-BF64-001E67504685.root,'
       '/store/data/Run2016G/SingleElectron/MINIAOD/23Sep2016-v1/100000/0874488C-5B8E-E611-AC87-002590E7E012.root,'
   ),
)


process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.20 $'),
    annotation = cms.untracked.string('RelVal nevts:100'),
    name = cms.untracked.string('Applications')
)

# JSON

import FWCore.PythonUtilities.LumiList as LumiList
process.source.lumisToProcess = LumiList.LumiList(filename = 'Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON.txt').getVLuminosityBlockRange()

# skim definitions

process.highpfmet = cms.EDFilter("PtMinCandViewSelector",
                           src = cms.InputTag("slimmedMETs"),
                           ptMin = cms.double(100)
)

process.metFilter = cms.EDFilter("CandViewCountFilter",
  src = cms.InputTag("highpfmet"),
  minNumber = cms.uint32(1),
)

process.pfmet_filter_step = cms.Path(process.highpfmet + process.metFilter)


# Output definition

process.Out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string ("skim_10files.root"),
                               outputCommands = cms.untracked.vstring('keep *'),
                               SelectEvents = cms.untracked.PSet(
                                   SelectEvents = cms.vstring('pfmet_filter_step')
                               ),
)
  
process.GlobalTag.globaltag = "80X_dataRun2_2016SeptRepro_v3"

# Path and EndPath definitions
process.output_step = cms.EndPath(process.Out)

process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 10000
