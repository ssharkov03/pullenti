# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
import io
from pullenti.unisharp.Utils import Utils

from pullenti.ner.core.NumberExType import NumberExType
from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.morph.MorphLang import MorphLang
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.ner.address.AddressReferent import AddressReferent
from pullenti.ner.Referent import Referent
from pullenti.ner.core.NumberHelper import NumberHelper
from pullenti.morph.MorphWordForm import MorphWordForm
from pullenti.morph.MorphClass import MorphClass
from pullenti.ner.date.DateReferent import DateReferent
from pullenti.morph.MorphCase import MorphCase
from pullenti.ner.geo.internal.NameTokenType import NameTokenType
from pullenti.morph.MorphBaseInfo import MorphBaseInfo
from pullenti.ner.geo.internal.Condition import Condition
from pullenti.morph.MorphologyService import MorphologyService
from pullenti.ner.address.StreetKind import StreetKind
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.TextToken import TextToken
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.address.internal.StreetItemType import StreetItemType
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.address.internal.AddressItemType import AddressItemType
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.address.AddressDetailType import AddressDetailType
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.geo.internal.GeoTokenData import GeoTokenData
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.geo.internal.GeoAnalyzerData import GeoAnalyzerData
from pullenti.ner.address.StreetReferent import StreetReferent
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.ner.Token import Token

