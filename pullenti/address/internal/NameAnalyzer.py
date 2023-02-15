# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
from pullenti.unisharp.Utils import Utils

from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.ReferentsEqualType import ReferentsEqualType
from pullenti.ner.Referent import Referent
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.address.StreetReferent import StreetReferent
from pullenti.address.internal.gar.AddressObjectStatus import AddressObjectStatus
from pullenti.ner.address.internal.StreetItemToken import StreetItemToken
from pullenti.ner.address.internal.StreetDefineHelper import StreetDefineHelper
from pullenti.ner.SourceOfAnalysis import SourceOfAnalysis
from pullenti.address.internal.FiasHelper import FiasHelper
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.org.OrganizationReferent import OrganizationReferent

class NameAnalyzer:
    
    def __init__(self) -> None:
        self.typ = None;
        self.names = None;
        self.res = AddressObjectStatus.ERROR
        self.ref = None;
        self.entry_strings = None;
        self.sec = None;
    
    def process(self, names_ : typing.List[str], typ_ : str, km_parent : str=None) -> None:
        self.typ = typ_
        self.names = names_
        self.entry_strings = (None)
        self.res = AddressObjectStatus.ERROR
        self.ref = (None)
        if (typ_ == "чувашия"): 
            typ_ = "республика"
            names_[0] = "Чувашская Республика"
        best_coef = 10000
        best_ref = None
        best_ref2 = None
        nn = 0
        while nn < len(names_): 
            name = FiasHelper.correct_fias_name(names_[nn])
            jj = nn + 1
            while jj < len(names_): 
                if (names_[jj] == name): 
                    del names_[jj]
                    jj -= 1
                jj += 1
            if ("Капотня" in name): 
                pass
            if (name.find('/') > 0): 
                ar = ProcessorService.get_empty_processor().process(SourceOfAnalysis._new118(name, "ADDRESS"), None, None)
                t = ar.first_token
                first_pass2724 = True
                while True:
                    if first_pass2724: first_pass2724 = False
                    else: t = t.next0_
                    if (not (t is not None)): break
                    if (t.is_char('/')): 
                        if (not (isinstance(t.previous, TextToken)) or not (isinstance(t.next0_, TextToken))): 
                            continue
                        if ((t.end_char + 5) > len(name)): 
                            break
                        if (t.begin_char < 10): 
                            break
                        if (not t.chars.is_capital_upper): 
                            break
                        n1 = name[0:0+t.begin_char].strip()
                        n2 = name[t.begin_char + 1:].strip()
                        names_[nn] = n1
                        name = names_[nn]
                        names_.insert(nn + 1, n2)
                        break
            name = NameAnalyzer.__corr_name(name)
            if (typ_ == "муниципальный округ"): 
                if (name.startswith("поселение ")): 
                    name = name[10:].strip()
            if ("Олимп.дер" in name): 
                name = "улица Олимпийская Деревня"
            elif (Utils.compareStrings("ЛЕНИНСКИЕ ГОРЫ", name, True) == 0): 
                name = ("улица " + name)
            for k in range(1):
                if (k > 0 and Utils.isNullOrEmpty(typ_)): 
                    continue
                txt = (name if Utils.isNullOrEmpty(typ_) else (("{0} \"{1}\"".format(typ_, name) if k == 1 else "{0} {1}".format(typ_, name))))
                if (Utils.compareStrings(Utils.ifNotNull(typ_, ""), "километр", True) == 0 and (len(name) < 6)): 
                    txt = "{0} {1}".format(name, typ_)
                txt0 = txt
                txt = ("Москва, " + txt)
                if ("километр" in txt): 
                    pass
                if (km_parent is not None and (len(name) < 6)): 
                    txt = "{0} {1}".format(txt, km_parent)
                ar = ProcessorService.get_standard_processor().process(SourceOfAnalysis._new118(txt, "ADDRESS"), None, None)
                r = None
                if (ar is None): 
                    continue
                for ii in range(len(ar.entities) - 1, -1, -1):
                    if (isinstance(ar.entities[ii], GeoReferent)): 
                        geo = Utils.asObjectOrNull(ar.entities[ii], GeoReferent)
                        if (geo.find_slot("NAME", "МОСКВА", True) is not None): 
                            if (Utils.compareStrings("МОСКВА", name, True) == 0): 
                                pass
                            else: 
                                continue
                        if (len(geo.occurrence) == 0 or geo.occurrence[0].begin_char > 8): 
                            continue
                        r = (geo)
                        break
                    elif (isinstance(ar.entities[ii], StreetReferent)): 
                        r = ar.entities[ii]
                        break
                    elif (isinstance(ar.entities[ii], OrganizationReferent)): 
                        r = ar.entities[ii]
                        if (ii > 0 and (((isinstance(ar.entities[ii - 1], GeoReferent)) or (isinstance(ar.entities[ii - 1], StreetReferent)))) and ar.entities[ii - 1].find_slot(None, r, True) is not None): 
                            r = ar.entities[ii - 1]
                        elif (ii > 1 and (((isinstance(ar.entities[ii - 2], GeoReferent)) or (isinstance(ar.entities[ii - 2], StreetReferent)))) and ar.entities[ii - 2].find_slot(None, r, True) is not None): 
                            r = ar.entities[ii - 2]
                        elif (ii > 0 and (isinstance(ar.entities[ii - 1], StreetReferent))): 
                            r = ar.entities[ii - 1]
                        break
                    else: 
                        pass
                co = 0
                if (r is None): 
                    if ((name.find(' ') < 0) and (name.find('.') < 0) and Utils.isNullOrEmpty(typ_)): 
                        r = (StreetReferent())
                        r.add_slot(StreetReferent.ATTR_NAME, name.upper(), False, 0)
                        r.add_slot(StreetReferent.ATTR_TYPE, "улица", False, 0)
                        co = 10
                    else: 
                        ar1 = ProcessorService.get_standard_processor().process(SourceOfAnalysis(txt0), None, None)
                        if (ar1 is not None and ar1.first_token is not None): 
                            if ("линия" in txt0): 
                                pass
                            strs = StreetItemToken.try_parse_list(ar1.first_token, 10, None)
                            rt = StreetDefineHelper.try_parse_ext_street(strs)
                            if (rt is not None and rt.end_token.next0_ is None): 
                                txt = txt0
                                r = rt.referent
                        if (r is None): 
                            continue
                else: 
                    if (r.occurrence[0].begin_char > 8): 
                        co += (r.occurrence[0].begin_char - 8)
                    if (r.occurrence[0].end_char < (len(txt) - 1)): 
                        co += (len(txt) - 1 - r.occurrence[0].end_char)
                if (co < best_coef): 
                    best_coef = co
                    best_ref = r
                    best_ref2 = (None)
                    if (best_coef == 0): 
                        break
                elif (co == best_coef): 
                    if (best_ref2 is None): 
                        best_ref2 = r
                    elif (best_ref2.can_be_equals(best_ref, ReferentsEqualType.WITHINONETEXT)): 
                        best_ref2 = r
            if (best_ref is not None): 
                self.ref = best_ref
                if (best_coef > 0): 
                    self.res = AddressObjectStatus.WARNING
                else: 
                    self.res = AddressObjectStatus.OK
                sec_ref = None
                if (isinstance(self.ref, StreetReferent)): 
                    str0_ = Utils.asObjectOrNull(self.ref, StreetReferent)
                    if (str0_.higher is not None): 
                        sec_ref = (str0_.higher)
                    else: 
                        geo = Utils.asObjectOrNull(str0_.get_slot_value("GEO"), GeoReferent)
                        if (geo is not None and geo.find_slot("NAME", "Москва", True) is None): 
                            sec_ref = (geo)
                if (sec_ref is not None): 
                    self.sec = NameAnalyzer()
                    self.sec.ref = self.ref
                    self.ref = sec_ref
                    self.entry_strings = FiasHelper._get_strings(self.ref)
                    self.sec.entry_strings = FiasHelper._get_strings(self.sec.ref)
                    self.sec.typ = self.sec.ref.get_string_value("TYP")
                else: 
                    self.entry_strings = FiasHelper._get_strings(self.ref)
                    if (best_ref2 is not None): 
                        strs2 = FiasHelper._get_strings(best_ref2)
                        if (strs2 is not None): 
                            for s in strs2: 
                                if (not s in self.entry_strings): 
                                    self.entry_strings.append(s)
            elif (typ_ == "километр" and str.isdigit(self.names[0][0])): 
                self.entry_strings = list()
                i = 0
                i = 0
                while i < len(self.names[0]): 
                    if (not str.isdigit(self.names[0][i])): 
                        break
                    i += 1
                self.entry_strings.append(self.names[0][0:0+i] + "км")
                self.res = AddressObjectStatus.OK
            nn += 1
    
    @staticmethod
    def __corr_name(name : str) -> str:
        jj = name.find('(')
        if (jj > 0): 
            name = name[0:0+jj].strip()
        if (str.isdigit(name[len(name) - 1])): 
            name += "-й"
        return name