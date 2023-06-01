import FWCore.ParameterSet.Config as cms

process = cms.Process('HLTANALYZER')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 10000
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

# Input source
process.source = cms.Source("PoolSource",
   fileNames = cms.untracked.vstring('/store/data/Run2022F/Muon/MINIAOD/PromptReco-v1/000/360/390/00000/282e5859-6f59-41bc-ae92-3892ec9aa3af.root'),
)


process.options = cms.untracked.PSet()

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.20 $'),
    annotation = cms.untracked.string('RelVal nevts:100'),
    name = cms.untracked.string('Applications')
)

# Output definition

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string('histos_SingleMuTrigAnalyzer.root')
)

### analyzer configuration

process.singleMuTrigAnalyzerMiniAOD = cms.EDAnalyzer("SingleMuTrigAnalyzerMiniAOD")
process.singleMuTrigAnalyzerMiniAOD.triggerName = cms.untracked.string("HLT_IsoMu24_v15") # HLT_IsoMu27_v18
process.singleMuTrigAnalyzerMiniAOD.verbose = cms.untracked.bool(False)

process.GlobalTag.globaltag = "124X_dataRun3_Prompt_v10"

# Path and EndPath definitions
process.HLTanalyzers = cms.Path(process.singleMuTrigAnalyzerMiniAOD)
