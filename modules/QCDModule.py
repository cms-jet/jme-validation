
from bamboo.plots import Plot, CutFlowReport
from bamboo.plots import EquidistantBinning as EqBin
from bamboo import treefunctions as op
from bamboo.analysisutils import forceDefine

import src.definitions as defs

from modules.baseModule import NanoBaseJME


class QCDModule(NanoBaseJME):
    """"""

    def __init__(self, args):
        super(QCDModule, self).__init__(args)

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

        ### dijet selection
        noLepton = noSel.refine("noLepton", cut=(
            op.AND(
                op.rng_len(muons) == 0,
                op.rng_len(clElectrons) ==0
            )))


        dijet = noLepton.refine("dijet", cut = (
            op.AND(
                op.rng_len(clak4Jets)>1,
                clak4Jets[0].pt > 50,
                op.deltaPhi(clak4Jets[0].p4,clak4Jets[1].p4)>2.7
            )))
        

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

        if "all" in sampleCfg['plot_level']:
            ### noSel
            plots+=cp.muonPlots(muons, noSel, "noSel")
            plots+=cp.electronPlots(electrons, noSel, "noSel")
            #CHS
            plots+=cp.AK4jetPlots(ak4Jets, noSel, "noSel")
            plots+=cp.AK4jetPlots(ak4JetsID, noSel, "noSelJetID")
            plots+=cp.AK4jetPlots(ak4Jetspt40, noSel, "noSelJetpt40")
            #PUPPI
            plots+=cp.AK4jetPlots(ak4PUPPIJets, noSel, "noSelPUPPI")
            plots+=cp.AK4jetPlots(ak4PUPPIJetsID, noSel, "noSelPUPPIJetID")
            plots+=cp.AK4jetPlots(ak4PUPPIJetspt40, noSel, "noSelPUPPIJetpt40")
            #ABC
            plots+=cp.AK4jetPlots(ak4ABCJets, noSel, "noSelABC")
            plots+=cp.AK4jetPlots(ak4ABCJetsID, noSel, "noSelABCJetID")
            plots+=cp.AK4jetPlots(ak4ABCJetspt40, noSel, "noSelABCJetpt40")
            
            plots+=cp.eventPlots(tree, noSel, "noSel")
            
            ### no leptons
            plots+=cp.muonPlots(muons, noLepton, "noLEpton")
            plots+=cp.electronPlots(electrons, noLepton, "noLepton")


            ### dijet
            plots+=cp.muonPlots(muons, dijet, "Dijet")
            plots+=cp.electronPlots(electrons, dijet, "Dijet")

        ### dijet
        #CHS
        plots+=cp.AK4jetPlots(ak4Jets, dijet, "Dijet")
        plots+=cp.AK4jetPlots(ak4JetsID, dijet, "DijetJetID")
        plots+=cp.AK4jetPlots(ak4Jetspt40, dijet, "DijetJetpt40")
        plots+=cp.AK4jetPlots(ak4Jetspt100, dijet, "DijetJetpt100")
        plots+=cp.AK4jetPlots(ak4Jetsetas2p4, dijet, "DijetJetetas2p4")
        plots+=cp.AK4jetPlots(ak4Jetsetag2p4, dijet, "DijetJetetag2p4")
        #PUPPI
        plots+=cp.AK4jetPlots(ak4PUPPIJets, dijet, "DijetPUPPI")
        plots+=cp.AK4jetPlots(ak4PUPPIJetsID, dijet, "DijetPUPPIJetID")
        plots+=cp.AK4jetPlots(ak4PUPPIJetspt40, dijet, "DijetPUPPIJetpt40")
        plots+=cp.AK4jetPlots(ak4PUPPIJetspt100, dijet, "DijetPUPPIJetpt100")
        plots+=cp.AK4jetPlots(ak4PUPPIJetsetas2p4, dijet, "DijetPUPPIJetetas2p4")
        plots+=cp.AK4jetPlots(ak4PUPPIJetsetag2p4, dijet, "DijetPUPPIJetetag2p4")
        #ABC
        plots+=cp.AK4jetPlots(ak4ABCJets, dijet, "DijetABC")
        plots+=cp.AK4jetPlots(ak4ABCJetsID, dijet, "DijetABCJetID")
        plots+=cp.AK4jetPlots(ak4ABCJetspt40, dijet, "DijetABCJetpt40")
        plots+=cp.AK4jetPlots(ak4ABCJetspt100, dijet, "DijetABCJetpt100")
        plots+=cp.AK4jetPlots(ak4ABCJetsetas2p4, dijet, "DijetABCJetetas2p4")
        plots+=cp.AK4jetPlots(ak4ABCJetsetag2p4, dijet, "DijetABCJetetag2p4")

        if sampleCfg['type'] == 'mc':
            #CHS
            plots+=cp.effPurityPlots(effjets,dijet,"effPurity_effmatched", tree)
            plots+=cp.effPurityPlots(recojetpt30,dijet,"effPurity_allrecojets",tree)
            plots+=cp.effPurityPlots(purityjets,dijet,"effPurity_puritymatched",tree)
            plots+=cp.effPurityPlots(pujets,dijet,"effPurity_pujets",tree)
            #PUPPI
            plots+=cp.effPurityPlots(effPUPPIjets,dijet,"effPurityPUPPI_effmatched", tree)
            plots+=cp.effPurityPlots(ak4PUPPIJets,dijet,"effPurityPUPPI_allrecojets",tree)
            plots+=cp.effPurityPlots(purityPUPPIjets,dijet,"effPurityPUPPI_puritymatched",tree)
            plots+=cp.effPurityPlots(puPUPPIjets,dijet,"effPurityPUPPI_pujets",tree)
            #ABC
            plots+=cp.effPurityPlots(effABCjets,dijet,"effPurityABC_effmatched", tree)
            plots+=cp.effPurityPlots(ak4ABCJets,dijet,"effPurityABC_allrecojets",tree)
            plots+=cp.effPurityPlots(purityABCjets,dijet,"effPurityABC_puritymatched",tree)
            plots+=cp.effPurityPlots(puABCjets,dijet,"effPurityABC_pujets",tree)

            if any([x in sampleCfg['plot_level'] for x in ["all","response"]]):
                #CHS
                plots+=cp.responsePlots(matchedjets, dijet, "dijet_response",tree)
                plots+=cp.responsePlots(matchedjets, noLepton, "noLepton_response",tree)
                plots+=cp.responsePlots(matchedjets, noSel, "noSel_response",tree)
                #PUPPI
                plots+=cp.responsePlots(matchedPUPPIjets, dijet, "dijetPUPPI_response",tree)
                plots+=cp.responsePlots(matchedPUPPIjets, noLepton, "noLeptonPUPPI_response",tree)
                plots+=cp.responsePlots(matchedPUPPIjets, noSel, "noSelPUPPI_response",tree)
                #ABC
                plots+=cp.responsePlots(matchedABCjets, dijet, "dijetABC_response",tree)
                plots+=cp.responsePlots(matchedABCjets, noLepton, "noLeptonABC_response",tree)
                plots+=cp.responsePlots(matchedABCjets, noSel, "noSelABC_response",tree)

        plots+=cp.eventPlots(tree, dijet, "Dijet")
        # Cutflow report
        yields.add(noLepton, 'no lepton')
        yields.add(dijet, 'dijet')
        return plots