class StreetItemToken(MetaToken):
    
    @staticmethod
    def try_parse_list(t : 'Token', max_count : int=10, ad : 'GeoAnalyzerData'=None) -> typing.List['StreetItemToken']:
        from pullenti.ner.geo.GeoAnalyzer import GeoAnalyzer
        if (t is None): 
            return None
        if (ad is None): 
            ad = GeoAnalyzer._get_data(t)
        if (ad is None): 
            return None
        if (ad.slevel > 2): 
            return None
        ad.slevel += 1
        res = StreetItemToken.__try_parse_list(t, max_count, ad)
        ad.slevel -= 1
        return res
    
    @staticmethod
    def __try_parse_list(t : 'Token', max_count : int, ad : 'GeoAnalyzerData') -> typing.List['StreetItemToken']:
        from pullenti.ner.address.internal.AddressItemToken import AddressItemToken
        from pullenti.ner.geo.internal.MiscLocationHelper import MiscLocationHelper
        from pullenti.ner.address.internal.StreetDefineHelper import StreetDefineHelper
        from pullenti.ner.geo.internal.CityItemToken import CityItemToken
        res = None
        sit = StreetItemToken.try_parse(t, None, False, ad)
        if (sit is not None): 
            res = list()
            res.append(sit)
            t = sit.end_token.next0_
        else: 
            res = StreetItemToken._try_parse_spec(t, None)
            if (res is None): 
                return None
            sit = res[len(res) - 1]
            t = sit.end_token.next0_
            sit2 = StreetItemToken.try_parse(t, None, False, None)
            if (sit2 is not None and sit2.typ == StreetItemType.NOUN): 
                pass
            elif (AddressItemToken.check_house_after(t, False, True)): 
                pass
            else: 
                return None
        first_pass2763 = True
        while True:
            if first_pass2763: first_pass2763 = False
            else: t = (None if t is None else t.next0_)
            if (not (t is not None)): break
            if (max_count > 0 and len(res) >= max_count): 
                break
            if (t.is_newline_before): 
                if (t.newlines_before_count > 1): 
                    break
                if (((t.whitespaces_after_count < 15) and sit is not None and sit.typ == StreetItemType.NOUN) and t.chars.is_capital_upper): 
                    pass
                else: 
                    break
            if (t.is_hiphen and sit is not None and ((sit.typ == StreetItemType.NAME or sit.typ == StreetItemType.STDNAME or ((sit.typ == StreetItemType.STDADJECTIVE and not sit.is_abridge))))): 
                sit1 = StreetItemToken.try_parse(t.next0_, sit, False, ad)
                if (sit1 is None): 
                    break
                if (sit1.typ == StreetItemType.NUMBER): 
                    tt = sit1.end_token.next0_
                    if (tt is not None and tt.is_comma): 
                        tt = tt.next0_
                    ok = False
                    ait = AddressItemToken.try_parse_pure_item(tt, None, None)
                    if (ait is not None): 
                        if (ait.typ == AddressItemType.HOUSE): 
                            ok = True
                    if (not ok): 
                        if (len(res) == 2 and res[0].typ == StreetItemType.NOUN): 
                            if (res[0].termin.canonic_text == "МИКРОРАЙОН"): 
                                ok = True
                    if (not ok and t.is_hiphen): 
                        ok = True
                    if (ok): 
                        sit = sit1
                        res.append(sit)
                        t = sit.end_token
                        sit.number_has_prefix = True
                        continue
                if (sit1.typ != StreetItemType.NAME and sit1.typ != StreetItemType.NAME): 
                    break
                if (t.is_whitespace_before and t.is_whitespace_after): 
                    break
                if (res[0].begin_token.previous is not None): 
                    aaa = AddressItemToken.try_parse_pure_item(res[0].begin_token.previous, None, None)
                    if (aaa is not None and aaa.typ == AddressItemType.DETAIL and aaa.detail_type == AddressDetailType.CROSS): 
                        break
                sit = sit1
                res.append(sit)
                t = sit.end_token
                continue
            elif (t.is_hiphen and sit is not None and sit.typ == StreetItemType.NUMBER): 
                sit1 = StreetItemToken.try_parse(t.next0_, None, False, ad)
                if (sit1 is not None and (((sit1.typ == StreetItemType.STDADJECTIVE or sit1.typ == StreetItemType.STDNAME or sit1.typ == StreetItemType.NAME) or sit1.typ == StreetItemType.NOUN))): 
                    sit.number_has_prefix = True
                    sit = sit1
                    res.append(sit)
                    t = sit.end_token
                    continue
            if (t.is_char('.') and sit is not None and sit.typ == StreetItemType.NOUN): 
                if (t.whitespaces_after_count > 1): 
                    break
                sit = StreetItemToken.try_parse(t.next0_, None, False, ad)
                if (sit is None): 
                    break
                if (sit.typ == StreetItemType.NUMBER or sit.typ == StreetItemType.STDADJECTIVE): 
                    sit1 = StreetItemToken.try_parse(sit.end_token.next0_, None, False, ad)
                    if (sit1 is not None and ((sit1.typ == StreetItemType.STDADJECTIVE or sit1.typ == StreetItemType.STDNAME or sit1.typ == StreetItemType.NAME))): 
                        pass
                    else: 
                        break
                elif (sit.typ != StreetItemType.NAME and sit.typ != StreetItemType.STDNAME and sit.typ != StreetItemType.AGE): 
                    break
                if (t.previous.get_morph_class_in_dictionary().is_noun): 
                    if (not sit.is_in_dictionary): 
                        tt = sit.end_token.next0_
                        has_house = False
                        first_pass2764 = True
                        while True:
                            if first_pass2764: first_pass2764 = False
                            else: tt = tt.next0_
                            if (not (tt is not None)): break
                            if (tt.is_newline_before): 
                                break
                            if (tt.is_comma): 
                                continue
                            ai = AddressItemToken.try_parse_pure_item(tt, None, None)
                            if (ai is not None and ((ai.typ == AddressItemType.HOUSE or ai.typ == AddressItemType.BUILDING or ai.typ == AddressItemType.CORPUS))): 
                                has_house = True
                                break
                            if (isinstance(tt, NumberToken)): 
                                has_house = True
                                break
                            vv = StreetItemToken.try_parse(tt, None, False, ad)
                            if (vv is None or vv.typ == StreetItemType.NOUN): 
                                break
                            tt = vv.end_token
                        if (not has_house): 
                            break
                    if (t.previous.previous is not None): 
                        npt11 = MiscLocationHelper._try_parse_npt(t.previous.previous)
                        if (npt11 is not None and npt11.end_token == t.previous): 
                            break
                res.append(sit)
            else: 
                sit = StreetItemToken.try_parse(t, res[len(res) - 1], False, ad)
                if (sit is None): 
                    spli = StreetItemToken._try_parse_spec(t, res[len(res) - 1])
                    if (spli is not None and len(spli) > 0): 
                        res.extend(spli)
                        t = spli[len(spli) - 1].end_token
                        continue
                    if (((isinstance(t, TextToken)) and ((len(res) == 2 or len(res) == 3)) and res[0].typ == StreetItemType.NOUN) and res[1].typ == StreetItemType.NUMBER and (((t.term == "ГОДА" or t.term == "МАЯ" or t.term == "МАРТА") or t.term == "СЪЕЗДА"))): 
                        sit = StreetItemToken._new343(t, t, StreetItemType.STDNAME, t.term)
                        res.append(sit)
                        continue
                    sit = res[len(res) - 1]
                    if (t is None): 
                        break
                    if (sit.typ == StreetItemType.NOUN and ((sit.termin.canonic_text == "МИКРОРАЙОН" or sit.termin.canonic_text == "МІКРОРАЙОН")) and (t.whitespaces_before_count < 2)): 
                        tt1 = t
                        if (tt1.is_hiphen and tt1.next0_ is not None): 
                            tt1 = tt1.next0_
                        if (BracketHelper.is_bracket(tt1, True) and tt1.next0_ is not None): 
                            tt1 = tt1.next0_
                        tt2 = tt1.next0_
                        br = False
                        if (BracketHelper.is_bracket(tt2, True)): 
                            tt2 = tt2.next0_
                            br = True
                        if (((isinstance(tt1, TextToken)) and tt1.length_char == 1 and tt1.chars.is_letter) and ((AddressItemToken.check_house_after(tt2, False, True) or tt2 is None))): 
                            sit = StreetItemToken._new343(t, (tt1.next0_ if br else tt1), StreetItemType.NAME, tt1.term)
                            ch1 = AddressItemToken.correct_char(sit.value[0])
                            if ((ord(ch1)) != 0 and ch1 != sit.value[0]): 
                                sit.alt_value = "{0}".format(ch1)
                            res.append(sit)
                            break
                    if (t.is_comma and (((sit.typ == StreetItemType.NAME or sit.typ == StreetItemType.STDNAME or sit.typ == StreetItemType.STDPARTOFNAME) or sit.typ == StreetItemType.STDADJECTIVE or ((sit.typ == StreetItemType.NUMBER and len(res) > 1 and (((res[len(res) - 2].typ == StreetItemType.NAME or res[len(res) - 2].typ == StreetItemType.STDNAME or res[len(res) - 2].typ == StreetItemType.STDADJECTIVE) or res[len(res) - 2].typ == StreetItemType.STDPARTOFNAME))))))): 
                        sit = StreetItemToken.try_parse(t.next0_, None, False, ad)
                        if (sit is not None and sit.typ == StreetItemType.NOUN): 
                            ttt = sit.end_token.next0_
                            if (ttt is not None and ttt.is_comma): 
                                ttt = ttt.next0_
                            add = AddressItemToken.try_parse_pure_item(ttt, None, None)
                            if (add is not None and ((add.typ == AddressItemType.HOUSE or add.typ == AddressItemType.CORPUS or add.typ == AddressItemType.BUILDING))): 
                                res.append(sit)
                                t = sit.end_token
                                continue
                    if (BracketHelper.can_be_start_of_sequence(t, True, False)): 
                        sit1 = res[len(res) - 1]
                        if (sit1.typ == StreetItemType.NOUN and ((sit1.noun_is_doubt_coef == 0 or (((isinstance(t.next0_, TextToken)) and not t.next0_.chars.is_all_lower))))): 
                            br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
                            if (br is not None and (br.length_char < 50)): 
                                sit2 = StreetItemToken.try_parse(t.next0_, None, False, ad)
                                if (sit2 is not None and sit2.end_token.next0_ == br.end_token): 
                                    if (sit2.value is None and sit2.typ == StreetItemType.NAME): 
                                        sit2.value = MiscHelper.get_text_value(sit2.begin_token, sit2.end_token, GetTextAttr.NO)
                                    sit2.begin_token = t
                                    sit2.is_in_brackets = True
                                    sit2.end_token = br.end_token
                                    t = sit2.end_token
                                    res.append(sit2)
                                    continue
                                res.append(StreetItemToken._new345(t, br.end_token, StreetItemType.NAME, MiscHelper.get_text_value(t, br.end_token, GetTextAttr.NO), True))
                                t = br.end_token
                                continue
                    if (t.is_hiphen and (isinstance(t.next0_, NumberToken)) and t.next0_.int_value is not None): 
                        sit = res[len(res) - 1]
                        if (sit.typ == StreetItemType.NOUN and (((sit.termin.canonic_text == "КВАРТАЛ" or sit.termin.canonic_text == "МИКРОРАЙОН" or sit.termin.canonic_text == "ГОРОДОК") or sit.termin.canonic_text == "МІКРОРАЙОН"))): 
                            sit = StreetItemToken._new346(t, t.next0_, StreetItemType.NUMBER, Utils.asObjectOrNull(t.next0_, NumberToken), True)
                            res.append(sit)
                            t = t.next0_
                            continue
                    break
                res.append(sit)
                if (sit.typ == StreetItemType.NAME): 
                    cou = 0
                    jj = 0
                    for jj in range(len(res) - 1, -1, -1):
                        if (res[jj].typ == StreetItemType.NAME): 
                            cou += 1
                        else: 
                            break
                    else: jj = -1
                    if (cou > 4): 
                        if (jj < 0): 
                            return None
                        del res[jj:jj+len(res) - jj]
                        break
                    if (len(res) > 1 and res[0].typ == StreetItemType.NOUN and res[0].is_road): 
                        tt = sit.end_token.next0_
                        if (tt is not None): 
                            if (tt.is_value("Ш", None) or tt.is_value("ШОССЕ", None) or tt.is_value("ШОС", None)): 
                                sit = sit.clone()
                                res[len(res) - 1] = sit
                                sit.end_token = tt
                                if (tt.next0_ is not None and tt.next0_.is_char('.') and tt.length_char <= 3): 
                                    sit.end_token = sit.end_token.next0_
            t = sit.end_token
        i = 0
        first_pass2765 = True
        while True:
            if first_pass2765: first_pass2765 = False
            else: i += 1
            if (not (i < (len(res) - 1))): break
            if (res[i].typ == StreetItemType.NAME and res[i + 1].typ == StreetItemType.NAME and (res[i].whitespaces_after_count < 3)): 
                is_prop = False
                is_pers = False
                if (res[i].begin_token.morph.class0_.is_noun): 
                    rt = res[i].kit.process_referent("PERSON", res[i].begin_token, None)
                    if (rt is not None): 
                        if (rt.referent.type_name == "PERSONPROPERTY"): 
                            is_prop = True
                        elif (rt.end_token == res[i + 1].end_token): 
                            is_pers = True
                if ((i == 0 and ((not is_prop and not is_pers)) and ((i + 2) < len(res))) and res[i + 2].typ == StreetItemType.NOUN and not res[i].begin_token.morph.class0_.is_adjective): 
                    if (MiscLocationHelper.check_geo_object_before(res[0].begin_token, False) and res[0].end_token.next0_ == res[1].begin_token and (res[0].whitespaces_after_count < 2)): 
                        pass
                    else: 
                        del res[i]
                        i -= 1
                        continue
                if (res[i].morph.class0_.is_adjective and res[i + 1].morph.class0_.is_adjective): 
                    if (res[i].end_token.next0_.is_hiphen): 
                        pass
                    elif (i == 1 and res[0].typ == StreetItemType.NOUN and len(res) == 3): 
                        pass
                    elif (i == 0 and len(res) == 3 and res[2].typ == StreetItemType.NOUN): 
                        pass
                    else: 
                        continue
                if (res[i].chars.value != res[i + 1].chars.value): 
                    rt = res[0].kit.process_referent("ORGANIZATION", res[i + 1].begin_token, None)
                    if (rt is not None): 
                        del res[i + 1:i + 1+len(res) - i - 1]
                        continue
                r = res[i].clone()
                r.value = MiscHelper.get_text_value(res[i].begin_token, res[i + 1].end_token, GetTextAttr.NO)
                if ("-" in r.value): 
                    r.value = r.value.replace('-', ' ')
                if (not res[i + 1].begin_token.previous.is_hiphen and ((not res[i].begin_token.morph.class0_.is_adjective or is_prop or is_pers))): 
                    if (is_pers and res[i + 1].end_token.get_morph_class_in_dictionary().is_proper_name and not res[i].end_token.get_morph_class_in_dictionary().is_proper_name): 
                        r.alt_value = MiscHelper.get_text_value(res[i].begin_token, res[i].end_token, GetTextAttr.NO)
                    else: 
                        r.alt_value = MiscHelper.get_text_value(res[i + 1].begin_token, res[i + 1].end_token, GetTextAttr.NO)
                    if ("-" in r.alt_value): 
                        r.alt_value = r.alt_value.replace('-', ' ')
                if (r.alt_value is None and res[i].begin_token.get_morph_class_in_dictionary().is_proper_name): 
                    r.alt_value = MiscHelper.get_text_value_of_meta_token(res[i + 1], GetTextAttr.NO)
                elif (r.alt_value is None and res[i + 1].begin_token.get_morph_class_in_dictionary().is_proper_name): 
                    r.alt_value = MiscHelper.get_text_value_of_meta_token(res[i], GetTextAttr.NO)
                r.end_token = res[i + 1].end_token
                r.exist_street = (None)
                r.is_in_dictionary = (res[i + 1].is_in_dictionary or res[i].is_in_dictionary)
                res[i] = r
                del res[i + 1]
                i -= 1
            elif ((res[i].typ == StreetItemType.NOUN and res[i + 1].typ == StreetItemType.NOUN and res[i].termin == res[i + 1].termin) and (res[i].whitespaces_after_count < 3)): 
                r = res[i].clone()
                r.end_token = res[i + 1].end_token
                del res[i + 1]
                i -= 1
        i = 0
        while i < (len(res) - 1): 
            if (res[i].typ == StreetItemType.STDADJECTIVE and res[i].end_token.is_char('.') and res[i + 1].__is_surname()): 
                r = res[i + 1].clone()
                r.value = res[i + 1].begin_token.term
                r.alt_value = MiscHelper.get_text_value(res[i].begin_token, res[i + 1].end_token, GetTextAttr.NO)
                r.begin_token = res[i].begin_token
                res[i + 1] = r
                del res[i]
                break
            i += 1
        i = 0
        while i < (len(res) - 1): 
            if ((res[i + 1].typ == StreetItemType.STDADJECTIVE and res[i + 1].end_token.is_char('.') and res[i + 1].begin_token.length_char == 1) and not res[i].begin_token.chars.is_all_lower): 
                if (res[i].__is_surname()): 
                    if (i == (len(res) - 2) or res[i + 2].typ != StreetItemType.NOUN): 
                        r = res[i].clone()
                        r.end_token = res[i + 1].end_token
                        res[i] = r
                        del res[i + 1]
                        break
            i += 1
        i = 0
        first_pass2766 = True
        while True:
            if first_pass2766: first_pass2766 = False
            else: i += 1
            if (not (i < (len(res) - 1))): break
            if (res[i].typ == StreetItemType.NAME or res[i].typ == StreetItemType.STDNAME or res[i].typ == StreetItemType.STDADJECTIVE): 
                if (res[i + 1].typ == StreetItemType.NOUN and not res[i + 1].is_abridge and res[i + 1].termin.canonic_text != "УЛИЦА"): 
                    res0 = list(res)
                    del res0[0:0+i + 1]
                    rtt = StreetDefineHelper._try_parse_street(res0, False, False, False)
                    if (rtt is not None): 
                        continue
                    i0 = -1
                    if (i == 1 and res[0].typ == StreetItemType.NOUN and len(res) == 3): 
                        i0 = 0
                    elif (i == 0 and len(res) == 3 and res[2].typ == StreetItemType.NOUN): 
                        i0 = 2
                    if (i0 < 0): 
                        continue
                    if (res[i0].termin == res[i + 1].termin): 
                        continue
                    r = res[i].clone()
                    r.alt_value = (Utils.ifNotNull(res[i].value, MiscHelper.get_text_value(res[i].begin_token, res[i].end_token, GetTextAttr.NO)))
                    if (res[i].typ == StreetItemType.STDADJECTIVE): 
                        adjs = MiscLocationHelper.get_std_adj_full(res[i].begin_token, res[i + 1].morph.gender, res[i + 1].morph.number, True)
                        if (adjs is not None and len(adjs) > 0): 
                            r.alt_value = adjs[0]
                    r.value = "{0} {1}".format(r.alt_value, res[i + 1].termin.canonic_text)
                    r.typ = StreetItemType.STDNAME
                    r.end_token = res[i + 1].end_token
                    res[i] = r
                    rr = res[i0].clone()
                    rr.alt_termin = res[i + 1].termin
                    res[i0] = rr
                    del res[i + 1]
                    i -= 1
        if ((len(res) >= 3 and res[0].typ == StreetItemType.NOUN and res[0].termin.canonic_text == "КВАРТАЛ") and ((res[1].typ == StreetItemType.NAME or res[1].typ == StreetItemType.STDNAME)) and res[2].typ == StreetItemType.NOUN): 
            if (len(res) == 3 or res[3].typ == StreetItemType.NUMBER): 
                res0 = list(res)
                del res0[0:0+2]
                rtt = StreetDefineHelper._try_parse_street(res0, False, False, False)
                if (rtt is None or res0[0].chars.is_capital_upper): 
                    r = res[1].clone()
                    r.value = "{0} {1}".format(MiscHelper.get_text_value_of_meta_token(res[1], GetTextAttr.NO), res[2].termin.canonic_text)
                    r.end_token = res[2].end_token
                    res[1] = r
                    del res[2]
        if ((len(res) >= 3 and res[0].typ == StreetItemType.NOUN and res[0].termin.canonic_text == "КВАРТАЛ") and ((res[2].typ == StreetItemType.NAME or res[2].typ == StreetItemType.STDNAME)) and res[1].typ == StreetItemType.NOUN): 
            if (len(res) == 3 or res[3].typ == StreetItemType.NUMBER): 
                r = res[1].clone()
                r.value = "{0} {1}".format(MiscHelper.get_text_value_of_meta_token(res[2], GetTextAttr.NO), res[1].termin.canonic_text)
                r.end_token = res[2].end_token
                r.typ = StreetItemType.NAME
                res[1] = r
                del res[2]
        if ((len(res) >= 3 and res[0].typ == StreetItemType.NUMBER and not res[0].is_number_km) and res[1].typ == StreetItemType.NOUN): 
            if (not MiscLocationHelper.is_user_param_address(res[0])): 
                nt = Utils.asObjectOrNull(res[0].begin_token, NumberToken)
                if (nt is not None and nt.typ == NumberSpellingType.DIGIT and nt.morph.class0_.is_undefined): 
                    return None
        if (len(res) > 1 and res[0].typ == StreetItemType.NOUN): 
            if (res[1].typ == StreetItemType.NOUN and res[1].noun_can_be_name): 
                r = res[1].clone()
                r.typ = StreetItemType.NAME
                r.value = res[1].termin.canonic_text
                res[1] = r
            elif ((len(res) > 2 and res[1].typ == StreetItemType.NUMBER and res[2].typ == StreetItemType.NOUN) and res[2].noun_can_be_name): 
                r = res[2].clone()
                r.typ = StreetItemType.NAME
                r.value = res[2].termin.canonic_text
                res[2] = r
        ii0 = -1
        ii1 = -1
        if (len(res) > 0 and res[0].typ == StreetItemType.NOUN and res[0].is_road): 
            ii1 = 0
            ii0 = ii1
            if (((ii0 + 1) < len(res)) and res[ii0 + 1].typ == StreetItemType.NUMBER and res[ii0 + 1].is_number_km): 
                ii0 += 1
        elif ((len(res) > 1 and res[0].typ == StreetItemType.NUMBER and res[0].is_number_km) and res[1].typ == StreetItemType.NOUN and res[1].is_road): 
            ii1 = 1
            ii0 = ii1
        if (ii0 >= 0): 
            if (len(res) == (ii0 + 1)): 
                tt = res[ii0].end_token.next0_
                num = StreetItemToken.__try_attach_road_num(tt)
                if (num is not None): 
                    res.append(num)
                    tt = num.end_token.next0_
                    res[0].is_abridge = False
                if (tt is not None and (isinstance(tt.get_referent(), GeoReferent))): 
                    g1 = Utils.asObjectOrNull(tt.get_referent(), GeoReferent)
                    tt = tt.next0_
                    if (tt is not None and tt.is_hiphen): 
                        tt = tt.next0_
                    g2 = (None if tt is None else Utils.asObjectOrNull(tt.get_referent(), GeoReferent))
                    if (g2 is not None): 
                        if (g1.is_city and g2.is_city): 
                            nam = StreetItemToken._new347(res[0].end_token.next0_, tt, StreetItemType.NAME)
                            nam.value = "{0} - {1}".format(g1.to_string_ex(True, tt.kit.base_language, 0), g2.to_string_ex(True, tt.kit.base_language, 0)).upper()
                            nam.alt_value = "{0} - {1}".format(g2.to_string_ex(True, tt.kit.base_language, 0), g1.to_string_ex(True, tt.kit.base_language, 0)).upper()
                            res.append(nam)
                elif (BracketHelper.is_bracket(tt, False)): 
                    br = BracketHelper.try_parse(tt, BracketParseAttr.NO, 100)
                    if (br is not None): 
                        nam = StreetItemToken._new348(tt, br.end_token, StreetItemType.NAME, True)
                        nam.value = MiscHelper.get_text_value(tt.next0_, br.end_token, GetTextAttr.NO)
                        res.append(nam)
            elif ((len(res) == (ii0 + 2) and res[ii0 + 1].typ == StreetItemType.NAME and res[ii0 + 1].end_token.next0_ is not None) and res[ii0 + 1].end_token.next0_.is_hiphen): 
                tt = res[ii0 + 1].end_token.next0_.next0_
                g2 = (None if tt is None else Utils.asObjectOrNull(tt.get_referent(), GeoReferent))
                te = None
                name2 = None
                if (g2 is None and tt is not None): 
                    rt = tt.kit.process_referent("GEO", tt, None)
                    if (rt is not None): 
                        te = rt.end_token
                        name2 = rt.referent.to_string_ex(True, te.kit.base_language, 0)
                    else: 
                        cits2 = CityItemToken.try_parse_list(tt, 2, None)
                        if (cits2 is not None): 
                            if (len(cits2) == 1 and ((cits2[0].typ == CityItemToken.ItemType.PROPERNAME or cits2[0].typ == CityItemToken.ItemType.CITY))): 
                                if (cits2[0].onto_item is not None): 
                                    name2 = cits2[0].onto_item.canonic_text
                                else: 
                                    name2 = cits2[0].value
                                te = cits2[0].end_token
                elif (g2 is not None): 
                    te = tt
                    name2 = g2.to_string_ex(True, te.kit.base_language, 0)
                if (((g2 is not None and g2.is_city)) or ((g2 is None and name2 is not None))): 
                    r = res[ii0 + 1].clone()
                    r.alt_value = "{0} - {1}".format(name2, Utils.ifNotNull(res[ii0 + 1].value, res[ii0 + 1].get_source_text())).upper()
                    r.value = "{0} - {1}".format(Utils.ifNotNull(res[ii0 + 1].value, res[ii0 + 1].get_source_text()), name2).upper()
                    r.end_token = te
                    res[ii0 + 1] = r
            nn = StreetItemToken.__try_attach_road_num(res[len(res) - 1].end_token.next0_)
            if (nn is not None): 
                res.append(nn)
                res[ii1].is_abridge = False
            if (len(res) > (ii0 + 1) and res[ii0 + 1].typ == StreetItemType.NAME and res[ii1].termin.canonic_text == "АВТОДОРОГА"): 
                if (res[ii0 + 1].begin_token.is_value("ФЕДЕРАЛЬНЫЙ", None)): 
                    return None
                npt = MiscLocationHelper._try_parse_npt(res[ii0 + 1].begin_token)
                if (npt is not None and len(npt.adjectives) > 0): 
                    if (npt.end_token.is_value("ЗНАЧЕНИЕ", None)): 
                        return None
        while len(res) > 1:
            it = res[len(res) - 1]
            it0 = (res[len(res) - 2] if len(res) > 1 else None)
            if (it.typ == StreetItemType.NUMBER and not it.number_has_prefix and not it.is_number_km): 
                if (isinstance(it.begin_token, NumberToken)): 
                    if (not it.begin_token.morph.class0_.is_adjective or it.begin_token.morph.class0_.is_noun): 
                        if (AddressItemToken.check_house_after(it.end_token.next0_, False, True)): 
                            it.number_has_prefix = True
                        elif (it0 is not None and it0.typ == StreetItemType.NOUN and (((it0.termin.canonic_text == "МИКРОРАЙОН" or it0.termin.canonic_text == "МІКРОРАЙОН" or it0.termin.canonic_text == "КВАРТАЛ") or it0.termin.canonic_text == "ГОРОДОК"))): 
                            ait = AddressItemToken.try_parse_pure_item(it.begin_token, None, None)
                            if (ait is not None and ait.typ == AddressItemType.NUMBER and ait.end_char > it.end_char): 
                                it.number = (None)
                                it.value = ait.value
                                it.end_token = ait.end_token
                                it.typ = StreetItemType.NAME
                        elif (it0 is not None and it0.termin is not None and it0.termin.canonic_text == "ПОЧТОВОЕ ОТДЕЛЕНИЕ"): 
                            it.number_has_prefix = True
                        elif (it0 is not None and it0.begin_token.is_value("ЛИНИЯ", None)): 
                            it.number_has_prefix = True
                        elif (len(res) == 2 and res[0].typ == StreetItemType.NOUN and (res[0].whitespaces_after_count < 2)): 
                            pass
                        elif (it.begin_token.morph.class0_.is_adjective and it.begin_token.typ == NumberSpellingType.WORDS and it.begin_token.chars.is_capital_upper): 
                            it.number_has_prefix = True
                        elif (it.begin_token.previous.is_hiphen): 
                            it.number_has_prefix = True
                        else: 
                            del res[len(res) - 1]
                            continue
                    else: 
                        it.number_has_prefix = True
            break
        if (len(res) == 0): 
            return None
        i = 0
        while i < len(res): 
            if ((res[i].typ == StreetItemType.NOUN and res[i].chars.is_capital_upper and (((res[i].termin.canonic_text == "НАБЕРЕЖНАЯ" or res[i].termin.canonic_text == "МИКРОРАЙОН" or res[i].termin.canonic_text == "НАБЕРЕЖНА") or res[i].termin.canonic_text == "МІКРОРАЙОН" or res[i].termin.canonic_text == "ГОРОДОК"))) and res[i].begin_token.is_value(res[i].termin.canonic_text, None)): 
                ok = False
                if (i > 0 and ((res[i - 1].typ == StreetItemType.NOUN or res[i - 1].typ == StreetItemType.STDADJECTIVE))): 
                    ok = True
                elif (i > 1 and ((res[i - 1].typ == StreetItemType.STDADJECTIVE or res[i - 1].typ == StreetItemType.NUMBER)) and res[i - 2].typ == StreetItemType.NOUN): 
                    ok = True
                if (ok): 
                    r = res[i].clone()
                    r.typ = StreetItemType.NAME
                    res[i] = r
            i += 1
        last = res[len(res) - 1]
        for kk in range(2):
            ttt = last.end_token.next0_
            if (((last.typ == StreetItemType.NAME and ttt is not None and ttt.length_char == 1) and ttt.chars.is_all_upper and (ttt.whitespaces_before_count < 2)) and ttt.next0_ is not None and ttt.next0_.is_char('.')): 
                if (AddressItemToken.try_parse_pure_item(ttt, None, None) is not None): 
                    break
                last = last.clone()
                last.end_token = ttt.next0_
                res[len(res) - 1] = last
        if (len(res) > 1): 
            if (res[len(res) - 1]._org0_ is not None): 
                del res[len(res) - 1]
        if (len(res) == 0): 
            return None
        return res
    
    def __init__(self, begin : 'Token', end : 'Token') -> None:
        super().__init__(begin, end, None)
        self.typ = StreetItemType.NOUN
        self.termin = None;
        self.alt_termin = None;
        self.exist_street = None;
        self.number = None;
        self.number_has_prefix = False
        self.is_number_km = False
        self.value = None;
        self.alt_value = None;
        self.alt_value2 = None;
        self.is_abridge = False
        self.is_in_dictionary = False
        self.is_in_brackets = False
        self.has_std_suffix = False
        self.noun_is_doubt_coef = 0
        self.noun_can_be_name = False
        self.is_road_name = False
        self.is_railway = False
        self._cond = None;
        self._no_geo_in_this_token = False
        self._org0_ = None;
        self._orto_terr = None;
    
    @property
    def is_road(self) -> bool:
        if (self.termin is None): 
            return False
        if ((self.termin.canonic_text == "АВТОДОРОГА" or self.termin.canonic_text == "ШОССЕ" or self.termin.canonic_text == "ТРАКТ") or self.termin.canonic_text == "АВТОШЛЯХ" or self.termin.canonic_text == "ШОСЕ"): 
            return True
        return False
    
    def clone(self) -> 'StreetItemToken':
        res = StreetItemToken(self.begin_token, self.end_token)
        res.morph = self.morph
        res.typ = self.typ
        res.termin = self.termin
        res.alt_termin = self.alt_termin
        res.value = self.value
        res.alt_value = self.alt_value
        res.alt_value2 = self.alt_value2
        res.is_railway = self.is_railway
        res.is_road_name = self.is_road_name
        res.noun_can_be_name = self.noun_can_be_name
        res.noun_is_doubt_coef = self.noun_is_doubt_coef
        res.has_std_suffix = self.has_std_suffix
        res.is_in_brackets = self.is_in_brackets
        res.is_abridge = self.is_abridge
        res.is_in_dictionary = self.is_in_dictionary
        res.exist_street = self.exist_street
        res.number = self.number
        res.number_has_prefix = self.number_has_prefix
        res.is_number_km = self.is_number_km
        res._cond = self._cond
        res._org0_ = self._org0_
        if (self._orto_terr is not None): 
            res._orto_terr = self._orto_terr.clone()
        return res
    
    def __str__(self) -> str:
        res = io.StringIO()
        print("{0}".format(Utils.enumToString(self.typ)), end="", file=res, flush=True)
        if (self.value is not None): 
            print(" {0}".format(self.value), end="", file=res, flush=True)
            if (self.alt_value is not None): 
                print("/{0}".format(self.alt_value), end="", file=res, flush=True)
        if (self.exist_street is not None): 
            print(" {0}".format(str(self.exist_street)), end="", file=res, flush=True)
        if (self.termin is not None): 
            print(" {0}".format(str(self.termin)), end="", file=res, flush=True)
            if (self.alt_termin is not None): 
                print("/{0}".format(str(self.alt_termin)), end="", file=res, flush=True)
        elif (self.number is not None): 
            print(" {0}".format(str(self.number)), end="", file=res, flush=True)
            if (self.is_number_km): 
                print("км", end="", file=res)
        else: 
            print(" {0}".format(super().__str__()), end="", file=res, flush=True)
        if (self._org0_ is not None): 
            print(" Org: {0}".format(self._org0_), end="", file=res, flush=True)
        if (self.is_abridge): 
            print(" (?)", end="", file=res)
        if (self._orto_terr is not None): 
            print(" TERR: {0}".format(self._orto_terr), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    def __is_surname(self) -> bool:
        if (self.typ != StreetItemType.NAME): 
            return False
        if (not (isinstance(self.end_token, TextToken))): 
            return False
        nam = self.end_token.term
        if (len(nam) > 4): 
            if (LanguageHelper.ends_with_ex(nam, "А", "Я", "КО", "ЧУКА")): 
                if (not LanguageHelper.ends_with_ex(nam, "АЯ", "ЯЯ", None, None)): 
                    return True
        return False
    
    SPEED_REGIME = False
    
    @staticmethod
    def _prepare_all_data(t0 : 'Token') -> None:
        from pullenti.ner.geo.GeoAnalyzer import GeoAnalyzer
        if (not StreetItemToken.SPEED_REGIME): 
            return
        ad = GeoAnalyzer._get_data(t0)
        if (ad is None): 
            return
        ad.sregime = False
        t = t0
        while t is not None: 
            d = Utils.asObjectOrNull(t.tag, GeoTokenData)
            prev = None
            kk = 0
            tt = t.previous
            first_pass2767 = True
            while True:
                if first_pass2767: first_pass2767 = False
                else: tt = tt.previous; kk += 1
                if (not (tt is not None and (kk < 10))): break
                dd = Utils.asObjectOrNull(tt.tag, GeoTokenData)
                if (dd is None or dd.street is None): 
                    continue
                if (dd.street.end_token.next0_ == t): 
                    prev = dd.street
                if (t.previous is not None and t.previous.is_hiphen and dd.street.end_token.next0_ == t.previous): 
                    prev = dd.street
            str0_ = StreetItemToken.try_parse(t, prev, False, ad)
            if (str0_ is not None): 
                if (d is None): 
                    d = GeoTokenData(t)
                d.street = str0_
                if (str0_._no_geo_in_this_token): 
                    tt = str0_.begin_token
                    while tt is not None and tt.end_char <= str0_.end_char: 
                        dd = Utils.asObjectOrNull(tt.tag, GeoTokenData)
                        if (dd is None): 
                            dd = GeoTokenData(tt)
                        dd.no_geo = True
                        tt = tt.next0_
            t = t.next0_
        ad.sregime = True
    
    @staticmethod
    def try_parse(t : 'Token', prev : 'StreetItemToken'=None, in_search : bool=False, ad : 'GeoAnalyzerData'=None) -> 'StreetItemToken':
        from pullenti.ner.address.internal.AddressItemToken import AddressItemToken
        from pullenti.ner.geo.GeoAnalyzer import GeoAnalyzer
        if (t is None): 
            return None
        if ((isinstance(t, TextToken)) and t.length_char == 1 and t.is_char_of(",.:")): 
            return None
        if (ad is None): 
            ad = (Utils.asObjectOrNull(GeoAnalyzer._get_data(t), GeoAnalyzerData))
        if (ad is None): 
            return None
        if ((StreetItemToken.SPEED_REGIME and ((ad.sregime or ad.all_regime)) and not in_search) and not (isinstance(t, ReferentToken))): 
            d = Utils.asObjectOrNull(t.tag, GeoTokenData)
            if (d is None): 
                return None
            if (d.street is not None): 
                if (d.street._cond is None): 
                    return d.street
                if (d.street._cond.check()): 
                    return d.street
                return None
            if (d.org0_ is not None): 
                return StreetItemToken._new232(t, d.org0_.end_token, StreetItemType.FIX, d.org0_)
            return None
        if (ad.slevel > 3): 
            return None
        ad.slevel += 1
        res = StreetItemToken._try_parse(t, False, prev, in_search)
        if (res is not None and res.typ != StreetItemType.NOUN): 
            tt = Utils.asObjectOrNull(res.end_token.next0_, TextToken)
            if (tt is not None and tt.is_char('(')): 
                if (res.value is None): 
                    res.value = MiscHelper.get_text_value(res.begin_token, res.end_token, GetTextAttr.NO)
                ait = AddressItemToken.try_parse(tt.next0_, False, None, None)
                if ((ait is not None and ait.typ == AddressItemType.STREET and ait.end_token.next0_ is not None) and ait.end_token.next0_.is_char(')')): 
                    res._orto_terr = ait
                    res.end_token = ait.end_token.next0_
                else: 
                    sit = StreetItemToken.try_parse(tt.next0_, None, False, None)
                    if ((sit is not None and ((sit.typ == StreetItemType.NAME or sit.typ == StreetItemType.STDNAME)) and sit.end_token.next0_ is not None) and sit.end_token.next0_.is_char(')')): 
                        ait = AddressItemToken(AddressItemType.STREET, tt.next0_, sit.end_token)
                        stre = StreetReferent()
                        stre.kind = StreetKind.AREA
                        stre._add_typ("территория")
                        stre._add_name(sit)
                        ait.referent = (stre)
                        res._orto_terr = ait
                        res.end_token = sit.end_token.next0_
        ad.slevel -= 1
        return res
    
    @staticmethod
    def _try_parse(t : 'Token', ignore_onto : bool, prev : 'StreetItemToken', in_search : bool) -> 'StreetItemToken':
        from pullenti.ner.address.internal.AddressItemToken import AddressItemToken
        from pullenti.ner.geo.internal.MiscLocationHelper import MiscLocationHelper
        from pullenti.ner.geo.internal.NameToken import NameToken
        from pullenti.ner.geo.GeoAnalyzer import GeoAnalyzer
        from pullenti.ner.geo.internal.OrgItemToken import OrgItemToken
        from pullenti.ner.geo.internal.CityItemToken import CityItemToken
        from pullenti.ner.geo.internal.TerrItemToken import TerrItemToken
        if (t is None): 
            return None
        if (prev is not None and prev.is_road): 
            res1 = StreetItemToken._try_parse_spec(t, prev)
            if (res1 is not None and res1[0].typ == StreetItemType.NAME): 
                return res1[0]
        if (t.is_value("ТЕРРИТОРИЯ", None)): 
            return None
        if ((t.is_value("А", None) or t.is_value("АД", None) or t.is_value("АВТ", None)) or t.is_value("АВТОДОР", None)): 
            tt1 = t
            if (t.is_value("А", None)): 
                tt1 = t.next0_
                if (tt1 is not None and tt1.is_char_of("\\/")): 
                    tt1 = tt1.next0_
                if (tt1 is not None and ((tt1.is_value("Д", None) or tt1.is_value("М", None)))): 
                    pass
                else: 
                    tt1 = (None)
            elif (tt1.next0_ is not None and tt1.next0_.is_char('.')): 
                tt1 = tt1.next0_
            if (tt1 is not None): 
                res = StreetItemToken._new350(t, tt1, StreetItemType.NOUN, StreetItemToken.__m_road)
                if (prev is not None and ((prev.is_road_name or prev.is_road))): 
                    return res
                next0__ = StreetItemToken.try_parse(tt1.next0_, res, False, None)
                if (next0__ is not None and next0__.is_road_name): 
                    return res
                if (t.previous is not None): 
                    if (t.previous.is_value("КМ", None) or t.previous.is_value("КИЛОМЕТР", None)): 
                        return res
        t0 = t
        tn = None
        if (t.is_value("ИМЕНИ", None) or t.is_value("ІМЕНІ", None)): 
            tn = t
        elif (t.is_value("ИМ", None) or t.is_value("ІМ", None)): 
            tn = t
            if (tn.next0_ is not None and tn.next0_.is_char('.')): 
                tn = tn.next0_
        if (tn is not None): 
            org0_ = OrgItemToken.try_parse(t, None)
            if (org0_ is not None): 
                return StreetItemToken._new232(t0, org0_.end_token, StreetItemType.FIX, org0_)
            if (tn.next0_ is None or tn.newlines_after_count > 1): 
                return None
            t = tn.next0_
        if (t.is_value("ДВАЖДЫ", None) or t.is_value("ТРИЖДЫ", None) or t.is_value("ЧЕТЫРЕЖДЫ", None)): 
            if (t.next0_ is not None): 
                t = t.next0_
        if (t.is_value("ГЕРОЙ", None)): 
            ters = TerrItemToken.try_parse_list(t.next0_, 3, None)
            if (ters is not None and len(ters) > 0): 
                tt1 = None
                if (ters[0].onto_item is not None): 
                    tt1 = ters[0].end_token.next0_
                elif (ters[0].termin_item is not None and len(ters) > 1 and ters[1].onto_item is not None): 
                    tt1 = ters[1].end_token.next0_
                nnn = StreetItemToken.try_parse(tt1, prev, in_search, None)
                if (nnn is not None and nnn.typ == StreetItemType.NAME): 
                    return nnn
        if (t.is_value("НЕЗАВИСИМОСТЬ", None)): 
            ters = TerrItemToken.try_parse_list(t.next0_, 3, None)
            if (ters is not None and len(ters) > 0): 
                tok2 = None
                if (ters[0].onto_item is not None): 
                    tok2 = ters[0]
                elif (ters[0].termin_item is not None and len(ters) > 1 and ters[1].onto_item is not None): 
                    tok2 = ters[1]
                if (tok2 is not None): 
                    res = StreetItemToken._new347(t, tok2.end_token, StreetItemType.NAME)
                    res.value = "НЕЗАВИСИМОСТИ {0}".format(tok2.onto_item.canonic_text)
                    return res
        if (t.is_value("ЖУКОВА", None)): 
            pass
        nt = NumberHelper.try_parse_age(t)
        if (nt is not None and nt.int_value is not None): 
            return StreetItemToken._new353(nt.begin_token, nt.end_token, StreetItemType.AGE, nt)
        nt = Utils.asObjectOrNull(t, NumberToken)
        if ((nt) is not None): 
            if (nt.int_value is None or nt.int_value == 0): 
                return None
            res = StreetItemToken._new354(nt, nt, StreetItemType.NUMBER, nt, nt.morph)
            if ((t.next0_ is not None and t.next0_.is_hiphen and t.next0_.next0_ is not None) and t.next0_.next0_.is_value("Я", None)): 
                res.end_token = t.next0_.next0_
            nex = NumberHelper.try_parse_number_with_postfix(t)
            if (nex is not None): 
                if (nex.ex_typ == NumberExType.KILOMETER): 
                    res.is_number_km = True
                    res.end_token = nex.end_token
                    tt2 = res.end_token.next0_
                    if (tt2 is not None and tt2.is_hiphen): 
                        tt2 = tt2.next0_
                    nex2 = NumberHelper.try_parse_number_with_postfix(tt2)
                    if (nex2 is not None and nex2.ex_typ == NumberExType.METER): 
                        res.end_token = nex2.end_token
                else: 
                    return None
            aaa = AddressItemToken.try_parse_pure_item(t, None, None)
            if (aaa is not None and aaa.typ == AddressItemType.NUMBER and aaa.end_char > t.end_char): 
                if (prev is not None and prev.typ == StreetItemType.NOUN and (((t.next0_.is_hiphen or prev.termin.canonic_text == "КВАРТАЛ" or prev.termin.canonic_text == "ЛИНИЯ") or prev.termin.canonic_text == "АЛЛЕЯ" or prev.termin.canonic_text == "ДОРОГА"))): 
                    if (StreetItemToken._m_ontology.try_parse(aaa.end_token, TerminParseAttr.NO) is not None): 
                        pass
                    else: 
                        res.end_token = aaa.end_token
                        res.value = aaa.value
                        res.number = (None)
                else: 
                    return None
            if (nt.typ == NumberSpellingType.WORDS and nt.morph.class0_.is_adjective): 
                npt2 = MiscLocationHelper._try_parse_npt(t)
                if (npt2 is not None and npt2.end_char > t.end_char and npt2.morph.number != MorphNumber.SINGULAR): 
                    if (t.next0_ is not None and not t.next0_.chars.is_all_lower): 
                        pass
                    else: 
                        return None
            if (not res.is_number_km and prev is not None and prev.begin_token.is_value("КИЛОМЕТР", None)): 
                res.is_number_km = True
            return res
        ntt = MiscHelper.check_number_prefix(t)
        if ((ntt is not None and (isinstance(ntt, NumberToken)) and prev is not None) and ntt.int_value is not None): 
            return StreetItemToken._new346(t, ntt, StreetItemType.NUMBER, Utils.asObjectOrNull(ntt, NumberToken), True)
        rrr = OrgItemToken.try_parse_railway(t)
        if (rrr is not None): 
            return rrr
        if ((isinstance(t, ReferentToken)) and t.begin_token == t.end_token and not t.chars.is_all_lower): 
            if (prev is not None and prev.typ == StreetItemType.NOUN): 
                if (((prev.morph.number) & (MorphNumber.PLURAL)) == (MorphNumber.UNDEFINED)): 
                    return StreetItemToken._new343(t, t, StreetItemType.NAME, MiscHelper.get_text_value_of_meta_token(Utils.asObjectOrNull(t, ReferentToken), GetTextAttr.NO))
        tt = Utils.asObjectOrNull(t, TextToken)
        npt = None
        if (tt is not None and tt.morph.class0_.is_adjective): 
            if (tt.chars.is_capital_upper or MiscLocationHelper.is_user_param_address(tt) or ((prev is not None and prev.typ == StreetItemType.NUMBER and tt.is_value("ТРАНСПОРТНЫЙ", None)))): 
                npt = MiscLocationHelper._try_parse_npt(tt)
                if (npt is not None and "-" in MiscHelper.get_text_value_of_meta_token(npt.noun, GetTextAttr.NO)): 
                    npt = (None)
                elif (npt is not None and len(npt.adjectives) > 0 and ((npt.adjectives[0].is_newline_after or npt.noun.is_newline_before))): 
                    npt = (None)
                tte = tt.next0_
                if (npt is not None and len(npt.adjectives) == 1): 
                    tte = npt.end_token
                if (tte is not None): 
                    if ((((((((((tte.is_value("ВАЛ", None) or tte.is_value("ТРАКТ", None) or tte.is_value("ПОЛЕ", None)) or tte.is_value("МАГИСТРАЛЬ", None) or tte.is_value("СПУСК", None)) or tte.is_value("ВЗВОЗ", None) or tte.is_value("РЯД", None)) or tte.is_value("СЛОБОДА", None) or tte.is_value("РОЩА", None)) or tte.is_value("ПРУД", None) or tte.is_value("СЪЕЗД", None)) or tte.is_value("КОЛЬЦО", None) or tte.is_value("МАГІСТРАЛЬ", None)) or tte.is_value("УЗВІЗ", None) or tte.is_value("ЛІНІЯ", None)) or tte.is_value("УЗВІЗ", None) or tte.is_value("ГАЙ", None)) or tte.is_value("СТАВОК", None) or tte.is_value("ЗЇЗД", None)) or tte.is_value("КІЛЬЦЕ", None)): 
                        sit = StreetItemToken._new357(tt, tte, True)
                        sit.typ = StreetItemType.NAME
                        if (npt is None or len(npt.adjectives) == 0): 
                            sit.value = MiscHelper.get_text_value(tt, tte, GetTextAttr.NO)
                        elif (npt.morph.case_.is_genitive): 
                            sit.value = MiscHelper.get_text_value(tt, tte, GetTextAttr.NO)
                            sit.alt_value = npt.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False)
                        else: 
                            sit.value = npt.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False)
                        tok2 = StreetItemToken._m_ontology.try_parse(tt, TerminParseAttr.NO)
                        if (tok2 is not None and tok2.termin is not None and tok2.end_token == tte): 
                            sit.termin = tok2.termin
                        return sit
                if (npt is not None and npt.begin_token != npt.end_token and len(npt.adjectives) <= 1): 
                    oo = StreetItemToken._m_ontology.try_parse(t, TerminParseAttr.NO)
                    if (oo is not None and (Utils.valToEnum(oo.termin.tag, StreetItemType)) == StreetItemType.NOUN): 
                        npt = (None)
                if (npt is not None and npt.begin_token != npt.end_token and len(npt.adjectives) <= 1): 
                    tt1 = npt.end_token.next0_
                    if (tt1 is not None and tt1.is_comma): 
                        tt1 = tt1.next0_
                    ok = False
                    sti1 = StreetItemToken.try_parse(tt1, None, False, None)
                    if (sti1 is not None and sti1.typ == StreetItemType.NOUN): 
                        ok = True
                    elif (tt1 is not None and tt1.is_hiphen and (isinstance(tt1.next0_, NumberToken))): 
                        ok = True
                    else: 
                        ait = AddressItemToken.try_parse_pure_item(tt1, None, None)
                        if (ait is not None): 
                            if (ait.typ == AddressItemType.HOUSE): 
                                ok = True
                            elif (ait.typ == AddressItemType.NUMBER): 
                                ait2 = AddressItemToken.try_parse_pure_item(npt.end_token, None, None)
                                if (ait2 is None): 
                                    ok = True
                    if (ok): 
                        sti1 = StreetItemToken.try_parse(npt.end_token, None, False, None)
                        if (sti1 is not None and sti1.typ == StreetItemType.NOUN): 
                            ok = (sti1.noun_is_doubt_coef >= 2 and sti1.termin.canonic_text != "КВАРТАЛ")
                        else: 
                            tok2 = StreetItemToken._m_ontology.try_parse(npt.end_token, TerminParseAttr.NO)
                            if (tok2 is not None): 
                                typ_ = Utils.valToEnum(tok2.termin.tag, StreetItemType)
                                if (typ_ == StreetItemType.NOUN or typ_ == StreetItemType.STDPARTOFNAME): 
                                    ok = False
                    if (ok): 
                        sit = StreetItemToken(tt, npt.end_token)
                        sit.typ = StreetItemType.NAME
                        sit.value = MiscHelper.get_text_value(tt, npt.end_token, GetTextAttr.NO)
                        sit.alt_value = npt.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False)
                        return sit
        if (tt is not None and (isinstance(tt.next0_, TextToken)) and ((tt.next0_.chars.is_capital_upper or MiscLocationHelper.is_user_param_address(tt)))): 
            if ((tt.is_value("ВАЛ", None) or tt.is_value("ТРАКТ", None) or tt.is_value("ПОЛЕ", None)) or tt.is_value("КОЛЬЦО", None) or tt.is_value("КІЛЬЦЕ", None)): 
                sit = StreetItemToken.try_parse(tt.next0_, None, False, None)
                if (sit is not None and sit.typ == StreetItemType.NAME): 
                    if (sit.value is not None): 
                        sit.value = "{0} {1}".format(sit.value, tt.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False))
                    else: 
                        sit.value = "{0} {1}".format(sit.get_source_text().upper(), tt.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False))
                    if (sit.alt_value is not None): 
                        sit.alt_value = "{0} {1}".format(sit.alt_value, tt.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False))
                    sit.begin_token = tt
                    return sit
        if (((tt is not None and tt.length_char == 1 and tt.chars.is_all_lower) and tt.next0_ is not None and tt.next0_.is_char('.')) and tt.kit.base_language.is_ru): 
            if (tt.is_value("М", None) or tt.is_value("M", None)): 
                if (prev is not None and prev.typ == StreetItemType.NOUN): 
                    pass
                else: 
                    tok1 = StreetItemToken._m_ontology.try_parse(tt, TerminParseAttr.NO)
                    if (tok1 is not None and tok1.termin.canonic_text == "МИКРОРАЙОН"): 
                        return StreetItemToken._new358(tt, tok1.end_token, tok1.termin, StreetItemType.NOUN)
                    return StreetItemToken._new359(tt, tt.next0_, StreetItemToken.__m_metro, StreetItemType.NOUN, True)
        ot = None
        if (t.kit.ontology is not None and ot is None): 
            ots = t.kit.ontology.attach_token(AddressReferent.OBJ_TYPENAME, t)
            if (ots is not None): 
                ot = ots[0]
        if (ot is not None and ot.begin_token == ot.end_token and ot.morph.class0_.is_adjective): 
            tok0 = StreetItemToken._m_ontology.try_parse(t, TerminParseAttr.NO)
            if (tok0 is not None): 
                if ((Utils.valToEnum(tok0.termin.tag, StreetItemType)) == StreetItemType.STDADJECTIVE): 
                    ot = (None)
        if (ot is not None): 
            res0 = StreetItemToken._new360(ot.begin_token, ot.end_token, StreetItemType.NAME, Utils.asObjectOrNull(ot.item.referent, StreetReferent), ot.morph, True)
            return res0
        if (prev is not None and prev.typ == StreetItemType.NOUN and prev.termin.canonic_text == "ПРОЕЗД"): 
            if (t.is_value("ПР", None)): 
                res1 = StreetItemToken._new343(t, t, StreetItemType.NAME, "ПРОЕКТИРУЕМЫЙ")
                if (t.next0_ is not None and t.next0_.is_char('.')): 
                    res1.end_token = t.next0_
                return res1
        tok = (None if ignore_onto else StreetItemToken._m_ontology.try_parse(t, TerminParseAttr.NO))
        tok_ex = (None if ignore_onto else StreetItemToken._m_ontology_ex.try_parse(t, TerminParseAttr.NO))
        if (tok is None): 
            tok = tok_ex
        elif (tok_ex is not None and tok_ex.end_char > tok.end_char): 
            tok = tok_ex
        if (tok is not None and tok.termin.canonic_text == "НАБЕРЕЖНАЯ" and not tok.chars.is_all_lower): 
            nex = StreetItemToken.try_parse(tok.end_token.next0_, None, False, None)
            if (nex is not None and ((nex.typ == StreetItemType.NOUN or nex.typ == StreetItemType.STDADJECTIVE))): 
                tok = (None)
            elif (nex is not None and nex.typ == StreetItemType.NAME and ((nex.begin_token.is_value("РЕКА", None) or nex.begin_token.is_value("РЕЧКА", "РІЧКА")))): 
                nex.begin_token = t
                nex.value = "НАБЕРЕЖНАЯ {0}".format(nex.value)
                if (nex.alt_value is not None): 
                    nex.alt_value = "НАБЕРЕЖНАЯ {0}".format(nex.alt_value)
                return nex
            elif (((t.morph.gender) & (MorphGender.FEMINIE)) == (MorphGender.UNDEFINED) and t.length_char > 7): 
                tok = (None)
        if ((tok is not None and t.length_char == 1 and t.is_value("Б", None)) and (isinstance(t.previous, NumberToken)) and t.previous.value == "26"): 
            tok = (None)
        if (tok is not None and tok.begin_token == tok.end_token): 
            if (((Utils.valToEnum(tok.termin.tag, StreetItemType)) == StreetItemType.NAME or t.is_value("ГАРАЖНО", None) or t.length_char == 1) or t.is_value("СТ", None)): 
                org0_ = OrgItemToken.try_parse(t, None)
                if (org0_ is not None): 
                    tok = (None)
                    if (t.length_char < 3): 
                        return StreetItemToken._new232(t, org0_.end_token, StreetItemType.FIX, org0_)
            elif ((Utils.valToEnum(tok.termin.tag, StreetItemType)) == StreetItemType.STDADJECTIVE and (isinstance(t, TextToken)) and t.term.endswith("О")): 
                tok = (None)
            elif ((Utils.valToEnum(tok.termin.tag, StreetItemType)) == StreetItemType.NOUN and t.is_value("САД", None) and t.previous is not None): 
                if (t.previous.is_value("ДЕТСКИЙ", None)): 
                    tok = (None)
                elif (t.previous.is_hiphen and t.previous.previous is not None and t.previous.previous.is_value("ЯСЛИ", None)): 
                    tok = (None)
        if (tok is not None and not ignore_onto): 
            if ((Utils.valToEnum(tok.termin.tag, StreetItemType)) == StreetItemType.NUMBER): 
                if ((isinstance(tok.end_token.next0_, NumberToken)) and tok.end_token.next0_.int_value is not None): 
                    return StreetItemToken._new363(t, tok.end_token.next0_, StreetItemType.NUMBER, Utils.asObjectOrNull(tok.end_token.next0_, NumberToken), True, tok.morph)
                return None
            if (tt is None): 
                return None
            abr = True
            swichVal = Utils.valToEnum(tok.termin.tag, StreetItemType)
            if (swichVal == StreetItemType.STDADJECTIVE): 
                while True:
                    if (tt.chars.is_all_lower and prev is None and not in_search): 
                        if (not MiscLocationHelper.is_user_param_address(tok)): 
                            return None
                    if (tt.is_value(tok.termin.canonic_text, None)): 
                        abr = False
                    elif (tt.length_char == 1): 
                        if (not tt.is_whitespace_before and not tt.previous.is_char_of(":,.")): 
                            break
                        if (not tok.end_token.is_char('.')): 
                            if (not tt.chars.is_all_upper and not in_search): 
                                break
                            oo2 = False
                            if (tok.end_token.is_newline_after and prev is not None): 
                                oo2 = True
                            elif (in_search): 
                                oo2 = True
                            else: 
                                next0__ = StreetItemToken.try_parse(tok.end_token.next0_, None, False, None)
                                if (next0__ is not None and ((next0__.typ == StreetItemType.NAME or next0__.typ == StreetItemType.NOUN))): 
                                    oo2 = True
                                elif (AddressItemToken.check_house_after(tok.end_token.next0_, False, True) and prev is not None): 
                                    oo2 = True
                            if (oo2): 
                                return StreetItemToken._new364(tok.begin_token, tok.end_token, StreetItemType.STDADJECTIVE, tok.termin, abr, tok.morph)
                            break
                        tt2 = tok.end_token.next0_
                        if (tt2 is not None and tt2.is_hiphen): 
                            tt2 = tt2.next0_
                        if (isinstance(tt2, TextToken)): 
                            if (tt2.length_char == 1 and tt2.chars.is_all_upper): 
                                break
                            if (tt2.chars.is_capital_upper): 
                                is_sur = False
                                txt = tt2.term
                                if (LanguageHelper.ends_with(txt, "ОГО")): 
                                    is_sur = True
                                else: 
                                    for wf in tt2.morph.items: 
                                        if (wf.class0_.is_proper_surname and wf.is_in_dictionary): 
                                            if (wf.case_.is_genitive): 
                                                is_sur = True
                                                break
                                if (is_sur): 
                                    break
                    return StreetItemToken._new364(tok.begin_token, tok.end_token, StreetItemType.STDADJECTIVE, tok.termin, abr, tok.morph)
            elif (swichVal == StreetItemType.NOUN): 
                while True:
                    if (tt.is_value(tok.termin.canonic_text, None) or tok.end_token.is_value(tok.termin.canonic_text, None) or tt.is_value("УЛ", None)): 
                        abr = False
                    elif (tok.begin_token != tok.end_token and ((tok.begin_token.next0_.is_hiphen or tok.begin_token.next0_.is_char_of("/\\")))): 
                        pass
                    elif (not tt.chars.is_all_lower and tt.length_char == 1): 
                        break
                    elif (tt.length_char == 1): 
                        if (not tt.is_whitespace_before): 
                            if (tt.previous is not None and tt.previous.is_char_of(",")): 
                                pass
                            else: 
                                return None
                        if (tok.end_token.is_char('.')): 
                            pass
                        elif (tok.begin_token != tok.end_token and tok.begin_token.next0_ is not None and ((tok.begin_token.next0_.is_hiphen or tok.begin_token.next0_.is_char_of("/\\")))): 
                            pass
                        elif (tok.length_char > 5): 
                            pass
                        elif (tok.begin_token == tok.end_token and tt.is_value("Ш", None) and tt.chars.is_all_lower): 
                            if (prev is not None and ((prev.typ == StreetItemType.NAME or prev.typ == StreetItemType.STDNAME or prev.typ == StreetItemType.STDPARTOFNAME))): 
                                pass
                            else: 
                                sii = StreetItemToken.try_parse(tt.next0_, None, False, None)
                                if (sii is not None and (((sii.typ == StreetItemType.NAME or sii.typ == StreetItemType.STDNAME or sii.typ == StreetItemType.STDPARTOFNAME) or sii.typ == StreetItemType.AGE))): 
                                    pass
                                else: 
                                    return None
                        else: 
                            return None
                    elif (((tt.term == "КВ" or tt.term == "КВАРТ")) and not tok.end_token.is_value("Л", None)): 
                        pass
                    if ((tok.end_token == tok.begin_token and not t.chars.is_all_lower and t.morph.class0_.is_proper_surname) and t.chars.is_cyrillic_letter): 
                        if (((t.morph.number) & (MorphNumber.PLURAL)) != (MorphNumber.UNDEFINED)): 
                            return None
                    if (tt.term == "ДОРОГОЙ"): 
                        return None
                    alt = None
                    if (tok.begin_token.is_value("ПР", None) and ((tok.begin_token == tok.end_token or tok.begin_token.next0_.is_char('.')))): 
                        alt = StreetItemToken.__m_prospect
                    res = StreetItemToken._new366(tok.begin_token, tok.end_token, StreetItemType.NOUN, tok.termin, alt, abr, tok.morph, (tok.termin.tag2 if isinstance(tok.termin.tag2, int) else 0))
                    if ((not abr and tok.begin_token == tok.end_token and tok.begin_token.chars.is_capital_upper) and tok.begin_token.get_morph_class_in_dictionary().is_noun): 
                        if (tok.morph.case_.is_nominative and not tok.morph.case_.is_genitive): 
                            res.noun_can_be_name = True
                        elif ((t.next0_ is not None and t.next0_.is_hiphen and (isinstance(t.next0_.next0_, NumberToken))) and not t.chars.is_all_lower): 
                            res.noun_can_be_name = True
                    if (res.is_road): 
                        next0__ = StreetItemToken._try_parse(res.end_token.next0_, False, None, False)
                        if (next0__ is not None and next0__.is_road): 
                            res.end_token = next0__.end_token
                            res.noun_is_doubt_coef = 0
                            res.is_abridge = False
                    return res
            elif (swichVal == StreetItemType.STDNAME): 
                is_post_off = tok.termin.canonic_text == "ПОЧТОВОЕ ОТДЕЛЕНИЕ" or tok.termin.canonic_text == "ПРОЕКТИРУЕМЫЙ"
                if (tok.begin_token.chars.is_all_lower and not is_post_off and tok.end_token.chars.is_all_lower): 
                    if (StreetItemToken.check_keyword(tok.end_token.next0_)): 
                        pass
                    elif (prev is not None and ((prev.typ == StreetItemType.NUMBER or prev.typ == StreetItemType.NOUN))): 
                        pass
                    else: 
                        return None
                sits = StreetItemToken._new367(tok.begin_token, tok.end_token, StreetItemType.STDNAME, tok.morph, tok.termin.canonic_text)
                if (tok.termin.additional_vars is not None and len(tok.termin.additional_vars) > 0): 
                    if (tok.termin.additional_vars[0].canonic_text.find(' ') < 0): 
                        sits.alt_value = sits.value
                        sits.value = tok.termin.additional_vars[0].canonic_text
                    else: 
                        sits.alt_value = tok.termin.additional_vars[0].canonic_text
                    if (len(tok.termin.additional_vars) > 1): 
                        if (tok.termin.additional_vars[0].canonic_text.find(' ') < 0): 
                            sits.alt_value2 = sits.value
                            sits.value = tok.termin.additional_vars[1].canonic_text
                        else: 
                            sits.alt_value2 = tok.termin.additional_vars[1].canonic_text
                if (tok.begin_token != tok.end_token and not is_post_off): 
                    if (tok.begin_token.next0_ == tok.end_token): 
                        if (((StreetItemToken.__m_std_ont_misc.try_parse(tok.begin_token, TerminParseAttr.NO) is not None or tok.begin_token.get_morph_class_in_dictionary().is_proper_name or (tok.begin_token.length_char < 4))) and tok.end_token.length_char > 2 and ((tok.end_token.morph.class0_.is_proper_surname or not tok.end_token.get_morph_class_in_dictionary().is_proper_name))): 
                            sits.alt_value2 = MiscHelper.get_text_value(tok.end_token, tok.end_token, GetTextAttr.NO)
                        elif (((tok.end_token.get_morph_class_in_dictionary().is_proper_name or StreetItemToken.__m_std_ont_misc.try_parse(tok.end_token, TerminParseAttr.NO) is not None)) and ((tok.begin_token.morph.class0_.is_proper_surname))): 
                            sits.alt_value2 = MiscHelper.get_text_value(tok.begin_token, tok.begin_token, GetTextAttr.NO)
                return sits
            elif (swichVal == StreetItemType.STDPARTOFNAME): 
                if (prev is not None and prev.typ == StreetItemType.NAME): 
                    nam = Utils.ifNotNull(prev.value, MiscHelper.get_text_value_of_meta_token(prev, GetTextAttr.NO))
                    if (prev.alt_value is None): 
                        prev.alt_value = "{0} {1}".format(tok.termin.canonic_text, nam)
                    else: 
                        prev.alt_value = "{0} {1}".format(tok.termin.canonic_text, prev.alt_value)
                    prev.end_token = tok.end_token
                    prev.value = nam
                    return StreetItemToken.try_parse(tok.end_token.next0_, prev, False, None)
                tt1 = tok.end_token
                vvv = tok.termin.canonic_text
                if ((isinstance(tt1.next0_, NumberToken)) and tt1.next0_.next0_ is not None and tt1.next0_.next0_.is_value("РАНГ", None)): 
                    tt1 = tt1.next0_.next0_
                tok2 = StreetItemToken._m_ontology.try_parse(tt1.next0_, TerminParseAttr.NO)
                if (tok2 is not None and (Utils.valToEnum(tok2.termin.tag, StreetItemType)) == StreetItemType.STDPARTOFNAME): 
                    tt1 = tok2.end_token
                    vvv = "{0} {1}".format(vvv, tok2.termin.canonic_text)
                sit = StreetItemToken.try_parse(tt1.next0_, None, False, None)
                if (sit is None or tt1.whitespaces_after_count > 3): 
                    for m in tok.morph.items: 
                        if (m.number == MorphNumber.PLURAL and m.case_.is_genitive): 
                            return StreetItemToken._new367(tok.begin_token, tt1, StreetItemType.NAME, tok.morph, MiscHelper.get_text_value_of_meta_token(tok, GetTextAttr.NO))
                    if (in_search): 
                        return StreetItemToken._new369(tok.begin_token, tt1, StreetItemType.STDPARTOFNAME, tok.morph, tok.termin)
                    return None
                if (sit.typ != StreetItemType.NAME and sit.typ != StreetItemType.NOUN): 
                    return None
                if (sit.typ == StreetItemType.NOUN): 
                    if (tok.morph.number == MorphNumber.PLURAL): 
                        return StreetItemToken._new367(tok.begin_token, tt1, StreetItemType.NAME, tok.morph, MiscHelper.get_text_value_of_meta_token(tok, GetTextAttr.NO))
                    else: 
                        return StreetItemToken._new369(tok.begin_token, tt1, StreetItemType.NAME, tok.morph, tok.termin)
                if (sit.value is not None): 
                    if (sit.alt_value is None): 
                        sit.alt_value = "{0} {1}".format(vvv, sit.value)
                    else: 
                        sit.value = "{0} {1}".format(vvv, sit.value)
                elif (sit.exist_street is None): 
                    sit.alt_value = sit.begin_token.term
                    sit.value = "{0} {1}".format(vvv, sit.begin_token.term)
                sit.begin_token = tok.begin_token
                return sit
            elif (swichVal == StreetItemType.NAME): 
                if (tok.begin_token.chars.is_all_lower): 
                    if (prev is not None and prev.typ == StreetItemType.STDADJECTIVE): 
                        pass
                    elif (prev is not None and prev.typ == StreetItemType.NOUN and AddressItemToken.check_house_after(tok.end_token.next0_, True, False)): 
                        pass
                    elif (t.is_value("ПРОЕКТИРУЕМЫЙ", None) or t.is_value("МИРА", None)): 
                        pass
                    else: 
                        nex = StreetItemToken.try_parse(tok.end_token.next0_, None, False, None)
                        if (nex is not None and nex.typ == StreetItemType.NOUN): 
                            tt2 = nex.end_token.next0_
                            while tt2 is not None and tt2.is_char_of(",."):
                                tt2 = tt2.next0_
                            if (tt2 is None or tt2.whitespaces_before_count > 1): 
                                return None
                            if (AddressItemToken.check_house_after(tt2, False, True)): 
                                pass
                            else: 
                                return None
                        else: 
                            return None
                sit0 = StreetItemToken.try_parse(tok.begin_token, prev, True, None)
                if (sit0 is not None and sit0.typ == StreetItemType.NAME and sit0.end_char > tok.end_char): 
                    sit0.is_in_dictionary = True
                    return sit0
                sit1 = StreetItemToken._new372(tok.begin_token, tok.end_token, StreetItemType.NAME, tok.morph, True)
                if ((not tok.is_whitespace_after and tok.end_token.next0_ is not None and tok.end_token.next0_.is_hiphen) and not tok.end_token.next0_.is_whitespace_after): 
                    sit2 = StreetItemToken.try_parse(tok.end_token.next0_.next0_, None, False, None)
                    if (sit2 is not None and ((sit2.typ == StreetItemType.NAME or sit2.typ == StreetItemType.STDPARTOFNAME or sit2.typ == StreetItemType.STDNAME))): 
                        sit1.end_token = sit2.end_token
                if (npt is not None and (sit1.end_char < npt.end_char) and StreetItemToken._m_ontology.try_parse(npt.end_token, TerminParseAttr.NO) is None): 
                    sit2 = StreetItemToken._try_parse(t, True, prev, in_search)
                    if (sit2 is not None and sit2.end_char > sit1.end_char): 
                        return sit2
                return sit1
            elif (swichVal == StreetItemType.FIX): 
                return StreetItemToken._new373(tok.begin_token, tok.end_token, StreetItemType.FIX, tok.morph, True, tok.termin)
        if (tt is not None and ((tt.is_value("КИЛОМЕТР", None) or tt.is_value("КМ", None)))): 
            tt1 = tt
            if (tt1.next0_ is not None and tt1.next0_.is_char('.')): 
                tt1 = tt1.next0_
            if ((tt1.whitespaces_after_count < 3) and (isinstance(tt1.next0_, NumberToken))): 
                sit = StreetItemToken._new347(tt, tt1.next0_, StreetItemType.NUMBER)
                sit.number = (Utils.asObjectOrNull(tt1.next0_, NumberToken))
                sit.is_number_km = True
                return sit
            next0__ = StreetItemToken.try_parse(tt.next0_, None, in_search, None)
            if (next0__ is not None and ((next0__.is_railway or next0__.is_road))): 
                next0__.begin_token = tt
                return next0__
        if (tt is not None): 
            if (((tt.is_value("РЕКА", None) or tt.is_value("РЕЧКА", "РІЧКА"))) and tt.next0_ is not None and ((not tt.next0_.chars.is_all_lower or MiscLocationHelper.is_user_param_address(tt)))): 
                nam = NameToken.try_parse(tt.next0_, NameTokenType.CITY, 0, False)
                if (nam is not None and nam.name is not None and nam.number is None): 
                    return StreetItemToken._new375(tt, nam.end_token, StreetItemType.NAME, tt.morph, MiscHelper.get_text_value(tt, nam.end_token, GetTextAttr.NO), nam.name)
            if ((isinstance(t.previous, NumberToken)) and t.previous.value == "26"): 
                if (tt.is_value("БАКИНСКИЙ", None) or "БАКИНСК".startswith(tt.term)): 
                    tt2 = tt
                    if (tt2.next0_ is not None and tt2.next0_.is_char('.')): 
                        tt2 = tt2.next0_
                    if (isinstance(tt2.next0_, TextToken)): 
                        tt2 = tt2.next0_
                        if (tt2.is_value("КОМИССАР", None) or tt2.is_value("КОММИССАР", None) or "КОМИС".startswith(tt2.term)): 
                            if (tt2.next0_ is not None and tt2.next0_.is_char('.')): 
                                tt2 = tt2.next0_
                            sit = StreetItemToken._new376(tt, tt2, StreetItemType.STDNAME, True, "БАКИНСКИХ КОМИССАРОВ", tt2.morph)
                            return sit
            if ((tt.next0_ is not None and ((tt.next0_.is_char('.') or ((tt.next0_.is_hiphen and tt.length_char == 1)))) and ((not tt.chars.is_all_lower or MiscLocationHelper.is_user_param_address(tt)))) and (tt.next0_.whitespaces_after_count < 3) and (isinstance(tt.next0_.next0_, TextToken))): 
                tt1 = tt.next0_.next0_
                if (tt1 is not None and tt1.is_hiphen and tt1.next0_ is not None): 
                    tt1 = tt1.next0_
                if (tt.length_char == 1 and tt1.length_char == 1 and (isinstance(tt1.next0_, TextToken))): 
                    if (tt1.is_and and tt1.next0_.chars.is_all_upper and tt1.next0_.length_char == 1): 
                        tt1 = tt1.next0_
                    if ((tt1.chars.is_all_upper and tt1.next0_.is_char('.') and (tt1.next0_.whitespaces_after_count < 3)) and (isinstance(tt1.next0_.next0_, TextToken))): 
                        tt1 = tt1.next0_.next0_
                    elif ((tt1.chars.is_all_upper and (tt1.whitespaces_after_count < 3) and (isinstance(tt1.next0_, TextToken))) and not tt1.next0_.chars.is_all_lower): 
                        tt1 = tt1.next0_
                sit = StreetItemToken.try_parse(tt1, None, False, None)
                if (sit is not None and (isinstance(tt1, TextToken))): 
                    str0_ = tt1.term
                    ok = False
                    mc = tt1.get_morph_class_in_dictionary()
                    cla = tt.next0_.next0_.get_morph_class_in_dictionary()
                    if (sit.is_in_dictionary): 
                        ok = True
                    elif (sit.__is_surname() or cla.is_proper_surname): 
                        ok = True
                    elif (LanguageHelper.ends_with(str0_, "ОЙ") and ((cla.is_proper_surname or ((sit.typ == StreetItemType.NAME and sit.is_in_dictionary))))): 
                        ok = True
                    elif (LanguageHelper.ends_with_ex(str0_, "ГО", "ИХ", None, None)): 
                        ok = True
                    elif ((tt1.is_whitespace_before and not mc.is_undefined and not mc.is_proper_surname) and not mc.is_proper_name): 
                        if (AddressItemToken.check_house_after(sit.end_token.next0_, False, True)): 
                            ok = True
                    elif (prev is not None and prev.typ == StreetItemType.NOUN and ((not prev.is_abridge or prev.length_char > 2))): 
                        ok = True
                    elif ((prev is not None and prev.typ == StreetItemType.NAME and sit.typ == StreetItemType.NOUN) and AddressItemToken.check_house_after(sit.end_token.next0_, False, True)): 
                        ok = True
                    elif (sit.typ == StreetItemType.NAME and AddressItemToken.check_house_after(sit.end_token.next0_, False, True)): 
                        if (MiscLocationHelper.check_geo_object_before(tt, False)): 
                            ok = True
                        else: 
                            ad = GeoAnalyzer._get_data(t)
                            if (not ad.sregime and StreetItemToken.SPEED_REGIME): 
                                ok = True
                                sit._cond = Condition._new377(tt, True)
                    if (not ok and MiscLocationHelper.is_user_param_address(tt) and ((sit.typ == StreetItemType.NAME or sit.typ == StreetItemType.STDADJECTIVE))): 
                        sit1 = StreetItemToken.try_parse(sit.end_token.next0_, None, False, None)
                        if (sit1 is not None and sit1.typ == StreetItemType.NOUN): 
                            ok = True
                        elif (AddressItemToken.check_house_after(sit.end_token.next0_, True, False)): 
                            ok = True
                    if (ok): 
                        sit.begin_token = tt
                        sit.value = str0_
                        return sit
            if (tt.chars.is_cyrillic_letter and tt.length_char > 1 and not tt.morph.class0_.is_preposition): 
                if (tt.is_value("ГЕРОЙ", None) or tt.is_value("ЗАЩИТНИК", "ЗАХИСНИК")): 
                    tt2 = None
                    if ((isinstance(tt.next0_, ReferentToken)) and (isinstance(tt.next0_.get_referent(), GeoReferent))): 
                        tt2 = tt.next0_
                    else: 
                        npt2 = MiscLocationHelper._try_parse_npt(tt.next0_)
                        if (npt2 is not None and npt2.morph.case_.is_genitive): 
                            tt2 = npt2.end_token
                        else: 
                            tee = TerrItemToken.check_onto_item(tt.next0_)
                            if (tee is not None): 
                                tt2 = tee.end_token
                            else: 
                                tee = CityItemToken.check_onto_item(tt.next0_)
                                if ((tee) is not None): 
                                    tt2 = tee.end_token
                    if (tt2 is not None): 
                        re = StreetItemToken._new378(tt, tt2, StreetItemType.STDPARTOFNAME, MiscHelper.get_text_value(tt, tt2, GetTextAttr.NO), True)
                        sit = StreetItemToken.try_parse(tt2.next0_, None, False, None)
                        if (sit is None or sit.typ != StreetItemType.NAME): 
                            ok2 = False
                            if (sit is not None and ((sit.typ == StreetItemType.STDADJECTIVE or sit.typ == StreetItemType.NOUN))): 
                                ok2 = True
                            elif (AddressItemToken.check_house_after(tt2.next0_, False, True)): 
                                ok2 = True
                            elif (tt2.is_newline_after): 
                                ok2 = True
                            if (ok2): 
                                sit = StreetItemToken._new379(tt, tt2, StreetItemType.NAME, True)
                                sit.value = MiscHelper.get_text_value(tt, tt2, GetTextAttr.NO)
                                return sit
                            return re
                        if (sit.value is None): 
                            sit.value = MiscHelper.get_text_value_of_meta_token(sit, GetTextAttr.NO)
                        if (sit.alt_value is None): 
                            sit.alt_value = sit.value
                            sit.value = "{0} {1}".format(re.value, sit.value)
                        else: 
                            sit.value = "{0} {1}".format(re.value, sit.value)
                        sit.begin_token = tt
                        return sit
                ani = NumberHelper.try_parse_anniversary(t)
                if (ani is not None): 
                    return StreetItemToken._new380(t, ani.end_token, StreetItemType.AGE, ani, str(ani.value))
                if (prev is not None and prev.typ == StreetItemType.NOUN): 
                    pass
                else: 
                    org0_ = OrgItemToken.try_parse(t, None)
                    if (org0_ is not None): 
                        if (org0_.is_gsk or org0_.has_terr_keyword): 
                            return StreetItemToken._new232(t, org0_.end_token, StreetItemType.FIX, org0_)
                ok1 = False
                cond = None
                if (not tt.chars.is_all_lower): 
                    ait = AddressItemToken.try_parse_pure_item(tt, None, None)
                    if (ait is not None): 
                        if (tt.next0_ is not None and tt.next0_.is_hiphen): 
                            ok1 = True
                    else: 
                        ok1 = True
                elif (prev is not None and prev.typ == StreetItemType.NOUN): 
                    if (AddressItemToken.check_house_after(tt.next0_, False, False)): 
                        if (not AddressItemToken.check_house_after(tt, False, False)): 
                            ok1 = True
                    if (not ok1): 
                        tt1 = prev.begin_token.previous
                        if (tt1 is not None and tt1.is_comma): 
                            tt1 = tt1.previous
                        if (tt1 is not None and (isinstance(tt1.get_referent(), GeoReferent))): 
                            ok1 = True
                        elif (MiscLocationHelper.is_user_param_address(prev)): 
                            ok1 = True
                        else: 
                            ad = GeoAnalyzer._get_data(t)
                            if (not ad.sregime and StreetItemToken.SPEED_REGIME): 
                                ok1 = True
                                cond = Condition._new377(prev.begin_token, True)
                elif (tt.whitespaces_after_count < 2): 
                    nex = StreetItemToken._m_ontology.try_parse(tt.next0_, TerminParseAttr.NO)
                    if (nex is not None and nex.termin is not None): 
                        if (nex.termin.canonic_text == "ПЛОЩАДЬ"): 
                            if (tt.is_value("ОБЩИЙ", None)): 
                                return None
                        tt1 = tt.previous
                        if (tt1 is not None and tt1.is_comma): 
                            tt1 = tt1.previous
                        if (tt1 is not None and (isinstance(tt1.get_referent(), GeoReferent))): 
                            ok1 = True
                        elif (AddressItemToken.check_house_after(nex.end_token.next0_, False, False)): 
                            ok1 = True
                        elif (MiscLocationHelper.is_user_param_address(tt)): 
                            ok1 = True
                    elif (MiscLocationHelper.is_user_param_address(tt) and tt.length_char > 3): 
                        if (AddressItemToken.try_parse_pure_item(tt, None, None) is None): 
                            ok1 = True
                if (ok1): 
                    dc = tt.get_morph_class_in_dictionary()
                    if (dc.is_adverb): 
                        if (not ((dc.is_proper))): 
                            if (tt.next0_ is not None and tt.next0_.is_hiphen): 
                                pass
                            else: 
                                return None
                    res = StreetItemToken._new383(tt, tt, StreetItemType.NAME, tt.morph, cond)
                    if ((tt.next0_ is not None and ((tt.next0_.is_hiphen or tt.next0_.is_char_of("\\/"))) and (isinstance(tt.next0_.next0_, TextToken))) and not tt.is_whitespace_after and not tt.next0_.is_whitespace_after): 
                        ok2 = AddressItemToken.check_house_after(tt.next0_.next0_.next0_, False, False) or tt.next0_.next0_.is_newline_after
                        if (not ok2): 
                            te2 = StreetItemToken.try_parse(tt.next0_.next0_.next0_, None, False, None)
                            if (te2 is not None and te2.typ == StreetItemType.NOUN): 
                                ok2 = True
                        if (((not ok2 and tt.next0_.is_hiphen and not tt.is_whitespace_after) and not tt.next0_.is_whitespace_after and (isinstance(tt.next0_.next0_, TextToken))) and tt.next0_.next0_.length_char > 3): 
                            ok2 = True
                        if (ok2): 
                            res.end_token = tt.next0_.next0_
                            res.value = "{0} {1}".format(MiscHelper.get_text_value(tt, tt, GetTextAttr.NO), MiscHelper.get_text_value(res.end_token, res.end_token, GetTextAttr.NO))
                    elif ((tt.whitespaces_after_count < 2) and (isinstance(tt.next0_, TextToken)) and tt.next0_.chars.is_letter): 
                        if (tt.next0_.is_value("БИ", None)): 
                            if (res.value is None): 
                                res.value = MiscHelper.get_text_value(tt, tt, GetTextAttr.NO)
                            res.end_token = tt.next0_
                            res.value = "{0} {1}".format(res.value, tt.next0_.term)
                            if (res.alt_value is not None): 
                                res.alt_value = "{0} {1}".format(res.alt_value, tt.next0_.term)
                        elif (not AddressItemToken.check_house_after(tt.next0_, False, False) or tt.next0_.is_newline_after): 
                            tt1 = tt.next0_
                            is_pref = False
                            if ((isinstance(tt1, TextToken)) and tt1.chars.is_all_lower): 
                                if (tt1.is_value("ДЕ", None) or tt1.is_value("ЛА", None)): 
                                    tt1 = tt1.next0_
                                    is_pref = True
                            nn = StreetItemToken.try_parse(tt1, None, False, None)
                            if (nn is None or nn.typ == StreetItemType.NAME): 
                                npt = MiscLocationHelper._try_parse_npt(tt)
                                if (npt is not None): 
                                    if (npt.begin_token == npt.end_token): 
                                        npt = (None)
                                    elif (StreetItemToken._m_ontology.try_parse(npt.end_token, TerminParseAttr.NO) is not None): 
                                        npt = (None)
                                if (npt is not None and ((npt.is_newline_after or AddressItemToken.check_house_after(npt.end_token.next0_, False, False) or ((npt.end_token.next0_ is not None and npt.end_token.next0_.is_comma_and))))): 
                                    res.end_token = npt.end_token
                                    if (npt.morph.case_.is_genitive): 
                                        res.value = MiscHelper.get_text_value_of_meta_token(npt, GetTextAttr.NO)
                                        res.alt_value = npt.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False)
                                    else: 
                                        res.value = npt.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False)
                                        res.alt_value = MiscHelper.get_text_value_of_meta_token(npt, GetTextAttr.NO)
                                elif ((tt1.length_char > 2 and AddressItemToken.check_house_after(tt1.next0_, False, False) and tt1.chars.is_cyrillic_letter == tt.chars.is_cyrillic_letter) and (t.whitespaces_after_count < 2)): 
                                    if (tt1.morph.class0_.is_verb and not tt1.is_value("ДАЛИ", None)): 
                                        pass
                                    elif (npt is None and not tt1.chars.is_all_lower and not is_pref): 
                                        pass
                                    else: 
                                        res.end_token = tt1
                                        res.value = "{0} {1}".format(MiscHelper.get_text_value(res.begin_token, res.begin_token, GetTextAttr.NO), MiscHelper.get_text_value(res.end_token, res.end_token, GetTextAttr.NO))
                            elif (nn.typ == StreetItemType.NOUN): 
                                gen = nn.termin.gender
                                if (gen == MorphGender.UNDEFINED): 
                                    npt = MiscLocationHelper._try_parse_npt(tt)
                                    if (npt is not None and npt.end_token == nn.end_token): 
                                        gen = npt.morph.gender
                                    elif (prev is not None and prev.typ == StreetItemType.NOUN): 
                                        gen = prev.termin.gender
                                else: 
                                    for ii in tt.morph.items: 
                                        if (((ii.class0_.is_proper_surname or ii.class0_.is_noun)) and ii.case_.is_genitive and (isinstance(ii, MorphWordForm))): 
                                            if (ii.is_in_dictionary): 
                                                gen = MorphGender.UNDEFINED
                                                break
                                if (gen != MorphGender.UNDEFINED and ((not nn.morph.case_.is_nominative or nn.morph.number != MorphNumber.SINGULAR))): 
                                    res.value = MiscHelper.get_text_value(res.begin_token, res.end_token, GetTextAttr.NO)
                                    var = MorphologyService.get_wordform(res.value, MorphBaseInfo._new384(MorphCase.NOMINATIVE, MorphClass.ADJECTIVE, MorphNumber.SINGULAR, gen))
                                    if (var is not None and var.endswith("ОЙ") and not res.begin_token.get_morph_class_in_dictionary().is_adjective): 
                                        if (gen == MorphGender.MASCULINE): 
                                            var = (var[0:0+len(var) - 2] + "ЫЙ")
                                        elif (gen == MorphGender.NEUTER): 
                                            var = (var[0:0+len(var) - 2] + "ОЕ")
                                        elif (gen == MorphGender.FEMINIE): 
                                            var = (var[0:0+len(var) - 2] + "АЯ")
                                    if (var is not None and var != res.value): 
                                        res.alt_value = res.value
                                        res.value = var
                    if (res is not None and res.typ == StreetItemType.NAME and (res.whitespaces_after_count < 2)): 
                        tt = (Utils.asObjectOrNull(res.end_token.next0_, TextToken))
                        if ((tt is not None and tt.length_char == 1 and tt.chars.is_all_upper) and tt.next0_ is not None and tt.next0_.is_char('.')): 
                            if (StreetItemToken.try_parse(tt, None, False, None) is not None or AddressItemToken.check_house_after(tt, False, False)): 
                                pass
                            else: 
                                rt = tt.kit.process_referent("PERSON", tt, None)
                                if (rt is None): 
                                    if (res.value is None): 
                                        res.value = MiscHelper.get_text_value_of_meta_token(res, GetTextAttr.NO)
                                    res.end_token = tt.next0_
                                    tt = (Utils.asObjectOrNull(res.end_token.next0_, TextToken))
                                    if ((((res.whitespaces_after_count < 2) and tt is not None and tt.length_char == 1) and tt.chars.is_all_upper and tt.next0_ is not None) and tt.next0_.is_char('.')): 
                                        res.end_token = tt.next0_
                        if (tt is not None and tt.get_morph_class_in_dictionary().is_proper_name): 
                            rt = tt.kit.process_referent("PERSON", res.begin_token, None)
                            if (rt is not None): 
                                ok2 = False
                                if (rt.end_token == tt): 
                                    ok2 = True
                                elif (rt.end_token == tt.next0_ and tt.next0_.get_morph_class_in_dictionary().is_proper_secname): 
                                    ok2 = True
                                if (ok2): 
                                    if (res.value is None): 
                                        res.value = MiscHelper.get_text_value_of_meta_token(res, GetTextAttr.NO)
                                    res.end_token = rt.end_token
                    return res
            if (tt.is_value("№", None) or tt.is_value("НОМЕР", None) or tt.is_value("НОМ", None)): 
                tt1 = tt.next0_
                if (tt1 is not None and tt1.is_char('.')): 
                    tt1 = tt1.next0_
                if ((isinstance(tt1, NumberToken)) and tt1.int_value is not None): 
                    return StreetItemToken._new346(tt, tt1, StreetItemType.NUMBER, Utils.asObjectOrNull(tt1, NumberToken), True)
            if (tt.is_hiphen and (isinstance(tt.next0_, NumberToken)) and tt.next0_.int_value is not None): 
                if (prev is not None and prev.typ == StreetItemType.NOUN): 
                    if ((prev.noun_can_be_name or prev.termin.canonic_text == "МИКРОРАЙОН" or prev.termin.canonic_text == "КВАРТАЛ") or LanguageHelper.ends_with(prev.termin.canonic_text, "ГОРОДОК")): 
                        return StreetItemToken._new346(tt, tt.next0_, StreetItemType.NUMBER, Utils.asObjectOrNull(tt.next0_, NumberToken), True)
            if (((isinstance(tt, TextToken)) and tt.length_char == 1 and (tt.whitespaces_before_count < 2)) and tt.chars.is_letter and tt.chars.is_all_upper): 
                if (prev is not None and prev.typ == StreetItemType.NOUN): 
                    if (prev.termin.canonic_text == "МИКРОРАЙОН" or prev.termin.canonic_text == "КВАРТАЛ" or LanguageHelper.ends_with(prev.termin.canonic_text, "ГОРОДОК")): 
                        return StreetItemToken._new343(tt, tt, StreetItemType.NAME, tt.term)
        r = (None if t is None else t.get_referent())
        if (isinstance(r, GeoReferent)): 
            geo = Utils.asObjectOrNull(r, GeoReferent)
            if (prev is not None and prev.typ == StreetItemType.NOUN): 
                if (AddressItemToken.check_house_after(t.next0_, False, False)): 
                    return StreetItemToken._new343(t, t, StreetItemType.NAME, MiscHelper.get_text_value(t, t, GetTextAttr.NO))
        if (((isinstance(tt, TextToken)) and tt.chars.is_capital_upper and tt.chars.is_latin_letter) and (tt.whitespaces_after_count < 2)): 
            if (MiscHelper.is_eng_article(tt)): 
                return None
            tt2 = tt.next0_
            if (MiscHelper.is_eng_adj_suffix(tt2)): 
                tt2 = tt2.next0_.next0_
            tok1 = StreetItemToken._m_ontology.try_parse(tt2, TerminParseAttr.NO)
            if (tok1 is not None): 
                return StreetItemToken._new367(tt, tt2.previous, StreetItemType.NAME, tt.morph, tt.term)
        if (((tt is not None and tt.is_value("ПОДЪЕЗД", None) and prev is not None) and prev.is_road and tt.next0_ is not None) and tt.next0_.is_value("К", None) and tt.next0_.next0_ is not None): 
            sit = StreetItemToken._new347(tt, tt.next0_, StreetItemType.NAME)
            sit.is_road_name = True
            t1 = tt.next0_.next0_
            g1 = None
            first_pass2768 = True
            while True:
                if first_pass2768: first_pass2768 = False
                else: t1 = t1.next0_
                if (not (t1 is not None)): break
                if (t1.whitespaces_before_count > 3): 
                    break
                g1 = Utils.asObjectOrNull(t1.get_referent(), GeoReferent)
                if ((g1) is not None): 
                    break
                if (t1.is_char('.') or (t1.length_char < 3)): 
                    continue
                if ((t1.length_char < 4) and t1.chars.is_all_lower): 
                    continue
                break
            if (g1 is not None): 
                sit.end_token = t1
                nams = g1.get_string_values(GeoReferent.ATTR_NAME)
                if (nams is None or len(nams) == 0): 
                    return None
                sit.value = ("ПОДЪЕЗД - " + nams[0])
                if (len(nams) > 1): 
                    sit.alt_value = ("ПОДЪЕЗД - " + nams[1])
                return sit
            if ((isinstance(t1, TextToken)) and (t1.whitespaces_before_count < 2) and t1.chars.is_capital_upper): 
                cit = CityItemToken.try_parse(t1, None, True, None)
                if (cit is not None and ((cit.typ == CityItemToken.ItemType.PROPERNAME or cit.typ == CityItemToken.ItemType.CITY))): 
                    sit.end_token = cit.end_token
                    sit.value = ("ПОДЪЕЗД - " + cit.value)
                    return sit
        return None
    
    @staticmethod
    def _try_parse_spec(t : 'Token', prev : 'StreetItemToken') -> typing.List['StreetItemToken']:
        from pullenti.ner.geo.internal.MiscLocationHelper import MiscLocationHelper
        from pullenti.ner.geo.internal.CityItemToken import CityItemToken
        if (t is None): 
            return None
        res = None
        sit = None
        if (isinstance(t.get_referent(), DateReferent)): 
            dr = Utils.asObjectOrNull(t.get_referent(), DateReferent)
            if (not (isinstance(t.begin_token, NumberToken))): 
                return None
            if (dr.year == 0 and dr.day > 0 and dr.month > 0): 
                res = list()
                res.append(StreetItemToken._new353(t, t, StreetItemType.NUMBER, NumberToken(t, t, str(dr.day), NumberSpellingType.DIGIT)))
                tmp = dr.to_string_ex(False, t.morph.language, 0)
                i = tmp.find(' ')
                sit = StreetItemToken._new343(t, t, StreetItemType.STDNAME, tmp[i + 1:].upper())
                res.append(sit)
                sit.chars.is_capital_upper = True
                return res
            if (dr.year > 0 and dr.month == 0): 
                res = list()
                res.append(StreetItemToken._new353(t, t, StreetItemType.NUMBER, NumberToken(t, t, str(dr.year), NumberSpellingType.DIGIT)))
                sit = StreetItemToken._new343(t, t, StreetItemType.STDNAME, ("РОКУ" if t.morph.language.is_ua else "ГОДА"))
                res.append(sit)
                sit.chars.is_capital_upper = True
                return res
            return None
        if (prev is not None and prev.typ == StreetItemType.AGE): 
            res = list()
            if (isinstance(t.get_referent(), GeoReferent)): 
                sit = StreetItemToken._new395(t, t, StreetItemType.NAME, t.get_source_text().upper(), t.get_referent().to_string_ex(True, t.kit.base_language, 0).upper())
                res.append(sit)
            elif (t.is_value("ГОРОД", None) or t.is_value("МІСТО", None)): 
                sit = StreetItemToken._new343(t, t, StreetItemType.NAME, "ГОРОДА")
                res.append(sit)
            else: 
                return None
            return res
        if (prev is not None and prev.typ == StreetItemType.NOUN): 
            num = NumberHelper.try_parse_roman(t)
            if ((num is not None and num.int_value is not None and not t.is_value("С", None)) and not t.is_value("C", None)): 
                res = list()
                sit = StreetItemToken._new353(num.begin_token, num.end_token, StreetItemType.NUMBER, num)
                res.append(sit)
                t = num.end_token.next0_
                if ((num.typ == NumberSpellingType.DIGIT and (isinstance(t, TextToken)) and t.chars.is_letter) and not t.is_whitespace_before and t.length_char == 1): 
                    sit.end_token = t
                    sit.value = "{0}{1}".format(num.value, t.term)
                    sit.number = (None)
                return res
        if (prev is not None and prev.is_road and (t.whitespaces_before_count < 3)): 
            vals = None
            t1 = None
            br = False
            tt = t
            first_pass2769 = True
            while True:
                if first_pass2769: first_pass2769 = False
                else: tt = tt.next0_
                if (not (tt is not None)): break
                if (tt.whitespaces_before_count > 3): 
                    break
                if (BracketHelper.is_bracket(tt, False)): 
                    if (tt == t): 
                        br = True
                        continue
                    break
                val = None
                if (isinstance(tt.get_referent(), GeoReferent)): 
                    rt = Utils.asObjectOrNull(tt, ReferentToken)
                    if (rt.begin_token == rt.end_token and (isinstance(rt.end_token, TextToken))): 
                        val = rt.end_token.term
                    else: 
                        val = tt.get_referent().to_string_ex(True, tt.kit.base_language, 0).upper()
                    t1 = tt
                elif ((isinstance(tt, TextToken)) and tt.chars.is_capital_upper): 
                    cit = CityItemToken.try_parse(tt, None, True, None)
                    if (cit is not None and cit.typ == CityItemToken.ItemType.PROPERNAME): 
                        val = cit.value
                        tt = cit.end_token
                        t1 = tt
                    else: 
                        break
                else: 
                    break
                if (vals is None): 
                    vals = list()
                if (val.find('-') > 0 and (isinstance(tt, TextToken))): 
                    vals.extend(Utils.splitString(val, '-', False))
                else: 
                    vals.append(val)
                if (tt.next0_ is not None and tt.next0_.is_hiphen): 
                    tt = tt.next0_
                else: 
                    break
            if (vals is not None): 
                ok = False
                if (len(vals) > 1): 
                    ok = True
                elif (MiscLocationHelper.check_geo_object_before(t, False)): 
                    ok = True
                else: 
                    sit1 = StreetItemToken.try_parse(t1.next0_, None, False, None)
                    if (sit1 is not None and sit1.typ == StreetItemType.NUMBER and sit1.is_number_km): 
                        ok = True
                if (ok): 
                    if (br): 
                        if (BracketHelper.is_bracket(t1.next0_, False)): 
                            t1 = t1.next0_
                    res = list()
                    prev.noun_is_doubt_coef = 0
                    prev.is_abridge = False
                    sit = StreetItemToken._new347(t, t1, StreetItemType.NAME)
                    res.append(sit)
                    if (len(vals) == 1): 
                        sit.value = vals[0]
                    elif (len(vals) == 2): 
                        sit.value = "{0} - {1}".format(vals[0], vals[1])
                        sit.alt_value = "{0} - {1}".format(vals[1], vals[0])
                    elif (len(vals) == 3): 
                        sit.value = "{0} - {1} - {2}".format(vals[0], vals[1], vals[2])
                        sit.alt_value = "{0} - {1} - {2}".format(vals[2], vals[1], vals[0])
                    elif (len(vals) == 4): 
                        sit.value = "{0} - {1} - {2} - {3}".format(vals[0], vals[1], vals[2], vals[3])
                        sit.alt_value = "{0} - {1} - {2} - {3}".format(vals[3], vals[2], vals[1], vals[0])
                    else: 
                        return None
                    return res
            if (((isinstance(t, TextToken)) and t.length_char == 1 and t.chars.is_letter) and t.next0_ is not None): 
                if (t.is_value("К", None) or t.is_value("Д", None)): 
                    return None
                tt = t.next0_
                if (tt.is_hiphen and tt.next0_ is not None): 
                    tt = tt.next0_
                if (isinstance(tt, NumberToken)): 
                    res = list()
                    prev.noun_is_doubt_coef = 0
                    sit = StreetItemToken._new347(t, tt, StreetItemType.NAME)
                    res.append(sit)
                    ch = t.term[0]
                    ch0 = LanguageHelper.get_cyr_for_lat(ch)
                    if ((ord(ch0)) != 0): 
                        ch = ch0
                    sit.value = "{0}{1}".format(ch, tt.value)
                    sit.is_road_name = True
                    tt = tt.next0_
                    br1 = BracketHelper.try_parse(tt, BracketParseAttr.NO, 100)
                    if (br1 is not None and (br1.length_char < 15)): 
                        sit.end_token = br1.end_token
                    elif (tt is not None and tt.length_char > 2 and not tt.chars.is_all_lower): 
                        if ((((((tt.is_value("ДОН", None) or tt.is_value("КАВКАЗ", None) or tt.is_value("УРАЛ", None)) or tt.is_value("БЕЛАРУСЬ", None) or tt.is_value("УКРАИНА", None)) or tt.is_value("КРЫМ", None) or tt.is_value("ВОЛГА", None)) or tt.is_value("ХОЛМОГОРЫ", None) or tt.is_value("БАЛТИЯ", None)) or tt.is_value("РОССИЯ", None) or tt.is_value("НЕВА", None)) or tt.is_value("КОЛА", None) or tt.is_value("КАСПИЙ", None)): 
                            sit.end_token = tt
                    return res
        return None
    
    @staticmethod
    def __try_attach_road_num(t : 'Token') -> 'StreetItemToken':
        if (t is None): 
            return None
        if (not t.chars.is_letter or t.length_char != 1): 
            return None
        tt = t.next0_
        if (tt is not None and tt.is_hiphen): 
            tt = tt.next0_
        if (not (isinstance(tt, NumberToken))): 
            return None
        res = StreetItemToken._new347(t, tt, StreetItemType.NAME)
        res.value = "{0}{1}".format(t.get_source_text().upper(), tt.value)
        return res
    
    @staticmethod
    def initialize() -> None:
        if (StreetItemToken._m_ontology is not None): 
            return
        StreetItemToken._m_ontology = TerminCollection()
        StreetItemToken._m_ontology_ex = TerminCollection()
        StreetItemToken.__m_std_ont_misc = TerminCollection()
        StreetItemToken.__m_std_adj = TerminCollection()
        t = None
        t = Termin._new401("УЛИЦА", StreetItemType.NOUN, MorphGender.FEMINIE)
        t.add_abridge("УЛ.")
        t.add_abridge("УЛЮ")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new402("ВУЛИЦЯ", StreetItemType.NOUN, MorphLang.UA, MorphGender.FEMINIE)
        t.add_abridge("ВУЛ.")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new264("STREET", StreetItemType.NOUN)
        t.add_abridge("ST.")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new404("ПЛОЩАДЬ", StreetItemType.NOUN, 1, MorphGender.FEMINIE)
        t.add_abridge("ПЛ.")
        t.add_abridge("ПЛОЩ.")
        t.add_abridge("ПЛ-ДЬ")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new405("ПЛОЩА", StreetItemType.NOUN, MorphLang.UA, 1, MorphGender.FEMINIE)
        t.add_abridge("ПЛ.")
        t.add_abridge("ПЛОЩ.")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new404("МАЙДАН", StreetItemType.NOUN, 0, MorphGender.MASCULINE)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new264("SQUARE", StreetItemType.NOUN)
        t.add_abridge("SQ.")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new404("ПРОЕЗД", StreetItemType.NOUN, 1, MorphGender.MASCULINE)
        t.add_abridge("ПР.")
        t.add_abridge("П-Д")
        t.add_abridge("ПР-Д")
        t.add_abridge("ПР-ЗД")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new405("ПРОЕЗД", StreetItemType.NOUN, MorphLang.UA, 1, MorphGender.MASCULINE)
        t.add_abridge("ПР.")
        t.add_abridge("П-Д")
        t.add_abridge("ПР-Д")
        t.add_abridge("ПР-ЗД")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new404("ЛИНИЯ", StreetItemType.NOUN, 2, MorphGender.FEMINIE)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new405("ЛІНІЯ", StreetItemType.NOUN, MorphLang.UA, 2, MorphGender.FEMINIE)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new404("РЯД", StreetItemType.NOUN, 2, MorphGender.MASCULINE)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new404("ПРОСПЕКТ", StreetItemType.NOUN, 0, MorphGender.MASCULINE)
        StreetItemToken.__m_prospect = t
        t.add_abridge("ПРОС.")
        t.add_abridge("ПРКТ")
        t.add_abridge("ПРОСП.")
        t.add_abridge("ПР-Т")
        t.add_abridge("ПР-КТ")
        t.add_abridge("П-Т")
        t.add_abridge("П-КТ")
        t.add_abridge("ПР Т")
        t.add_abridge("ПР-ТЕ")
        t.add_abridge("ПР-КТЕ")
        t.add_abridge("П-ТЕ")
        t.add_abridge("П-КТЕ")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new404("ПЕРЕУЛОК", StreetItemType.NOUN, 0, MorphGender.MASCULINE)
        t.add_abridge("ПЕР.")
        t.add_abridge("ПЕР-К")
        t.add_variant("ПРЕУЛОК", False)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new404("ПРОУЛОК", StreetItemType.NOUN, 0, MorphGender.MASCULINE)
        t.add_abridge("ПРОУЛ.")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new405("ПРОВУЛОК", StreetItemType.NOUN, MorphLang.UA, 0, MorphGender.MASCULINE)
        t.add_abridge("ПРОВ.")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new266("LANE", StreetItemType.NOUN, 0)
        t.add_abridge("LN.")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new404("ТУПИК", StreetItemType.NOUN, 1, MorphGender.MASCULINE)
        t.add_abridge("ТУП.")
        t.add_abridge("Т.")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new404("БУЛЬВАР", StreetItemType.NOUN, 0, MorphGender.MASCULINE)
        t.add_abridge("БУЛЬВ.")
        t.add_abridge("БУЛ.")
        t.add_abridge("Б-Р")
        t.add_abridge("Б-РЕ")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new266("BOULEVARD", StreetItemType.NOUN, 0)
        t.add_abridge("BLVD")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new266("СКВЕР", StreetItemType.NOUN, 1)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new404("НАБЕРЕЖНАЯ", StreetItemType.NOUN, 0, MorphGender.FEMINIE)
        t.add_abridge("НАБ.")
        t.add_abridge("НАБЕР.")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new405("НАБЕРЕЖНА", StreetItemType.NOUN, MorphLang.UA, 0, MorphGender.FEMINIE)
        t.add_abridge("НАБ.")
        t.add_abridge("НАБЕР.")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new404("АЛЛЕЯ", StreetItemType.NOUN, 0, MorphGender.FEMINIE)
        t.add_abridge("АЛ.")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new405("АЛЕЯ", StreetItemType.NOUN, MorphLang.UA, 0, MorphGender.FEMINIE)
        t.add_abridge("АЛ.")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new266("ALLEY", StreetItemType.NOUN, 0)
        t.add_abridge("ALY.")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new404("АВЕНЮ", StreetItemType.NOUN, 0, MorphGender.FEMINIE)
        t.add_variant("АВЕНЬЮ", False)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new404("ПРОСЕКА", StreetItemType.NOUN, 1, MorphGender.FEMINIE)
        t.add_variant("ПРОСЕК", False)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new405("ПРОСІКА", StreetItemType.NOUN, MorphLang.UA, 1, MorphGender.FEMINIE)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new404("ТРАКТ", StreetItemType.NOUN, 1, MorphGender.NEUTER)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new404("ШОССЕ", StreetItemType.NOUN, 1, MorphGender.NEUTER)
        t.add_abridge("Ш.")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new405("ШОСЕ", StreetItemType.NOUN, MorphLang.UA, 1, MorphGender.NEUTER)
        t.add_abridge("Ш.")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new266("ROAD", StreetItemType.NOUN, 1)
        t.add_abridge("RD.")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new404("МИКРОРАЙОН", StreetItemType.NOUN, 0, MorphGender.MASCULINE)
        t.add_abridge("МКР.")
        t.add_abridge("МИКР-Н")
        t.add_abridge("МКР-Н")
        t.add_abridge("МКРН.")
        t.add_abridge("М-Н")
        t.add_abridge("М-ОН")
        t.add_abridge("М.Р-Н")
        t.add_variant("МИКРОН", False)
        t.add_abridge("М/Р")
        t.add_variant("МІКРОРАЙОН", False)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new404("КВАРТАЛ", StreetItemType.NOUN, 2, MorphGender.MASCULINE)
        t.add_abridge("КВАРТ.")
        t.add_abridge("КВ-Л")
        t.add_abridge("КВ.")
        StreetItemToken._m_ontology.add(t)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new436("КВАРТАЛ ДАЧНОЙ ЗАСТРОЙКИ", "КВАРТАЛ", StreetItemType.NOUN, 0, MorphGender.MASCULINE)
        t.add_variant("ПРОМЫШЛЕННЫЙ КВАРТАЛ", False)
        t.add_variant("ИНДУСТРИАЛЬНЫЙ КВАРТАЛ", False)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new437("ЖИЛОЙ КОМПЛЕКС", StreetItemType.NOUN, "ЖК", 0, MorphGender.MASCULINE)
        t.add_variant("ЖИЛКОМПЛЕКС", False)
        t.add_abridge("ЖИЛ.К.")
        t.add_abridge("Ж/К")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new404("БРИГАДА", StreetItemType.NOUN, 2, MorphGender.MASCULINE)
        t.add_abridge("БРИГ.")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new404("ГОРОДОК", StreetItemType.NOUN, 0, MorphGender.MASCULINE)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new405("МІСТЕЧКО", StreetItemType.NOUN, MorphLang.UA, 0, MorphGender.NEUTER)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new266("HILL", StreetItemType.NOUN, 0)
        t.add_abridge("HL.")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new404("ВОЕННЫЙ ГОРОДОК", StreetItemType.NOUN, 0, MorphGender.MASCULINE)
        t.add_abridge("В.ГОРОДОК")
        t.add_abridge("В/Г")
        t.add_abridge("В/ГОРОДОК")
        t.add_abridge("В/ГОР")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new404("ПРОМЗОНА", StreetItemType.NOUN, 1, MorphGender.FEMINIE)
        t.add_variant("ПРОМЫШЛЕННАЯ ЗОНА", False)
        t.add_variant("ПРОИЗВОДСТВЕННАЯ ЗОНА", False)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new404("ПРОИЗВОДСТВЕННО АДМИНИСТРАТИВНАЯ ЗОНА", StreetItemType.NOUN, 1, MorphGender.FEMINIE)
        t.add_abridge("ПРОИЗВ. АДМ. ЗОНА")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new404("ЖИЛАЯ ЗОНА", StreetItemType.NOUN, 1, MorphGender.FEMINIE)
        t.add_variant("ЖИЛЗОНА", False)
        t.add_variant("ЖИЛОЙ РАЙОН", False)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new404("КОММУНАЛЬНАЯ ЗОНА", StreetItemType.NOUN, 1, MorphGender.FEMINIE)
        t.add_variant("КОМЗОНА", False)
        t.add_abridge("КОММУН. ЗОНА")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new404("МАССИВ", StreetItemType.NOUN, 2, MorphGender.MASCULINE)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new404("ЖИЛОЙ МАССИВ", StreetItemType.NOUN, 1, MorphGender.MASCULINE)
        t.add_abridge("Ж.М.")
        t.add_abridge("Ж/М")
        t.add_variant("ЖИЛМАССИВ", False)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new404("ЗОНА", StreetItemType.NOUN, 2, MorphGender.FEMINIE)
        t.add_variant("ЗОНА (МАССИВ)", False)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new404("ИНДУСТРИАЛЬНЫЙ ПАРК", StreetItemType.NOUN, 1, MorphGender.MASCULINE)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new404("МОСТ", StreetItemType.NOUN, 2, MorphGender.MASCULINE)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new405("МІСТ", StreetItemType.NOUN, MorphLang.UA, 2, MorphGender.MASCULINE)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new404("ПАРК", StreetItemType.NOUN, 2, MorphGender.MASCULINE)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new404("САД", StreetItemType.NOUN, 2, MorphGender.MASCULINE)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new404("УРОЧИЩЕ", StreetItemType.NOUN, 1, MorphGender.NEUTER)
        t.add_abridge("УР-ЩЕ")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new266("PLAZA", StreetItemType.NOUN, 1)
        t.add_abridge("PLZ")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new436("СТАНЦИЯ МЕТРО", "МЕТРО", StreetItemType.NOUN, 0, MorphGender.FEMINIE)
        StreetItemToken.__m_metro = t
        t.add_variant("СТАНЦІЯ МЕТРО", False)
        t.add_abridge("СТ.МЕТРО")
        t.add_abridge("СТ.М.")
        t.add_abridge("МЕТРО")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new437("АВТОДОРОГА", StreetItemType.NOUN, "ФАД", 0, MorphGender.FEMINIE)
        StreetItemToken.__m_road = t
        t.add_variant("ФЕДЕРАЛЬНАЯ АВТОДОРОГА", False)
        t.add_variant("АВТОМОБИЛЬНАЯ ДОРОГА", False)
        t.add_variant("АВТОТРАССА", False)
        t.add_variant("ФЕДЕРАЛЬНАЯ ТРАССА", False)
        t.add_variant("ФЕДЕР ТРАССА", False)
        t.add_variant("АВТОМАГИСТРАЛЬ", False)
        t.add_abridge("А/Д")
        t.add_abridge("ФЕДЕР.ТРАССА")
        t.add_abridge("ФЕД.ТРАССА")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new436("ДОРОГА", "АВТОДОРОГА", StreetItemType.NOUN, 1, MorphGender.FEMINIE)
        t.add_variant("ТРАССА", False)
        t.add_variant("МАГИСТРАЛЬ", False)
        t.add_abridge("ДОР.")
        t.add_variant("ДОР", False)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new405("АВТОДОРОГА", StreetItemType.NOUN, MorphLang.UA, 0, MorphGender.FEMINIE)
        t.add_variant("ФЕДЕРАЛЬНА АВТОДОРОГА", False)
        t.add_variant("АВТОМОБІЛЬНА ДОРОГА", False)
        t.add_variant("АВТОТРАСА", False)
        t.add_variant("ФЕДЕРАЛЬНА ТРАСА", False)
        t.add_variant("АВТОМАГІСТРАЛЬ", False)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new461("ДОРОГА", "АВТОДОРОГА", StreetItemType.NOUN, MorphLang.UA, 1, MorphGender.FEMINIE)
        t.add_variant("ТРАСА", False)
        t.add_variant("МАГІСТРАЛЬ", False)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new462("МОСКОВСКАЯ КОЛЬЦЕВАЯ АВТОМОБИЛЬНАЯ ДОРОГА", "МКАД", StreetItemType.FIX, MorphGender.FEMINIE)
        t.add_variant("МОСКОВСКАЯ КОЛЬЦЕВАЯ АВТОДОРОГА", False)
        StreetItemToken._m_ontology.add(t)
        StreetItemToken._m_ontology.add(Termin._new264("САДОВОЕ КОЛЬЦО", StreetItemType.FIX))
        StreetItemToken._m_ontology.add(Termin._new264("БУЛЬВАРНОЕ КОЛЬЦО", StreetItemType.FIX))
        StreetItemToken._m_ontology.add(Termin._new264("ТРАНСПОРТНОЕ КОЛЬЦО", StreetItemType.FIX))
        t = Termin._new466("ПОЧТОВОЕ ОТДЕЛЕНИЕ", StreetItemType.NOUN, "ОПС", MorphGender.NEUTER)
        t.add_abridge("П.О.")
        t.add_abridge("ПОЧТ.ОТД.")
        t.add_abridge("ПОЧТОВ.ОТД.")
        t.add_abridge("ПОЧТОВОЕ ОТД.")
        t.add_abridge("П/О")
        t.add_variant("ОТДЕЛЕНИЕ ПОЧТОВОЙ СВЯЗИ", False)
        t.add_variant("ПОЧТАМТ", False)
        t.add_variant("ГЛАВПОЧТАМТ", False)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new401("БУДКА", StreetItemType.NOUN, MorphGender.FEMINIE)
        t.add_variant("ЖЕЛЕЗНОДОРОЖНАЯ БУДКА", False)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new401("КАЗАРМА", StreetItemType.NOUN, MorphGender.FEMINIE)
        t.add_variant("ЖЕЛЕЗНОДОРОЖНАЯ КАЗАРМА", False)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new401("МЕСТНОСТЬ", StreetItemType.NOUN, MorphGender.FEMINIE)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new401("СТОЯНКА", StreetItemType.NOUN, MorphGender.FEMINIE)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new401("ПУНКТ", StreetItemType.NOUN, MorphGender.MASCULINE)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new401("РАЗЪЕЗД", StreetItemType.NOUN, MorphGender.MASCULINE)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new401("ЗАЕЗД", StreetItemType.NOUN, MorphGender.MASCULINE)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new401("ПЕРЕЕЗД", StreetItemType.NOUN, MorphGender.MASCULINE)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new264("БОЛЬШОЙ", StreetItemType.STDADJECTIVE)
        t.add_abridge("БОЛ.")
        t.add_abridge("Б.")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new264("ВЕЛИКИЙ", StreetItemType.STDADJECTIVE)
        t.add_abridge("ВЕЛ.")
        t.add_abridge("В.")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new264("МАЛЫЙ", StreetItemType.STDADJECTIVE)
        t.add_abridge("МАЛ.")
        t.add_abridge("М.")
        t.add_variant("МАЛИЙ", False)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new264("СРЕДНИЙ", StreetItemType.STDADJECTIVE)
        t.add_abridge("СРЕД.")
        t.add_abridge("СР.")
        t.add_abridge("С.")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new265("СЕРЕДНІЙ", StreetItemType.STDADJECTIVE, MorphLang.UA)
        t.add_abridge("СЕРЕД.")
        t.add_abridge("СЕР.")
        t.add_abridge("С.")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new264("ВЕРХНИЙ", StreetItemType.STDADJECTIVE)
        t.add_abridge("ВЕРХН.")
        t.add_abridge("ВЕРХ.")
        t.add_abridge("ВЕР.")
        t.add_abridge("В.")
        t.add_variant("ВЕРХНІЙ", False)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new264("НИЖНИЙ", StreetItemType.STDADJECTIVE)
        t.add_abridge("НИЖН.")
        t.add_abridge("НИЖ.")
        t.add_abridge("Н.")
        t.add_variant("НИЖНІЙ", False)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new264("СТАРЫЙ", StreetItemType.STDADJECTIVE)
        t.add_abridge("СТАР.")
        t.add_abridge("СТ.")
        t.add_variant("СТАРИЙ", False)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new264("НОВЫЙ", StreetItemType.STDADJECTIVE)
        t.add_abridge("НОВ.")
        t.add_variant("НОВИЙ", False)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new264("НОМЕР", StreetItemType.STDADJECTIVE)
        t.add_abridge("N")
        t.add_abridge("№")
        t.add_abridge("НОМ.")
        StreetItemToken._m_ontology.add(t)
        for s in ["ПРОЕКТИРУЕМЫЙ", "ЭНГЕЛЬСА;ФРИДРИХА ЭНГЕЛЬСА;ФРИД.ЭНГЕЛЬСА;ФР.ЭНГЕЛЬСА;Ф.ЭНГЕЛЬСА", "МАРКСА;КАРЛА МАРКСА;К.МАРКСА", "ЛЮКСЕМБУРГ;РОЗЫ ЛЮКСЕМБУРГ;Р.ЛЮКСЕМБУРГ", "ВЕЛИКОЙ ПОБЕДЫ;ВЕЛ.ПОБЕДЫ;В.ПОБЕДЫ", "ЮНЫХ ЛЕНИНЦЕВ;ЮН. ЛЕНИНЦЕВ", "МАРКСА И ЭНГЕЛЬСА;КАРЛА МАРКСА И ФРИДРИХА ЭНГЕЛЬСА", "БАКИНСКИХ КОМИССАРОВ;БАК.КОМИССАРОВ;Б.КОМИССАРОВ", "САККО И ВАНЦЕТТИ", "СЕРП И МОЛОТ", "ЗАВОДА СЕРП И МОЛОТ", "ШАРЛЯ ДЕ ГОЛЛЯ;ДЕ ГОЛЛЯ", "МИНИНА И ПОЖАРСКОГО", "ХО ШИ МИНА;ХОШИМИНА", "ЗОИ И АЛЕКСАНДРА КОСМОДЕМЬЯНСКИХ;З.И А.КОСМОДЕМЬЯНСКИХ;З.А.КОСМОДЕМЬЯНСКИХ", "АРМАНД;ИНЕССЫ АРМАНД", "МИРА", "СВОБОДЫ", "КРАСНОЙ АРМИИ;КР.АРМИИ", "СОВЕТСКОЙ АРМИИ;СОВ.АРМИИ", "СОВЕТСКОЙ ВЛАСТИ;СОВ.ВЛАСТИ", "РИМСКОГО-КОРСАКОВА"]: 
            pp = Utils.splitString(s, ';', False)
            t = Termin._new485(pp[0], StreetItemType.STDNAME, True)
            kk = 1
            while kk < len(pp): 
                if (pp[kk].find('.') > 0): 
                    t.add_abridge(pp[kk])
                else: 
                    t.add_variant(pp[kk], False)
                kk += 1
            StreetItemToken._m_ontology.add(t)
        for s in ["МАРТА", "МАЯ", "ОКТЯБРЯ", "НОЯБРЯ", "БЕРЕЗНЯ", "ТРАВНЯ", "ЖОВТНЯ", "ЛИСТОПАДА", "ДОРОЖКА", "ЛУЧ", "НАДЕЛ", "ПОЛЕ", "СКЛОН"]: 
            StreetItemToken._m_ontology.add(Termin._new264(s, StreetItemType.STDNAME))
        for s in ["МАРШАЛА", "ГЕНЕРАЛА", "ГЕНЕРАЛ-МАЙОРА", "ГЕНЕРАЛ-ЛЕЙТЕНАНТА", "ГЕНЕРАЛ-ПОЛКОВНИКА", "АДМИРАЛА", "КОНТРАДМИРАЛА", "КОСМОНАВТА", "ЛЕТЧИКА", "ПОГРАНИЧНИКА", "ПУТЕШЕСТВЕННИКА", "АВИАКОНСТРУКТОРА", "АРХИТЕКТОРА", "СКУЛЬПТОРА", "ХУДОЖНИКА", "КОНСТРУКТОРА", "АКАДЕМИКА", "ПРОФЕССОРА", "КОМПОЗИТОРА", "ПИСАТЕЛЯ", "ПОЭТА", "ДИРИЖЕРА", "ЛЕЙТЕНАНТА", "КАПИТАНА", "КАПИТАНА-ЛЕЙТЕНАНТА", "МАЙОРА", "ПОДПОЛКОВНИКА", "ПОЛКОВНИКА", "СЕРЖАНТА", "ЕФРЕЙТОРА", "СТАРШИНЫ", "ПРАПОРЩИКА", "ПОЛИТРУКА", "ПОЛИЦИИ", "МИЛИЦИИ", "ГВАРДИИ", "АРМИИ"]: 
            StreetItemToken.__m_std_ont_misc.add(Termin(s))
            t = Termin._new264(s, StreetItemType.STDPARTOFNAME)
            t.add_all_abridges(0, 0, 2)
            t.add_all_abridges(2, 5, 0)
            t.add_abridge("ГЛ." + s)
            t.add_abridge("ГЛАВ." + s)
            StreetItemToken._m_ontology.add(t)
        for s in ["МАРШАЛА", "ГЕНЕРАЛА", "АДМІРАЛА", "КОСМОНАВТА", "ЛЬОТЧИКА", "АВІАКОНСТРУКТОРА", "АРХІТЕКТОРА", "СКУЛЬПТОРА", "ХУДОЖНИКА", "КОНСТРУКТОРА", "АКАДЕМІКА", "ПРОФЕСОРА", "ЛЕЙТЕНАНТА", "КАПІТАН", "КАПІТАН-ЛЕЙТЕНАНТА", "МАЙОР", "ПІДПОЛКОВНИК", "ПОЛКОВНИК", "ПОЛІЦІЇ", "МІЛІЦІЇ"]: 
            StreetItemToken.__m_std_ont_misc.add(Termin(s))
            t = Termin._new265(s, StreetItemType.STDPARTOFNAME, MorphLang.UA)
            t.add_all_abridges(0, 0, 2)
            t.add_all_abridges(2, 5, 0)
            t.add_abridge("ГЛ." + s)
            t.add_abridge("ГЛАВ." + s)
            StreetItemToken._m_ontology.add(t)
        t = Termin._new292("ВАСИЛЬЕВСКОГО ОСТРОВА", StreetItemType.STDNAME, "ВО")
        t.add_abridge("В.О.")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new264("ПЕТРОГРАДСКОЙ СТОРОНЫ", StreetItemType.STDNAME)
        t.add_abridge("П.С.")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new264("ОЛИМПИЙСКАЯ ДЕРЕВНЯ", StreetItemType.FIX)
        t.add_abridge("ОЛИМП. ДЕРЕВНЯ")
        t.add_abridge("ОЛИМП. ДЕР.")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new264("ЛЕНИНСКИЕ ГОРЫ", StreetItemType.FIX)
        StreetItemToken._m_ontology.add(t)
        for s in ["КРАСНЫЙ", "СОВЕТСТКИЙ", "ЛЕНИНСКИЙ"]: 
            StreetItemToken.__m_std_adj.add(Termin(s))
    
    @staticmethod
    def check_std_name(t : 'Token') -> 'Token':
        if (t is None): 
            return None
        if (StreetItemToken.__m_std_adj.try_parse(t, TerminParseAttr.NO) is not None): 
            return t
        tok = StreetItemToken._m_ontology.try_parse(t, TerminParseAttr.NO)
        if (tok is None): 
            return None
        if ((Utils.valToEnum(tok.termin.tag, StreetItemType)) == StreetItemType.STDNAME): 
            return tok.end_token
        return None
    
    @staticmethod
    def check_keyword(t : 'Token') -> bool:
        if (t is None): 
            return False
        tok = StreetItemToken._m_ontology.try_parse(t, TerminParseAttr.NO)
        if (tok is None): 
            return False
        return (Utils.valToEnum(tok.termin.tag, StreetItemType)) == StreetItemType.NOUN
    
    @staticmethod
    def check_onto(t : 'Token') -> bool:
        if (t is None): 
            return False
        tok = StreetItemToken._m_ontology_ex.try_parse(t, TerminParseAttr.NO)
        if (tok is None): 
            return False
        return True
    
    _m_ontology = None
    
    _m_ontology_ex = None
    
    __m_std_ont_misc = None
    
    __m_std_adj = None
    
    __m_prospect = None
    
    __m_metro = None
    
    __m_road = None
    
    __m_reg_tails = None
    
    @staticmethod
    def _is_region(txt : str) -> bool:
        txt = txt.upper()
        for v in StreetItemToken.__m_reg_tails: 
            if (LanguageHelper.ends_with(txt, v)): 
                return True
        return False
    
    __m_spec_tails = None
    
    @staticmethod
    def _is_spec(txt : str) -> bool:
        txt = txt.upper()
        for v in StreetItemToken.__m_spec_tails: 
            if (LanguageHelper.ends_with(txt, v)): 
                return True
        return False
    
    @staticmethod
    def _new232(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : 'OrgItemToken') -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res._org0_ = _arg4
        return res
    
    @staticmethod
    def _new343(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : str) -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        return res
    
    @staticmethod
    def _new345(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : str, _arg5 : bool) -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        res.is_in_brackets = _arg5
        return res
    
    @staticmethod
    def _new346(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : 'NumberToken', _arg5 : bool) -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.number = _arg4
        res.number_has_prefix = _arg5
        return res
    
    @staticmethod
    def _new347(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType') -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        return res
    
    @staticmethod
    def _new348(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : bool) -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.is_in_brackets = _arg4
        return res
    
    @staticmethod
    def _new350(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : 'Termin') -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.termin = _arg4
        return res
    
    @staticmethod
    def _new353(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : 'NumberToken') -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.number = _arg4
        return res
    
    @staticmethod
    def _new354(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : 'NumberToken', _arg5 : 'MorphCollection') -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.number = _arg4
        res.morph = _arg5
        return res
    
    @staticmethod
    def _new357(_arg1 : 'Token', _arg2 : 'Token', _arg3 : bool) -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.has_std_suffix = _arg3
        return res
    
    @staticmethod
    def _new358(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'Termin', _arg4 : 'StreetItemType') -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.termin = _arg3
        res.typ = _arg4
        return res
    
    @staticmethod
    def _new359(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'Termin', _arg4 : 'StreetItemType', _arg5 : bool) -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.termin = _arg3
        res.typ = _arg4
        res.is_abridge = _arg5
        return res
    
    @staticmethod
    def _new360(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : 'StreetReferent', _arg5 : 'MorphCollection', _arg6 : bool) -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.exist_street = _arg4
        res.morph = _arg5
        res.is_in_dictionary = _arg6
        return res
    
    @staticmethod
    def _new363(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : 'NumberToken', _arg5 : bool, _arg6 : 'MorphCollection') -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.number = _arg4
        res.number_has_prefix = _arg5
        res.morph = _arg6
        return res
    
    @staticmethod
    def _new364(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : 'Termin', _arg5 : bool, _arg6 : 'MorphCollection') -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.termin = _arg4
        res.is_abridge = _arg5
        res.morph = _arg6
        return res
    
    @staticmethod
    def _new366(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : 'Termin', _arg5 : 'Termin', _arg6 : bool, _arg7 : 'MorphCollection', _arg8 : int) -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.termin = _arg4
        res.alt_termin = _arg5
        res.is_abridge = _arg6
        res.morph = _arg7
        res.noun_is_doubt_coef = _arg8
        return res
    
    @staticmethod
    def _new367(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : 'MorphCollection', _arg5 : str) -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.morph = _arg4
        res.value = _arg5
        return res
    
    @staticmethod
    def _new369(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : 'MorphCollection', _arg5 : 'Termin') -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.morph = _arg4
        res.termin = _arg5
        return res
    
    @staticmethod
    def _new372(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : 'MorphCollection', _arg5 : bool) -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.morph = _arg4
        res.is_in_dictionary = _arg5
        return res
    
    @staticmethod
    def _new373(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : 'MorphCollection', _arg5 : bool, _arg6 : 'Termin') -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.morph = _arg4
        res.is_in_dictionary = _arg5
        res.termin = _arg6
        return res
    
    @staticmethod
    def _new375(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : 'MorphCollection', _arg5 : str, _arg6 : str) -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.morph = _arg4
        res.value = _arg5
        res.alt_value = _arg6
        return res
    
    @staticmethod
    def _new376(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : bool, _arg5 : str, _arg6 : 'MorphCollection') -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.is_in_dictionary = _arg4
        res.value = _arg5
        res.morph = _arg6
        return res
    
    @staticmethod
    def _new378(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : str, _arg5 : bool) -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        res._no_geo_in_this_token = _arg5
        return res
    
    @staticmethod
    def _new379(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : bool) -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res._no_geo_in_this_token = _arg4
        return res
    
    @staticmethod
    def _new380(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : 'NumberToken', _arg5 : str) -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.number = _arg4
        res.value = _arg5
        return res
    
    @staticmethod
    def _new383(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : 'MorphCollection', _arg5 : 'Condition') -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.morph = _arg4
        res._cond = _arg5
        return res
    
    @staticmethod
    def _new395(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : str, _arg5 : str) -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        res.alt_value = _arg5
        return res
    
    @staticmethod
    def _new1117(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : bool) -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.is_railway = _arg4
        return res
    
    @staticmethod
    def _new1118(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : bool, _arg5 : int) -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.is_railway = _arg4
        res.noun_is_doubt_coef = _arg5
        return res
    
    # static constructor for class StreetItemToken
    @staticmethod
    def _static_ctor():
        StreetItemToken.__m_reg_tails = ["ГОРОДОК", "РАЙОН", "МАССИВ", "МАСИВ", "КОМПЛЕКС", "ЗОНА", "КВАРТАЛ", "ОТДЕЛЕНИЕ", "ПАРК", "МЕСТНОСТЬ", "РАЗЪЕЗД", "УРОЧИЩЕ", "САД"]
        StreetItemToken.__m_spec_tails = ["БУДКА", "КАЗАРМА"]

StreetItemToken._static_ctor()