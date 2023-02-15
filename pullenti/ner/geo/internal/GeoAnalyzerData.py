# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

from pullenti.ner.Referent import Referent
from pullenti.ner.core.AnalyzerDataWithOntology import AnalyzerDataWithOntology
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.geo.GeoReferent import GeoReferent

class GeoAnalyzerData(AnalyzerDataWithOntology):
    
    def __init__(self) -> None:
        super().__init__()
        self.all_regime = False
        self.tregime = False
        self.cregime = False
        self.oregime = False
        self.otregime = False
        self.sregime = False
        self.aregime = False
        self.check_regime = False
        self.tlevel = 0
        self.clevel = 0
        self.olevel = 0
        self.slevel = 0
        self.alevel = 0
        self.geo_before = 0
        self.step = 0
    
    def __str__(self) -> str:
        tmp = io.StringIO()
        if (self.all_regime): 
            print("AllRegime ", end="", file=tmp)
        if (self.tregime): 
            print("TRegime ", end="", file=tmp)
        if (self.cregime): 
            print("CRegime ", end="", file=tmp)
        if (self.oregime): 
            print("ORegime ", end="", file=tmp)
        if (self.otregime): 
            print("OTRegime ", end="", file=tmp)
        if (self.sregime): 
            print("SRegime ", end="", file=tmp)
        if (self.aregime): 
            print("ARegime ", end="", file=tmp)
        if (self.check_regime): 
            print("CheckRegime ", end="", file=tmp)
        if (self.tlevel > 0): 
            print("TLev={0} ".format(self.tlevel), end="", file=tmp, flush=True)
        if (self.clevel > 0): 
            print("CLev={0} ".format(self.clevel), end="", file=tmp, flush=True)
        if (self.olevel > 0): 
            print("OLev={0} ".format(self.olevel), end="", file=tmp, flush=True)
        if (self.slevel > 0): 
            print("SLev={0} ".format(self.slevel), end="", file=tmp, flush=True)
        if (self.alevel > 0): 
            print("ALev={0} ".format(self.alevel), end="", file=tmp, flush=True)
        print("{0} referents".format(len(self.referents)), end="", file=tmp, flush=True)
        return Utils.toStringStringIO(tmp)
    
    __ends = None
    
    def register_referent(self, referent : 'Referent') -> 'Referent':
        g = Utils.asObjectOrNull(referent, GeoReferent)
        if (g is not None): 
            if (g.is_state): 
                pass
            elif (g.is_region or ((g.is_city and not g.is_big_city))): 
                names = list()
                gen = MorphGender.UNDEFINED
                bas_nam = None
                for s in g.slots: 
                    if (s.type_name == GeoReferent.ATTR_NAME): 
                        names.append(Utils.asObjectOrNull(s.value, str))
                    elif (s.type_name == GeoReferent.ATTR_TYPE): 
                        typ = Utils.asObjectOrNull(s.value, str)
                        if (LanguageHelper.ends_with_ex(typ, "район", "край", "округ", "улус")): 
                            gen = (Utils.valToEnum((gen) | (MorphGender.MASCULINE), MorphGender))
                        elif (LanguageHelper.ends_with_ex(typ, "область", "территория", None, None)): 
                            gen = (Utils.valToEnum((gen) | (MorphGender.FEMINIE), MorphGender))
                i = 0
                first_pass2881 = True
                while True:
                    if first_pass2881: first_pass2881 = False
                    else: i += 1
                    if (not (i < len(names))): break
                    n = names[i]
                    ii = n.find(' ')
                    if (ii > 0): 
                        if (isinstance(g.get_slot_value(GeoReferent.ATTR_REF), Referent)): 
                            continue
                        nn = "{0} {1}".format(n[ii + 1:], n[0:0+ii])
                        if (not nn in names): 
                            names.append(nn)
                            g.add_slot(GeoReferent.ATTR_NAME, nn, False, 0)
                            continue
                        continue
                    for end in GeoAnalyzerData.__ends: 
                        if (LanguageHelper.ends_with(n, end)): 
                            nn = n[0:0+len(n) - 3]
                            for end2 in GeoAnalyzerData.__ends: 
                                if (end2 != end): 
                                    if (not nn + end2 in names): 
                                        names.append(nn + end2)
                                        g.add_slot(GeoReferent.ATTR_NAME, nn + end2, False, 0)
                            if (gen == MorphGender.MASCULINE): 
                                for na in names: 
                                    if (LanguageHelper.ends_with(na, "ИЙ")): 
                                        bas_nam = na
                            elif (gen == MorphGender.FEMINIE): 
                                for na in names: 
                                    if (LanguageHelper.ends_with(na, "АЯ")): 
                                        bas_nam = na
                            elif (gen == MorphGender.NEUTER): 
                                for na in names: 
                                    if (LanguageHelper.ends_with(na, "ОЕ")): 
                                        bas_nam = na
                            break
                if (bas_nam is not None and len(names) > 0 and names[0] != bas_nam): 
                    sl = g.find_slot(GeoReferent.ATTR_NAME, bas_nam, True)
                    if (sl is not None): 
                        g.slots.remove(sl)
                        g.slots.insert(0, sl)
        return super().register_referent(referent)
    
    # static constructor for class GeoAnalyzerData
    @staticmethod
    def _static_ctor():
        GeoAnalyzerData.__ends = ["КИЙ", "КОЕ", "КАЯ"]

GeoAnalyzerData._static_ctor()