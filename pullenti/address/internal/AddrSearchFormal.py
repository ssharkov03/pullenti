# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import typing
from pullenti.unisharp.Utils import Utils

from pullenti.ner.geo.internal.TerrItemToken import TerrItemToken
from pullenti.address.internal.SearchLevel import SearchLevel
from pullenti.ner.TextToken import TextToken
from pullenti.address.internal.gar.AddrTyp import AddrTyp
from pullenti.address.internal.SearchAddressItem import SearchAddressItem
from pullenti.ner.address.internal.StreetItemType import StreetItemType
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.SourceOfAnalysis import SourceOfAnalysis
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.address.internal.StreetItemToken import StreetItemToken
from pullenti.ner.geo.internal.CityItemToken import CityItemToken
from pullenti.ner.fias.FiasAnalyzer import FiasAnalyzer

class AddrSearchFormal:
    
    def __str__(self) -> str:
        res = io.StringIO()
        if (self.typ is not None): 
            print("{0} ".format(self.typ), end="", file=res, flush=True)
        for w in self.words: 
            print("{0} ".format(w), end="", file=res, flush=True)
        return Utils.toStringStringIO(res).strip()
    
    def __init__(self, src_ : 'SearchAddressItem') -> None:
        self.src = None;
        self.typ = None;
        self.words = list()
        self.reg_id = 0
        self.src = src_
        ar = ProcessorService.get_empty_processor().process(SourceOfAnalysis(src_.text), None, None)
        if (ar is None): 
            return
        if (FiasAnalyzer.FIAS_DB is None): 
            return
        t = ar.first_token
        first_pass2717 = True
        while True:
            if first_pass2717: first_pass2717 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (isinstance(t, NumberToken)): 
                self.words.append(t.value)
                continue
            sit = StreetItemToken.try_parse(t, None, True, None)
            if (sit is not None and ((sit.typ == StreetItemType.STDADJECTIVE or sit.typ == StreetItemType.STDPARTOFNAME)) and sit.termin is not None): 
                self.words.append(sit.termin.canonic_text[0:0+1])
                t = sit.end_token
                continue
            if (self.typ is None): 
                if (sit is not None and sit.typ == StreetItemType.NOUN): 
                    self.typ = FiasAnalyzer.FIAS_DB.find_addr_type(sit.termin.canonic_text.lower())
                    if ((self.typ) is not None): 
                        if (((self.typ.name == "улица" or self.typ.name == "переулок" or self.typ.name == "проезд") or self.typ.name == "проспект" or self.typ.name == "тупик") or self.typ.name == "шоссе"): 
                            t = sit.end_token
                            continue
                        self.typ = (None)
                cit = CityItemToken.try_parse(t, None, False, None)
                if (cit is not None and cit.typ == CityItemToken.ItemType.NOUN): 
                    self.typ = FiasAnalyzer.FIAS_DB.find_addr_type(cit.value.lower())
                    if ((self.typ) is not None): 
                        t = cit.end_token
                        continue
                ter = TerrItemToken.try_parse(t, None, None)
                if (ter is not None and ter.termin_item is not None): 
                    self.typ = FiasAnalyzer.FIAS_DB.find_addr_type(ter.termin_item.canonic_text.lower())
                    if ((self.typ) is not None): 
                        t = ter.end_token
                        continue
            if ((isinstance(t, TextToken)) and t.length_char > 2): 
                self.words.append(t.term)
        if (len(self.words) > 1 and ((str.isdigit(self.words[0][0]) or len(self.words[0]) == 1))): 
            n = self.words[0]
            del self.words[0]
            self.words.append(n)
    
    def check(self, ao : 'AddressObject', lite : bool) -> bool:
        if (len(self.words) == 1): 
            if (ao.names[0].find(' ') > 0 or ao.names[0].find('.') > 0): 
                if (lite): 
                    pass
                else: 
                    return False
            return True
        for n in ao.names: 
            frm = AddrSearchFormal(SearchAddressItem._new90(n))
            if (len(frm.words) != len(self.words)): 
                continue
            i = 0
            i = 0
            while i < len(self.words): 
                eq = False
                for ww in frm.words: 
                    if (str.isdigit(ww[0])): 
                        if (ww == self.words[i]): 
                            eq = True
                            break
                    elif (ww.startswith(self.words[i]) or self.words[i].startswith(ww)): 
                        eq = True
                        break
                if (not eq): 
                    break
                i += 1
            if (i >= len(self.words)): 
                return True
        return False
    
    def search(self) -> typing.List['AddrInfo']:
        if (len(self.words) == 0): 
            return list()
        res = FiasAnalyzer.FIAS_DB.get_all_string_entries_by_start(self.words[0], self.reg_id)
        if (len(self.words) > 1 and len(res) == 0): 
            res2 = FiasAnalyzer.FIAS_DB.get_all_string_entries_by_start(self.words[1], self.reg_id)
            if (len(res) == 0): 
                res = res2
            elif (len(res2) > 0): 
                hash0_ = dict()
                for r in res2: 
                    if (not r.id0_ in hash0_): 
                        hash0_[r.id0_] = True
                res3 = list()
                for i in range(len(res) - 1, -1, -1):
                    if (res[i].id0_ in hash0_): 
                        res3.append(res[i])
                res = res3
        for i in range(len(res) - 1, -1, -1):
            if (self.typ is not None): 
                if (res[i].typ_id != self.typ.id0_): 
                    del res[i]
                continue
            ty = FiasAnalyzer.FIAS_DB.get_addr_type(res[i].typ_id)
            if (ty is None): 
                continue
            if (self.src.level == SearchLevel.STREET): 
                if (ty.typ != AddrTyp.Typs.STREET and ty.typ != AddrTyp.Typs.ORG): 
                    del res[i]
            elif ((self.src.level == SearchLevel.CITY and ty.typ != AddrTyp.Typs.CITY and ty.typ != AddrTyp.Typs.VILLAGE) and ty.typ != AddrTyp.Typs.ORG): 
                del res[i]
            elif (ty.typ == AddrTyp.Typs.STREET or ty.typ == AddrTyp.Typs.ORG): 
                del res[i]
            elif (ty.typ == AddrTyp.Typs.VILLAGE and self.src.level != SearchLevel.CITY): 
                del res[i]
        return res