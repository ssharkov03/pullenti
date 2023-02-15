# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru


from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.AnalyzerDataWithOntology import AnalyzerDataWithOntology
from pullenti.ner.org.OrganizationReferent import OrganizationReferent
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.ner.core.IntOntologyCollection import IntOntologyCollection

class OrgAnalyzerData(AnalyzerDataWithOntology):
    
    def __init__(self) -> None:
        super().__init__()
        self.loc_orgs = IntOntologyCollection()
        self.org_pure_names = TerminCollection()
        self.aliases = TerminCollection()
        self.large_text_regim = False
        self.tregime = False
        self.tlevel = 0
    
    def register_referent(self, referent : 'Referent') -> 'Referent':
        if (isinstance(referent, OrganizationReferent)): 
            referent._final_correction()
        slots = len(referent.slots)
        res = super().register_referent(referent)
        if (not self.large_text_regim and (isinstance(res, OrganizationReferent)) and ((res == referent))): 
            ioi = res.create_ontology_item_ex(2, True, False)
            if (ioi is not None): 
                self.loc_orgs.add_item(ioi)
            names = res._get_pure_names()
            if (names is not None): 
                for n in names: 
                    self.org_pure_names.add(Termin(n))
        return res