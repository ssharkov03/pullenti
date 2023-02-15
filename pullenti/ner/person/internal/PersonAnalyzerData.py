# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils

from pullenti.ner.core.ReferentsEqualType import ReferentsEqualType
from pullenti.ner.Referent import Referent
from pullenti.ner.core.AnalyzerData import AnalyzerData
from pullenti.ner.core.AnalyzerDataWithOntology import AnalyzerDataWithOntology
from pullenti.ner.person.PersonPropertyReferent import PersonPropertyReferent
from pullenti.ner.person.PersonReferent import PersonReferent
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.person.internal.PersonAttrToken import PersonAttrToken

class PersonAnalyzerData(AnalyzerDataWithOntology):
    
    def __init__(self) -> None:
        super().__init__()
        self.nominative_case_always = False
        self.text_starts_with_lastname_firstname_middlename = False
        self.need_second_step = False
        self.can_be_person_prop_begin_chars = dict()
        self.aregime = False
    
    def register_referent(self, referent : 'Referent') -> 'Referent':
        if (isinstance(referent, PersonReferent)): 
            exist_props = None
            i = 0
            first_pass2977 = True
            while True:
                if first_pass2977: first_pass2977 = False
                else: i += 1
                if (not (i < len(referent.slots))): break
                a = referent.slots[i]
                if (a.type_name == PersonReferent.ATTR_ATTR): 
                    pat = Utils.asObjectOrNull(a.value, PersonAttrToken)
                    if (pat is None or pat.prop_ref is None): 
                        if (isinstance(a.value, PersonPropertyReferent)): 
                            if (exist_props is None): 
                                exist_props = list()
                            exist_props.append(Utils.asObjectOrNull(a.value, PersonPropertyReferent))
                        continue
                    if (pat.prop_ref is not None): 
                        for ss in pat.prop_ref.slots: 
                            if (ss.type_name == PersonPropertyReferent.ATTR_REF): 
                                if (isinstance(ss.value, ReferentToken)): 
                                    if (ss.value.referent == referent): 
                                        pat.prop_ref.slots.remove(ss)
                                        break
                    if (exist_props is not None): 
                        for pp in exist_props: 
                            if (pp.can_be_equals(pat.prop_ref, ReferentsEqualType.WITHINONETEXT)): 
                                if (pat.prop_ref.can_be_general_for(pp)): 
                                    pat.prop_ref.merge_slots(pp, True)
                                    break
                    pat.data = (self)
                    pat.save_to_local_ontology()
                    if (pat.prop_ref is not None): 
                        if (referent.find_slot(a.type_name, pat.prop_ref, True) is not None): 
                            if (i >= 0 and (i < len(referent.slots))): 
                                del referent.slots[i]
                                i -= 1
                        else: 
                            referent.upload_slot(a, pat.referent)
        if (isinstance(referent, PersonPropertyReferent)): 
            i = 0
            first_pass2978 = True
            while True:
                if first_pass2978: first_pass2978 = False
                else: i += 1
                if (not (i < len(referent.slots))): break
                a = referent.slots[i]
                if (a.type_name == PersonPropertyReferent.ATTR_REF or a.type_name == PersonPropertyReferent.ATTR_HIGHER): 
                    pat = Utils.asObjectOrNull(a.value, ReferentToken)
                    if (pat is not None): 
                        pat.data = (self)
                        pat.save_to_local_ontology()
                        if (pat.referent is not None): 
                            referent.upload_slot(a, pat.referent)
                    elif (isinstance(a.value, PersonPropertyReferent)): 
                        if (a.value == referent): 
                            del referent.slots[i]
                            i -= 1
                            continue
                        referent.upload_slot(a, self.register_referent(Utils.asObjectOrNull(a.value, PersonPropertyReferent)))
        res = super().register_referent(referent)
        return res