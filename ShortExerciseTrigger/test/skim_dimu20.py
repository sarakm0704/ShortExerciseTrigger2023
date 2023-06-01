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
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(100)
)

# Input source
process.source = cms.Source("PoolSource",
   fileNames = cms.untracked.vstring(
       '/store/data/Run2022F/Muon/MINIAOD/PromptReco-v1/000/360/390/00000/282e5859-6f59-41bc-ae92-3892ec9aa3af.root',
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
process.source.lumisToProcess = LumiList.LumiList(filename = 'Cert_Collisions2022_355100_362760_Golden_JSON.txt').getVLuminosityBlockRange()

# skim definitions

process.highptMuons = cms.EDFilter("PtMinCandViewSelector",
                           src = cms.InputTag("slimmedMuons"),
                           ptMin = cms.double(20)
)

process.dimuonFilter = cms.EDFilter("CandViewCountFilter",
  src = cms.InputTag("highptMuons"),
  minNumber = cms.uint32(2),
)

process.dimu_filter_step = cms.Path(process.highptMuons + process.dimuonFilter)


# Output definition

process.Out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string ("skim.root"),
                               outputCommands = cms.untracked.vstring('keep *'),
                               SelectEvents = cms.untracked.PSet(
                                   SelectEvents = cms.vstring('dimu_filter_step')
                               ),
)
  
process.GlobalTag.globaltag = "124X_dataRun3_Prompt_v10"

# Path and EndPath definitions
process.output_step = cms.EndPath(process.Out)

process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 10000
