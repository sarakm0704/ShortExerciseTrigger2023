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
                        fileNames = cms.untracked.vstring(
                            '/store/data/Run2022F/EGamma/MINIAOD/PromptReco-v1/000/360/390/00000/b48438da-5b5a-470a-893b-42967da4b8fc.root',
                            '/store/data/Run2022F/EGamma/MINIAOD/PromptReco-v1/000/360/390/00000/c4d1bcfd-1925-4c6c-8fc9-88ab310225dd.root',
                            '/store/data/Run2022F/EGamma/MINIAOD/PromptReco-v1/000/360/390/00000/e69d1e3b-83db-48ab-879f-bc3d45906c43.root',
                            '/store/data/Run2022F/EGamma/MINIAOD/PromptReco-v1/000/360/390/00000/f83cc5a2-919b-4abe-a1e6-e1bf0684f003.root',
                            '/store/data/Run2022F/EGamma/MINIAOD/PromptReco-v1/000/360/391/00000/0ef6c507-06ad-4fd1-8fab-e22314522d71.root',
                            '/store/data/Run2022F/EGamma/MINIAOD/PromptReco-v1/000/360/391/00000/b44da03a-7b2f-4967-9e1f-201ea98359b6.root',
                            '/store/data/Run2022F/EGamma/MINIAOD/PromptReco-v1/000/360/392/00000/023ce115-2a93-4b4f-badc-f172a543535e.root',
                            '/store/data/Run2022F/EGamma/MINIAOD/PromptReco-v1/000/360/392/00000/2bca83f1-12c6-4a27-87d6-039388a14971.root',
                            '/store/data/Run2022F/EGamma/MINIAOD/PromptReco-v1/000/360/392/00000/376ca6c1-9113-4f44-aff9-c5a7731657c5.root',
                            '/store/data/Run2022F/EGamma/MINIAOD/PromptReco-v1/000/360/392/00000/4a3ae865-edd2-4d70-8a18-0bea703f6139.root',
                            '/store/data/Run2022F/EGamma/MINIAOD/PromptReco-v1/000/360/392/00000/5edecd2b-be5e-40bd-8937-d3090cf78955.root',
                            '/store/data/Run2022F/EGamma/MINIAOD/PromptReco-v1/000/360/392/00000/67c53908-f7ea-477e-847d-9589e760b846.root',
                            '/store/data/Run2022F/EGamma/MINIAOD/PromptReco-v1/000/360/392/00000/7eed6970-1477-44f1-a37f-152c21755bb9.root',
                            '/store/data/Run2022F/EGamma/MINIAOD/PromptReco-v1/000/360/392/00000/82669627-2125-4798-9159-a1215044e72a.root',
                            '/store/data/Run2022F/EGamma/MINIAOD/PromptReco-v1/000/360/392/00000/8aae9809-d857-4cb9-94f7-408590b2cf66.root',
                            '/store/data/Run2022F/EGamma/MINIAOD/PromptReco-v1/000/360/392/00000/93d674d4-b955-4972-84c4-b8282deede48.root',
                            '/store/data/Run2022F/EGamma/MINIAOD/PromptReco-v1/000/360/392/00000/c9827edd-8c14-4154-a089-aa08dff57e63.root',
                            '/store/data/Run2022F/EGamma/MINIAOD/PromptReco-v1/000/360/392/00000/d64152e3-deda-4d3c-86e4-9f14f6f00bfa.root',
                            '/store/data/Run2022F/EGamma/MINIAOD/PromptReco-v1/000/360/393/00000/030796b3-93b9-4697-9a17-f88dba418af1.root',
                            '/store/data/Run2022F/EGamma/MINIAOD/PromptReco-v1/000/360/393/00000/0b4f9e93-a49f-4065-992c-fc955ffeceae.root',
                            '/store/data/Run2022F/EGamma/MINIAOD/PromptReco-v1/000/360/393/00000/24bf6866-b01b-4328-a8fe-07e7d5a7b0ca.root',
                            '/store/data/Run2022F/EGamma/MINIAOD/PromptReco-v1/000/360/393/00000/2ca0c6df-a61c-4df1-a17a-e617489cc990.root',
                            '/store/data/Run2022F/EGamma/MINIAOD/PromptReco-v1/000/360/393/00000/2cab50cd-2fd9-4df6-a7a8-87d6c6f44dfa.root',
                            '/store/data/Run2022F/EGamma/MINIAOD/PromptReco-v1/000/360/393/00000/3630a486-ce3b-4d3a-a7f2-2da92ae5b0fc.root',
                            '/store/data/Run2022F/EGamma/MINIAOD/PromptReco-v1/000/360/393/00000/3f852506-7b59-4aa1-8cee-bc7c2397af01.root',
                            '/store/data/Run2022F/EGamma/MINIAOD/PromptReco-v1/000/360/393/00000/5dd83845-f5c4-4283-a276-68847a5b1306.root',
                            '/store/data/Run2022F/EGamma/MINIAOD/PromptReco-v1/000/360/393/00000/5f79451d-1927-4873-9422-93c6f8c1ffe2.root',
                            '/store/data/Run2022F/EGamma/MINIAOD/PromptReco-v1/000/360/393/00000/605fc6f6-a108-439d-ba0d-54ab7682ff0e.root',
                            '/store/data/Run2022F/EGamma/MINIAOD/PromptReco-v1/000/360/393/00000/646be6f4-02a7-4b59-a257-d7dccf637093.root',
                            '/store/data/Run2022F/EGamma/MINIAOD/PromptReco-v1/000/360/393/00000/6f1dbd30-3e7e-4db9-a45c-aec0f3ccafea.root',
                            '/store/data/Run2022F/EGamma/MINIAOD/PromptReco-v1/000/360/393/00000/6f332799-9af8-48b6-a0e1-8ed9cb00a153.root',
                        ),
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
                                       fileName = cms.string('histos_METTrigAnalyzer.root')
                                   )

### analyzer configuration
process.metTrigAnalyzerMiniAOD = cms.EDAnalyzer("METTrigAnalyzerMiniAOD")
process.metTrigAnalyzerMiniAOD.refTriggerName = cms.untracked.string("HLT_Ele32_WPTight_Gsf_v17")
process.metTrigAnalyzerMiniAOD.sigTriggerNames= cms.untracked.vstring("HLT_PFMET120_PFMHT120_IDTight_v22", "HLT_PFMET130_PFMHT130_IDTight_v22", "HLT_PFMET140_PFMHT140_IDTight_v22",
                                                                      "HLT_PFMETTypeOne140_PFMHT140_IDTight_v13", "HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v22", "HLT_PFMETNoMu130_PFMHTNoMu130_IDTight_v21",
                                                                      "HLT_PFMETNoMu140_PFMHTNoMu140_IDTight_v21")
process.metTrigAnalyzerMiniAOD.verbose = cms.untracked.bool(False)

process.GlobalTag.globaltag = "124X_dataRun3_Prompt_v10"

# Path and EndPath definitions
process.HLTanalyzers = cms.Path(process.metTrigAnalyzerMiniAOD)
