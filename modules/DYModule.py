
from bamboo.plots import Plot, CutFlowReport
from bamboo.plots import EquidistantBinning as EqBin
from bamboo import treefunctions as op
from bamboo.analysisutils import forceDefine

import src.definitions as defs

from modules.baseModule import NanoBaseJME


class DYModule(NanoBaseJME):
    """"""

    def __init__(self, args):
        super(DYModule, self).__init__(args)

    def definePlots(self, tree, noSel, sample=None, sampleCfg=None):
        plots = []
        yields = CutFlowReport("yields", printInLog=True, recursive=True)
        plots.append(yields)
        yields.add(noSel, 'No Selection')


        # # AK8 Jets
        # ak8Jets = op.sort(
        #     op.select(tree.FatJet, lambda jet: defs.ak8jetDef(jet)), lambda jet: -jet.pt)

        # ak8JetsID = op.sort(
        #     ak8Jets, lambda jet: jet.jetId & 2)


        muons, electrons, clElectrons, ak4Jets, clak4Jets, ak4JetsID, ak4Jetspt40, ak4Jetspt100, ak4Jetsetas2p4, ak4Jetsetag2p4, ak4PUPPIJets, clak4PUPPIJets, ak4PUPPIJetsID, ak4PUPPIJetspt40, ak4PUPPIJetspt100, ak4PUPPIJetsetas2p4, ak4PUPPIJetsetag2p4, ak4ABCJets, clak4ABCJets, ak4ABCJetsID, ak4ABCJetspt40, ak4ABCJetspt100, ak4ABCJetsetas2p4, ak4ABCJetsetag2p4 = defs.defineObjects(tree)

        # ak4bJets = op.select(
        #     ak4Jets, lambda jet: jet.btagDeepB > 0.2770)  # 2018 WP

        ### Di-leptonic channel ###

        # 2 muon and 2 electron selection
        hasTwoSFLeptons = noSel.refine('hasTwoSFLeptons', cut=(
            op.OR(
                op.AND(op.rng_len(muons) == 2, op.rng_len(clElectrons) ==0, 
                       muons[0].charge != muons[1].charge, 
                       muons[0].pt > 25., muons[1].pt > 15.),
                op.AND(op.rng_len(clElectrons) == 2, op.rng_len(muons) ==0,
                       clElectrons[0].charge != clElectrons[1].charge, 
                       clElectrons[0].pt > 25., clElectrons[1].pt > 15. )
            )
        ))



        # lepton channels
        # eePair = op.combine(clElectrons, N=2, pred=lambda el1,
        #                     el2: el1.charge != el2.charge)
        # mumuPair = op.combine(muons, N=2, pred=lambda mu1,
        #                       mu2: mu1.charge != mu2.charge)


        ### reconstruct Z boson
        Zboson = op.multiSwitch(
            (op.rng_len(muons)>0,op.sum(muons[0].p4,muons[1].p4)),
            (op.rng_len(clElectrons)>0,op.sum(clElectrons[0].p4,clElectrons[1].p4)),
            op.withMass(muons[0].p4,0)
        )

        ### Z mass selection
        Zmasscut = hasTwoSFLeptons.refine("Zmasscut", cut = (
                op.AND(Zboson.M() > 80, Zboson.M() < 100)
        ))


        #### deltaphi selection on jets

        if sampleCfg['type'] == 'mc':
            #### efficiency and purity
            ### efficiency match to generator jets with deltaR<0.2 and pT gen >30, pt reco > 20
            recojetpt30 = op.select(ak4Jets, lambda jet: jet.pt > 30)
            recojetpt20 = op.select(ak4Jets, lambda jet: jet.pt > 20)
            
            recoPUPPIjetpt30 = op.select(ak4PUPPIJets, lambda jet: jet.pt > 30)
            recoPUPPIjetpt20 = op.select(ak4PUPPIJets, lambda jet: jet.pt > 20)
            
            recoABCjetpt30 = op.select(ak4ABCJets, lambda jet: jet.pt > 30)
            recoABCjetpt20 = op.select(ak4ABCJets, lambda jet: jet.pt > 20)
            
            # firstgenjet = tree.Jet[0].chHEF
            
            effjets = defs.effjets(recojetpt20) #USING NEITHER CLEANED NOR ID JETS IN EFF/PUR/PU JETS. IS THIS INTENDED?
            effPUPPIjets = defs.effjets(recoPUPPIjetpt20)
            effABCjets = defs.effjets(recoABCjetpt20)
            
            purityjets = defs.purityjets(recojetpt30)
            purityPUPPIjets = defs.purityjets(recoPUPPIjetpt30)
            purityABCjets = defs.purityjets(recoABCjetpt30)
            
            pujets = defs.pujets(ak4Jets)
            puPUPPIjets = defs.pujets(ak4PUPPIJets)
            puABCjets = defs.pujets(ak4ABCJets)
            
            matchedjets = defs.matchedjets(tree.Jet)
            matchedPUPPIjets = defs.matchedjets(tree.JetPuppi)
            matchedABCjets = defs.matchedjets(tree.JetABC)

        #############################################################################
        #                                 Plots                                     #
        #############################################################################
        import src.controlPlots as cp

        ### noSel
        plots+=cp.muonPlots(muons, noSel, "noSel")
        plots+=cp.electronPlots(electrons, noSel, "noSel")
        #CHS
        plots+=cp.AK4jetPlots(ak4Jets, noSel, "noSel")
        plots+=cp.AK4jetPlots(ak4JetsID, noSel, "noSelJetID")
        plots+=cp.AK4jetPlots(ak4Jetspt40, noSel, "noSelJetpt40")
        plots+=cp.eventPlots(tree, noSel, "noSel")
        #PUPPI
        plots+=cp.AK4jetPlots(ak4PUPPIJets, noSel, "noSelPUPPI")
        plots+=cp.AK4jetPlots(ak4PUPPIJetsID, noSel, "noSelPUPPIJetID")
        plots+=cp.AK4jetPlots(ak4PUPPIJetspt40, noSel, "noSelPUPPIJetpt40")
        #ABC
        plots+=cp.AK4jetPlots(ak4ABCJets, noSel, "noSelABC")
        plots+=cp.AK4jetPlots(ak4ABCJetsID, noSel, "noSelABCJetID")
        plots+=cp.AK4jetPlots(ak4ABCJetspt40, noSel, "noSelABCJetpt40")
        
        ### two leptons
        plots+=cp.muonPlots(muons, hasTwoSFLeptons, "hasTwoSFLeptons")
        plots+=cp.electronPlots(electrons, hasTwoSFLeptons, "hasTwoSFLeptons")
        plots+=cp.ZbosonPlots(Zboson, hasTwoSFLeptons, "hasTwoSFLeptons")

        ### zmass cut
        plots+=cp.muonPlots(muons, Zmasscut, "Zmasscut")
        plots+=cp.electronPlots(electrons, Zmasscut, "Zmasscut")
        plots+=cp.ZbosonPlots(Zboson, Zmasscut, "Zmasscut")
        #CHS
        plots+=cp.AK4jetPlots(ak4Jets, Zmasscut, "Zmasscut")
        plots+=cp.AK4jetPlots(ak4JetsID, Zmasscut, "ZmasscutJetID")
        plots+=cp.AK4jetPlots(ak4Jetspt40, Zmasscut, "ZmasscutJetpt40")
        plots+=cp.AK4jetPlots(ak4Jetspt100, Zmasscut, "ZmasscutJetpt100")
        plots+=cp.AK4jetPlots(ak4Jetsetas2p4, Zmasscut, "ZmasscutJetetas2p4")
        plots+=cp.AK4jetPlots(ak4Jetsetag2p4, Zmasscut, "ZmasscutJetetag2p4")
        #PUPPI
        plots+=cp.AK4jetPlots(ak4PUPPIJets, Zmasscut, "ZmasscutPUPPI")
        plots+=cp.AK4jetPlots(ak4PUPPIJetsID, Zmasscut, "ZmasscutPUPPIJetID")
        plots+=cp.AK4jetPlots(ak4PUPPIJetspt40, Zmasscut, "ZmasscutPUPPIJetpt40")
        plots+=cp.AK4jetPlots(ak4PUPPIJetspt100, Zmasscut, "ZmasscutPUPPIJetpt100")
        plots+=cp.AK4jetPlots(ak4PUPPIJetsetas2p4, Zmasscut, "ZmasscutPUPPIJetetas2p4")
        plots+=cp.AK4jetPlots(ak4PUPPIJetsetag2p4, Zmasscut, "ZmasscutPUPPIJetetag2p4")
        #ABC
        plots+=cp.AK4jetPlots(ak4ABCJets, Zmasscut, "ZmasscutABC")
        plots+=cp.AK4jetPlots(ak4ABCJetsID, Zmasscut, "ZmasscutABCJetID")
        plots+=cp.AK4jetPlots(ak4ABCJetspt40, Zmasscut, "ZmasscutABCJetpt40")
        plots+=cp.AK4jetPlots(ak4ABCJetspt100, Zmasscut, "ZmasscutABCJetpt100")
        plots+=cp.AK4jetPlots(ak4ABCJetsetas2p4, Zmasscut, "ZmasscutABCJetetas2p4")
        plots+=cp.AK4jetPlots(ak4ABCJetsetag2p4, Zmasscut, "ZmasscutABCJetetag2p4")
        
        if sampleCfg['type'] == 'mc':
            #CHS
            plots+=cp.effPurityPlots(effjets,Zmasscut,"effPurity_effmatched", tree)
            plots+=cp.effPurityPlots(recojetpt30,Zmasscut,"effPurity_allrecojets",tree)
            plots+=cp.effPurityPlots(purityjets,Zmasscut,"effPurity_puritymatched",tree)
            plots+=cp.effPurityPlots(pujets,Zmasscut,"effPurity_pujets",tree)
            #PUPPI
            plots+=cp.effPurityPlots(effPUPPIjets,Zmasscut,"effPurityPUPPI_effmatched", tree)
            plots+=cp.effPurityPlots(ak4PUPPIJets,Zmasscut,"effPurityPUPPI_allrecojets",tree)
            plots+=cp.effPurityPlots(purityPUPPIjets,Zmasscut,"effPurityPUPPI_puritymatched",tree)
            plots+=cp.effPurityPlots(puPUPPIjets,Zmasscut,"effPurityPUPPI_pujets",tree)
            #ABC
            plots+=cp.effPurityPlots(effABCjets,Zmasscut,"effPurityABC_effmatched", tree)
            plots+=cp.effPurityPlots(ak4ABCJets,Zmasscut,"effPurityABC_allrecojets",tree)
            plots+=cp.effPurityPlots(purityABCjets,Zmasscut,"effPurityABC_puritymatched",tree)
            plots+=cp.effPurityPlots(puABCjets,Zmasscut,"effPurityABC_pujets",tree)

            #CHS
            plots+=cp.responsePlots(matchedjets, Zmasscut, "Zmasscut_response",tree)
            # plots+=cp.responsePlots(matchedjets, noLepton, "noLepton_response",tree)
            plots+=cp.responsePlots(matchedjets, noSel, "hasTwoSFLeptons_response",tree)
            #PUPPI
            plots+=cp.responsePlots(matchedPUPPIjets, Zmasscut, "ZmasscutPUPPI_response",tree)
            # plots+=cp.responsePlots(matchedjets, noLepton, "noLepton_response",tree)
            plots+=cp.responsePlots(matchedPUPPIjets, noSel, "hasTwoSFLeptonsPUPPI_response",tree)
            #ABC
            plots+=cp.responsePlots(matchedABCjets, Zmasscut, "ZmasscutABC_response",tree)
            # plots+=cp.responsePlots(matchedjets, noLepton, "noLepton_response",tree)
            plots+=cp.responsePlots(matchedABCjets, noSel, "hasTwoSFLeptonsABC_response",tree)

            #CHS
            plots+=cp.AK4jetPlots(pujets, Zmasscut, "ZmasscutPuJets")
            plots+=cp.AK4jetPlots(matchedjets, Zmasscut, "ZmasscutMatchedJets")
            #PUPPI
            plots+=cp.AK4jetPlots(puPUPPIjets, Zmasscut, "ZmasscutPuPUPPIJets")
            plots+=cp.AK4jetPlots(matchedPUPPIjets, Zmasscut, "ZmasscutMatchedPUPPIJets")
            #ABC
            plots+=cp.AK4jetPlots(puABCjets, Zmasscut, "ZmasscutPuABCJets")
            plots+=cp.AK4jetPlots(matchedABCjets, Zmasscut, "ZmasscutMatchedABCJets")
            

        plots+=cp.eventPlots(tree, Zmasscut, "Zmasscut")
        # Cutflow report
        yields.add(hasTwoSFLeptons, 'two lepton')
        yields.add(Zmasscut, 'zmass cut')
        return plots
