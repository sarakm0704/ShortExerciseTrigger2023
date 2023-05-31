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
                        fileNames = cms.untracked.vstring('/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/439/00000/0b6eac11-e39f-4b55-8c18-f668bc5b175b.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/439/00000/1547ae07-0a63-4721-968e-bbaf8d35a246.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/439/00000/155bf187-ae18-48b5-93b6-2459c1c82399.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/439/00000/1c0502c4-4f4b-4235-b7e1-025401eb9d5b.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/439/00000/2d7bcbb0-459f-4652-86d5-cbaf8ee8e252.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/439/00000/3a94c905-97a0-4325-899e-4b9e1495798f.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/439/00000/3aae1d3a-78f4-4e75-9a02-14c7fdf63186.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/439/00000/40b15437-65b2-40c5-9c2e-4a09b0d38867.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/439/00000/42be7c7d-9fee-4048-9d1d-ad572affdabe.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/439/00000/4e39ddb1-9b35-4528-8ba1-6d5fa45b164b.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/439/00000/5d9fcbde-9d63-48dd-97b1-ef510fe59d03.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/439/00000/625ee365-dfb5-42a3-9c09-d2501f3867bf.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/439/00000/692b9ac0-d50c-4e7b-a416-9beac174ab02.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/439/00000/769da93d-0db0-4c6a-8ec4-0cd8bbcd5e6b.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/439/00000/7be9895f-81ed-4ff1-a6fe-2b32532bdd85.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/439/00000/7d00cc4c-5ae5-40d0-ac17-9352ad2ca776.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/439/00000/81ab6516-edac-4e78-bf83-389bd5f45305.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/439/00000/8371db4d-d5c0-4521-b48a-9d82aa16b4c6.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/439/00000/a09ff6ba-bd1d-4ae8-b38f-7745f10b1b9f.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/439/00000/ab849508-c986-41fc-8675-f2e8f9f89b9f.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/439/00000/ae6f12bb-0537-4ae6-a415-46481aa6e0a6.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/439/00000/b4c67738-323d-4922-b7a1-6a5faf72dadd.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/439/00000/c3e195a8-8f7b-43df-a472-535c329234fc.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/439/00000/e2549e9a-e550-4175-915d-69a99fcc304c.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/439/00000/e9568221-9eff-47b2-a7ba-af0da711eb58.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/452/00000/b6afffc2-ba04-4ad3-8067-b9f16e305475.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/457/00000/5d928684-733e-47da-9599-7abb9d47aef0.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/459/00000/30cf5f05-30f4-43e8-a12b-cfff77430202.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/503/00000/02d29d82-dfe5-4c2a-afc4-7ad80d79457d.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/587/00000/7daedf5a-c811-4fde-b4b5-5094968409c6.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/596/00000/2ca75f0f-03e8-43df-9942-734de4488dfa.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/597/00000/3452161e-1091-4c9e-ae34-9f40a012dd7f.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/597/00000/3dd66089-19f1-4bab-ba77-050865348fae.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/597/00000/7471d72b-13d3-47f8-953a-a51f1a4e65ff.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/597/00000/ed39623c-f193-4556-8020-99db038a4cf9.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/613/00000/443cd44d-2bee-40c3-a5ed-567944594515.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/614/00000/01aadb42-f144-406c-abda-3d5c749cee92.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/614/00000/ace83ef6-c735-4bd4-a3a8-58a8f0c59522.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/614/00000/d1e7ac24-9754-4866-9a8a-4ca47247eb08.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/614/00000/d31e5e2c-09bb-4104-9498-eabbbb4c5fef.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/614/00000/fea83857-0250-4ade-ad27-6969fd628fa6.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/615/00000/1a18c062-1a74-44b7-9965-d9757a192cab.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/615/00000/7ecaf7a6-4e3a-443a-82d9-dc710ddac2ae.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/615/00000/b6a394ab-f8b4-4727-8e29-34da2393aac5.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/615/00000/be26d2b5-c55c-490d-a618-12b62dd6534c.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/615/00000/fbac131a-3417-4c48-93e0-254d147bd746.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/616/00000/068e36b9-cbae-4c39-8fa8-3bca5c0e1bd4.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/616/00000/0e7aa5ba-bf9d-407b-a089-9d81dbac5d0a.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/616/00000/596ba03c-06c6-4df4-915e-1fde9cf31cc1.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/616/00000/749cbcce-085a-4729-be67-af714cffefa0.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/616/00000/769147ee-85c3-491d-a536-a7a083feb5ce.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/616/00000/83e56be6-7653-4199-8cf5-e615a8038c0a.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/616/00000/b119e8a1-ab35-4c8f-8cee-2101f126c219.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/616/00000/ef91e626-30f4-4975-86e4-435e6a9f04d0.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/616/00000/fac58b6e-4bc7-4f84-b5bb-63889cbb81b1.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/616/00000/fd787336-971a-4d4d-92dc-2f45aa216fef.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/617/00000/01c6836a-a837-44f6-b415-3a9581404465.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/617/00000/0968661f-6fae-44f9-8b31-4554b0eac5cf.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/617/00000/0f97f65f-6931-4c3f-87c4-aab1978425b9.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/617/00000/179299dd-96a8-44e6-a698-373717431af6.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/617/00000/722ab8fb-b165-4057-8a16-3f7cea587990.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/617/00000/ac2f9c6e-3045-4c0b-ac1c-66c35565c656.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/617/00000/d2ba58be-504e-4b0d-a697-3a12c0966826.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/618/00000/31ad253a-8f3a-4fbc-97e2-61c48302e4cd.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/618/00000/33afb960-6102-47b1-b158-e264d3eff7b4.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/618/00000/36328135-303d-4ce5-b943-c4f795c0ae1f.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/618/00000/693883be-56e8-43bb-b443-443d96308fe5.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/618/00000/de496da7-dda1-4515-b4f9-cb829f93ddb1.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/618/00000/f5723a96-b141-4247-8ef2-5d79839255c4.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/653/00000/34f54c2d-eb77-4f95-9707-7446804ff751.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/653/00000/3c649bc5-491f-43e0-8c29-fd147e021040.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/653/00000/41673b30-879c-47f3-a017-a79ea2631f93.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/653/00000/4960bfa2-b4fc-407f-87f6-c648bf3d62b9.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/653/00000/73789ccf-8547-477e-bafc-244fd66447a6.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/653/00000/9a6795ac-a913-46cc-87f8-f55a751278af.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/654/00000/09298e52-a86b-4351-9eae-46b59b18bfcb.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/655/00000/0cdcbce4-e42b-4155-8208-e82eabc2147d.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/655/00000/41062d6e-a9b3-4692-8850-35d3e3eeb1b2.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/655/00000/601081b4-343a-4f0a-b113-708acd59c81d.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/655/00000/71c7d67d-0a69-4865-8267-9641ade73cc0.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/655/00000/a5f768f5-e5e5-4ad0-aaa1-90a0e2e179f6.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/655/00000/b860eff5-0e49-41cd-89fd-923dfd560c27.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/655/00000/d0fce115-431b-4326-9a2f-690102d78644.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/655/00000/fbd26f23-67ef-4a52-a105-fa2fdadfef74.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/656/00000/9028a7ba-5ec6-4b53-87ed-47ff3bca2d50.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/657/00000/10a59677-a505-474e-bf53-1f98ab591094.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/657/00000/311dae3d-5141-48d4-b1cb-cb5b8187a7d6.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/657/00000/bcffefbb-7efd-401a-874e-0b370209b612.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/657/00000/cd493c42-fc54-44d0-b172-fa4de186e23a.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/657/00000/f965917c-c96b-470b-8ec7-40ea3a7981fc.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/673/00000/b64acf91-6912-4f62-b4ef-8505b16e4749.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/695/00000/2f177fab-ad3f-4a17-b00a-c58b56ac644d.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/695/00000/55e940ff-4122-41a1-b458-bc8cf7086b16.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/695/00000/77eeec26-bae6-42b9-bef5-7d1664834e75.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/695/00000/83f8bd20-43d3-4596-9271-4279551f4cd6.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/695/00000/8a27fcf4-e3ff-4b13-8686-a04504ded409.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/695/00000/9184d34a-c4fa-458c-ae89-ba100fd9143f.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/695/00000/9498cf58-e756-43c5-9899-96d9e61ea97c.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/695/00000/9809b82d-8b44-4eb5-b812-2513e58a2883.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/695/00000/ed394b4f-218d-4860-a593-7c67d57a219a.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/696/00000/0011576b-9b6b-4868-8f57-c0b13a24fdce.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/696/00000/0b253c13-fc2e-4674-9267-9a90fc0dcebd.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/696/00000/0bffe812-9556-4f7e-bef7-7c30ec27193f.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/696/00000/1566f0bf-6232-43e1-838f-7ed5fb94f366.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/696/00000/233d03b6-83d7-4bdf-a6ba-7ef75f37e900.root',
                                                          '/store/data/Run2022G/MuonEG/MINIAOD/PromptReco-v1/000/362/696/00000/2f8471bb-c7dd-48e8-b280-a2f6cd3a314f.root',
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

#process.GlobalTag.globaltag = "80X_dataRun2_2016SeptRepro_v3"
process.GlobalTag.globaltag = "124X_dataRun3_Prompt_v10"

# Path and EndPath definitions
process.HLTanalyzers = cms.Path(process.metTrigAnalyzerMiniAOD)
