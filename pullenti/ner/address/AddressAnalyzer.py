# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
import math
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import Stopwatch

from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.Referent import Referent
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.address.internal.AddressItemType import AddressItemType
from pullenti.ner.address.StreetKind import StreetKind
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.address.StreetReferent import StreetReferent
from pullenti.ner.address.internal.MetaStreet import MetaStreet
from pullenti.ner.address.internal.AddressDefineHelper import AddressDefineHelper
from pullenti.ner.address.internal.MetaAddress import MetaAddress
from pullenti.ner.core.internal.PullentiNerCoreInternalResourceHelper import PullentiNerCoreInternalResourceHelper
from pullenti.ner.address.internal.AddressItemToken import AddressItemToken
from pullenti.ner.address.AddressReferent import AddressReferent
from pullenti.ner.address.internal.StreetItemToken import StreetItemToken
from pullenti.ner.geo.GeoAnalyzer import GeoAnalyzer
from pullenti.ner.core.AnalyzerData import AnalyzerData
from pullenti.ner.Analyzer import Analyzer
from pullenti.ner.address.internal.StreetDefineHelper import StreetDefineHelper
from pullenti.ner.core.AnalyzerDataWithOntology import AnalyzerDataWithOntology

class AddressAnalyzer(Analyzer):
    """ Анализатор адресов """
    
    class AddressAnalyzerData(AnalyzerData):
        
        def __init__(self) -> None:
            from pullenti.ner.core.AnalyzerData import AnalyzerData
            from pullenti.ner.core.AnalyzerDataWithOntology import AnalyzerDataWithOntology
            super().__init__()
            self.__m_addresses = AnalyzerData()
            self.streets = AnalyzerDataWithOntology()
        
        def register_referent(self, referent : 'Referent') -> 'Referent':
            from pullenti.ner.address.StreetReferent import StreetReferent
            if (isinstance(referent, StreetReferent)): 
                referent._correct()
                return self.streets.register_referent(referent)
            else: 
                return self.__m_addresses.register_referent(referent)
        
        @property
        def referents(self) -> typing.List['Referent']:
            if (len(self.streets.referents) == 0): 
                return self.__m_addresses.referents
            elif (len(self.__m_addresses.referents) == 0): 
                return self.streets.referents
            res = list(self.streets.referents)
            res.extend(self.__m_addresses.referents)
            return res
    
    ANALYZER_NAME = "ADDRESS"
    """ Имя анализатора ("ADDRESS") """
    
    @property
    def name(self) -> str:
        return AddressAnalyzer.ANALYZER_NAME
    
    @property
    def caption(self) -> str:
        return "Адреса"
    
    @property
    def description(self) -> str:
        return "Адреса (улицы, дома ...)"
    
    def clone(self) -> 'Analyzer':
        return AddressAnalyzer()
    
    @property
    def type_system(self) -> typing.List['ReferentClass']:
        return [MetaAddress._global_meta, MetaStreet._global_meta]
    
    @property
    def images(self) -> typing.List[tuple]:
        res = dict()
        res[MetaAddress.ADDRESS_IMAGE_ID] = PullentiNerCoreInternalResourceHelper.get_bytes("address.png")
        res[MetaStreet.IMAGE_ID] = PullentiNerCoreInternalResourceHelper.get_bytes("street.png")
        res[MetaStreet.IMAGE_TERR_ORG_ID] = PullentiNerCoreInternalResourceHelper.get_bytes("terrorg.png")
        res[MetaStreet.IMAGE_TERR_SPEC_ID] = PullentiNerCoreInternalResourceHelper.get_bytes("terrspec.png")
        res[MetaStreet.IMAGE_TERR_ID] = PullentiNerCoreInternalResourceHelper.get_bytes("territory.png")
        return res
    
    @property
    def progress_weight(self) -> int:
        return 4
    
    def create_referent(self, type0_ : str) -> 'Referent':
        if (type0_ == AddressReferent.OBJ_TYPENAME): 
            return AddressReferent()
        if (type0_ == StreetReferent.OBJ_TYPENAME): 
            return StreetReferent()
        return None
    
    @property
    def used_extern_object_types(self) -> typing.List[str]:
        return [GeoReferent.OBJ_TYPENAME, "PHONE", "URI"]
    
    def create_analyzer_data(self) -> 'AnalyzerData':
        return AddressAnalyzer.AddressAnalyzerData()
    
    def process(self, kit : 'AnalysisKit') -> None:
        ad = Utils.asObjectOrNull(kit.get_analyzer_data(self), AddressAnalyzer.AddressAnalyzerData)
        gad = GeoAnalyzer._get_data(kit.first_token)
        if (gad is None): 
            return
        gad.all_regime = True
        steps = 1
        max0_ = steps
        delta = 100000
        parts = math.floor((((len(kit.sofa.text) + delta) - 1)) / delta)
        if (parts == 0): 
            parts = 1
        max0_ *= parts
        cur = 0
        next_pos = delta
        sw = Stopwatch()
        sw.reset()
        sw.start()
        t = kit.first_token
        first_pass2770 = True
        while True:
            if first_pass2770: first_pass2770 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.begin_char > next_pos): 
                next_pos += delta
                cur += 1
                if (not self._on_progress(cur, max0_, kit)): 
                    return
            li = AddressItemToken.try_parse_list(t, 20)
            if (li is None or len(li) == 0): 
                continue
            if ((len(li) == 1 and li[0].typ == AddressItemType.STREET and li[0].referent.kind == StreetKind.RAILWAY) and li[0].referent.number is None): 
                t = li[0].end_token
                continue
            tt = AddressDefineHelper.try_define(li, t, ad)
            if (tt is not None): 
                t = tt
        sw.stop()
        sli = list()
        t = kit.first_token
        first_pass2771 = True
        while True:
            if first_pass2771: first_pass2771 = False
            else: t = (None if t is None else t.next0_)
            if (not (t is not None)): break
            sr = Utils.asObjectOrNull(t.get_referent(), StreetReferent)
            if (sr is None): 
                continue
            if (t.next0_ is None or not t.next0_.is_comma_and): 
                continue
            sli.clear()
            sli.append(sr)
            t = t.next0_
            first_pass2772 = True
            while True:
                if first_pass2772: first_pass2772 = False
                else: t = t.next0_
                if (not (t is not None)): break
                if (t.is_comma_and): 
                    continue
                sr = Utils.asObjectOrNull(t.get_referent(), StreetReferent)
                if ((sr) is not None): 
                    sli.append(sr)
                    continue
                adr = Utils.asObjectOrNull(t.get_referent(), AddressReferent)
                if (adr is None): 
                    break
                if (len(adr.streets) == 0): 
                    break
                for ss in adr.streets: 
                    if (isinstance(ss, StreetReferent)): 
                        sli.append(Utils.asObjectOrNull(ss, StreetReferent))
            if (len(sli) < 2): 
                continue
            ok = True
            hi = None
            for s in sli: 
                if (len(s.geos) == 0): 
                    continue
                elif (len(s.geos) == 1): 
                    if (hi is None or hi == s.geos[0]): 
                        hi = s.geos[0]
                    else: 
                        ok = False
                        break
                else: 
                    ok = False
                    break
            if (ok and hi is not None): 
                for s in sli: 
                    if (len(s.geos) == 0): 
                        s.add_slot(StreetReferent.ATTR_GEO, hi, False, 0)
        for a in ad.referents: 
            if (isinstance(a, AddressReferent)): 
                a._correct()
        gad.all_regime = False
    
    def process_ontology_item(self, begin : 'Token') -> 'ReferentToken':
        li = StreetItemToken.try_parse_list(begin, 10, None)
        if (li is None or (len(li) < 2)): 
            return None
        rt = StreetDefineHelper._try_parse_street(li, True, False, False)
        if (rt is None): 
            return None
        street = Utils.asObjectOrNull(rt.referent, StreetReferent)
        t = rt.end_token.next0_
        first_pass2773 = True
        while True:
            if first_pass2773: first_pass2773 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (not t.is_char(';')): 
                continue
            t = t.next0_
            if (t is None): 
                break
            li = StreetItemToken.try_parse_list(begin, 10, None)
            rt1 = StreetDefineHelper._try_parse_street(li, True, False, False)
            if (rt1 is not None): 
                rt.end_token = rt1.end_token
                t = rt.end_token
                street.merge_slots(rt1.referent, True)
            else: 
                tt = None
                ttt = t
                while ttt is not None: 
                    if (ttt.is_char(';')): 
                        break
                    else: 
                        tt = ttt
                    ttt = ttt.next0_
                if (tt is not None): 
                    str0_ = MiscHelper.get_text_value(t, tt, GetTextAttr.NO)
                    if (str0_ is not None): 
                        street.add_slot(StreetReferent.ATTR_NAME, MiscHelper.convert_first_char_upper_and_other_lower(str0_), False, 0)
                    rt.end_token = tt
                    t = rt.end_token
        return ReferentToken(street, rt.begin_token, rt.end_token)
    
    M_INITIALIZED = False
    
    @staticmethod
    def initialize() -> None:
        if (AddressAnalyzer.M_INITIALIZED): 
            return
        AddressAnalyzer.M_INITIALIZED = True
        try: 
            AddressItemToken.initialize()
        except Exception as ex: 
            raise Utils.newException(ex.__str__(), ex)
        ProcessorService.register_analyzer(AddressAnalyzer())