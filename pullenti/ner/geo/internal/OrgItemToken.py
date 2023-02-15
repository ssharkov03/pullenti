# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.core.Termin import Termin
from pullenti.ner.address.internal.StreetItemType import StreetItemType
from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.morph.MorphClass import MorphClass
from pullenti.ner.geo.internal.GeoTokenData import GeoTokenData
from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.geo.internal.MiscLocationHelper import MiscLocationHelper
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.geo.internal.NameTokenType import NameTokenType
from pullenti.ner.address.internal.AddressItemToken import AddressItemToken
from pullenti.ner.address.internal.StreetItemToken import StreetItemToken
from pullenti.ner.geo.GeoAnalyzer import GeoAnalyzer

class OrgItemToken(ReferentToken):
    
    def __init__(self, r : 'Referent', b : 'Token', e0_ : 'Token') -> None:
        super().__init__(r, b, e0_, None)
        self.is_doubt = False
        self.has_terr_keyword = False
        self.keyword_after = False
        self.is_gsk = False
        self.is_massive = False
    
    def set_gsk(self) -> None:
        self.is_gsk = False
        if (self.is_massive): 
            self.is_gsk = True
            return
        for s in self.referent.slots: 
            if (s.type_name == "TYPE" and (isinstance(s.value, str))): 
                ty = Utils.asObjectOrNull(s.value, str)
                if ((((("товарищество" in ty or "кооператив" in ty or "коллектив" in ty) or LanguageHelper.ends_with_ex(ty, "поселок", " отдыха", " часть", "хозяйство") or "партнерство" in ty) or "объединение" in ty or "бизнес" in ty) or (("станция" in ty and not "заправоч" in ty)) or "аэропорт" in ty) or "пансионат" in ty or "санаторий" in ty): 
                    self.is_gsk = True
                    return
                if (ty == "АОЗТ"): 
                    self.is_gsk = True
                    return
            elif (s.type_name == "NAME" and (isinstance(s.value, str))): 
                nam = Utils.asObjectOrNull(s.value, str)
                if (LanguageHelper.ends_with_ex(nam, "ГЭС", "АЭС", "ТЭС", None)): 
                    self.is_gsk = True
                    return
    
    def __str__(self) -> str:
        tmp = io.StringIO()
        if (self.is_doubt): 
            print("? ", end="", file=tmp)
        if (self.has_terr_keyword): 
            print("Terr ", end="", file=tmp)
        if (self.is_gsk): 
            print("Gsk ", end="", file=tmp)
        if (self.is_massive): 
            print("Massive ", end="", file=tmp)
        print(str(self.referent), end="", file=tmp)
        return Utils.toStringStringIO(tmp)
    
    SPEED_REGIME = False
    
    @staticmethod
    def _prepare_all_data(t0 : 'Token') -> None:
        if (not OrgItemToken.SPEED_REGIME): 
            return
        ad = GeoAnalyzer._get_data(t0)
        if (ad is None): 
            return
        ad.oregime = False
        t = t0
        while t is not None: 
            d = Utils.asObjectOrNull(t.tag, GeoTokenData)
            org0_ = OrgItemToken.try_parse(t, ad)
            if (org0_ is not None): 
                if (d is None): 
                    d = GeoTokenData(t)
                d.org0_ = org0_
                if (org0_.has_terr_keyword or ((org0_.is_gsk and not org0_.keyword_after))): 
                    tt = org0_.begin_token
                    while tt is not None and tt.end_char <= org0_.end_char: 
                        dd = Utils.asObjectOrNull(tt.tag, GeoTokenData)
                        if (dd is None): 
                            dd = GeoTokenData(tt)
                        dd.no_geo = True
                        tt = tt.next0_
                    if (not org0_.has_terr_keyword): 
                        t = org0_.end_token
            t = t.next0_
        ad.oregime = True
    
    @staticmethod
    def try_parse(t : 'Token', ad : 'GeoAnalyzerData'=None) -> 'OrgItemToken':
        if (not (isinstance(t, TextToken))): 
            return None
        if (ad is None): 
            ad = GeoAnalyzer._get_data(t)
        if (ad is None): 
            return None
        if (OrgItemToken.SPEED_REGIME and ((ad.oregime or ad.all_regime))): 
            d = Utils.asObjectOrNull(t.tag, GeoTokenData)
            if (d is not None): 
                return d.org0_
            return None
        if (ad.olevel > 1): 
            return None
        ad.olevel += 1
        res = OrgItemToken.__try_parse(t, False, 0, ad)
        ad.olevel -= 1
        return res
    
    @staticmethod
    def __try_parse(t : 'Token', after_terr : bool, lev : int, ad : 'GeoAnalyzerData') -> 'OrgItemToken':
        from pullenti.ner.geo.internal.CityItemToken import CityItemToken
        from pullenti.ner.geo.internal.TerrItemToken import TerrItemToken
        from pullenti.ner.geo.internal.NameToken import NameToken
        from pullenti.ner.geo.internal.OrgTypToken import OrgTypToken
        if (lev > 3 or t is None or t.is_comma): 
            return None
        tt2 = MiscLocationHelper.check_territory(t)
        if (tt2 is not None and tt2.next0_ is not None): 
            tt2 = tt2.next0_
            br = False
            if (BracketHelper.is_bracket(tt2, True)): 
                br = True
                tt2 = tt2.next0_
            if (tt2 is None or lev > 3): 
                return None
            re2 = OrgItemToken.__try_parse(tt2, True, lev + 1, ad)
            if (re2 is not None): 
                a = t.kit.processor.find_analyzer("GEO")
                if (a is not None): 
                    rt = a.process_referent(tt2, None)
                    if (rt is not None): 
                        return None
                re2.begin_token = t
                if (br and BracketHelper.can_be_end_of_sequence(re2.end_token.next0_, False, None, False)): 
                    re2.end_token = re2.end_token.next0_
                re2.has_terr_keyword = True
                return re2
            elif ((isinstance(t, TextToken)) and ((t.term.startswith("ТЕР") or t.term.startswith("ПЛОЩ"))) and (tt2.whitespaces_before_count < 3)): 
                nam1 = NameToken.try_parse(tt2, NameTokenType.ORG, 0, True)
                if (nam1 is not None and nam1.name is not None): 
                    if (StreetItemToken.check_keyword(tt2)): 
                        return None
                    if (t.next0_ != nam1.end_token and StreetItemToken.check_keyword(nam1.end_token)): 
                        return None
                    if (TerrItemToken.check_keyword(tt2) is not None): 
                        return None
                    if (t.next0_ != nam1.end_token and TerrItemToken.check_keyword(nam1.end_token) is not None): 
                        return None
                    ter = TerrItemToken.check_onto_item(tt2)
                    if (ter is not None): 
                        geo_ = Utils.asObjectOrNull(ter.item.referent, GeoReferent)
                        if (geo_.is_city or geo_.is_state): 
                            return None
                    if (CityItemToken.check_keyword(tt2) is not None): 
                        return None
                    if (CityItemToken.check_onto_item(tt2) is not None): 
                        return None
                    tt = nam1.end_token
                    ok = False
                    if (tt.is_newline_after): 
                        ok = True
                    elif (tt.next0_ is not None and ((tt.next0_.is_comma or tt.next0_.is_char(')')))): 
                        ok = True
                    elif (AddressItemToken.check_house_after(tt2, False, False)): 
                        ok = True
                    else: 
                        a2 = AddressItemToken.try_parse(nam1.end_token.next0_, False, None, ad)
                        if (a2 is not None): 
                            a1 = AddressItemToken.try_parse(tt2, False, None, ad)
                            if (a1 is None or (a1.end_char < a2.end_char)): 
                                ok = True
                    if (ok): 
                        org1 = t.kit.create_referent("ORGANIZATION")
                        org1.add_slot("NAME", nam1.name, False, 0)
                        if (nam1.number is not None): 
                            org1.add_slot("NUMBER", nam1.number, False, 0)
                        res1 = OrgItemToken(org1, t, nam1.end_token)
                        res1.data = t.kit.get_analyzer_data_by_analyzer_name("ORGANIZATION")
                        res1.has_terr_keyword = True
                        return res1
                rt = t.kit.process_referent("NAMEDENTITY", tt2, None)
                if (rt is not None): 
                    res1 = OrgItemToken(rt.referent, t, rt.end_token)
                    res1.data = t.kit.get_analyzer_data_by_analyzer_name("NAMEDENTITY")
                    res1.has_terr_keyword = True
                    return res1
            if (not t.is_value("САД", None)): 
                return None
        typ_after = False
        doubt0 = False
        tok_typ = OrgTypToken.try_parse(t, after_terr, ad)
        nam = None
        if (tok_typ is None): 
            ok = 0
            if (BracketHelper.can_be_start_of_sequence(t, True, False)): 
                ok = 2
            elif (t.is_value("ИМ", None)): 
                ok = 2
            elif ((isinstance(t, TextToken)) and not t.chars.is_all_lower and t.length_char > 1): 
                ok = 1
            elif (after_terr): 
                ok = 1
            if (ok == 0): 
                return None
            if ((t.length_char > 5 and (isinstance(t, TextToken)) and not t.chars.is_all_upper) and not t.chars.is_all_lower and not t.chars.is_capital_upper): 
                namm = t.get_source_text()
                if (str.isupper(namm[0]) and str.isupper(namm[1])): 
                    i = 0
                    while i < len(namm): 
                        if (str.islower(namm[i]) and i > 2): 
                            abbr = namm[0:0+i - 1]
                            te = Termin._new1113(abbr, abbr)
                            li = OrgTypToken.find_termin_by_acronym(abbr)
                            if (li is not None and len(li) > 0): 
                                nam = NameToken(t, t)
                                nam.name = t.term[i - 1:]
                                tok_typ = OrgTypToken(t, t)
                                tok_typ.vals.append(li[0].canonic_text.lower())
                                tok_typ.vals.append(abbr)
                                nam.try_attach_number()
                                break
                        i += 1
            if (nam is None): 
                if (after_terr): 
                    ok = 2
                if (ok < 2): 
                    kk = 0
                    tt = t.next0_
                    first_pass2887 = True
                    while True:
                        if first_pass2887: first_pass2887 = False
                        else: tt = tt.next0_; kk += 1
                        if (not (tt is not None and (kk < 5))): break
                        ty22 = OrgTypToken.try_parse(tt, False, ad)
                        if (ty22 is None or ty22.is_doubt): 
                            continue
                        ok = 2
                        break
                if (ok < 2): 
                    return None
                typ_after = True
                nam = NameToken.try_parse(t, NameTokenType.ORG, 0, False)
                if (nam is None): 
                    return None
                tok_typ = OrgTypToken.try_parse(nam.end_token.next0_, after_terr, ad)
                if (nam.name is None): 
                    if (nam.number is not None and tok_typ is not None): 
                        pass
                    else: 
                        return None
                if (tok_typ is not None): 
                    if (nam.begin_token == nam.end_token): 
                        mc = nam.get_morph_class_in_dictionary()
                        if (mc.is_conjunction or mc.is_preposition or mc.is_pronoun): 
                            return None
                    nam2 = NameToken.try_parse(tok_typ.end_token.next0_, NameTokenType.ORG, 0, False)
                    rt2 = OrgItemToken.try_parse(tok_typ.begin_token, None)
                    if (rt2 is not None and rt2.end_char > tok_typ.end_char): 
                        if ((nam.number is None and nam2 is not None and nam2.name is None) and nam2.number is not None and nam2.end_token == rt2.end_token): 
                            nam.number = nam2.number
                            tok_typ = tok_typ.clone()
                            tok_typ.end_token = nam2.end_token
                        else: 
                            return None
                    elif ((nam.number is None and nam2 is not None and nam2.name is None) and nam2.number is not None): 
                        nam.number = nam2.number
                        tok_typ = tok_typ.clone()
                        tok_typ.end_token = nam2.end_token
                    nam.end_token = tok_typ.end_token
                    doubt0 = True
                else: 
                    if (nam.name.endswith("ПЛАЗА") or nam.name.startswith("БИЗНЕС")): 
                        pass
                    elif (nam.begin_token == nam.end_token): 
                        return None
                    else: 
                        tok_typ = OrgTypToken.try_parse(nam.end_token, False, ad)
                        if ((tok_typ) is None): 
                            return None
                        elif (nam.morph.case_.is_genitive and not nam.morph.case_.is_nominative): 
                            nam.name = MiscHelper.get_text_value_of_meta_token(nam, GetTextAttr.FIRSTNOUNGROUPTONOMINATIVESINGLE).replace("-", " ")
                    if (tok_typ is None): 
                        tok_typ = OrgTypToken(t, t)
                        tok_typ.vals.append("бизнес центр")
                        tok_typ.vals.append("БЦ")
                    nam.is_doubt = False
        else: 
            if (tok_typ.whitespaces_after_count > 3): 
                return None
            tt3 = MiscLocationHelper.check_territory(tok_typ.end_token.next0_)
            if (tt3 is not None): 
                tok_typ = tok_typ.clone()
                tok_typ.end_token = tt3
                after_terr = True
                tok_typ2 = OrgTypToken.try_parse(tok_typ.end_token.next0_, True, ad)
                if (tok_typ2 is not None and not tok_typ2.is_doubt): 
                    tok_typ.merge_with(tok_typ2)
            if (BracketHelper.can_be_start_of_sequence(tok_typ.end_token.next0_, True, False)): 
                tok_typ2 = OrgTypToken.try_parse(tok_typ.end_token.next0_.next0_, after_terr, ad)
                if (tok_typ2 is not None and not tok_typ2.is_doubt): 
                    tok_typ = tok_typ.clone()
                    tok_typ.is_doubt = False
                    nam = NameToken.try_parse(tok_typ2.end_token.next0_, NameTokenType.ORG, 0, False)
                    if (nam is not None and BracketHelper.can_be_end_of_sequence(nam.end_token.next0_, False, None, False)): 
                        tok_typ.merge_with(tok_typ2)
                        nam.end_token = nam.end_token.next0_
                    elif (nam is not None and BracketHelper.can_be_end_of_sequence(nam.end_token, False, None, False)): 
                        tok_typ.merge_with(tok_typ2)
                    else: 
                        nam = (None)
        if (nam is None): 
            nam = NameToken.try_parse(tok_typ.end_token.next0_, NameTokenType.ORG, 0, True)
        if (nam is None): 
            return None
        if (tok_typ.is_doubt and ((nam.is_doubt or nam.chars.is_all_upper))): 
            return None
        if ((tok_typ.length_char < 3) and nam.name is None and nam.pref is None): 
            return None
        org0_ = t.kit.create_referent("ORGANIZATION")
        res = OrgItemToken(org0_, t, nam.end_token)
        res.data = t.kit.get_analyzer_data_by_analyzer_name("ORGANIZATION")
        res.has_terr_keyword = after_terr
        res.is_doubt = (doubt0 or tok_typ.is_doubt)
        res.keyword_after = typ_after
        res.is_massive = tok_typ.is_massiv
        for ty in tok_typ.vals: 
            org0_.add_slot("TYPE", ty, False, 0)
        ignore_next = False
        if ((res.whitespaces_after_count < 3) and res.end_token.next0_ is not None and res.end_token.next0_.is_value("ТЕРРИТОРИЯ", None)): 
            if (OrgItemToken.__try_parse(res.end_token.next0_.next0_, True, lev + 1, ad) is None): 
                res.end_token = res.end_token.next0_
                ignore_next = True
        if ((res.whitespaces_after_count < 3) and not tok_typ.is_massiv): 
            tt = res.end_token.next0_
            next0__ = OrgItemToken.__try_parse(tt, False, lev + 1, ad)
            if (next0__ is not None): 
                if (next0__.is_gsk): 
                    next0__ = (None)
                else: 
                    res.end_token = next0__.end_token
                ignore_next = True
            else: 
                if (tt is not None and tt.is_value("ПРИ", None)): 
                    tt = tt.next0_
                rt = t.kit.process_referent("ORGANIZATION", tt, None)
                if (rt is not None): 
                    pass
                if (rt is not None): 
                    res.end_token = rt.end_token
                    ter = TerrItemToken.check_onto_item(res.end_token.next0_)
                    if (ter is not None): 
                        res.end_token = ter.end_token
                    ignore_next = True
        suff_name = None
        if (not ignore_next and (res.whitespaces_after_count < 2) and not tok_typ.is_massiv): 
            tok_typ2 = OrgTypToken.try_parse(res.end_token.next0_, True, ad)
            if (tok_typ2 is not None): 
                res.end_token = tok_typ2.end_token
                if (tok_typ2.is_doubt and nam.name is not None): 
                    suff_name = tok_typ2.vals[0]
                else: 
                    for ty in tok_typ2.vals: 
                        org0_.add_slot("TYPE", ty, False, 0)
                if (nam.number is None): 
                    nam2 = NameToken.try_parse(res.end_token.next0_, NameTokenType.ORG, 0, False)
                    if ((nam2 is not None and nam2.number is not None and nam2.name is None) and nam2.pref is None): 
                        nam.number = nam2.number
                        res.end_token = nam2.end_token
        if (nam.name is not None): 
            if (nam.pref is not None): 
                org0_.add_slot("NAME", "{0} {1}".format(nam.pref, nam.name), False, 0)
                if (suff_name is not None): 
                    org0_.add_slot("NAME", "{0} {1} {2}".format(nam.pref, nam.name, suff_name), False, 0)
            else: 
                org0_.add_slot("NAME", nam.name, False, 0)
                if (suff_name is not None): 
                    org0_.add_slot("NAME", "{0} {1}".format(nam.name, suff_name), False, 0)
        elif (nam.pref is not None): 
            org0_.add_slot("NAME", nam.pref, False, 0)
        elif (nam.number is not None and (res.whitespaces_after_count < 2)): 
            nam2 = NameToken.try_parse(res.end_token.next0_, NameTokenType.ORG, 0, False)
            if (nam2 is not None and nam2.name is not None and nam2.number is None): 
                res.end_token = nam2.end_token
                org0_.add_slot("NAME", nam2.name, False, 0)
        if (nam.number is not None): 
            org0_.add_slot("NUMBER", nam.number, False, 0)
        ok1 = False
        cou = 0
        tt = res.begin_token
        while tt is not None and tt.end_char <= res.end_char: 
            if ((isinstance(tt, TextToken)) and tt.length_char > 1): 
                if (nam is not None and tt.begin_char >= nam.begin_char and tt.end_char <= nam.end_char): 
                    if (tok_typ is not None and tt.begin_char >= tok_typ.begin_char and tt.end_char <= tok_typ.end_char): 
                        pass
                    else: 
                        cou += 1
                if (not tt.chars.is_all_lower): 
                    ok1 = True
            elif (isinstance(tt, ReferentToken)): 
                ok1 = True
            tt = tt.next0_
        res.set_gsk()
        if (not ok1): 
            if (not res.is_gsk and not res.has_terr_keyword): 
                return None
        if (cou > 4): 
            return None
        if (res.is_massive and (res.whitespaces_after_count < 2)): 
            tt = res.end_token.next0_
            if ((isinstance(tt, TextToken)) and tt.length_char == 1 and ((tt.is_value("П", None) or tt.is_value("Д", None)))): 
                if (not AddressItemToken.check_house_after(tt, False, False)): 
                    res.end_token = res.end_token.next0_
                    if (res.end_token.next0_ is not None and res.end_token.next0_.is_char('.')): 
                        res.end_token = res.end_token.next0_
        return res
    
    @staticmethod
    def try_parse_railway(t : 'Token') -> 'StreetItemToken':
        if (not (isinstance(t, TextToken)) or not t.chars.is_letter): 
            return None
        if (t.is_value("ДОРОГА", None) and (t.whitespaces_after_count < 3)): 
            next0__ = OrgItemToken.try_parse_railway(t.next0_)
            if (next0__ is not None): 
                next0__.begin_token = t
                return next0__
        ad = GeoAnalyzer._get_data(t)
        if (ad is None): 
            return None
        if (ad.olevel > 0): 
            return None
        ad.olevel += 1
        res = OrgItemToken.__try_parse_railway(t)
        ad.olevel -= 1
        return res
    
    @staticmethod
    def __try_parse_railway_org(t : 'Token') -> 'ReferentToken':
        if (t is None): 
            return None
        cou = 0
        ok = False
        tt = t
        while tt is not None and (cou < 4): 
            if (isinstance(tt, TextToken)): 
                val = tt.term
                if (val == "Ж" or val.startswith("ЖЕЛЕЗ")): 
                    ok = True
                    break
                if (LanguageHelper.ends_with(val, "ЖД")): 
                    ok = True
                    break
            tt = tt.next0_; cou += 1
        if (not ok): 
            return None
        rt = t.kit.process_referent("ORGANIZATION", t, None)
        if (rt is None): 
            return None
        for ty in rt.referent.get_string_values("TYPE"): 
            if (ty.endswith("дорога")): 
                return rt
        return None
    
    @staticmethod
    def __try_parse_railway(t : 'Token') -> 'StreetItemToken':
        rt0 = OrgItemToken.__try_parse_railway_org(t)
        if (rt0 is not None): 
            res = StreetItemToken._new1117(t, rt0.end_token, StreetItemType.FIX, True)
            res.value = rt0.referent.get_string_value("NAME")
            t = res.end_token.next0_
            if (t is not None and t.is_comma): 
                t = t.next0_
            next0__ = OrgItemToken.__try_parse_rzd_dir(t)
            if (next0__ is not None): 
                res.end_token = next0__.end_token
                res.value = "{0} {1}".format(res.value, next0__.value)
            elif ((isinstance(t, TextToken)) and t.morph.class0_.is_adjective and not t.chars.is_all_lower): 
                ok = False
                if (t.is_newline_after or t.next0_ is None): 
                    ok = True
                elif (t.next0_.is_char_of(".,")): 
                    ok = True
                elif (AddressItemToken.check_house_after(t.next0_, False, False) or AddressItemToken.check_km_after(t.next0_)): 
                    ok = True
                if (ok): 
                    res.value = "{0} {1} НАПРАВЛЕНИЕ".format(res.value, t.term)
                    res.end_token = t
            if (res.value == "РОССИЙСКИЕ ЖЕЛЕЗНЫЕ ДОРОГИ"): 
                res.noun_is_doubt_coef = 2
            return res
        dir0_ = OrgItemToken.__try_parse_rzd_dir(t)
        if (dir0_ is not None and dir0_.noun_is_doubt_coef == 0): 
            return dir0_
        return None
    
    @staticmethod
    def __try_parse_rzd_dir(t : 'Token') -> 'StreetItemToken':
        napr = None
        tt0 = None
        tt1 = None
        val = None
        cou = 0
        tt = t
        first_pass2888 = True
        while True:
            if first_pass2888: first_pass2888 = False
            else: tt = tt.next0_; cou += 1
            if (not (tt is not None and (cou < 4))): break
            if (tt.is_char_of(",.")): 
                continue
            if (tt.is_newline_before): 
                break
            if (tt.is_value("НАПРАВЛЕНИЕ", None)): 
                napr = tt
                continue
            if (tt.is_value("НАПР", None)): 
                if (tt.next0_ is not None and tt.next0_.is_char('.')): 
                    tt = tt.next0_
                napr = tt
                continue
            npt = MiscLocationHelper._try_parse_npt(tt)
            if (npt is not None and len(npt.adjectives) > 0 and npt.noun.is_value("КОЛЬЦО", None)): 
                tt0 = tt
                tt1 = npt.end_token
                val = npt.get_normal_case_text(None, MorphNumber.SINGULAR, MorphGender.UNDEFINED, False)
                break
            if ((isinstance(tt, TextToken)) and ((not tt.chars.is_all_lower or napr is not None)) and ((tt.morph.gender) & (MorphGender.NEUTER)) != (MorphGender.UNDEFINED)): 
                tt1 = tt
                tt0 = tt1
                continue
            if ((((isinstance(tt, TextToken)) and ((not tt.chars.is_all_lower or napr is not None)) and tt.next0_ is not None) and tt.next0_.is_hiphen and (isinstance(tt.next0_.next0_, TextToken))) and ((tt.next0_.next0_.morph.gender) & (MorphGender.NEUTER)) != (MorphGender.UNDEFINED)): 
                tt0 = tt
                tt = tt.next0_.next0_
                tt1 = tt
                continue
            break
        if (tt0 is None): 
            return None
        res = StreetItemToken._new1118(tt0, tt1, StreetItemType.FIX, True, 1)
        if (val is not None): 
            res.value = val
        else: 
            res.value = tt1.get_normal_case_text(MorphClass.ADJECTIVE, MorphNumber.SINGULAR, MorphGender.NEUTER, False)
            if (tt0 != tt1): 
                res.value = "{0} {1}".format(tt0.term, res.value)
            res.value += " НАПРАВЛЕНИЕ"
        if (napr is not None and napr.end_char > res.end_char): 
            res.end_token = napr
        t = res.end_token.next0_
        if (t is not None and t.is_comma): 
            t = t.next0_
        if (t is not None): 
            rt0 = OrgItemToken.__try_parse_railway_org(t)
            if (rt0 is not None): 
                res.value = "{0} {1}".format(rt0.referent.get_string_value("NAME"), res.value)
                res.end_token = rt0.end_token
                res.noun_is_doubt_coef = 0
        return res