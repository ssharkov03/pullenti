# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import math
import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.core.NumberHelper import NumberHelper
from pullenti.morph.MorphLang import MorphLang
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.core.NumberExType import NumberExType
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.ner.date.DateReferent import DateReferent
from pullenti.ner.geo.internal.GeoTokenData import GeoTokenData
from pullenti.ner.address.internal.AddressItemType import AddressItemType
from pullenti.ner.address.StreetKind import StreetKind
from pullenti.ner.address.StreetReferent import StreetReferent
from pullenti.ner.address.AddressDetailType import AddressDetailType
from pullenti.ner.address.AddressBuildingType import AddressBuildingType
from pullenti.ner.address.AddressHouseType import AddressHouseType
from pullenti.ner.Token import Token
from pullenti.ner.address.internal.StreetItemType import StreetItemType
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.TextToken import TextToken

class AddressItemToken(MetaToken):
    
    def __init__(self, typ_ : 'AddressItemType', begin : 'Token', end : 'Token') -> None:
        super().__init__(begin, end, None)
        self.__m_typ = AddressItemType.PREFIX
        self.value = None;
        self.referent = None;
        self.ref_token = None;
        self.ref_token_is_gsk = False
        self.ref_token_is_massive = False
        self.is_doubt = False
        self.detail_type = AddressDetailType.UNDEFINED
        self.building_type = AddressBuildingType.UNDEFINED
        self.house_type = AddressHouseType.UNDEFINED
        self.detail_meters = 0
        self.orto_terr = None;
        self.typ = typ_
    
    @property
    def typ(self) -> 'AddressItemType':
        return self.__m_typ
    @typ.setter
    def typ(self, value_) -> 'AddressItemType':
        self.__m_typ = value_
        if (value_ == AddressItemType.HOUSE): 
            pass
        return value_
    
    def clone(self) -> 'AddressItemToken':
        res = AddressItemToken(self.typ, self.begin_token, self.end_token)
        res.morph = self.morph
        res.value = self.value
        res.referent = self.referent
        res.ref_token = self.ref_token
        res.ref_token_is_gsk = self.ref_token_is_gsk
        res.ref_token_is_massive = self.ref_token_is_massive
        res.is_doubt = self.is_doubt
        res.detail_type = self.detail_type
        res.building_type = self.building_type
        res.house_type = self.house_type
        res.detail_meters = self.detail_meters
        if (self.orto_terr is not None): 
            res.orto_terr = self.orto_terr.clone()
        return res
    
    @property
    def is_street_road(self) -> bool:
        if (self.typ != AddressItemType.STREET): 
            return False
        if (not (isinstance(self.referent, StreetReferent))): 
            return False
        return self.referent.kind == StreetKind.ROAD
    
    @property
    def is_digit(self) -> bool:
        if (self.value == "Б/Н"): 
            return True
        if (Utils.isNullOrEmpty(self.value)): 
            return False
        if (str.isdigit(self.value[0])): 
            return True
        if (len(self.value) > 1): 
            if (str.isalpha(self.value[0]) and str.isdigit(self.value[1])): 
                return True
        if (len(self.value) != 1 or not str.isalpha(self.value[0])): 
            return False
        if (not self.begin_token.chars.is_all_lower): 
            return False
        return True
    
    def __str__(self) -> str:
        res = io.StringIO()
        print("{0} {1}".format(Utils.enumToString(self.typ), Utils.ifNotNull(self.value, "")), end="", file=res, flush=True)
        if (self.referent is not None): 
            print(" <{0}>".format(str(self.referent)), end="", file=res, flush=True)
        if (self.detail_type != AddressDetailType.UNDEFINED or self.detail_meters > 0): 
            print(" [{0}, {1}]".format(Utils.enumToString(self.detail_type), self.detail_meters), end="", file=res, flush=True)
        if (self.orto_terr is not None): 
            print(" TERR: {0}".format(self.orto_terr), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def __find_addr_typ(t : 'Token', max_char : int, lev : int=0) -> 'AddressItemToken':
        if (t is None or t.end_char > max_char): 
            return None
        if (lev > 5): 
            return None
        if (isinstance(t, ReferentToken)): 
            geo = Utils.asObjectOrNull(t.get_referent(), GeoReferent)
            if (geo is not None): 
                for s in geo.slots: 
                    if (s.type_name == GeoReferent.ATTR_TYPE): 
                        ty = s.value
                        if ("район" in ty): 
                            return None
            tt = t.begin_token
            while tt is not None and tt.end_char <= t.end_char: 
                if (tt.end_char > max_char): 
                    break
                ty = AddressItemToken.__find_addr_typ(tt, max_char, lev + 1)
                if (ty is not None): 
                    return ty
                tt = tt.next0_
        else: 
            ai = AddressItemToken.__try_attach_detail(t, None)
            if (ai is not None): 
                if (ai.detail_type != AddressDetailType.UNDEFINED or ai.detail_meters > 0): 
                    return ai
        return None
    
    @staticmethod
    def try_parse(t : 'Token', prefix_before : bool=False, prev : 'AddressItemToken'=None, ad : 'GeoAnalyzerData'=None) -> 'AddressItemToken':
        from pullenti.ner.geo.GeoAnalyzer import GeoAnalyzer
        if (t is None): 
            return None
        if (ad is None): 
            ad = GeoAnalyzer._get_data(t)
        if (ad is None): 
            return None
        if (ad.alevel > 1): 
            return None
        ad.alevel += 1
        res = AddressItemToken.__try_parse(t, prefix_before, prev, ad)
        ad.alevel -= 1
        if (((res is not None and not res.is_whitespace_after and res.end_token.next0_ is not None) and res.end_token.next0_.is_hiphen and not res.end_token.next0_.is_whitespace_after) and res.value is not None): 
            if (res.typ == AddressItemType.HOUSE or res.typ == AddressItemType.BUILDING or res.typ == AddressItemType.CORPUS): 
                tt = res.end_token.next0_.next0_
                if (isinstance(tt, NumberToken)): 
                    res.value = "{0}-{1}".format(res.value, tt.value)
                    res.end_token = tt
                    if ((not tt.is_whitespace_after and (isinstance(tt.next0_, TextToken)) and tt.next0_.length_char == 1) and tt.next0_.chars.is_all_upper): 
                        tt = tt.next0_
                        res.end_token = tt
                        res.value += tt.term
                    if ((not tt.is_whitespace_after and tt.next0_ is not None and tt.next0_.is_char_of("\\/")) and (isinstance(tt.next0_.next0_, NumberToken))): 
                        tt = tt.next0_.next0_
                        res.end_token = tt
                        res.value = "{0}/{1}".format(res.value, tt.value)
                    if ((not tt.is_whitespace_after and tt.next0_ is not None and tt.next0_.is_hiphen) and (isinstance(tt.next0_.next0_, NumberToken))): 
                        tt = tt.next0_.next0_
                        res.end_token = tt
                        res.value = "{0}-{1}".format(res.value, tt.value)
                        if ((not tt.is_whitespace_after and (isinstance(tt.next0_, TextToken)) and tt.next0_.length_char == 1) and tt.next0_.chars.is_all_upper): 
                            tt = tt.next0_
                            res.end_token = tt
                            res.value += tt.term
                elif ((isinstance(tt, TextToken)) and tt.length_char == 1 and tt.chars.is_all_upper): 
                    res.value = "{0}-{1}".format(res.value, tt.term)
                    res.end_token = tt
        return res
    
    @staticmethod
    def __try_parse(t : 'Token', prefix_before : bool, prev : 'AddressItemToken', ad : 'GeoAnalyzerData') -> 'AddressItemToken':
        from pullenti.ner.geo.internal.MiscLocationHelper import MiscLocationHelper
        from pullenti.ner.address.internal.StreetItemToken import StreetItemToken
        from pullenti.ner.geo.internal.OrgItemToken import OrgItemToken
        from pullenti.ner.address.internal.StreetDefineHelper import StreetDefineHelper
        if (t is None): 
            return None
        if (isinstance(t, ReferentToken)): 
            rt = Utils.asObjectOrNull(t, ReferentToken)
            ty = None
            geo = Utils.asObjectOrNull(rt.referent, GeoReferent)
            if (geo is not None): 
                if (geo.is_city): 
                    ty = AddressItemType.CITY
                elif (geo.is_state): 
                    ty = AddressItemType.COUNTRY
                else: 
                    ty = AddressItemType.REGION
                res = AddressItemToken._new231(ty, t, t, rt.referent)
                if (ty != AddressItemType.CITY): 
                    return res
                tt = t.begin_token
                first_pass2748 = True
                while True:
                    if first_pass2748: first_pass2748 = False
                    else: tt = tt.next0_
                    if (not (tt is not None and tt.end_char <= t.end_char)): break
                    if (isinstance(tt, ReferentToken)): 
                        if (tt.get_referent() == geo): 
                            res1 = AddressItemToken.__try_parse(tt, False, prev, ad)
                            if (res1 is not None and ((res1.detail_meters > 0 or res1.detail_type != AddressDetailType.UNDEFINED))): 
                                res1.begin_token = res1.end_token = t
                                return res1
                        continue
                    det = AddressItemToken.__try_parse_pure_item(tt, False, None)
                    if (det is not None): 
                        if (det.detail_type != AddressDetailType.UNDEFINED and res.detail_type == AddressDetailType.UNDEFINED): 
                            res.detail_type = det.detail_type
                        if (det.detail_meters > 0): 
                            res.detail_meters = det.detail_meters
                return res
        if (prev is not None): 
            if (t.is_value("КВ", None) or t.is_value("КВАРТ", None)): 
                if ((((prev.typ == AddressItemType.HOUSE or prev.typ == AddressItemType.NUMBER or prev.typ == AddressItemType.BUILDING) or prev.typ == AddressItemType.FLOOR or prev.typ == AddressItemType.POTCH) or prev.typ == AddressItemType.CORPUS or prev.typ == AddressItemType.CORPUSORFLAT) or prev.typ == AddressItemType.DETAIL): 
                    return AddressItemToken.try_parse_pure_item(t, prev, None)
        sli = StreetItemToken.try_parse_list(t, 10, ad)
        if (sli is not None): 
            rt = StreetDefineHelper._try_parse_street(sli, prefix_before, False, (prev is not None and prev.typ == AddressItemType.STREET))
            if (rt is None and sli[0].typ != StreetItemType.FIX): 
                org0_ = OrgItemToken.try_parse(t, None)
                if (org0_ is not None): 
                    si = StreetItemToken._new232(t, org0_.end_token, StreetItemType.FIX, org0_)
                    sli.clear()
                    sli.append(si)
                    rt = StreetDefineHelper._try_parse_street(sli, prefix_before or prev is not None, False, False)
            if (((rt is None and prev is not None and prev.typ == AddressItemType.CITY) and MiscLocationHelper.is_user_param_address(sli[0]) and len(sli) == 1) and ((sli[0].typ == StreetItemType.NAME or sli[0].typ == StreetItemType.STDNAME or sli[0].typ == StreetItemType.STDADJECTIVE))): 
                rt = StreetDefineHelper._try_parse_street(sli, True, False, False)
            if (rt is not None): 
                if (len(sli) > 2): 
                    pass
                if (rt.begin_char > sli[0].begin_char): 
                    return None
                crlf = False
                ttt = rt.begin_token
                while ttt != rt.end_token and (ttt.end_char < rt.end_char): 
                    if (ttt.is_newline_after): 
                        crlf = True
                        break
                    ttt = ttt.next0_
                if (crlf): 
                    ttt = rt.begin_token.previous
                    first_pass2749 = True
                    while True:
                        if first_pass2749: first_pass2749 = False
                        else: ttt = ttt.previous
                        if (not (ttt is not None)): break
                        if (ttt.morph.class0_.is_preposition or ttt.is_comma): 
                            continue
                        if (isinstance(ttt.get_referent(), GeoReferent)): 
                            crlf = False
                        break
                    if (sli[0].typ == StreetItemType.NOUN and "ДОРОГА" in sli[0].termin.canonic_text): 
                        crlf = False
                if (crlf): 
                    aat = AddressItemToken.try_parse_pure_item(rt.end_token.next0_, None, None)
                    if (aat is None): 
                        return None
                    if (aat.typ != AddressItemType.HOUSE): 
                        return None
                return rt
            if (len(sli) == 1 and sli[0].typ == StreetItemType.NOUN): 
                tt = sli[0].end_token.next0_
                if (tt is not None and ((tt.is_hiphen or tt.is_char('_') or tt.is_value("НЕТ", None)))): 
                    ttt = tt.next0_
                    if (ttt is not None and ttt.is_comma): 
                        ttt = ttt.next0_
                    att = AddressItemToken.try_parse_pure_item(ttt, None, None)
                    if (att is not None): 
                        if (att.typ == AddressItemType.HOUSE or att.typ == AddressItemType.CORPUS or att.typ == AddressItemType.BUILDING): 
                            return AddressItemToken(AddressItemType.STREET, t, tt)
        return AddressItemToken.try_parse_pure_item(t, prev, ad)
    
    SPEED_REGIME = False
    
    @staticmethod
    def _prepare_all_data(t0 : 'Token') -> None:
        from pullenti.ner.geo.GeoAnalyzer import GeoAnalyzer
        if (not AddressItemToken.SPEED_REGIME): 
            return
        ad = GeoAnalyzer._get_data(t0)
        if (ad is None): 
            return
        ad.aregime = False
        t = t0
        while t is not None: 
            d = Utils.asObjectOrNull(t.tag, GeoTokenData)
            prev = None
            kk = 0
            tt = t.previous
            first_pass2750 = True
            while True:
                if first_pass2750: first_pass2750 = False
                else: tt = tt.previous; kk += 1
                if (not (tt is not None and (kk < 10))): break
                dd = Utils.asObjectOrNull(tt.tag, GeoTokenData)
                if (dd is None or dd.street is None): 
                    continue
                if (dd.street.end_token.next0_ == t): 
                    prev = dd.addr
                if (t.previous is not None and t.previous.is_comma and dd.street.end_token.next0_ == t.previous): 
                    prev = dd.addr
            str0_ = AddressItemToken.try_parse_pure_item(t, prev, None)
            if (str0_ is not None): 
                if (d is None): 
                    d = GeoTokenData(t)
                d.addr = str0_
            t = t.next0_
        ad.aregime = True
    
    @staticmethod
    def try_parse_pure_item(t : 'Token', prev : 'AddressItemToken'=None, ad : 'GeoAnalyzerData'=None) -> 'AddressItemToken':
        from pullenti.ner.geo.GeoAnalyzer import GeoAnalyzer
        if (t is None): 
            return None
        if (t.is_char(',')): 
            return None
        if (ad is None): 
            ad = GeoAnalyzer._get_data(t)
        if (ad is None): 
            return None
        if (AddressItemToken.SPEED_REGIME and ((ad.aregime or ad.all_regime)) and not (isinstance(t, ReferentToken))): 
            d = Utils.asObjectOrNull(t.tag, GeoTokenData)
            if (d is None): 
                return None
            if (d.addr is None): 
                return None
            return d.addr
        if (ad.alevel > 0): 
            return None
        ad.level += 1
        res = AddressItemToken.__try_parse_pure_item(t, False, prev)
        if (res is not None and res.typ == AddressItemType.DETAIL): 
            pass
        else: 
            det = AddressItemToken.__try_attach_detail(t, None)
            if (res is None): 
                res = det
            elif (det is not None and det.end_char > res.end_char): 
                res = det
        ad.level -= 1
        return res
    
    @staticmethod
    def __try_parse_pure_item(t : 'Token', prefix_before : bool, prev : 'AddressItemToken') -> 'AddressItemToken':
        from pullenti.ner.address.AddressReferent import AddressReferent
        from pullenti.ner.geo.internal.MiscLocationHelper import MiscLocationHelper
        from pullenti.ner.geo.internal.TerrItemToken import TerrItemToken
        from pullenti.ner.address.internal.StreetItemToken import StreetItemToken
        from pullenti.ner.geo.internal.CityItemToken import CityItemToken
        if (isinstance(t, NumberToken)): 
            n = Utils.asObjectOrNull(t, NumberToken)
            if (((n.length_char == 6 or n.length_char == 5)) and n.typ == NumberSpellingType.DIGIT and not n.morph.class0_.is_adjective): 
                return AddressItemToken._new233(AddressItemType.ZIP, t, t, str(n.value))
            ok = False
            if ((t.previous is not None and t.previous.morph.class0_.is_preposition and t.next0_ is not None) and t.next0_.chars.is_letter and t.next0_.chars.is_all_lower): 
                ok = True
            elif (t.morph.class0_.is_adjective and not t.morph.class0_.is_noun): 
                ok = True
            tok0 = AddressItemToken.__m_ontology.try_parse(t.next0_, TerminParseAttr.NO)
            if (tok0 is not None and (isinstance(tok0.termin.tag, AddressItemType))): 
                if (tok0.end_token.next0_ is None or tok0.end_token.next0_.is_comma or tok0.end_token.is_newline_after): 
                    ok = True
                typ0 = Utils.valToEnum(tok0.termin.tag, AddressItemType)
                if (typ0 == AddressItemType.FLAT): 
                    if ((isinstance(t.next0_, TextToken)) and t.next0_.is_value("КВ", None)): 
                        if (t.next0_.get_source_text() == "кВ"): 
                            return None
                    if ((isinstance(tok0.end_token.next0_, NumberToken)) and (tok0.end_token.whitespaces_after_count < 3)): 
                        if (prev is not None and ((prev.typ == AddressItemType.STREET or prev.typ == AddressItemType.CITY))): 
                            return AddressItemToken._new233(AddressItemType.NUMBER, t, t, str(n.value))
                if (isinstance(tok0.end_token.next0_, NumberToken)): 
                    pass
                elif ((typ0 == AddressItemType.KILOMETER or typ0 == AddressItemType.FLOOR or typ0 == AddressItemType.BLOCK) or typ0 == AddressItemType.POTCH or typ0 == AddressItemType.FLAT): 
                    return AddressItemToken._new233(typ0, t, tok0.end_token, str(n.value))
        prepos = False
        tok = None
        if (t is not None and t.morph.class0_.is_preposition): 
            tok = AddressItemToken.__m_ontology.try_parse(t, TerminParseAttr.NO)
            if ((tok) is None): 
                if (t.begin_char < t.end_char): 
                    return None
                if (not t.is_char_of("КСкс")): 
                    t = t.next0_
                prepos = True
        if (t is None): 
            return None
        if ((isinstance(t, TextToken)) and t.length_char == 1 and t.chars.is_letter): 
            if (t.previous is not None and t.previous.is_comma): 
                if (t.is_newline_after or t.next0_.is_comma): 
                    return AddressItemToken._new236(AddressItemType.BUILDING, t, t, AddressBuildingType.LITER, t.term)
        if (tok is None): 
            tok = AddressItemToken.__m_ontology.try_parse(t, TerminParseAttr.NO)
        t1 = t
        typ_ = AddressItemType.NUMBER
        house_typ = AddressHouseType.UNDEFINED
        build_typ = AddressBuildingType.UNDEFINED
        if (tok is not None): 
            if (t.is_value("УЖЕ", None)): 
                return None
            if (t.is_value("ЛИТЕРА", None)): 
                str0_ = t.get_source_text()
                if (str.isupper(str0_[len(str0_) - 1]) and str.islower(str0_[len(str0_) - 2])): 
                    return AddressItemToken._new236(AddressItemType.BUILDING, t, t, AddressBuildingType.LITER, str0_[len(str0_) - 1:])
            if (tok.termin.canonic_text == "ТАМ ЖЕ"): 
                cou = 0
                tt = t.previous
                first_pass2751 = True
                while True:
                    if first_pass2751: first_pass2751 = False
                    else: tt = tt.previous
                    if (not (tt is not None)): break
                    if (cou > 1000): 
                        break
                    r = tt.get_referent()
                    if (r is None): 
                        continue
                    if (isinstance(r, AddressReferent)): 
                        g = Utils.asObjectOrNull(r.get_slot_value(AddressReferent.ATTR_GEO), GeoReferent)
                        if (g is not None): 
                            return AddressItemToken._new231(AddressItemType.CITY, t, tok.end_token, g)
                        break
                    elif (isinstance(r, GeoReferent)): 
                        g = Utils.asObjectOrNull(r, GeoReferent)
                        if (not g.is_state): 
                            return AddressItemToken._new231(AddressItemType.CITY, t, tok.end_token, g)
                return None
            if (isinstance(tok.termin.tag, AddressDetailType)): 
                return AddressItemToken.__try_attach_detail(t, tok)
            t1 = tok.end_token.next0_
            if (isinstance(tok.termin.tag, AddressItemType)): 
                if (isinstance(tok.termin.tag2, AddressHouseType)): 
                    house_typ = (Utils.valToEnum(tok.termin.tag2, AddressHouseType))
                if (isinstance(tok.termin.tag2, AddressBuildingType)): 
                    build_typ = (Utils.valToEnum(tok.termin.tag2, AddressBuildingType))
                typ_ = (Utils.valToEnum(tok.termin.tag, AddressItemType))
                if (typ_ == AddressItemType.PLOT): 
                    if (t.previous is not None and ((t.previous.is_value("СУДЕБНЫЙ", "СУДОВИЙ") or t.previous.is_value("ИЗБИРАТЕЛЬНЫЙ", "ВИБОРЧИЙ")))): 
                        return None
                if (typ_ == AddressItemType.PREFIX): 
                    first_pass2752 = True
                    while True:
                        if first_pass2752: first_pass2752 = False
                        else: t1 = t1.next0_
                        if (not (t1 is not None)): break
                        if (((t1.morph.class0_.is_preposition or t1.morph.class0_.is_conjunction)) and t1.whitespaces_after_count == 1): 
                            continue
                        if (t1.is_char(':')): 
                            t1 = t1.next0_
                            break
                        if (t1.is_char('(')): 
                            br = BracketHelper.try_parse(t1, BracketParseAttr.NO, 100)
                            if (br is not None and (br.length_char < 50)): 
                                t1 = br.end_token
                                continue
                        if (isinstance(t1, TextToken)): 
                            if (t1.chars.is_all_lower or (t1.whitespaces_before_count < 3)): 
                                npt = MiscLocationHelper._try_parse_npt(t1)
                                if (npt is not None and ((npt.chars.is_all_lower or npt.morph.case_.is_genitive))): 
                                    if (CityItemToken.check_keyword(npt.end_token) is None and TerrItemToken.check_keyword(npt.end_token) is None): 
                                        t1 = npt.end_token
                                        continue
                        if (t1.is_value("УКАЗАННЫЙ", None) or t1.is_value("ЕГРИП", None) or t1.is_value("ФАКТИЧЕСКИЙ", None)): 
                            continue
                        if (t1.is_comma): 
                            if (t1.next0_ is not None and t1.next0_.is_value("УКАЗАННЫЙ", None)): 
                                continue
                        break
                    if (t1 is not None): 
                        t0 = t
                        if (((t0.previous is not None and not t0.is_newline_before and t0.previous.is_char(')')) and (isinstance(t0.previous.previous, TextToken)) and t0.previous.previous.previous is not None) and t0.previous.previous.previous.is_char('(')): 
                            t = t0.previous.previous.previous.previous
                            if (t is not None and t.get_morph_class_in_dictionary().is_adjective and not t.is_newline_after): 
                                t0 = t
                        res = AddressItemToken(AddressItemType.PREFIX, t0, t1.previous)
                        tt = t0.previous
                        first_pass2753 = True
                        while True:
                            if first_pass2753: first_pass2753 = False
                            else: tt = tt.previous
                            if (not (tt is not None)): break
                            if (tt.newlines_after_count > 3): 
                                break
                            if (tt.is_comma_and or tt.is_char_of("().")): 
                                continue
                            if (not (isinstance(tt, TextToken))): 
                                break
                            if (((tt.is_value("ПОЧТОВЫЙ", None) or tt.is_value("ЮРИДИЧЕСКИЙ", None) or tt.is_value("ЮР", None)) or tt.is_value("ФАКТИЧЕСКИЙ", None) or tt.is_value("ФАКТ", None)) or tt.is_value("ПОЧТ", None) or tt.is_value("АДРЕС", None)): 
                                res.begin_token = tt
                            else: 
                                break
                        return res
                    else: 
                        return None
                elif ((typ_ == AddressItemType.CORPUSORFLAT and not tok.is_whitespace_before and not tok.is_whitespace_after) and tok.begin_token == tok.end_token and tok.begin_token.is_value("К", None)): 
                    typ_ = AddressItemType.CORPUS
                if (typ_ == AddressItemType.DETAIL and t.is_value("У", None)): 
                    if (not MiscLocationHelper.check_geo_object_before(t, False)): 
                        return None
                if (typ_ == AddressItemType.FLAT and t.is_value("КВ", None)): 
                    if (t.get_source_text() == "кВ"): 
                        return None
                if (typ_ == AddressItemType.KILOMETER or typ_ == AddressItemType.FLOOR or typ_ == AddressItemType.POTCH): 
                    return AddressItemToken(typ_, t, tok.end_token)
                if ((typ_ == AddressItemType.HOUSE or typ_ == AddressItemType.BUILDING or typ_ == AddressItemType.CORPUS) or typ_ == AddressItemType.PLOT): 
                    if (t1 is not None and ((t1.morph.class0_.is_preposition or t1.morph.class0_.is_conjunction)) and (t1.whitespaces_after_count < 2)): 
                        tok2 = AddressItemToken.__m_ontology.try_parse(t1.next0_, TerminParseAttr.NO)
                        if (tok2 is not None and (isinstance(tok2.termin.tag, AddressItemType))): 
                            typ2 = Utils.valToEnum(tok2.termin.tag, AddressItemType)
                            if (typ2 != typ_ and ((typ2 == AddressItemType.PLOT or ((typ2 == AddressItemType.HOUSE and typ_ == AddressItemType.PLOT))))): 
                                typ_ = typ2
                                if (isinstance(tok.termin.tag2, AddressHouseType)): 
                                    house_typ = (Utils.valToEnum(tok.termin.tag2, AddressHouseType))
                                t1 = tok2.end_token.next0_
                                if (t1 is None): 
                                    return AddressItemToken._new240(typ_, t, tok2.end_token, "0", house_typ)
                if (typ_ == AddressItemType.FIELD): 
                    re = AddressItemToken(typ_, t, tok.end_token)
                    nnn = io.StringIO()
                    tt = tok.end_token.next0_
                    first_pass2754 = True
                    while True:
                        if first_pass2754: first_pass2754 = False
                        else: tt = tt.next0_
                        if (not (tt is not None)): break
                        ll = NumberHelper.try_parse_roman(tt)
                        if (ll is not None and ll.int_value is not None): 
                            if (nnn.tell() > 0): 
                                print("-", end="", file=nnn)
                            print(NumberHelper.get_number_roman(ll.int_value), end="", file=nnn)
                            tt = ll.end_token
                            re.end_token = tt
                            continue
                        if (tt.is_hiphen): 
                            continue
                        if (tt.is_whitespace_before): 
                            break
                        if (isinstance(tt, NumberToken)): 
                            if (nnn.tell() > 0): 
                                print("-", end="", file=nnn)
                            print(tt.value, end="", file=nnn)
                            re.end_token = tt
                            continue
                        if ((isinstance(tt, TextToken)) and tt.chars.is_all_upper): 
                            if (nnn.tell() > 0): 
                                print("-", end="", file=nnn)
                            print(tt.term, end="", file=nnn)
                            re.end_token = tt
                            continue
                        break
                    if (nnn.tell() > 0): 
                        re.value = Utils.toStringStringIO(nnn)
                        return re
                if (typ_ != AddressItemType.NUMBER): 
                    if (t1 is None and t.length_char > 1): 
                        return AddressItemToken._new241(typ_, t, tok.end_token, house_typ, build_typ)
                    if ((isinstance(t1, NumberToken)) and t1.value == "0"): 
                        return AddressItemToken._new242(typ_, t, t1, "0", house_typ, build_typ)
        if (t1 is not None and t1.is_char('.') and t1.next0_ is not None): 
            if (not t1.is_whitespace_after): 
                t1 = t1.next0_
            elif ((isinstance(t1.next0_, NumberToken)) and t1.next0_.typ == NumberSpellingType.DIGIT and (t1.whitespaces_after_count < 2)): 
                t1 = t1.next0_
        if ((t1 is not None and not t1.is_whitespace_after and ((t1.is_hiphen or t1.is_char('_')))) and (isinstance(t1.next0_, NumberToken))): 
            t1 = t1.next0_
        tok = AddressItemToken.__m_ontology.try_parse(t1, TerminParseAttr.NO)
        if (tok is not None and (isinstance(tok.termin.tag, AddressItemType)) and (Utils.valToEnum(tok.termin.tag, AddressItemType)) == AddressItemType.NUMBER): 
            t1 = tok.end_token.next0_
        elif (tok is not None and (isinstance(tok.termin.tag, AddressItemType)) and (Utils.valToEnum(tok.termin.tag, AddressItemType)) == AddressItemType.NONUMBER): 
            re0 = AddressItemToken._new242(typ_, t, tok.end_token, "0", house_typ, build_typ)
            if (not re0.is_whitespace_after and (isinstance(re0.end_token.next0_, NumberToken))): 
                re0.end_token = re0.end_token.next0_
                re0.value = str(re0.end_token.value)
            return re0
        elif (isinstance(t1, TextToken)): 
            term = t1.term
            if (((len(term) == 7 and term.startswith("ЛИТЕРА"))) or ((len(term) == 6 and term.startswith("ЛИТЕР")))): 
                res1 = AddressItemToken(AddressItemType.BUILDING, t, t1)
                res1.building_type = AddressBuildingType.LITER
                res1.value = term[len(term) - 1:]
                return res1
            if (typ_ == AddressItemType.FLAT): 
                tok2 = AddressItemToken.__m_ontology.try_parse(t1, TerminParseAttr.NO)
                if (tok2 is not None and (Utils.valToEnum(tok2.termin.tag, AddressItemType)) == AddressItemType.FLAT): 
                    t1 = tok2.end_token.next0_
            if (t1 is not None and t1.is_value("СТРОИТЕЛЬНЫЙ", None) and t1.next0_ is not None): 
                t1 = t1.next0_
            ttt = MiscHelper.check_number_prefix(t1)
            if (ttt is not None): 
                t1 = ttt
                if (t1.is_hiphen or t1.is_char('_')): 
                    t1 = t1.next0_
        if (t1 is None): 
            return None
        num = io.StringIO()
        nt = Utils.asObjectOrNull(t1, NumberToken)
        re11 = None
        if (nt is not None): 
            if (nt.int_value is None or nt.int_value == 0): 
                return None
            print(nt.value, end="", file=num)
            if (nt.typ == NumberSpellingType.DIGIT or nt.typ == NumberSpellingType.WORDS): 
                if (((isinstance(nt.end_token, TextToken)) and nt.end_token.term == "Е" and nt.end_token.previous == nt.begin_token) and not nt.end_token.is_whitespace_before): 
                    print("Е", end="", file=num)
                drob = False
                hiph = False
                lit = False
                et = nt.next0_
                if (et is not None and ((et.is_char_of("\\/") or et.is_value("ДРОБЬ", None)))): 
                    next0__ = AddressItemToken.__try_parse_pure_item(et.next0_, False, None)
                    if (next0__ is not None and next0__.typ != AddressItemType.NUMBER): 
                        t1 = et
                    else: 
                        drob = True
                        et = et.next0_
                        if (et is not None and et.is_char_of("\\/")): 
                            et = et.next0_
                        t1 = et
                elif (et is not None and ((et.is_hiphen or et.is_char('_')))): 
                    hiph = True
                    et = et.next0_
                elif ((et is not None and et.is_char('.') and (isinstance(et.next0_, NumberToken))) and not et.is_whitespace_after): 
                    return None
                if (isinstance(et, NumberToken)): 
                    if (drob): 
                        print("/{0}".format(et.value), end="", file=num, flush=True)
                        drob = False
                        t1 = et
                        et = et.next0_
                        if (et is not None and et.is_char_of("\\/") and (isinstance(et.next0_, NumberToken))): 
                            t1 = et.next0_
                            print("/{0}".format(t1.value), end="", file=num, flush=True)
                            et = t1.next0_
                    elif ((hiph and not t1.is_whitespace_after and (isinstance(et, NumberToken))) and not et.is_whitespace_before): 
                        numm = AddressItemToken.try_parse_pure_item(et, None, None)
                        if (numm is not None and numm.typ == AddressItemType.NUMBER): 
                            merge = False
                            if (typ_ == AddressItemType.FLAT or typ_ == AddressItemType.PLOT): 
                                merge = True
                            elif (typ_ == AddressItemType.HOUSE or typ_ == AddressItemType.BUILDING or typ_ == AddressItemType.CORPUS): 
                                ttt = numm.end_token.next0_
                                if (ttt is not None and ttt.is_comma): 
                                    ttt = ttt.next0_
                                numm2 = AddressItemToken.try_parse_pure_item(ttt, None, None)
                                if (numm2 is not None): 
                                    if ((numm2.typ == AddressItemType.FLAT or numm2.typ == AddressItemType.BUILDING or ((numm2.typ == AddressItemType.CORPUSORFLAT and numm2.value is not None))) or numm2.typ == AddressItemType.CORPUS): 
                                        merge = True
                            if (merge): 
                                print("/{0}".format(numm.value), end="", file=num, flush=True)
                                t1 = numm.end_token
                                et = t1.next0_
                elif (et is not None and ((et.is_hiphen or et.is_char('_') or et.is_value("НЕТ", None))) and drob): 
                    t1 = et
                ett = et
                if ((ett is not None and ett.is_char_of(",.") and (ett.whitespaces_after_count < 2)) and (isinstance(ett.next0_, TextToken)) and BracketHelper.is_bracket(ett.next0_, False)): 
                    ett = ett.next0_
                if (((BracketHelper.is_bracket(ett, False) and (isinstance(ett.next0_, TextToken)) and ett.next0_.length_char == 1) and ett.next0_.is_letters and BracketHelper.is_bracket(ett.next0_.next0_, False)) and not ett.is_whitespace_after and not ett.next0_.is_whitespace_after): 
                    ch = AddressItemToken.__correct_char_token(ett.next0_)
                    if (ch is None): 
                        return None
                    print(ch, end="", file=num)
                    t1 = ett.next0_.next0_
                elif (BracketHelper.can_be_start_of_sequence(ett, True, False) and (ett.whitespaces_before_count < 2)): 
                    br = BracketHelper.try_parse(ett, BracketParseAttr.NO, 100)
                    if (br is not None and (isinstance(br.begin_token.next0_, TextToken)) and br.begin_token.next0_.next0_ == br.end_token): 
                        s = AddressItemToken.__correct_char_token(br.begin_token.next0_)
                        if (s is not None): 
                            print(s, end="", file=num)
                            t1 = br.end_token
                elif ((isinstance(et, TextToken)) and et.length_char == 1 and et.chars.is_letter): 
                    ttt = StreetItemToken.try_parse(et, None, False, None)
                    s = AddressItemToken.__correct_char_token(et)
                    if (ttt is not None and ttt.typ == StreetItemType.STDNAME): 
                        s = (None)
                    if (s is not None): 
                        if (((s == "К" or s == "С")) and (isinstance(et.next0_, NumberToken)) and not et.is_whitespace_after): 
                            pass
                        elif ((s == "Б" and et.next0_ is not None and et.next0_.is_char_of("/\\")) and (isinstance(et.next0_.next0_, TextToken)) and et.next0_.next0_.is_value("Н", None)): 
                            et = et.next0_.next0_
                            t1 = et
                        else: 
                            ok = False
                            if (drob or hiph or lit): 
                                ok = True
                            elif (not et.is_whitespace_before or ((et.whitespaces_before_count == 1 and ((et.chars.is_all_upper or ((et.is_newline_after or ((et.next0_ is not None and et.next0_.is_comma))))))))): 
                                ok = True
                                if (isinstance(et.next0_, NumberToken)): 
                                    if (not et.is_whitespace_before and et.is_whitespace_after): 
                                        pass
                                    else: 
                                        ok = False
                            elif (((et.next0_ is None or et.next0_.is_comma)) and (et.whitespaces_before_count < 2)): 
                                ok = True
                            elif (et.is_whitespace_before and et.chars.is_all_lower and et.is_value("В", "У")): 
                                pass
                            else: 
                                ait_next = AddressItemToken.try_parse_pure_item(et.next0_, None, None)
                                if (ait_next is not None): 
                                    if ((ait_next.typ == AddressItemType.CORPUS or ait_next.typ == AddressItemType.FLAT or ait_next.typ == AddressItemType.BUILDING) or ait_next.typ == AddressItemType.OFFICE or ait_next.typ == AddressItemType.ROOM): 
                                        ok = True
                            if (ok): 
                                print(s, end="", file=num)
                                t1 = et
                                if (et.next0_ is not None and et.next0_.is_char_of("\\/") and et.next0_.next0_ is not None): 
                                    if (isinstance(et.next0_.next0_, NumberToken)): 
                                        print("/{0}".format(et.next0_.next0_.value), end="", file=num, flush=True)
                                        et = et.next0_.next0_
                                        t1 = et
                                    elif (et.next0_.next0_.is_hiphen or et.next0_.next0_.is_char('_') or et.next0_.next0_.is_value("НЕТ", None)): 
                                        et = et.next0_.next0_
                                        t1 = et
                elif ((isinstance(et, TextToken)) and not et.is_whitespace_before): 
                    val = et.term
                    if (val == "КМ" and typ_ == AddressItemType.HOUSE): 
                        t1 = et
                        print("КМ", end="", file=num)
                    elif (val == "БН"): 
                        t1 = et
                    elif (((len(val) == 2 and val[1] == 'Б' and et.next0_ is not None) and et.next0_.is_char_of("\\/") and et.next0_.next0_ is not None) and et.next0_.next0_.is_value("Н", None)): 
                        print(val[0], end="", file=num)
                        et = et.next0_.next0_
                        t1 = et
        else: 
            re11 = AddressItemToken.__try_attachvch(t1, typ_)
            if ((re11) is not None): 
                re11.begin_token = t
                re11.house_type = house_typ
                re11.building_type = build_typ
                return re11
            elif (((isinstance(t1, TextToken)) and t1.length_char == 2 and t1.is_letters) and not t1.is_whitespace_before and (isinstance(t1.previous, NumberToken))): 
                src = t1.get_source_text()
                if ((src is not None and len(src) == 2 and ((src[0] == 'к' or src[0] == 'k'))) and str.isupper(src[1])): 
                    ch = AddressItemToken.correct_char(src[1])
                    if (ch != (chr(0))): 
                        return AddressItemToken._new233(AddressItemType.CORPUS, t1, t1, "{0}".format(ch))
            elif ((isinstance(t1, TextToken)) and t1.length_char == 1 and t1.is_letters): 
                ch = AddressItemToken.__correct_char_token(t1)
                if (ch is not None): 
                    if (typ_ == AddressItemType.NUMBER): 
                        return None
                    if (ch == "К" or ch == "С"): 
                        if (not t1.is_whitespace_after and (isinstance(t1.next0_, NumberToken))): 
                            return None
                    if (ch == "Д" and typ_ == AddressItemType.PLOT): 
                        rrr = AddressItemToken.try_parse_pure_item(t1, None, None)
                        if (rrr is not None): 
                            rrr.typ = AddressItemType.PLOT
                            rrr.begin_token = t
                            return rrr
                    if (t1.chars.is_all_lower and ((t1.morph.class0_.is_preposition or t1.morph.class0_.is_conjunction))): 
                        if ((t1.whitespaces_after_count < 2) and t1.next0_.chars.is_letter): 
                            return None
                    if (t.chars.is_all_upper and t.length_char == 1 and t.next0_.is_char('.')): 
                        return None
                    print(ch, end="", file=num)
                    if ((t1.next0_ is not None and ((t1.next0_.is_hiphen or t1.next0_.is_char('_'))) and not t1.is_whitespace_after) and (isinstance(t1.next0_.next0_, NumberToken)) and not t1.next0_.is_whitespace_after): 
                        print(t1.next0_.next0_.value, end="", file=num)
                        t1 = t1.next0_.next0_
                    elif ((isinstance(t1.next0_, NumberToken)) and not t1.is_whitespace_after and t1.chars.is_all_upper): 
                        print(t1.next0_.value, end="", file=num)
                        t1 = t1.next0_
                    if (num.tell() == 1 and ((typ_ == AddressItemType.OFFICE or typ_ == AddressItemType.ROOM))): 
                        return None
                if (typ_ == AddressItemType.BOX and num.tell() == 0): 
                    rom = NumberHelper.try_parse_roman(t1)
                    if (rom is not None): 
                        return AddressItemToken._new233(typ_, t, rom.end_token, str(rom.value))
            elif (((BracketHelper.is_bracket(t1, False) and (isinstance(t1.next0_, TextToken)) and t1.next0_.length_char == 1) and t1.next0_.is_letters and BracketHelper.is_bracket(t1.next0_.next0_, False)) and not t1.is_whitespace_after and not t1.next0_.is_whitespace_after): 
                ch = AddressItemToken.__correct_char_token(t1.next0_)
                if (ch is None): 
                    return None
                print(ch, end="", file=num)
                t1 = t1.next0_.next0_
            elif ((isinstance(t1, TextToken)) and ((((t1.length_char == 1 and ((t1.is_hiphen or t1.is_char('_'))))) or t1.is_value("НЕТ", None) or t1.is_value("БН", None))) and (((typ_ == AddressItemType.CORPUS or typ_ == AddressItemType.CORPUSORFLAT or typ_ == AddressItemType.BUILDING) or typ_ == AddressItemType.HOUSE or typ_ == AddressItemType.FLAT))): 
                while t1.next0_ is not None and ((t1.next0_.is_hiphen or t1.next0_.is_char('_'))) and not t1.is_whitespace_after:
                    t1 = t1.next0_
                val = None
                if (not t1.is_whitespace_after and (isinstance(t1.next0_, NumberToken))): 
                    t1 = t1.next0_
                    val = str(t1.value)
                if (t1.is_value("БН", None)): 
                    val = "0"
                return AddressItemToken._new233(typ_, t, t1, val)
            else: 
                if (((typ_ == AddressItemType.FLOOR or typ_ == AddressItemType.KILOMETER or typ_ == AddressItemType.POTCH)) and (isinstance(t.previous, NumberToken))): 
                    return AddressItemToken(typ_, t, t1.previous)
                if ((isinstance(t1, ReferentToken)) and (isinstance(t1.get_referent(), DateReferent))): 
                    nn = AddressItemToken.try_parse_pure_item(t1.begin_token, None, None)
                    if (nn is not None and nn.end_char == t1.end_char and nn.typ == AddressItemType.NUMBER): 
                        nn.begin_token = t
                        nn.end_token = t1
                        nn.typ = typ_
                        return nn
                if ((isinstance(t1, TextToken)) and ((typ_ == AddressItemType.HOUSE or typ_ == AddressItemType.BUILDING or typ_ == AddressItemType.CORPUS))): 
                    ter = t1.term
                    if (ter == "АБ" or ter == "АБВ" or ter == "МГУ"): 
                        return AddressItemToken._new242(typ_, t, t1, ter, house_typ, build_typ)
                    ccc = AddressItemToken.__corr_number(ter)
                    if (ccc is not None): 
                        return AddressItemToken._new242(typ_, t, t1, ccc, house_typ, build_typ)
                    if (t1.chars.is_all_upper): 
                        if (prev is not None and ((prev.typ == AddressItemType.STREET or prev.typ == AddressItemType.CITY))): 
                            return AddressItemToken._new242(typ_, t, t1, ter, house_typ, build_typ)
                        if (typ_ == AddressItemType.CORPUS and (t1.length_char < 4)): 
                            return AddressItemToken._new242(typ_, t, t1, ter, house_typ, build_typ)
                        if (typ_ == AddressItemType.BUILDING and build_typ == AddressBuildingType.LITER and (t1.length_char < 4)): 
                            return AddressItemToken._new242(typ_, t, t1, ter, house_typ, build_typ)
                if (typ_ == AddressItemType.BOX): 
                    rom = NumberHelper.try_parse_roman(t1)
                    if (rom is not None): 
                        return AddressItemToken._new233(typ_, t, rom.end_token, str(rom.value))
                if (typ_ == AddressItemType.PLOT and t1 is not None): 
                    if ((t1.is_value("ОКОЛО", None) or t1.is_value("РЯДОМ", None) or t1.is_value("НАПРОТИВ", None)) or t1.is_value("БЛИЗЬКО", None) or t1.is_value("НАВПАКИ", None)): 
                        return AddressItemToken._new233(typ_, t, t1, t1.get_source_text().lower())
                return None
        if (typ_ == AddressItemType.NUMBER and prepos): 
            return None
        if (t1 is None): 
            t1 = t
            while t1.next0_ is not None:
                t1 = t1.next0_
        tt = t.next0_
        while tt is not None and tt.end_char <= t1.end_char: 
            if (tt.is_newline_before): 
                return None
            tt = tt.next0_
        return AddressItemToken._new254(typ_, t, t1, Utils.toStringStringIO(num), t.morph, house_typ, build_typ)
    
    @staticmethod
    def __try_attachvch(t : 'Token', ty : 'AddressItemType') -> 'AddressItemToken':
        if (t is None): 
            return None
        tt = t
        if ((((tt.is_value("В", None) or tt.is_value("B", None))) and tt.next0_ is not None and tt.next0_.is_char_of("./\\")) and (isinstance(tt.next0_.next0_, TextToken)) and tt.next0_.next0_.is_value("Ч", None)): 
            tt = tt.next0_.next0_
            if (tt.next0_ is not None and tt.next0_.is_char('.')): 
                tt = tt.next0_
            tt2 = MiscHelper.check_number_prefix(tt.next0_)
            if (tt2 is not None): 
                tt = tt2
            if (tt.next0_ is not None and (isinstance(tt.next0_, NumberToken)) and (tt.whitespaces_after_count < 2)): 
                tt = tt.next0_
            return AddressItemToken._new233(ty, t, tt, "В/Ч")
        if (((tt.is_value("ВОЙСКОВОЙ", None) or tt.is_value("ВОИНСКИЙ", None))) and tt.next0_ is not None and tt.next0_.is_value("ЧАСТЬ", None)): 
            tt = tt.next0_
            tt2 = MiscHelper.check_number_prefix(tt.next0_)
            if (tt2 is not None): 
                tt = tt2
            if (tt.next0_ is not None and (isinstance(tt.next0_, NumberToken)) and (tt.whitespaces_after_count < 2)): 
                tt = tt.next0_
            return AddressItemToken._new233(ty, t, tt, "В/Ч")
        if (ty == AddressItemType.FLAT): 
            if (tt.whitespaces_before_count > 1): 
                return None
            if (not (isinstance(tt, TextToken))): 
                return None
            if (tt.term.startswith("ОБЩ")): 
                if (tt.next0_ is not None and tt.next0_.is_char('.')): 
                    tt = tt.next0_
                re = AddressItemToken.__try_attachvch(tt.next0_, ty)
                if (re is not None): 
                    return re
                return AddressItemToken._new233(ty, t, tt, "ОБЩ")
            if (tt.chars.is_all_upper and tt.length_char > 1): 
                re = AddressItemToken._new233(ty, t, tt, tt.term)
                if ((tt.whitespaces_after_count < 2) and (isinstance(tt.next0_, TextToken)) and tt.next0_.chars.is_all_upper): 
                    tt = tt.next0_
                    re.end_token = tt
                    re.value += tt.term
                return re
        return None
    
    @staticmethod
    def __try_attach_detail(t : 'Token', tok : 'TerminToken') -> 'AddressItemToken':
        if (t is None or (isinstance(t, ReferentToken))): 
            return None
        tt = t
        if (t.chars.is_capital_upper and not t.morph.class0_.is_preposition): 
            return None
        if (tok is None): 
            tok = AddressItemToken.__m_ontology.try_parse(t, TerminParseAttr.NO)
        if (tok is None and t.morph.class0_.is_preposition and t.next0_ is not None): 
            tt = t.next0_
            if (isinstance(tt, NumberToken)): 
                pass
            else: 
                if (tt.chars.is_capital_upper and not tt.morph.class0_.is_preposition): 
                    return None
                tok = AddressItemToken.__m_ontology.try_parse(tt, TerminParseAttr.NO)
        res = None
        first_num = False
        if (tok is None): 
            if (isinstance(tt, NumberToken)): 
                first_num = True
                nex = NumberHelper.try_parse_number_with_postfix(tt)
                if (nex is not None and ((nex.ex_typ == NumberExType.METER or nex.ex_typ == NumberExType.KILOMETER))): 
                    res = AddressItemToken(AddressItemType.DETAIL, t, nex.end_token)
                    tyy = NumberExType.METER
                    wraptyy259 = RefOutArgWrapper(tyy)
                    res.detail_meters = (math.floor(nex.normalize_value(wraptyy259)))
                    tyy = wraptyy259.value
            if (res is None): 
                return None
        else: 
            if (not (isinstance(tok.termin.tag, AddressDetailType))): 
                return None
            res = AddressItemToken._new260(AddressItemType.DETAIL, t, tok.end_token, Utils.valToEnum(tok.termin.tag, AddressDetailType))
        tt = res.end_token.next0_
        first_pass2755 = True
        while True:
            if first_pass2755: first_pass2755 = False
            else: tt = tt.next0_
            if (not (tt is not None)): break
            if (isinstance(tt, ReferentToken)): 
                break
            if (not tt.morph.class0_.is_preposition): 
                if (tt.chars.is_capital_upper or tt.chars.is_all_upper): 
                    break
            tok = AddressItemToken.__m_ontology.try_parse(tt, TerminParseAttr.NO)
            if (tok is not None and (isinstance(tok.termin.tag, AddressDetailType))): 
                ty = Utils.valToEnum(tok.termin.tag, AddressDetailType)
                if (ty != AddressDetailType.UNDEFINED): 
                    if (ty == AddressDetailType.NEAR and res.detail_type != AddressDetailType.UNDEFINED and res.detail_type != ty): 
                        pass
                    else: 
                        res.detail_type = ty
                tt = tok.end_token
                res.end_token = tt
                continue
            if (tt.is_value("ОРИЕНТИР", None) or tt.is_value("НАПРАВЛЕНИЕ", None) or tt.is_value("ОТ", None)): 
                res.end_token = tt
                continue
            if (tt.is_comma or tt.morph.class0_.is_preposition): 
                continue
            if ((isinstance(tt, NumberToken)) and tt.next0_ is not None): 
                nex = NumberHelper.try_parse_number_with_postfix(tt)
                if (nex is not None and ((nex.ex_typ == NumberExType.METER or nex.ex_typ == NumberExType.KILOMETER))): 
                    tt = nex.end_token
                    res.end_token = tt
                    tyy = NumberExType.METER
                    wraptyy261 = RefOutArgWrapper(tyy)
                    res.detail_meters = (math.floor(nex.normalize_value(wraptyy261)))
                    tyy = wraptyy261.value
                    continue
            break
        if (first_num and res.detail_type == AddressDetailType.UNDEFINED): 
            return None
        if (res is not None and res.end_token.next0_ is not None and res.end_token.next0_.morph.class0_.is_preposition): 
            if (res.end_token.whitespaces_after_count == 1 and res.end_token.next0_.whitespaces_after_count == 1): 
                res.end_token = res.end_token.next0_
        return res
    
    @staticmethod
    def check_street_after(t : 'Token', check_this_and_not_next : bool=False) -> bool:
        from pullenti.ner.geo.internal.OrgItemToken import OrgItemToken
        cou = 0
        while t is not None and (cou < 4): 
            if (t.is_char_of(",.") or t.is_hiphen or t.morph.class0_.is_preposition): 
                pass
            else: 
                break
            t = t.next0_; cou += 1
        if (t is None): 
            return False
        if (t.is_newline_before): 
            return False
        ait = AddressItemToken.try_parse(t, False, None, None)
        if (ait is None or ait.typ != AddressItemType.STREET): 
            return False
        if (ait.ref_token is not None): 
            if (not ait.ref_token_is_gsk): 
                return False
            oo = Utils.asObjectOrNull(ait.ref_token, OrgItemToken)
            if (oo is not None and oo.is_doubt): 
                return False
        if (not check_this_and_not_next): 
            return True
        if (t.next0_ is None or ait.end_char <= t.end_char): 
            return True
        ait2 = AddressItemToken.try_parse(t.next0_, False, None, None)
        if (ait2 is None): 
            return True
        aits1 = AddressItemToken.try_parse_list(t, 20)
        aits2 = AddressItemToken.try_parse_list(t.next0_, 20)
        if (aits1 is not None and aits2 is not None): 
            if (aits2[len(aits2) - 1].end_char >= aits1[len(aits1) - 1].end_char): 
                return False
        return True
    
    @staticmethod
    def check_house_after(t : 'Token', leek : bool=False, pure_house : bool=False) -> bool:
        if (t is None): 
            return False
        cou = 0
        while t is not None and (cou < 4): 
            if (t.is_char_of(",.") or t.morph.class0_.is_preposition): 
                pass
            else: 
                break
            t = t.next0_; cou += 1
        if (t is None): 
            return False
        if (t.is_newline_before): 
            return False
        ait = AddressItemToken.try_parse_pure_item(t, None, None)
        if (ait is not None): 
            if (pure_house): 
                return ait.typ == AddressItemType.HOUSE or ait.typ == AddressItemType.PLOT
            if (((ait.typ == AddressItemType.HOUSE or ait.typ == AddressItemType.FLOOR or ait.typ == AddressItemType.OFFICE) or ait.typ == AddressItemType.FLAT or ait.typ == AddressItemType.PLOT) or ait.typ == AddressItemType.ROOM): 
                if (((isinstance(t, TextToken)) and t.chars.is_all_upper and t.next0_ is not None) and t.next0_.is_hiphen and (isinstance(t.next0_.next0_, NumberToken))): 
                    return False
                if ((isinstance(t, TextToken)) and t.next0_ == ait.end_token and t.next0_.is_hiphen): 
                    return False
                return True
            if (leek): 
                if (ait.typ == AddressItemType.NUMBER): 
                    return True
            if (ait.typ == AddressItemType.NUMBER): 
                t1 = t.next0_
                while t1 is not None and t1.is_char_of(".,"):
                    t1 = t1.next0_
                ait = AddressItemToken.try_parse_pure_item(t1, None, None)
                if (ait is not None and ((((ait.typ == AddressItemType.BUILDING or ait.typ == AddressItemType.CORPUS or ait.typ == AddressItemType.FLAT) or ait.typ == AddressItemType.FLOOR or ait.typ == AddressItemType.OFFICE) or ait.typ == AddressItemType.ROOM))): 
                    return True
        return False
    
    @staticmethod
    def check_km_after(t : 'Token') -> bool:
        cou = 0
        while t is not None and (cou < 4): 
            if (t.is_char_of(",.") or t.morph.class0_.is_preposition): 
                pass
            else: 
                break
            t = t.next0_; cou += 1
        if (t is None): 
            return False
        km = AddressItemToken.try_parse_pure_item(t, None, None)
        if (km is not None and km.typ == AddressItemType.KILOMETER): 
            return True
        if (not (isinstance(t, NumberToken)) or t.next0_ is None): 
            return False
        if (t.next0_.is_value("КИЛОМЕТР", None) or t.next0_.is_value("МЕТР", None) or t.next0_.is_value("КМ", None)): 
            return True
        return False
    
    @staticmethod
    def check_km_before(t : 'Token') -> bool:
        cou = 0
        while t is not None and (cou < 4): 
            if (t.is_char_of(",.")): 
                pass
            elif (t.is_value("КМ", None) or t.is_value("КИЛОМЕТР", None) or t.is_value("МЕТР", None)): 
                return True
            t = t.previous; cou += 1
        return False
    
    @staticmethod
    def correct_char(v : 'char') -> 'char':
        if (v == 'A' or v == 'А'): 
            return 'А'
        if (v == 'Б' or v == 'Г'): 
            return v
        if (v == 'B' or v == 'В'): 
            return 'В'
        if (v == 'C' or v == 'С'): 
            return 'С'
        if (v == 'D' or v == 'Д'): 
            return 'Д'
        if (v == 'E' or v == 'Е'): 
            return 'Е'
        if (v == 'H' or v == 'Н'): 
            return 'Н'
        if (v == 'K' or v == 'К'): 
            return 'К'
        return chr(0)
    
    @staticmethod
    def __correct_char_token(t : 'Token') -> str:
        tt = Utils.asObjectOrNull(t, TextToken)
        if (tt is None): 
            return None
        v = tt.term
        if (len(v) != 1): 
            return None
        corr = AddressItemToken.correct_char(v[0])
        if (corr != (chr(0))): 
            return "{0}".format(corr)
        if (t.chars.is_cyrillic_letter): 
            return v
        return None
    
    @staticmethod
    def __corr_number(num : str) -> str:
        if (Utils.isNullOrEmpty(num)): 
            return None
        if (num[0] != 'З'): 
            return None
        res = "3"
        i = 0
        i = 1
        while i < len(num): 
            if (num[i] == 'З'): 
                res += "3"
            elif (num[i] == 'О'): 
                res += "0"
            else: 
                break
            i += 1
        if (i == len(num)): 
            return res
        if ((i + 1) < len(num)): 
            return None
        if (num[i] == 'А' or num[i] == 'Б' or num[i] == 'В'): 
            return "{0}{1}".format(res, num[i])
        return None
    
    @staticmethod
    def try_parse_list(t : 'Token', max_count : int=20) -> typing.List['AddressItemToken']:
        from pullenti.ner.geo.GeoAnalyzer import GeoAnalyzer
        if (t is None): 
            return None
        ad = GeoAnalyzer._get_data(t)
        if (ad is not None): 
            if (ad.level > 0): 
                return None
            ad.level += 1
        res = AddressItemToken.__try_parse_list_int(t, max_count)
        if (ad is not None): 
            ad.level -= 1
        if (res is not None and len(res) == 0): 
            return None
        return res
    
    @staticmethod
    def __try_parse_list_int(t : 'Token', max_count : int=20) -> typing.List['AddressItemToken']:
        from pullenti.ner.geo.internal.MiscLocationHelper import MiscLocationHelper
        from pullenti.ner.address.internal.StreetItemToken import StreetItemToken
        from pullenti.ner.geo.internal.OrgItemToken import OrgItemToken
        from pullenti.ner.address.internal.StreetDefineHelper import StreetDefineHelper
        if (isinstance(t, NumberToken)): 
            if (t.int_value is None): 
                return None
            v = t.int_value
            if ((v < 100000) or v >= 10000000): 
                if (t.typ == NumberSpellingType.DIGIT and not t.morph.class0_.is_adjective): 
                    if (t.next0_ is None or (isinstance(t.next0_, NumberToken))): 
                        if (t.previous is None or not t.previous.morph.class0_.is_preposition): 
                            return None
        it = AddressItemToken.try_parse(t, False, None, None)
        if (it is None): 
            return None
        if (it.typ == AddressItemType.NUMBER): 
            return None
        if (it.typ == AddressItemType.KILOMETER and (isinstance(it.begin_token.previous, NumberToken))): 
            it = it.clone()
            it.begin_token = it.begin_token.previous
            it.value = str(it.begin_token.value)
            if (it.begin_token.previous is not None and it.begin_token.previous.morph.class0_.is_preposition): 
                it.begin_token = it.begin_token.previous
        res = list()
        res.append(it)
        pref = it.typ == AddressItemType.PREFIX
        t = it.end_token.next0_
        first_pass2756 = True
        while True:
            if first_pass2756: first_pass2756 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (max_count > 0 and len(res) >= max_count): 
                break
            last = res[len(res) - 1]
            if (len(res) > 1): 
                if (last.is_newline_before and res[len(res) - 2].typ != AddressItemType.PREFIX): 
                    i = 0
                    i = 0
                    first_pass2757 = True
                    while True:
                        if first_pass2757: first_pass2757 = False
                        else: i += 1
                        if (not (i < (len(res) - 1))): break
                        if (res[i].typ == last.typ): 
                            if (i == (len(res) - 2) and ((last.typ == AddressItemType.CITY or last.typ == AddressItemType.REGION))): 
                                jj = 0
                                jj = 0
                                while jj < i: 
                                    if ((res[jj].typ != AddressItemType.PREFIX and res[jj].typ != AddressItemType.ZIP and res[jj].typ != AddressItemType.REGION) and res[jj].typ != AddressItemType.COUNTRY): 
                                        break
                                    jj += 1
                                if (jj >= i): 
                                    continue
                            break
                    if ((i < (len(res) - 1)) or last.typ == AddressItemType.ZIP): 
                        res.remove(last)
                        break
            if (t.is_table_control_char): 
                break
            if (t.is_char(',')): 
                continue
            if (BracketHelper.can_be_end_of_sequence(t, True, None, False) and last.typ == AddressItemType.STREET): 
                continue
            if (t.is_char('.')): 
                if (t.is_newline_after): 
                    break
                if (t.previous is not None and t.previous.is_char('.')): 
                    break
                continue
            if (t.is_hiphen or t.is_char('_')): 
                if (((it.typ == AddressItemType.NUMBER or it.typ == AddressItemType.STREET)) and (isinstance(t.next0_, NumberToken))): 
                    continue
            if (it.typ == AddressItemType.DETAIL and it.detail_type == AddressDetailType.CROSS): 
                str1 = AddressItemToken.try_parse(t, True, None, None)
                if (str1 is not None and str1.typ == AddressItemType.STREET): 
                    if (str1.end_token.next0_ is not None and ((str1.end_token.next0_.is_and or str1.end_token.next0_.is_hiphen))): 
                        str2 = AddressItemToken.try_parse(str1.end_token.next0_.next0_, True, None, None)
                        if (str2 is None or str2.typ != AddressItemType.STREET): 
                            str2 = StreetDefineHelper._try_parse_second_street(str1.begin_token, str1.end_token.next0_.next0_)
                            if (str2 is not None and str2.is_doubt): 
                                str2 = str2.clone()
                                str2.is_doubt = False
                        if (str2 is not None and str2.typ == AddressItemType.STREET): 
                            res.append(str1)
                            res.append(str2)
                            t = str2.end_token
                            it = str2
                            continue
            pre = pref
            if (it.typ == AddressItemType.KILOMETER or ((it.typ == AddressItemType.HOUSE and it.value is not None))): 
                if (not t.is_newline_before): 
                    pre = True
            it0 = AddressItemToken.try_parse(t, pre, it, None)
            if (it0 is None): 
                if (t.newlines_before_count > 2): 
                    break
                if (it.typ == AddressItemType.POSTOFFICEBOX): 
                    break
                if (t.is_hiphen and t.next0_ is not None and t.next0_.is_comma): 
                    continue
                if (t.is_value("НЕТ", None)): 
                    continue
                tt1 = StreetItemToken.check_std_name(t)
                if (tt1 is not None): 
                    t = tt1
                    continue
                if (t.morph.class0_.is_preposition): 
                    it0 = AddressItemToken.try_parse(t.next0_, False, it, None)
                    if (it0 is not None and it0.typ == AddressItemType.BUILDING and it0.begin_token.is_value("СТ", None)): 
                        it0 = (None)
                        break
                    if (it0 is not None): 
                        if ((it0.typ == AddressItemType.DETAIL and it.typ == AddressItemType.CITY and it.detail_meters > 0) and it.detail_type == AddressDetailType.UNDEFINED): 
                            it.detail_type = it0.detail_type
                            it.end_token = it0.end_token
                            t = it.end_token
                            continue
                        if ((it0.typ == AddressItemType.HOUSE or it0.typ == AddressItemType.BUILDING or it0.typ == AddressItemType.CORPUS) or it0.typ == AddressItemType.STREET or it0.typ == AddressItemType.DETAIL): 
                            it = it0
                            res.append(it)
                            t = it.end_token
                            continue
                if (it.typ == AddressItemType.HOUSE or it.typ == AddressItemType.BUILDING or it.typ == AddressItemType.NUMBER): 
                    if ((not t.is_whitespace_before and t.length_char == 1 and t.chars.is_letter) and not t.is_whitespace_after and (isinstance(t.next0_, NumberToken))): 
                        ch = AddressItemToken.__correct_char_token(t)
                        if (ch == "К" or ch == "С"): 
                            it0 = AddressItemToken._new233((AddressItemType.CORPUS if ch == "К" else AddressItemType.BUILDING), t, t.next0_, str(t.next0_.value))
                            it = it0
                            res.append(it)
                            t = it.end_token
                            tt = t.next0_
                            if (((tt is not None and not tt.is_whitespace_before and tt.length_char == 1) and tt.chars.is_letter and not tt.is_whitespace_after) and (isinstance(tt.next0_, NumberToken))): 
                                ch = AddressItemToken.__correct_char_token(tt)
                                if (ch == "К" or ch == "С"): 
                                    it = AddressItemToken._new233((AddressItemType.CORPUS if ch == "К" else AddressItemType.BUILDING), tt, tt.next0_, str(tt.next0_.value))
                                    res.append(it)
                                    t = it.end_token
                            continue
                if (t.morph.class0_.is_preposition): 
                    if ((((t.is_value("У", None) or t.is_value("ВОЗЛЕ", None) or t.is_value("НАПРОТИВ", None)) or t.is_value("НА", None) or t.is_value("В", None)) or t.is_value("ВО", None) or t.is_value("ПО", None)) or t.is_value("ОКОЛО", None)): 
                        continue
                if (t.morph.class0_.is_noun): 
                    if ((t.is_value("ДВОР", None) or t.is_value("ПОДЪЕЗД", None) or t.is_value("КРЫША", None)) or t.is_value("ПОДВАЛ", None)): 
                        continue
                if (t.is_value("ТЕРРИТОРИЯ", "ТЕРИТОРІЯ")): 
                    continue
                if (t.is_char('(') and t.next0_ is not None): 
                    it0 = AddressItemToken.try_parse(t.next0_, pre, None, None)
                    if (it0 is not None and it0.end_token.next0_ is not None and it0.end_token.next0_.is_char(')')): 
                        it0 = it0.clone()
                        it0.begin_token = t
                        it0.end_token = it0.end_token.next0_
                        it = it0
                        res.append(it)
                        t = it.end_token
                        continue
                    br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
                    if (br is not None and (br.length_char < 100)): 
                        if (t.next0_.is_value("БЫВШИЙ", None) or t.next0_.is_value("БЫВШ", None)): 
                            it = AddressItemToken(AddressItemType.DETAIL, t, br.end_token)
                            res.append(it)
                        t = br.end_token
                        continue
                check_kv = False
                if (t.is_value("КВ", None) or t.is_value("KB", None)): 
                    if (it.typ == AddressItemType.NUMBER and len(res) > 1 and res[len(res) - 2].typ == AddressItemType.STREET): 
                        check_kv = True
                    elif ((it.typ == AddressItemType.HOUSE or it.typ == AddressItemType.BUILDING or it.typ == AddressItemType.CORPUS) or it.typ == AddressItemType.CORPUSORFLAT): 
                        for jj in range(len(res) - 2, -1, -1):
                            if (res[jj].typ == AddressItemType.STREET or res[jj].typ == AddressItemType.CITY): 
                                check_kv = True
                    if (check_kv): 
                        tt2 = t.next0_
                        if (tt2 is not None and tt2.is_char('.')): 
                            tt2 = tt2.next0_
                        it22 = AddressItemToken.try_parse_pure_item(tt2, None, None)
                        if (it22 is not None and it22.typ == AddressItemType.NUMBER): 
                            it22 = it22.clone()
                            it22.begin_token = t
                            it22.typ = AddressItemType.FLAT
                            res.append(it22)
                            t = it22.end_token
                            continue
                if (res[len(res) - 1].typ == AddressItemType.CITY): 
                    if (((t.is_hiphen or t.is_char('_') or t.is_value("НЕТ", None))) and t.next0_ is not None and t.next0_.is_comma): 
                        att = AddressItemToken.try_parse_pure_item(t.next0_.next0_, None, None)
                        if (att is not None): 
                            if (att.typ == AddressItemType.HOUSE or att.typ == AddressItemType.BUILDING or att.typ == AddressItemType.CORPUS): 
                                it = AddressItemToken(AddressItemType.STREET, t, t)
                                res.append(it)
                                continue
                if (t.length_char == 2 and (isinstance(t, TextToken)) and t.chars.is_all_upper): 
                    term = t.term
                    if (not Utils.isNullOrEmpty(term) and term[0] == 'Р'): 
                        continue
                break
            if (t.whitespaces_before_count > 15): 
                if (it0.typ == AddressItemType.STREET and last.typ == AddressItemType.CITY): 
                    pass
                else: 
                    break
            if (t.is_newline_before and it0.typ == AddressItemType.STREET and it0.ref_token is not None): 
                if (not it0.ref_token_is_gsk): 
                    break
            if (it0.typ == AddressItemType.STREET and t.is_value("КВ", None)): 
                if (it is not None): 
                    if (it.typ == AddressItemType.HOUSE or it.typ == AddressItemType.BUILDING or it.typ == AddressItemType.CORPUS): 
                        it2 = AddressItemToken.try_parse_pure_item(t, None, None)
                        if (it2 is not None and it2.typ == AddressItemType.FLAT): 
                            it0 = it2
            if (it0.typ == AddressItemType.PREFIX): 
                break
            if (it0.typ == AddressItemType.NUMBER): 
                if (Utils.isNullOrEmpty(it0.value)): 
                    break
                if (not str.isdigit(it0.value[0])): 
                    break
                cou = 0
                for i in range(len(res) - 1, -1, -1):
                    if (res[i].typ == AddressItemType.NUMBER): 
                        cou += 1
                    else: 
                        break
                if (cou > 5): 
                    break
                if (it.is_doubt and t.is_newline_before): 
                    break
            if (it0.typ == AddressItemType.CORPUSORFLAT and it is not None and it.typ == AddressItemType.FLAT): 
                it0.typ = AddressItemType.ROOM
            if (((((it0.typ == AddressItemType.FLOOR or it0.typ == AddressItemType.POTCH or it0.typ == AddressItemType.BLOCK) or it0.typ == AddressItemType.KILOMETER)) and Utils.isNullOrEmpty(it0.value) and it.typ == AddressItemType.NUMBER) and it.end_token.next0_ == it0.begin_token): 
                it = it.clone()
                res[len(res) - 1] = it
                it.typ = it0.typ
                it.end_token = it0.end_token
            elif ((((it.typ == AddressItemType.FLOOR or it.typ == AddressItemType.POTCH)) and Utils.isNullOrEmpty(it.value) and it0.typ == AddressItemType.NUMBER) and it.end_token.next0_ == it0.begin_token): 
                it = it.clone()
                res[len(res) - 1] = it
                it.value = it0.value
                it.end_token = it0.end_token
            else: 
                it = it0
                res.append(it)
            t = it.end_token
        if (len(res) > 0): 
            it = res[len(res) - 1]
            it0 = (res[len(res) - 2] if len(res) > 1 else None)
            if (it.typ == AddressItemType.NUMBER and it0 is not None and it0.ref_token is not None): 
                for s in it0.ref_token.referent.slots: 
                    if (s.type_name == "TYPE"): 
                        ss = Utils.asObjectOrNull(s.value, str)
                        if ("гараж" in ss or ((ss[0] == 'Г' and ss[len(ss) - 1] == 'К'))): 
                            if (it0.ref_token.referent.find_slot("NAME", "РОСАТОМ", True) is not None): 
                                break
                            it.typ = AddressItemType.BOX
                            break
            if (it.typ == AddressItemType.NUMBER or it.typ == AddressItemType.ZIP): 
                del0_ = False
                if (it.begin_token.previous is not None and it.begin_token.previous.morph.class0_.is_preposition): 
                    del0_ = True
                elif (it.morph.class0_.is_noun): 
                    del0_ = True
                if ((not del0_ and it.end_token.whitespaces_after_count == 1 and it.whitespaces_before_count > 0) and it.typ == AddressItemType.NUMBER): 
                    npt = MiscLocationHelper._try_parse_npt(it.end_token.next0_)
                    if (npt is not None): 
                        del0_ = True
                if (del0_): 
                    del res[len(res) - 1]
                elif ((it.typ == AddressItemType.NUMBER and it0 is not None and it0.typ == AddressItemType.STREET) and it0.ref_token is None): 
                    if (it.begin_token.previous.is_char(',') or it.is_newline_after): 
                        it = it.clone()
                        res[len(res) - 1] = it
                        it.typ = AddressItemType.HOUSE
                        it.is_doubt = True
        if (len(res) == 0): 
            return None
        for r in res: 
            if (r.typ == AddressItemType.CITY): 
                ty = AddressItemToken.__find_addr_typ(r.begin_token, r.end_char, 0)
                if (ty is not None): 
                    if (r.detail_type == AddressDetailType.UNDEFINED): 
                        r.detail_type = ty.detail_type
                    if (ty.detail_meters > 0): 
                        r.detail_meters = ty.detail_meters
        i = 0
        while i < (len(res) - 2): 
            if (res[i].typ == AddressItemType.STREET and res[i + 1].typ == AddressItemType.NUMBER): 
                if ((res[i + 2].typ == AddressItemType.BUILDING or res[i + 2].typ == AddressItemType.CORPUS or res[i + 2].typ == AddressItemType.OFFICE) or res[i + 2].typ == AddressItemType.FLAT): 
                    res[i + 1] = res[i + 1].clone()
                    res[i + 1].typ = AddressItemType.HOUSE
            i += 1
        i = 0
        while i < (len(res) - 1): 
            if ((res[i].typ == AddressItemType.STREET and res[i + 1].typ == AddressItemType.KILOMETER and (isinstance(res[i].referent, StreetReferent))) and res[i].referent.number is None): 
                res[i] = res[i].clone()
                res[i].referent.number = res[i + 1].value + "км"
                res[i].end_token = res[i + 1].end_token
                del res[i + 1]
            i += 1
        i = 0
        while i < (len(res) - 1): 
            if ((res[i + 1].typ == AddressItemType.STREET and res[i].typ == AddressItemType.KILOMETER and (isinstance(res[i + 1].referent, StreetReferent))) and res[i + 1].referent.number is None): 
                res[i + 1] = res[i + 1].clone()
                res[i + 1].referent.number = res[i].value + "км"
                res[i + 1].begin_token = res[i].begin_token
                del res[i]
                break
            i += 1
        while len(res) > 0:
            last = res[len(res) - 1]
            if (last.typ != AddressItemType.STREET or not (isinstance(last.ref_token, OrgItemToken))): 
                break
            if (last.ref_token.is_gsk or last.ref_token.has_terr_keyword): 
                break
            if (MiscLocationHelper.is_user_param_address(last)): 
                break
            del res[len(res) - 1]
        return res
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.address.internal.StreetItemToken import StreetItemToken
        if (AddressItemToken.__m_ontology is not None): 
            return
        StreetItemToken.initialize()
        AddressItemToken.__m_ontology = TerminCollection()
        t = None
        t = Termin._new264("ДОМ", AddressItemType.HOUSE)
        t.add_abridge("Д.")
        t.add_variant("КОТТЕДЖ", False)
        t.add_abridge("КОТ.")
        t.add_variant("ДАЧА", False)
        t.add_variant("ЗДАНИЕ", False)
        t.add_variant("ДО ДОМА", False)
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new265("БУДИНОК", AddressItemType.HOUSE, MorphLang.UA)
        t.add_abridge("Б.")
        t.add_variant("КОТЕДЖ", False)
        t.add_abridge("БУД.")
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new266("ВЛАДЕНИЕ", AddressItemType.HOUSE, AddressHouseType.ESTATE)
        t.add_abridge("ВЛАД.")
        t.add_abridge("ВЛД.")
        t.add_abridge("ВЛ.")
        AddressItemToken.__m_ontology.add(t)
        AddressItemToken.M_OWNER = t
        t = Termin._new266("ДОМОВЛАДЕНИЕ", AddressItemType.HOUSE, AddressHouseType.HOUSEESTATE)
        t.add_variant("ДОМОВЛАДЕНИЕ", False)
        t.add_abridge("ДВЛД.")
        t.add_abridge("ДМВЛД.")
        t.add_variant("ДОМОВЛ", False)
        t.add_variant("ДОМОВА", False)
        t.add_variant("ДОМОВЛАД", False)
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new264("ПОДЪЕЗД ДОМА", AddressItemType.HOUSE)
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new264("ПОДВАЛ ДОМА", AddressItemType.HOUSE)
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new264("КРЫША ДОМА", AddressItemType.HOUSE)
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new264("ЭТАЖ", AddressItemType.FLOOR)
        t.add_abridge("ЭТ.")
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new264("ПОДЪЕЗД", AddressItemType.POTCH)
        t.add_abridge("ПОД.")
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new264("КОРПУС", AddressItemType.CORPUS)
        t.add_abridge("КОРП.")
        t.add_abridge("КОР.")
        t.add_abridge("Д.КОРП.")
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new264("К", AddressItemType.CORPUSORFLAT)
        t.add_abridge("К.")
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new264("СТРОЕНИЕ", AddressItemType.BUILDING)
        t.add_abridge("СТРОЕН.")
        t.add_abridge("СТР.")
        t.add_abridge("СТ.")
        t.add_abridge("ПОМ.СТР.")
        t.add_abridge("Д.СТР.")
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new266("СООРУЖЕНИЕ", AddressItemType.BUILDING, AddressBuildingType.CONSTRUCTION)
        t.add_abridge("СООР.")
        t.add_abridge("СООРУЖ.")
        t.add_abridge("СООРУЖЕН.")
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new266("ЛИТЕРА", AddressItemType.BUILDING, AddressBuildingType.LITER)
        t.add_abridge("ЛИТ.")
        t.add_variant("ЛИТЕР", False)
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new264("УЧАСТОК", AddressItemType.PLOT)
        t.add_abridge("УЧАСТ.")
        t.add_abridge("УЧ.")
        t.add_abridge("УЧ-К")
        t.add_abridge("ДОМ УЧ.")
        t.add_abridge("ДОМ.УЧ.")
        t.add_variant("ЗЕМЕЛЬНЫЙ УЧАСТОК", False)
        t.add_abridge("ЗЕМ.УЧ.")
        t.add_abridge("ЗЕМ.УЧ-К")
        t.add_abridge("З/У")
        t.add_abridge("ПОЗ.")
        AddressItemToken.__m_ontology.add(t)
        AddressItemToken.M_PLOT = t
        t = Termin._new264("ПОЛЕ", AddressItemType.FIELD)
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new264("КВАРТИРА", AddressItemType.FLAT)
        t.add_abridge("КВАРТ.")
        t.add_abridge("КВАР.")
        t.add_abridge("КВ.")
        t.add_abridge("KB.")
        t.add_abridge("КВ-РА")
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new264("ОФИС", AddressItemType.OFFICE)
        t.add_abridge("ОФ.")
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new265("ОФІС", AddressItemType.OFFICE, MorphLang.UA)
        t.add_abridge("ОФ.")
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new264("ПАВИЛЬОН", AddressItemType.PAVILION)
        t.add_abridge("ПАВ.")
        t.add_variant("ТОРГОВЫЙ ПАВИЛЬОН", False)
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new265("ПАВІЛЬЙОН", AddressItemType.PAVILION, MorphLang.UA)
        t.add_abridge("ПАВ.")
        t.add_variant("ТОРГОВИЙ ПАВІЛЬЙОН", False)
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new264("БЛОК", AddressItemType.BLOCK)
        t.add_variant("СЕКТОР", False)
        t.add_abridge("СЕК.")
        t.add_variant("СЕКЦИЯ", False)
        t.add_variant("ОЧЕРЕДЬ", False)
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new264("БОКС", AddressItemType.BOX)
        t.add_variant("ГАРАЖ", False)
        t.add_variant("САРАЙ", False)
        t.add_abridge("ГАР.")
        t.add_variant("МАШИНОМЕСТО", False)
        t.add_variant("ПОМЕЩЕНИЕ", False)
        t.add_abridge("ПОМ.")
        t.add_variant("НЕЖИЛОЕ ПОМЕЩЕНИЕ", False)
        t.add_abridge("Н.П.")
        t.add_abridge("НП")
        t.add_variant("ПОДВАЛ", False)
        t.add_variant("ПОГРЕБ", False)
        t.add_variant("ПОДВАЛЬНОЕ ПОМЕЩЕНИЕ", False)
        t.add_variant("ПОДЪЕЗД", False)
        t.add_abridge("ГАРАЖ-БОКС")
        t.add_variant("ГАРАЖНЫЙ БОКС", False)
        t.add_abridge("ГБ.")
        t.add_abridge("Г.Б.")
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new264("КОМНАТА", AddressItemType.ROOM)
        t.add_abridge("КОМ.")
        t.add_abridge("КОМН.")
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new264("КАБИНЕТ", AddressItemType.OFFICE)
        t.add_abridge("КАБ.")
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new264("НОМЕР", AddressItemType.NUMBER)
        t.add_abridge("НОМ.")
        t.add_abridge("№")
        t.add_abridge("N")
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new290("БЕЗ НОМЕРА", "Б/Н", AddressItemType.NONUMBER)
        t.add_abridge("Б.Н.")
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new264("АБОНЕНТСКИЙ ЯЩИК", AddressItemType.POSTOFFICEBOX)
        t.add_abridge("А.Я.")
        t.add_variant("ПОЧТОВЫЙ ЯЩИК", False)
        t.add_abridge("П.Я.")
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new292("ГОРОДСКАЯ СЛУЖЕБНАЯ ПОЧТА", AddressItemType.CSP, "ГСП")
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new264("АДРЕС", AddressItemType.PREFIX)
        t.add_variant("ЮРИДИЧЕСКИЙ АДРЕС", False)
        t.add_variant("ФАКТИЧЕСКИЙ АДРЕС", False)
        t.add_abridge("ЮР.АДРЕС")
        t.add_abridge("ПОЧТ.АДРЕС")
        t.add_abridge("ФАКТ.АДРЕС")
        t.add_abridge("П.АДРЕС")
        t.add_variant("ЮРИДИЧЕСКИЙ/ФАКТИЧЕСКИЙ АДРЕС", False)
        t.add_variant("ПОЧТОВЫЙ АДРЕС", False)
        t.add_variant("АДРЕС ПРОЖИВАНИЯ", False)
        t.add_variant("МЕСТО НАХОЖДЕНИЯ", False)
        t.add_variant("МЕСТОНАХОЖДЕНИЕ", False)
        t.add_variant("МЕСТОПОЛОЖЕНИЕ", False)
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new264("АДРЕСА", AddressItemType.PREFIX)
        t.add_variant("ЮРИДИЧНА АДРЕСА", False)
        t.add_variant("ФАКТИЧНА АДРЕСА", False)
        t.add_variant("ПОШТОВА АДРЕСА", False)
        t.add_variant("АДРЕСА ПРОЖИВАННЯ", False)
        t.add_variant("МІСЦЕ ПЕРЕБУВАННЯ", False)
        t.add_variant("ПРОПИСКА", False)
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new264("КИЛОМЕТР", AddressItemType.KILOMETER)
        t.add_abridge("КИЛОМ.")
        t.add_abridge("КМ.")
        AddressItemToken.__m_ontology.add(t)
        AddressItemToken.__m_ontology.add(Termin._new264("ПЕРЕСЕЧЕНИЕ", AddressDetailType.CROSS))
        AddressItemToken.__m_ontology.add(Termin._new264("НА ПЕРЕСЕЧЕНИИ", AddressDetailType.CROSS))
        AddressItemToken.__m_ontology.add(Termin._new264("ПЕРЕКРЕСТОК", AddressDetailType.CROSS))
        AddressItemToken.__m_ontology.add(Termin._new264("НА ПЕРЕКРЕСТКЕ", AddressDetailType.CROSS))
        AddressItemToken.__m_ontology.add(Termin._new264("НА ТЕРРИТОРИИ", AddressDetailType.NEAR))
        AddressItemToken.__m_ontology.add(Termin._new264("СЕРЕДИНА", AddressDetailType.NEAR))
        AddressItemToken.__m_ontology.add(Termin._new264("ПРИМЫКАТЬ", AddressDetailType.NEAR))
        AddressItemToken.__m_ontology.add(Termin._new264("ГРАНИЧИТЬ", AddressDetailType.NEAR))
        t = Termin._new264("ВБЛИЗИ", AddressDetailType.NEAR)
        t.add_variant("У", False)
        t.add_abridge("ВБЛ.")
        t.add_variant("ВОЗЛЕ", False)
        t.add_variant("ОКОЛО", False)
        t.add_variant("НЕДАЛЕКО ОТ", False)
        t.add_variant("РЯДОМ С", False)
        t.add_variant("ГРАНИЦА", False)
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new264("РАЙОН", AddressDetailType.NEAR)
        t.add_abridge("Р-Н")
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new290("В РАЙОНЕ", "РАЙОН", AddressDetailType.NEAR)
        t.add_abridge("В Р-НЕ")
        AddressItemToken.__m_ontology.add(t)
        AddressItemToken.__m_ontology.add(Termin._new264("ПРИМЕРНО", AddressDetailType.UNDEFINED))
        AddressItemToken.__m_ontology.add(Termin._new264("ПОРЯДКА", AddressDetailType.UNDEFINED))
        AddressItemToken.__m_ontology.add(Termin._new264("ПРИБЛИЗИТЕЛЬНО", AddressDetailType.UNDEFINED))
        AddressItemToken.__m_ontology.add(Termin._new264("ОРИЕНТИР", AddressDetailType.UNDEFINED))
        AddressItemToken.__m_ontology.add(Termin._new264("НАПРАВЛЕНИЕ", AddressDetailType.UNDEFINED))
        t = Termin._new264("ОБЩЕЖИТИЕ", AddressDetailType.HOSTEL)
        t.add_abridge("ОБЩ.")
        t.add_abridge("ПОМ.ОБЩ.")
        AddressItemToken.__m_ontology.add(t)
        Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = True
        AddressItemToken.__m_ontology.add(Termin._new264("СЕВЕРНЕЕ", AddressDetailType.NORTH))
        AddressItemToken.__m_ontology.add(Termin._new264("СЕВЕР", AddressDetailType.NORTH))
        AddressItemToken.__m_ontology.add(Termin._new264("ЮЖНЕЕ", AddressDetailType.SOUTH))
        AddressItemToken.__m_ontology.add(Termin._new264("ЮГ", AddressDetailType.SOUTH))
        AddressItemToken.__m_ontology.add(Termin._new264("ЗАПАДНЕЕ", AddressDetailType.WEST))
        AddressItemToken.__m_ontology.add(Termin._new264("ЗАПАД", AddressDetailType.WEST))
        AddressItemToken.__m_ontology.add(Termin._new264("ВОСТОЧНЕЕ", AddressDetailType.EAST))
        AddressItemToken.__m_ontology.add(Termin._new264("ВОСТОК", AddressDetailType.EAST))
        AddressItemToken.__m_ontology.add(Termin._new264("СЕВЕРО-ЗАПАДНЕЕ", AddressDetailType.NORTHWEST))
        AddressItemToken.__m_ontology.add(Termin._new264("СЕВЕРО-ЗАПАД", AddressDetailType.NORTHWEST))
        AddressItemToken.__m_ontology.add(Termin._new264("СЕВЕРО-ВОСТОЧНЕЕ", AddressDetailType.NORTHEAST))
        AddressItemToken.__m_ontology.add(Termin._new264("СЕВЕРО-ВОСТОК", AddressDetailType.NORTHEAST))
        AddressItemToken.__m_ontology.add(Termin._new264("ЮГО-ЗАПАДНЕЕ", AddressDetailType.SOUTHWEST))
        AddressItemToken.__m_ontology.add(Termin._new264("ЮГО-ЗАПАД", AddressDetailType.SOUTHWEST))
        AddressItemToken.__m_ontology.add(Termin._new264("ЮГО-ВОСТОЧНЕЕ", AddressDetailType.SOUTHEAST))
        AddressItemToken.__m_ontology.add(Termin._new264("ЮГО-ВОСТОК", AddressDetailType.SOUTHEAST))
        t = Termin("ТАМ ЖЕ")
        t.add_abridge("ТАМЖЕ")
        AddressItemToken.__m_ontology.add(t)
        Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = False
    
    __m_ontology = None
    
    M_PLOT = None
    
    M_OWNER = None
    
    @staticmethod
    def _new231(_arg1 : 'AddressItemType', _arg2 : 'Token', _arg3 : 'Token', _arg4 : 'Referent') -> 'AddressItemToken':
        res = AddressItemToken(_arg1, _arg2, _arg3)
        res.referent = _arg4
        return res
    
    @staticmethod
    def _new233(_arg1 : 'AddressItemType', _arg2 : 'Token', _arg3 : 'Token', _arg4 : str) -> 'AddressItemToken':
        res = AddressItemToken(_arg1, _arg2, _arg3)
        res.value = _arg4
        return res
    
    @staticmethod
    def _new236(_arg1 : 'AddressItemType', _arg2 : 'Token', _arg3 : 'Token', _arg4 : 'AddressBuildingType', _arg5 : str) -> 'AddressItemToken':
        res = AddressItemToken(_arg1, _arg2, _arg3)
        res.building_type = _arg4
        res.value = _arg5
        return res
    
    @staticmethod
    def _new240(_arg1 : 'AddressItemType', _arg2 : 'Token', _arg3 : 'Token', _arg4 : str, _arg5 : 'AddressHouseType') -> 'AddressItemToken':
        res = AddressItemToken(_arg1, _arg2, _arg3)
        res.value = _arg4
        res.house_type = _arg5
        return res
    
    @staticmethod
    def _new241(_arg1 : 'AddressItemType', _arg2 : 'Token', _arg3 : 'Token', _arg4 : 'AddressHouseType', _arg5 : 'AddressBuildingType') -> 'AddressItemToken':
        res = AddressItemToken(_arg1, _arg2, _arg3)
        res.house_type = _arg4
        res.building_type = _arg5
        return res
    
    @staticmethod
    def _new242(_arg1 : 'AddressItemType', _arg2 : 'Token', _arg3 : 'Token', _arg4 : str, _arg5 : 'AddressHouseType', _arg6 : 'AddressBuildingType') -> 'AddressItemToken':
        res = AddressItemToken(_arg1, _arg2, _arg3)
        res.value = _arg4
        res.house_type = _arg5
        res.building_type = _arg6
        return res
    
    @staticmethod
    def _new254(_arg1 : 'AddressItemType', _arg2 : 'Token', _arg3 : 'Token', _arg4 : str, _arg5 : 'MorphCollection', _arg6 : 'AddressHouseType', _arg7 : 'AddressBuildingType') -> 'AddressItemToken':
        res = AddressItemToken(_arg1, _arg2, _arg3)
        res.value = _arg4
        res.morph = _arg5
        res.house_type = _arg6
        res.building_type = _arg7
        return res
    
    @staticmethod
    def _new260(_arg1 : 'AddressItemType', _arg2 : 'Token', _arg3 : 'Token', _arg4 : 'AddressDetailType') -> 'AddressItemToken':
        res = AddressItemToken(_arg1, _arg2, _arg3)
        res.detail_type = _arg4
        return res
    
    @staticmethod
    def _new329(_arg1 : 'AddressItemType', _arg2 : 'Token', _arg3 : 'Token', _arg4 : 'Referent', _arg5 : bool) -> 'AddressItemToken':
        res = AddressItemToken(_arg1, _arg2, _arg3)
        res.referent = _arg4
        res.is_doubt = _arg5
        return res