# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
import io
from pullenti.unisharp.Utils import Utils

from pullenti.morph.MorphClass import MorphClass
from pullenti.morph.MorphCase import MorphCase
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.morph.MorphWordForm import MorphWordForm
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.Referent import Referent
from pullenti.ner.MetaToken import MetaToken
from pullenti.morph.MorphBaseInfo import MorphBaseInfo
from pullenti.morph.MorphologyService import MorphologyService
from pullenti.ner.geo.internal.OrgItemToken import OrgItemToken
from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.address.StreetKind import StreetKind
from pullenti.ner.Token import Token
from pullenti.ner.TextToken import TextToken
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.address.internal.StreetItemType import StreetItemType
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.ner.address.internal.AddressItemType import AddressItemType
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.core.NumberHelper import NumberHelper
from pullenti.ner.address.StreetReferent import StreetReferent
from pullenti.ner.address.internal.AddressItemToken import AddressItemToken
from pullenti.ner.geo.internal.MiscLocationHelper import MiscLocationHelper
from pullenti.ner.address.internal.StreetItemToken import StreetItemToken

class StreetDefineHelper:
    
    @staticmethod
    def check_street_after(t : 'Token') -> bool:
        if (t is None): 
            return False
        while t is not None and ((t.is_char_of(",;") or t.morph.class0_.is_preposition)):
            t = t.next0_
        li = StreetItemToken.try_parse_list(t, 10, None)
        if (li is None): 
            return False
        rt = StreetDefineHelper._try_parse_street(li, False, False, False)
        if (rt is not None and rt.begin_token == t): 
            return True
        else: 
            return False
    
    @staticmethod
    def try_parse_ext_street(sli : typing.List['StreetItemToken']) -> 'ReferentToken':
        a = StreetDefineHelper._try_parse_street(sli, True, False, False)
        if (a is not None): 
            return ReferentToken(a.referent, a.begin_token, a.end_token)
        return None
    
    @staticmethod
    def _try_parse_street(sli : typing.List['StreetItemToken'], ext_onto_regim : bool=False, for_metro : bool=False, street_before : bool=False) -> 'AddressItemToken':
        if (sli is None or len(sli) == 0): 
            return None
        if ((len(sli) == 2 and sli[0].typ == StreetItemType.NUMBER and sli[1].typ == StreetItemType.NOUN) and sli[1].is_abridge): 
            if (MiscLocationHelper.check_geo_object_before(sli[0].begin_token, False)): 
                pass
            elif (StreetItemToken._is_region(sli[1].termin.canonic_text) and MiscLocationHelper.is_user_param_address(sli[1])): 
                pass
            else: 
                return None
        if ((len(sli) == 2 and sli[0].typ == StreetItemType.NOUN and sli[0].noun_is_doubt_coef > 1) and sli[0].begin_token.is_value("КВ", None) and sli[1].typ == StreetItemType.NUMBER): 
            at = AddressItemToken.try_parse_pure_item(sli[0].begin_token, None, None)
            if (at is not None and at.value is not None): 
                return None
        if (((len(sli) == 4 and sli[0].typ == StreetItemType.NOUN and sli[1].typ == StreetItemType.NUMBER) and sli[2].typ == StreetItemType.NOUN and sli[0].termin == sli[2].termin) and ((sli[3].typ == StreetItemType.NAME or sli[3].typ == StreetItemType.STDNAME or sli[3].typ == StreetItemType.STDADJECTIVE))): 
            del sli[2]
        i = 0
        j = 0
        not_doubt = False
        is_terr = False
        i = 0
        while i < len(sli): 
            if (i == 0 and sli[i].typ == StreetItemType.FIX and ((len(sli) == 1 or sli[1].typ != StreetItemType.NOUN or sli[0]._org0_ is not None))): 
                return StreetDefineHelper.__try_parse_fix(sli)
            elif (sli[i].typ == StreetItemType.NOUN): 
                if (((i + 1) < len(sli)) and sli[i + 1]._org0_ is not None): 
                    return None
                if (i == 0 and sli[i].termin.canonic_text == "УЛИЦА" and ((i + 2) < len(sli))): 
                    if (sli[i + 1].typ == StreetItemType.NOUN and ((StreetItemToken._is_region(sli[i + 1].termin.canonic_text) or sli[i + 1].termin.canonic_text == "ЛИНИЯ" or sli[i + 1].begin_token.is_value("ДОРОГА", None)))): 
                        ss = sli[i + 1].clone()
                        ss.begin_token = sli[i].begin_token
                        sli[i + 1] = ss
                        del sli[i]
                        not_doubt = True
                        break
                    elif ((((i + 2) < len(sli)) and sli[i + 1].typ == StreetItemType.NUMBER and sli[i + 2].typ == StreetItemType.NOUN) and (((StreetItemToken._is_region(sli[i + 2].termin.canonic_text) or sli[i + 2].termin.canonic_text == "ЛИНИЯ" or sli[i + 2].begin_token.is_value("ДОРОГА", None)) or ((sli[i + 2].typ == StreetItemType.NOUN and len(sli) == (i + 3)))))): 
                        ss = sli[i + 1].clone()
                        ss.begin_token = sli[i].begin_token
                        sli[i + 1] = ss
                        del sli[i]
                        not_doubt = True
                        i += 1
                        break
                if (sli[i].termin.canonic_text == "МЕТРО"): 
                    if ((i + 1) < len(sli)): 
                        sli1 = list()
                        ii = i + 1
                        while ii < len(sli): 
                            sli1.append(sli[ii])
                            ii += 1
                        str1 = StreetDefineHelper._try_parse_street(sli1, ext_onto_regim, True, False)
                        if (str1 is not None): 
                            str1.begin_token = sli[i].begin_token
                            str1.is_doubt = sli[i].is_abridge
                            if (sli[i + 1].is_in_brackets): 
                                str1.is_doubt = False
                            return str1
                    elif (i == 1 and sli[0].typ == StreetItemType.NAME): 
                        for_metro = True
                        break
                    if (i == 0 and len(sli) > 0): 
                        for_metro = True
                        break
                    return None
                if (i == 0 and (i + 1) >= len(sli) and ((sli[i].termin.canonic_text == "ВОЕННЫЙ ГОРОДОК" or sli[i].termin.canonic_text == "ПРОМЗОНА"))): 
                    stri0 = StreetReferent()
                    stri0._add_typ("микрорайон")
                    stri0.add_slot(StreetReferent.ATTR_NAME, sli[i].termin.canonic_text, False, 0)
                    return AddressItemToken._new329(AddressItemType.STREET, sli[0].begin_token, sli[0].end_token, stri0, True)
                if (i == 0 and (i + 1) >= len(sli) and sli[i].termin.canonic_text == "МИКРОРАЙОН"): 
                    stri0 = StreetReferent()
                    stri0.kind = StreetKind.AREA
                    stri0.add_slot(StreetReferent.ATTR_TYPE, sli[i].termin.canonic_text.lower(), False, 0)
                    return AddressItemToken._new329(AddressItemType.STREET, sli[0].begin_token, sli[0].end_token, stri0, True)
                if (sli[i].termin.canonic_text == "ПЛОЩАДЬ" or sli[i].termin.canonic_text == "ПЛОЩА"): 
                    tt = sli[i].end_token.next0_
                    if (tt is not None and ((tt.is_hiphen or tt.is_char(':')))): 
                        tt = tt.next0_
                    nex = NumberHelper.try_parse_number_with_postfix(tt)
                    if (nex is not None): 
                        return None
                    if (i > 0 and sli[i - 1].value == "ПРОЕКТИРУЕМЫЙ"): 
                        return None
                break
            i += 1
        if (i >= len(sli)): 
            return StreetDefineHelper.__try_detect_non_noun(sli, ext_onto_regim, for_metro, street_before)
        name = None
        number = None
        age = None
        adj = None
        noun = sli[i]
        alt_noun = None
        is_micro_raion = StreetItemToken._is_region(noun.termin.canonic_text)
        before = 0
        after = 0
        j = 0
        while j < i: 
            if (((sli[j].typ == StreetItemType.NAME or sli[j].typ == StreetItemType.STDNAME or sli[j].typ == StreetItemType.FIX) or sli[j].typ == StreetItemType.STDADJECTIVE or sli[j].typ == StreetItemType.STDPARTOFNAME) or sli[j].typ == StreetItemType.AGE): 
                before += 1
            elif (sli[j].typ == StreetItemType.NUMBER): 
                if (sli[j].is_newline_after): 
                    return None
                if (sli[j].number is not None and sli[j].number.morph.class0_.is_adjective): 
                    before += 1
                elif (is_micro_raion or not_doubt): 
                    before += 1
                elif (sli[i].number_has_prefix or sli[i].is_number_km): 
                    before += 1
                elif (MiscLocationHelper.is_user_param_address(sli[i])): 
                    before += 1
            else: 
                before += 1
            j += 1
        j = (i + 1)
        while j < len(sli): 
            if (before > 0 and sli[j].is_newline_before): 
                break
            elif (((sli[j].typ == StreetItemType.NAME or sli[j].typ == StreetItemType.STDNAME or sli[j].typ == StreetItemType.FIX) or sli[j].typ == StreetItemType.STDADJECTIVE or sli[j].typ == StreetItemType.STDPARTOFNAME) or sli[j].typ == StreetItemType.AGE): 
                after += 1
            elif (sli[j].typ == StreetItemType.NUMBER): 
                if (sli[j].number is not None and sli[j].number.morph.class0_.is_adjective): 
                    after += 1
                elif (is_micro_raion or not_doubt): 
                    after += 1
                elif (sli[j].number_has_prefix or sli[j].is_number_km): 
                    after += 1
                elif (ext_onto_regim): 
                    after += 1
                elif (len(sli) == 2 and sli[0].typ == StreetItemType.NOUN and j == 1): 
                    after += 1
                elif ((len(sli) == 3 and sli[0].typ == StreetItemType.NOUN and sli[2].typ == StreetItemType.NOUN) and j == 1 and sli[2].termin.canonic_text == "ЛИНИЯ"): 
                    after += 1
            elif (sli[j].typ == StreetItemType.NOUN): 
                if (j == (i + 1) and alt_noun is None and not StreetItemToken._is_region(sli[j].termin.canonic_text)): 
                    alt_noun = sli[j]
                else: 
                    break
            else: 
                after += 1
            j += 1
        rli = list()
        n0 = 0
        n1 = 0
        if (before > after): 
            if (noun.termin.canonic_text == "МЕТРО"): 
                return None
            if (noun.termin.canonic_text == "КВАРТАЛ" and not ext_onto_regim and not street_before): 
                if (sli[0].typ == StreetItemType.NUMBER and len(sli) == 2): 
                    if (not AddressItemToken.check_house_after(sli[1].end_token.next0_, False, False)): 
                        if (not MiscLocationHelper.check_geo_object_before(sli[0].begin_token, False)): 
                            return None
                        if (sli[0].begin_token.previous is not None and sli[0].begin_token.previous.get_morph_class_in_dictionary().is_preposition): 
                            return None
            tt = sli[0].begin_token
            if (tt == sli[0].end_token and noun.begin_token == sli[0].end_token.next0_): 
                if (not tt.morph.class0_.is_adjective and not (isinstance(tt, NumberToken))): 
                    if ((sli[0].is_newline_before or not MiscLocationHelper.check_geo_object_before(sli[0].begin_token, False) or noun.morph.case_.is_genitive) or noun.morph.case_.is_instrumental): 
                        ok = False
                        if (AddressItemToken.check_house_after(noun.end_token.next0_, False, True)): 
                            ok = True
                        elif (noun.end_token.next0_ is None): 
                            ok = True
                        elif (noun.is_newline_after and MiscLocationHelper.check_geo_object_before(sli[0].begin_token, False)): 
                            ok = True
                        if (not ok): 
                            if ((noun.chars.is_latin_letter and noun.chars.is_capital_upper and sli[0].chars.is_latin_letter) and sli[0].chars.is_capital_upper): 
                                ok = True
                        if (not ok): 
                            return None
            n0 = 0
            n1 = (i - 1)
        elif (i == 1 and sli[0].typ == StreetItemType.NUMBER): 
            if (not sli[0].is_whitespace_after): 
                return None
            number = (sli[0].value if sli[0].number is None else str(sli[0].number.int_value))
            if (sli[0].is_number_km): 
                number += "км"
            n0 = (i + 1)
            n1 = (len(sli) - 1)
            rli.append(sli[0])
            rli.append(sli[i])
        elif (after > before): 
            n0 = (i + 1)
            n1 = (len(sli) - 1)
            rli.append(sli[i])
            if (alt_noun is not None and alt_noun == sli[i + 1]): 
                rli.append(sli[i + 1])
                n0 += 1
        elif (after == 0): 
            return None
        elif ((len(sli) > 2 and ((sli[0].typ == StreetItemType.NAME or sli[0].typ == StreetItemType.STDADJECTIVE or sli[0].typ == StreetItemType.STDNAME)) and sli[1].typ == StreetItemType.NOUN) and sli[2].typ == StreetItemType.NUMBER): 
            n0 = 0
            n1 = 0
            num = False
            tt2 = sli[2].end_token.next0_
            if (sli[2].is_number_km): 
                num = True
            elif (sli[0].begin_token.previous is not None and sli[0].begin_token.previous.is_value("КИЛОМЕТР", None)): 
                sli[2].is_number_km = True
                num = True
            elif (sli[2].begin_token.previous.is_comma): 
                pass
            elif (sli[2].begin_token != sli[2].end_token): 
                num = True
            elif (AddressItemToken.check_house_after(sli[2].end_token.next0_, False, True)): 
                num = True
            elif (sli[2].morph.class0_.is_adjective and (sli[2].whitespaces_before_count < 2)): 
                if (sli[2].end_token.next0_ is None or sli[2].end_token.is_comma or sli[2].is_newline_after): 
                    num = True
            if (num): 
                number = (sli[2].value if sli[2].number is None else str(sli[2].number.int_value))
                if (sli[2].is_number_km): 
                    number += "км"
                rli.append(sli[2])
            else: 
                del sli[2:2+len(sli) - 2]
        elif ((len(sli) > 2 and sli[0].typ == StreetItemType.STDADJECTIVE and sli[1].typ == StreetItemType.NOUN) and sli[2].typ == StreetItemType.STDNAME): 
            n0 = 0
            n1 = -1
            rli.append(sli[0])
            rli.append(sli[2])
            adj = sli[0]
            name = sli[2]
        else: 
            return None
        sec_number = None
        j = n0
        first_pass2758 = True
        while True:
            if first_pass2758: first_pass2758 = False
            else: j += 1
            if (not (j <= n1)): break
            if (sli[j].typ == StreetItemType.NUMBER): 
                if (sli[j].is_newline_before and j > 0): 
                    break
                if (number is not None): 
                    if (name is not None and name.typ == StreetItemType.STDNAME): 
                        sec_number = (sli[j].value if sli[j].number is None else str(sli[j].number.int_value))
                        if (sli[j].is_number_km): 
                            sec_number += "км"
                        rli.append(sli[j])
                        continue
                    if (((j + 1) < len(sli)) and sli[j + 1].typ == StreetItemType.STDNAME): 
                        sec_number = (sli[j].value if sli[j].number is None else str(sli[j].number.int_value))
                        if (sli[j].is_number_km): 
                            sec_number += "км"
                        rli.append(sli[j])
                        continue
                    break
                if (sli[j].number is not None and sli[j].number.typ == NumberSpellingType.DIGIT and not sli[j].number.morph.class0_.is_adjective): 
                    if (sli[j].whitespaces_before_count > 2 and j > 0): 
                        break
                    if (sli[j].number is not None and sli[j].number.int_value > 20): 
                        if (j > n0): 
                            if (((j + 1) < len(sli)) and sli[j + 1].typ == StreetItemType.NOUN): 
                                pass
                            else: 
                                break
                    if (j == n0 and n0 > 0): 
                        pass
                    elif (j == n0 and n0 == 0 and sli[j].whitespaces_after_count == 1): 
                        pass
                    elif (sli[j].number_has_prefix or sli[j].is_number_km): 
                        pass
                    elif (j == n1 and ((n1 + 1) < len(sli)) and sli[n1 + 1].typ == StreetItemType.NOUN): 
                        pass
                    else: 
                        break
                number = (sli[j].value if sli[j].number is None else str(sli[j].number.int_value))
                if (sli[j].is_number_km): 
                    number += "км"
                rli.append(sli[j])
            elif (sli[j].typ == StreetItemType.AGE): 
                if (number is not None or age is not None): 
                    break
                age = str(sli[j].number.int_value)
                rli.append(sli[j])
            elif (sli[j].typ == StreetItemType.STDADJECTIVE): 
                if (adj is not None): 
                    if (j == (len(sli) - 1) and not sli[j].is_abridge and name is None): 
                        name = sli[j]
                        rli.append(sli[j])
                        continue
                    else: 
                        return None
                adj = sli[j]
                rli.append(sli[j])
            elif (sli[j].typ == StreetItemType.NAME or sli[j].typ == StreetItemType.STDNAME or sli[j].typ == StreetItemType.FIX): 
                if (name is not None): 
                    if (j > 1 and sli[j - 2].typ == StreetItemType.NOUN): 
                        if (name.noun_can_be_name and sli[j - 2].termin.canonic_text == "УЛИЦА" and j == (len(sli) - 1)): 
                            noun = name
                        elif ((is_micro_raion and sli[j - 1].termin is not None and StreetItemToken._is_region(sli[j - 1].termin.canonic_text)) and j == (len(sli) - 1)): 
                            noun = name
                        else: 
                            break
                    elif (i < j): 
                        break
                    else: 
                        return None
                name = sli[j]
                rli.append(sli[j])
            elif (sli[j].typ == StreetItemType.STDPARTOFNAME and j == n1): 
                if (name is not None): 
                    break
                name = sli[j]
                rli.append(sli[j])
            elif (sli[j].typ == StreetItemType.NOUN): 
                if ((sli[0] == noun and ((noun.termin.canonic_text == "УЛИЦА" or noun.termin.canonic_text == "ВУЛИЦЯ")) and j > 0) and name is None): 
                    if (sli[j].termin.canonic_text == "ЛИНИЯ"): 
                        name = sli[j]
                    else: 
                        alt_noun = noun
                        noun = sli[j]
                    rli.append(sli[j])
                else: 
                    break
        if (((n1 < i) and number is None and ((i + 1) < len(sli))) and sli[i + 1].typ == StreetItemType.NUMBER and sli[i + 1].number_has_prefix): 
            number = (sli[i + 1].value if sli[i + 1].number is None else str(sli[i + 1].number.int_value))
            rli.append(sli[i + 1])
        elif ((((i < n0) and ((name is not None or adj is not None)) and (j < len(sli))) and sli[j].typ == StreetItemType.NOUN and ((noun.termin.canonic_text == "УЛИЦА" or noun.termin.canonic_text == "ВУЛИЦЯ"))) and (((sli[j].termin.canonic_text == "ПЛОЩАДЬ" or sli[j].termin.canonic_text == "БУЛЬВАР" or sli[j].termin.canonic_text == "ПЛОЩА") or sli[j].termin.canonic_text == "МАЙДАН" or (j + 1) == len(sli)))): 
            alt_noun = noun
            noun = sli[j]
            rli.append(sli[j])
        if (name is None): 
            if (number is None and age is None and adj is None): 
                return None
            if (noun.is_abridge): 
                if (is_micro_raion or not_doubt): 
                    pass
                elif (noun.termin is not None and ((noun.termin.canonic_text == "ПРОЕЗД" or noun.termin.canonic_text == "ПРОЇЗД"))): 
                    pass
                elif (adj is None or adj.is_abridge): 
                    return None
            if (adj is not None and adj.is_abridge): 
                if (not noun.is_abridge and MiscLocationHelper.is_user_param_address(adj)): 
                    pass
                else: 
                    return None
        if (not sli[i] in rli): 
            rli.append(sli[i])
        street = StreetReferent()
        if (not for_metro): 
            street._add_typ(noun.termin.canonic_text.lower())
            if (noun.alt_termin is not None): 
                if (noun.alt_termin.canonic_text == "ПРОСПЕКТ" and number is not None): 
                    pass
                else: 
                    street.add_slot(StreetReferent.ATTR_TYPE, noun.alt_termin.canonic_text.lower(), False, 0)
            if (alt_noun is not None): 
                street._add_typ(alt_noun.termin.canonic_text.lower())
        else: 
            street._add_typ("метро")
        res = AddressItemToken._new231(AddressItemType.STREET, rli[0].begin_token, rli[0].end_token, street)
        if (noun.termin.canonic_text == "ЛИНИЯ"): 
            if (number is None): 
                if (MiscLocationHelper.check_geo_object_before(sli[0].begin_token, False)): 
                    pass
                else: 
                    return None
            res.is_doubt = True
        elif (noun.termin.canonic_text == "ПУНКТ"): 
            if (not MiscLocationHelper.check_geo_object_before(sli[0].begin_token, False)): 
                return None
            if (name is None or number is not None): 
                return None
        for r in rli: 
            if (res.begin_char > r.begin_char): 
                res.begin_token = r.begin_token
            if (res.end_char < r.end_char): 
                res.end_token = r.end_token
        if (for_metro and noun in rli and noun.termin.canonic_text == "МЕТРО"): 
            rli.remove(noun)
        if (noun.is_abridge and (noun.length_char < 4)): 
            res.is_doubt = True
        elif (noun.noun_is_doubt_coef > 0 and not not_doubt and not MiscLocationHelper.is_user_param_address(noun)): 
            res.is_doubt = True
            if ((name is not None and name.end_char > noun.end_char and noun.chars.is_all_lower) and not name.chars.is_all_lower and not (isinstance(name.begin_token, ReferentToken))): 
                npt2 = MiscLocationHelper._try_parse_npt(name.begin_token)
                if (npt2 is not None and npt2.end_char > name.end_char): 
                    pass
                elif (AddressItemToken.check_house_after(res.end_token.next0_, False, False)): 
                    res.is_doubt = False
                elif (name.chars.is_capital_upper and noun.noun_is_doubt_coef == 1): 
                    res.is_doubt = False
        name_base = io.StringIO()
        name_alt = io.StringIO()
        name_alt2 = None
        gen = noun.termin.gender
        adj_gen = MorphGender.UNDEFINED
        if (number is not None): 
            street.number = number
            if (sec_number is not None): 
                street.sec_number = sec_number
        if (age is not None): 
            if (street.number is None): 
                street.number = age
            else: 
                street.sec_number = age
        if (name is not None and name.value is not None): 
            if (street.kind == StreetKind.ROAD): 
                for r in rli: 
                    if (r.typ == StreetItemType.NAME and r != name): 
                        print(r.value, end="", file=name_alt)
                        break
            if (name.alt_value is not None and name_alt.tell() == 0): 
                print("{0} {1}".format(Utils.toStringStringIO(name_base), name.alt_value), end="", file=name_alt, flush=True)
            print(" {0}".format(name.value), end="", file=name_base, flush=True)
        elif (name is not None): 
            is_adj = False
            if (isinstance(name.end_token, TextToken)): 
                for wf in name.end_token.morph.items: 
                    if ((isinstance(wf, MorphWordForm)) and wf.is_in_dictionary): 
                        is_adj = (wf.class0_.is_adjective | wf.class0_.is_proper_geo)
                        adj_gen = wf.gender
                        break
                    elif (wf.class0_.is_adjective | wf.class0_.is_proper_geo): 
                        is_adj = True
            if (is_adj): 
                tmp = io.StringIO()
                vars0_ = list()
                t = name.begin_token
                while t is not None: 
                    tt = Utils.asObjectOrNull(t, TextToken)
                    if (tt is None): 
                        break
                    if (tmp.tell() > 0 and Utils.getCharAtStringIO(tmp, tmp.tell() - 1) != ' '): 
                        print(' ', end="", file=tmp)
                    if (t == name.end_token): 
                        is_padez = False
                        if (not noun.is_abridge): 
                            if (not noun.morph.case_.is_undefined and not noun.morph.case_.is_nominative): 
                                is_padez = True
                            elif (noun.termin.canonic_text == "ШОССЕ" or noun.termin.canonic_text == "ШОСЕ"): 
                                is_padez = True
                        if (res.begin_token.previous is not None and res.begin_token.previous.morph.class0_.is_preposition): 
                            is_padez = True
                        if (not is_padez): 
                            print(tt.term, end="", file=tmp)
                            break
                        for wf in tt.morph.items: 
                            if (((wf.class0_.is_adjective or wf.class0_.is_proper_geo)) and ((wf.gender) & (gen)) != (MorphGender.UNDEFINED)): 
                                if (noun.morph.case_.is_undefined or not ((wf.case_) & noun.morph.case_).is_undefined): 
                                    wff = Utils.asObjectOrNull(wf, MorphWordForm)
                                    if (wff is None): 
                                        continue
                                    if (gen == MorphGender.MASCULINE and "ОЙ" in wff.normal_case): 
                                        continue
                                    if (not wff.normal_case in vars0_): 
                                        vars0_.append(wff.normal_case)
                        if (not tt.term in vars0_ and Utils.indexOfList(sli, name, 0) > Utils.indexOfList(sli, noun, 0)): 
                            vars0_.append(tt.term)
                        if (len(vars0_) == 0): 
                            vars0_.append(tt.term)
                        break
                    if (not tt.is_hiphen): 
                        print(tt.term, end="", file=tmp)
                    t = t.next0_
                if (len(vars0_) == 0): 
                    print(" {0}".format(Utils.toStringStringIO(tmp)), end="", file=name_base, flush=True)
                else: 
                    head = Utils.toStringStringIO(name_base)
                    print(" {0}{1}".format(Utils.toStringStringIO(tmp), vars0_[0]), end="", file=name_base, flush=True)
                    src = MiscHelper.get_text_value_of_meta_token(name, GetTextAttr.NO)
                    ii = Utils.indexOfList(vars0_, src, 0)
                    if (ii > 1): 
                        del vars0_[ii]
                        vars0_.insert(1, src)
                    elif (ii < 0): 
                        vars0_.insert(1, src)
                    if (len(vars0_) > 1): 
                        Utils.setLengthStringIO(name_alt, 0)
                        print("{0} {1}{2}".format(head, Utils.toStringStringIO(tmp), vars0_[1]), end="", file=name_alt, flush=True)
                    if (len(vars0_) > 2): 
                        name_alt2 = "{0} {1}{2}".format(head, Utils.toStringStringIO(tmp), vars0_[2])
            else: 
                str_nam = None
                nits = list()
                has_adj = False
                has_proper_name = False
                t = name.begin_token
                while t is not None and t.end_char <= name.end_char: 
                    if (t.morph.class0_.is_adjective or t.morph.class0_.is_conjunction): 
                        has_adj = True
                    if ((isinstance(t, TextToken)) and not t.is_hiphen): 
                        if (name.termin is not None): 
                            nits.append(name.termin.canonic_text)
                            break
                        elif (not t.chars.is_letter and len(nits) > 0): 
                            nits[len(nits) - 1] += t.term
                        else: 
                            nits.append(t.term)
                            if (t == name.begin_token and t.get_morph_class_in_dictionary().is_proper_name): 
                                has_proper_name = True
                    elif ((isinstance(t, ReferentToken)) and name.termin is None): 
                        nits.append(t.get_source_text().upper())
                    t = t.next0_
                if (not has_adj and not has_proper_name and not name.is_in_dictionary): 
                    nits.sort()
                str_nam = Utils.joinStrings(" ", list(nits))
                if (has_proper_name and len(nits) == 2): 
                    Utils.setLengthStringIO(name_alt, 0)
                    print("{0} {1}".format(Utils.toStringStringIO(name_base), nits[1]), end="", file=name_alt, flush=True)
                print(" {0}".format(str_nam), end="", file=name_base, flush=True)
        adj_str = None
        adj_can_be_initial = False
        if (adj is not None): 
            s = None
            if (adj_gen == MorphGender.UNDEFINED and name is not None and ((name.morph.number) & (MorphNumber.PLURAL)) == (MorphNumber.UNDEFINED)): 
                if (name.morph.gender == MorphGender.FEMINIE or name.morph.gender == MorphGender.MASCULINE or name.morph.gender == MorphGender.NEUTER): 
                    adj_gen = name.morph.gender
            if (name is not None and ((name.morph.number) & (MorphNumber.PLURAL)) != (MorphNumber.UNDEFINED)): 
                s = MorphologyService.get_wordform(adj.termin.canonic_text, MorphBaseInfo._new332(MorphClass.ADJECTIVE, MorphNumber.PLURAL))
            elif (adj_gen != MorphGender.UNDEFINED): 
                s = MorphologyService.get_wordform(adj.termin.canonic_text, MorphBaseInfo._new333(MorphClass.ADJECTIVE, adj_gen))
            elif (((adj.morph.gender) & (gen)) == (MorphGender.UNDEFINED)): 
                s = MorphologyService.get_wordform(adj.termin.canonic_text, MorphBaseInfo._new333(MorphClass.ADJECTIVE, adj.morph.gender))
            else: 
                s = MorphologyService.get_wordform(adj.termin.canonic_text, MorphBaseInfo._new333(MorphClass.ADJECTIVE, gen))
            adj_str = s
            if (name is not None and (Utils.indexOfList(sli, adj, 0) < Utils.indexOfList(sli, name, 0))): 
                if (adj.end_token.is_char('.') and adj.length_char <= 3 and not adj.begin_token.chars.is_all_lower): 
                    adj_can_be_initial = True
        s1 = Utils.toStringStringIO(name_base).strip()
        s2 = Utils.toStringStringIO(name_alt).strip()
        if ((len(s1) < 3) and street.kind != StreetKind.ROAD): 
            if (street.number is not None): 
                if (adj_str is not None): 
                    if (adj.is_abridge): 
                        return None
                    street.add_slot(StreetReferent.ATTR_NAME, adj_str, False, 0)
            elif (adj_str is None): 
                if (len(s1) < 1): 
                    return None
                if (is_micro_raion): 
                    street.add_slot(StreetReferent.ATTR_NAME, s1, False, 0)
                    if (not Utils.isNullOrEmpty(s2)): 
                        street.add_slot(StreetReferent.ATTR_NAME, s2, False, 0)
                else: 
                    return None
            else: 
                if (adj.is_abridge and not MiscLocationHelper.is_user_param_address(adj)): 
                    return None
                street.add_slot(StreetReferent.ATTR_NAME, adj_str, False, 0)
        elif (adj_can_be_initial): 
            street.add_slot(StreetReferent.ATTR_NAME, s1, False, 0)
            street.add_slot(StreetReferent.ATTR_NAME, MiscHelper.get_text_value(adj.begin_token, name.end_token, GetTextAttr.NO), False, 0)
            street.add_slot(StreetReferent.ATTR_NAME, "{0} {1}".format(adj_str, s1), False, 0)
        elif (adj_str is None): 
            street.add_slot(StreetReferent.ATTR_NAME, s1, False, 0)
        else: 
            street.add_slot(StreetReferent.ATTR_NAME, "{0} {1}".format(adj_str, s1), False, 0)
        if (name_alt.tell() > 0): 
            s1 = Utils.toStringStringIO(name_alt).strip()
            if (adj_str is None): 
                street.add_slot(StreetReferent.ATTR_NAME, s1, False, 0)
            else: 
                street.add_slot(StreetReferent.ATTR_NAME, "{0} {1}".format(adj_str, s1), False, 0)
        if (name_alt2 is not None): 
            if (adj_str is None): 
                if (for_metro and noun is not None): 
                    street.add_slot(StreetReferent.ATTR_NAME, "{0} {1}".format(alt_noun.termin.canonic_text, name_alt2.strip()), False, 0)
                else: 
                    street.add_slot(StreetReferent.ATTR_NAME, name_alt2.strip(), False, 0)
            else: 
                street.add_slot(StreetReferent.ATTR_NAME, "{0} {1}".format(adj_str, name_alt2.strip()), False, 0)
        if (name is not None and name.alt_value2 is not None): 
            street.add_slot(StreetReferent.ATTR_NAME, name.alt_value2, False, 0)
        if ((name is not None and adj is None and name.exist_street is not None) and not for_metro): 
            for n in name.exist_street.names: 
                street.add_slot(StreetReferent.ATTR_NAME, n, False, 0)
        if (alt_noun is not None and not for_metro): 
            street._add_typ(alt_noun.termin.canonic_text.lower())
        if (noun.termin.canonic_text == "ПЛОЩАДЬ" or noun.termin.canonic_text == "КВАРТАЛ" or noun.termin.canonic_text == "ПЛОЩА"): 
            res.is_doubt = True
            if (name is not None and name.is_in_dictionary): 
                res.is_doubt = False
            elif (alt_noun is not None or for_metro): 
                res.is_doubt = False
            elif (name is not None and StreetItemToken.check_std_name(name.begin_token) is not None): 
                res.is_doubt = False
            elif (res.begin_token.previous is None or MiscLocationHelper.check_geo_object_before(res.begin_token.previous, False)): 
                if (res.end_token.next0_ is None or AddressItemToken.check_house_after(res.end_token.next0_, False, True)): 
                    res.is_doubt = False
        if (LanguageHelper.ends_with(noun.termin.canonic_text, "ГОРОДОК")): 
            street.kind = StreetKind.AREA
            for s in street.slots: 
                if (s.type_name == StreetReferent.ATTR_TYPE): 
                    street.upload_slot(s, "микрорайон")
                elif (s.type_name == StreetReferent.ATTR_NAME): 
                    street.upload_slot(s, "{0} {1}".format(noun.termin.canonic_text, s.value))
            if (street.find_slot(StreetReferent.ATTR_NAME, None, True) is None): 
                street.add_slot(StreetReferent.ATTR_NAME, noun.termin.canonic_text, False, 0)
        t1 = res.end_token.next0_
        if (t1 is not None and t1.is_comma): 
            t1 = t1.next0_
        non = StreetItemToken.try_parse(t1, None, False, None)
        if (non is not None and non.typ == StreetItemType.NOUN and len(street.typs) > 0): 
            if (AddressItemToken.check_house_after(non.end_token.next0_, False, True)): 
                street._correct()
                nams = street.names
                for t in street.typs: 
                    if (t != "улица"): 
                        for n in nams: 
                            street.add_slot(StreetReferent.ATTR_NAME, "{0} {1}".format(t.upper(), n), False, 0)
                street.add_slot(StreetReferent.ATTR_TYPE, non.termin.canonic_text.lower(), False, 0)
                res.end_token = non.end_token
        if (street.find_slot(StreetReferent.ATTR_NAME, "ПРОЕКТИРУЕМЫЙ", True) is not None and street.number is None): 
            if (non is not None and non.typ == StreetItemType.NUMBER): 
                street.number = non.number.value
                res.end_token = non.end_token
            else: 
                ttt = MiscHelper.check_number_prefix(res.end_token.next0_)
                if (ttt is not None): 
                    non = StreetItemToken.try_parse(ttt, None, False, None)
                    if (non is not None and non.typ == StreetItemType.NUMBER): 
                        street.number = non.number.value
                        res.end_token = non.end_token
        if (res.is_doubt): 
            if (noun.is_road): 
                street.kind = StreetKind.ROAD
                if (street.number is not None and Utils.endsWithString(street.number, "КМ", True)): 
                    res.is_doubt = False
                elif (AddressItemToken.check_km_after(res.end_token.next0_)): 
                    res.is_doubt = False
                elif (AddressItemToken.check_km_before(res.begin_token.previous)): 
                    res.is_doubt = False
            elif (noun.termin.canonic_text == "ПРОЕЗД" and street.find_slot(StreetReferent.ATTR_NAME, "ПРОЕКТИРУЕМЫЙ", True) is not None): 
                res.is_doubt = False
            tt0 = res.begin_token.previous
            first_pass2759 = True
            while True:
                if first_pass2759: first_pass2759 = False
                else: tt0 = tt0.previous
                if (not (tt0 is not None)): break
                if (tt0.is_char_of(",.") or tt0.is_comma_and): 
                    continue
                str0 = Utils.asObjectOrNull(tt0.get_referent(), StreetReferent)
                if (str0 is not None): 
                    res.is_doubt = False
                break
            if (res.is_doubt): 
                if (AddressItemToken.check_house_after(res.end_token.next0_, False, False)): 
                    res.is_doubt = False
                elif (AddressItemToken.check_street_after(res.end_token.next0_, False)): 
                    res.is_doubt = False
                elif (MiscLocationHelper.check_geo_object_before(res.begin_token, False)): 
                    res.is_doubt = False
                ttt = res.begin_token.next0_
                while ttt is not None and ttt.end_char <= res.end_char: 
                    if (ttt.is_newline_before): 
                        res.is_doubt = True
                    ttt = ttt.next0_
        if (noun.termin.canonic_text == "КВАРТАЛ" and (res.whitespaces_after_count < 2) and number is None): 
            ait = AddressItemToken.try_parse_pure_item(res.end_token.next0_, None, None)
            if (ait is not None and ait.typ == AddressItemType.NUMBER and ait.value is not None): 
                street.add_slot(StreetReferent.ATTR_NUMBER, ait.value, False, 0)
                res.end_token = ait.end_token
        if (age is not None and street.find_slot(StreetReferent.ATTR_NAME, None, True) is None): 
            street.add_slot(StreetReferent.ATTR_NAME, "ЛЕТ", False, 0)
        for r in rli: 
            if (r._orto_terr is not None): 
                res.orto_terr = r._orto_terr
                break
        return res
    
    @staticmethod
    def __try_detect_non_noun(sli : typing.List['StreetItemToken'], onto_regim : bool, for_metro : bool, street_before : bool) -> 'AddressItemToken':
        if (len(sli) > 1 and sli[len(sli) - 1].typ == StreetItemType.NUMBER and not sli[len(sli) - 1].number_has_prefix): 
            del sli[len(sli) - 1]
        street = None
        if (len(sli) == 1 and ((sli[0].typ == StreetItemType.NAME or sli[0].typ == StreetItemType.STDNAME or sli[0].typ == StreetItemType.STDADJECTIVE)) and ((onto_regim or for_metro))): 
            s = MiscHelper.get_text_value(sli[0].begin_token, sli[0].end_token, GetTextAttr.NO)
            if (s is None): 
                return None
            if (not for_metro and not sli[0].is_in_dictionary and sli[0].exist_street is None): 
                tt = sli[0].end_token.next0_
                if (tt is not None and tt.is_comma): 
                    tt = tt.next0_
                ait1 = AddressItemToken.try_parse_pure_item(tt, None, None)
                if (ait1 is not None and ((ait1.typ == AddressItemType.NUMBER or ait1.typ == AddressItemType.HOUSE))): 
                    pass
                else: 
                    return None
            street = StreetReferent()
            street.add_slot(StreetReferent.ATTR_TYPE, ("метро" if for_metro else (("вулиця" if sli[0].kit.base_language.is_ua else "улица"))), False, 0)
            if (sli[0].value is not None): 
                street.add_slot(StreetReferent.ATTR_NAME, sli[0].value, False, 0)
            if (sli[0].alt_value is not None): 
                street.add_slot(StreetReferent.ATTR_NAME, sli[0].alt_value, False, 0)
            if (sli[0].alt_value2 is not None): 
                street.add_slot(StreetReferent.ATTR_NAME, sli[0].alt_value2, False, 0)
            street.add_slot(StreetReferent.ATTR_NAME, s, False, 0)
            res0 = AddressItemToken._new329(AddressItemType.STREET, sli[0].begin_token, sli[0].end_token, street, True)
            if (sli[0].is_in_brackets): 
                res0.is_doubt = False
            return res0
        i1 = 0
        if (len(sli) == 1 and ((sli[0].typ == StreetItemType.STDNAME or sli[0].typ == StreetItemType.NAME or sli[0].typ == StreetItemType.STDADJECTIVE))): 
            if (not onto_regim): 
                is_street_before = street_before
                tt = sli[0].begin_token.previous
                if ((tt is not None and tt.is_comma_and and tt.previous is not None) and (isinstance(tt.previous.get_referent(), StreetReferent))): 
                    is_street_before = True
                cou = 0
                tt = sli[0].end_token.next0_
                first_pass2760 = True
                while True:
                    if first_pass2760: first_pass2760 = False
                    else: tt = tt.next0_
                    if (not (tt is not None)): break
                    if (not tt.is_comma_and or tt.next0_ is None): 
                        break
                    sli2 = StreetItemToken.try_parse_list(tt.next0_, 10, None)
                    if (sli2 is None): 
                        break
                    noun = None
                    empty = True
                    for si in sli2: 
                        if (si.typ == StreetItemType.NOUN): 
                            noun = si
                        elif ((si.typ == StreetItemType.NAME or si.typ == StreetItemType.STDNAME or si.typ == StreetItemType.NUMBER) or si.typ == StreetItemType.STDADJECTIVE): 
                            empty = False
                    if (empty): 
                        break
                    if (noun is None): 
                        if (tt.is_and and not is_street_before): 
                            break
                        cou += 1
                        if (cou > 4): 
                            break
                        tt = sli2[len(sli2) - 1].end_token
                        continue
                    if (not tt.is_and and not is_street_before): 
                        break
                    tmp = list()
                    tmp.append(sli[0])
                    tmp.append(noun)
                    re = StreetDefineHelper._try_parse_street(tmp, False, for_metro, False)
                    if (re is not None): 
                        re.end_token = tmp[0].end_token
                        return re
            if (sli[0].whitespaces_after_count < 2): 
                tt = MiscLocationHelper.check_territory(sli[0].end_token.next0_)
                if (tt is not None): 
                    ok1 = False
                    if ((tt.is_newline_after or tt.next0_ is None or tt.next0_.is_comma) or tt.next0_.is_char(')')): 
                        ok1 = True
                    elif (AddressItemToken.check_house_after(tt.next0_, False, False)): 
                        ok1 = True
                    elif (AddressItemToken.check_street_after(tt.next0_, False)): 
                        ok1 = True
                    if (ok1): 
                        street = StreetReferent()
                        street._add_typ("территория")
                        street.kind = StreetKind.AREA
                        street.add_slot(StreetReferent.ATTR_NAME, Utils.ifNotNull(sli[0].value, MiscHelper.get_text_value_of_meta_token(sli[0], GetTextAttr.NO)), False, 0)
                        if (sli[0].alt_value is not None): 
                            street.add_slot(StreetReferent.ATTR_NAME, sli[0].alt_value, False, 0)
                        if (sli[0].alt_value2 is not None): 
                            street.add_slot(StreetReferent.ATTR_NAME, sli[0].alt_value2, False, 0)
                        return AddressItemToken._new231(AddressItemType.STREET, sli[0].begin_token, tt, street)
        elif (len(sli) == 2 and ((sli[0].typ == StreetItemType.STDADJECTIVE or sli[0].typ == StreetItemType.NUMBER or sli[0].typ == StreetItemType.AGE)) and ((sli[1].typ == StreetItemType.STDNAME or sli[1].typ == StreetItemType.NAME))): 
            i1 = 1
        elif (len(sli) == 2 and ((sli[0].typ == StreetItemType.STDNAME or sli[0].typ == StreetItemType.NAME)) and sli[1].typ == StreetItemType.NUMBER): 
            i1 = 0
        elif (len(sli) == 1 and sli[0].typ == StreetItemType.NUMBER and sli[0].is_number_km): 
            tt = sli[0].begin_token.previous
            first_pass2761 = True
            while True:
                if first_pass2761: first_pass2761 = False
                else: tt = tt.previous
                if (not (tt is not None)): break
                if (tt.length_char == 1): 
                    continue
                geo = Utils.asObjectOrNull(tt.get_referent(), GeoReferent)
                if (geo is None): 
                    break
                ok1 = False
                if (geo.find_slot(GeoReferent.ATTR_TYPE, "станция", True) is not None): 
                    ok1 = True
                if (ok1): 
                    street = StreetReferent()
                    street.add_slot(StreetReferent.ATTR_NUMBER, "{0}км".format(sli[0].number.value), False, 0)
                    res0 = AddressItemToken._new329(AddressItemType.STREET, sli[0].begin_token, sli[0].end_token, street, True)
                    if (sli[0].is_in_brackets): 
                        res0.is_doubt = False
                    return res0
            return None
        else: 
            return None
        val = sli[i1].value
        alt_val = sli[i1].alt_value
        if (val is None): 
            if (sli[i1].exist_street is not None): 
                names = sli[i1].exist_street.names
                if (len(names) > 0): 
                    val = names[0]
                    if (len(names) > 1): 
                        alt_val = names[1]
            else: 
                te = Utils.asObjectOrNull(sli[i1].begin_token, TextToken)
                if (te is not None): 
                    for wf in te.morph.items: 
                        if (wf.class0_.is_adjective and wf.gender == MorphGender.FEMINIE and not wf.contains_attr("к.ф.", None)): 
                            val = wf.normal_case
                            break
                if (i1 > 0 and sli[0].typ == StreetItemType.AGE): 
                    val = MiscHelper.get_text_value_of_meta_token(sli[i1], GetTextAttr.NO)
                else: 
                    alt_val = MiscHelper.get_text_value_of_meta_token(sli[i1], GetTextAttr.NO)
                    if (val is None and te.morph.class0_.is_adjective): 
                        val = alt_val
                        alt_val = (None)
                if (len(sli) > 1 and val is None and alt_val is not None): 
                    val = alt_val
                    alt_val = (None)
        very_doubt = False
        if (val is None and len(sli) == 1 and sli[0].chars.is_capital_upper): 
            very_doubt = True
            t0 = sli[0].begin_token.previous
            if (t0 is not None and t0.is_char(',')): 
                t0 = t0.previous
            if ((isinstance(t0, ReferentToken)) and (isinstance(t0.get_referent(), GeoReferent))): 
                val = MiscHelper.get_text_value(sli[0].begin_token, sli[0].end_token, GetTextAttr.NO)
        if (val is None): 
            return None
        t = sli[len(sli) - 1].end_token.next0_
        if (t is not None and t.is_char(',')): 
            t = t.next0_
        if (t is None or t.is_newline_before): 
            return None
        ok = False
        doubt = True
        if (sli[i1].termin is not None and (Utils.valToEnum(sli[i1].termin.tag, StreetItemType)) == StreetItemType.FIX): 
            ok = True
            doubt = False
        elif (((sli[i1].exist_street is not None or sli[0].exist_street is not None)) and sli[0].begin_token != sli[i1].end_token): 
            ok = True
            doubt = False
            if (t.kit.process_referent("PERSON", sli[0].begin_token, None) is not None): 
                if (AddressItemToken.check_house_after(t, False, False)): 
                    pass
                else: 
                    doubt = True
        elif (AddressItemToken.check_house_after(t, False, False)): 
            if (t.previous is not None): 
                if (t.previous.is_value("АРЕНДА", "ОРЕНДА") or t.previous.is_value("СДАЧА", "ЗДАЧА") or t.previous.is_value("СЪЕМ", "ЗНІМАННЯ")): 
                    return None
            vv = MiscLocationHelper._try_parse_npt(t.previous)
            if (vv is not None and vv.end_char >= t.begin_char): 
                return None
            ok = True
        else: 
            ait = AddressItemToken.try_parse_pure_item(t, None, None)
            if (ait is None): 
                return None
            if (ait.typ == AddressItemType.HOUSE and ait.value is not None): 
                ok = True
            elif (very_doubt): 
                return None
            elif (((val == "ТАБЛИЦА" or val == "РИСУНОК" or val == "ДИАГРАММА") or val == "ТАБЛИЦЯ" or val == "МАЛЮНОК") or val == "ДІАГРАМА"): 
                return None
            elif (ait.typ == AddressItemType.NUMBER and (ait.begin_token.whitespaces_before_count < 4)): 
                nt = Utils.asObjectOrNull(ait.begin_token, NumberToken)
                if ((nt is None or nt.int_value is None or nt.typ != NumberSpellingType.DIGIT) or nt.morph.class0_.is_adjective): 
                    return None
                if (ait.end_token.next0_ is not None and not ait.end_token.is_newline_after): 
                    mc = ait.end_token.next0_.get_morph_class_in_dictionary()
                    if (mc.is_adjective or mc.is_noun): 
                        return None
                if (nt.int_value > 100): 
                    return None
                nex = NumberHelper.try_parse_number_with_postfix(ait.begin_token)
                if (nex is not None): 
                    return None
                t = sli[0].begin_token.previous
                first_pass2762 = True
                while True:
                    if first_pass2762: first_pass2762 = False
                    else: t = t.previous
                    if (not (t is not None)): break
                    if (t.is_newline_after): 
                        break
                    if (isinstance(t.get_referent(), GeoReferent)): 
                        ok = True
                        break
                    if (t.is_char(',')): 
                        continue
                    if (t.is_char('.')): 
                        break
                    ait0 = AddressItemToken.try_parse_pure_item(t, None, None)
                    if (ait is not None): 
                        if (ait.typ == AddressItemType.PREFIX): 
                            ok = True
                            break
                    if (t.chars.is_letter): 
                        break
                if (not ok): 
                    if (MiscLocationHelper.is_user_param_address(sli[0])): 
                        ok = True
        if (not ok): 
            return None
        ooo = OrgItemToken.try_parse(sli[0].begin_token, None)
        if (ooo is None and len(sli) > 1): 
            ooo = OrgItemToken.try_parse(sli[1].begin_token, None)
        if (ooo is not None): 
            return None
        street = StreetReferent()
        street.add_slot(StreetReferent.ATTR_TYPE, ("вулиця" if sli[0].kit.base_language.is_ua else "улица"), False, 0)
        if (len(sli) > 1): 
            if (sli[0].typ == StreetItemType.NUMBER or sli[0].typ == StreetItemType.AGE): 
                street.number = (sli[0].value if sli[0].number is None else str(sli[0].number.int_value))
            elif (sli[1].typ == StreetItemType.NUMBER or sli[1].typ == StreetItemType.AGE): 
                street.number = (sli[1].value if sli[1].number is None else str(sli[1].number.int_value))
            else: 
                adjs = MiscLocationHelper.get_std_adj_full(sli[0].begin_token, sli[1].morph.gender, sli[1].morph.number, True)
                if (adjs is None): 
                    adjs = MiscLocationHelper.get_std_adj_full(sli[0].begin_token, MorphGender.FEMINIE, MorphNumber.SINGULAR, False)
                if (adjs is not None): 
                    if (len(adjs) > 1): 
                        alt_val = "{0} {1}".format(adjs[1], val)
                    val = "{0} {1}".format(adjs[0], val)
        street.add_slot(StreetReferent.ATTR_NAME, val, False, 0)
        if (alt_val is not None): 
            street.add_slot(StreetReferent.ATTR_NAME, alt_val, False, 0)
        return AddressItemToken._new329(AddressItemType.STREET, sli[0].begin_token, sli[len(sli) - 1].end_token, street, doubt)
    
    @staticmethod
    def __try_parse_fix(sits : typing.List['StreetItemToken']) -> 'AddressItemToken':
        if (len(sits) < 1): 
            return None
        if (sits[0]._org0_ is not None): 
            o = sits[0]._org0_
            str0_ = StreetReferent()
            str0_._add_typ("территория")
            for s in o.referent.slots: 
                if (s.type_name == "NAME" or s.type_name == "NUMBER"): 
                    str0_.add_slot(s.type_name, s.value, False, 0)
            for ty in o.referent.get_string_values("TYPE"): 
                if (str.isupper(ty[0]) or (ty.find(' ') < 0)): 
                    names = o.referent.get_string_values("NAME")
                    if (len(names) == 0): 
                        str0_.add_slot("NAME", ty.upper(), False, 0)
                    else: 
                        for nam in names: 
                            str0_.add_slot("NAME", "{0} {1}".format(ty.upper(), nam), False, 0)
            no_org = False
            if (o.referent.find_slot("TYPE", "владение", True) is not None or o.referent.find_slot("TYPE", "участок", True) is not None): 
                no_org = True
            if (str0_.find_slot("NAME", None, True) is None): 
                typ = None
                for s in o.referent.slots: 
                    if (s.type_name == "TYPE"): 
                        ss = Utils.asObjectOrNull(s.value, str)
                        if (typ is None or len(typ) > len(ss)): 
                            typ = ss
                if (typ is not None): 
                    str0_.add_slot("NAME", typ.upper(), False, 0)
            if (no_org or o.referent.find_slot("TYPE", None, True) is None): 
                str0_.kind = StreetKind.AREA
            else: 
                str0_.kind = StreetKind.ORG
                str0_.add_slot(StreetReferent.ATTR_REF, o.referent, False, 0)
                str0_.add_ext_referent(sits[0]._org0_)
            b = sits[0].begin_token
            e0_ = sits[0].end_token
            if (sits[0].length_char > 500): 
                pass
            re = AddressItemToken(AddressItemType.STREET, b, e0_)
            re.referent = (str0_)
            if (o.is_massive): 
                str0_.kind = StreetKind.AREA
            re.ref_token = (o)
            re.ref_token_is_gsk = (o.is_gsk or o.has_terr_keyword)
            re.ref_token_is_massive = o.is_massive
            re.is_doubt = o.is_doubt
            if (not o.is_gsk and not o.has_terr_keyword): 
                if (not AddressItemToken.check_house_after(sits[0].end_token.next0_, False, False)): 
                    if (not MiscLocationHelper.is_user_param_address(sits[0])): 
                        re.is_doubt = True
            return re
        if (sits[0].is_railway): 
            str0_ = StreetReferent()
            str0_.kind = StreetKind.RAILWAY
            str0_.add_slot(StreetReferent.ATTR_TYPE, "железная дорога", False, 0)
            str0_.add_slot(StreetReferent.ATTR_NAME, sits[0].value.replace(" ЖЕЛЕЗНАЯ ДОРОГА", ""), False, 0)
            t0 = sits[0].begin_token
            t1 = sits[0].end_token
            if (len(sits) > 1 and sits[1].typ == StreetItemType.NUMBER): 
                num = (sits[1].value if sits[1].number is None else str(sits[1].number.int_value))
                if (t0.previous is not None and ((t0.previous.is_value("КИЛОМЕТР", None) or t0.previous.is_value("КМ", None)))): 
                    t0 = t0.previous
                    str0_.add_slot(StreetReferent.ATTR_NUMBER, num + "км", False, 0)
                    t1 = sits[1].end_token
                elif (sits[1].is_number_km): 
                    str0_.add_slot(StreetReferent.ATTR_NUMBER, num + "км", False, 0)
                    t1 = sits[1].end_token
            elif (sits[0].noun_is_doubt_coef > 1): 
                return None
            return AddressItemToken._new231(AddressItemType.STREET, t0, t1, str0_)
        if (sits[0].termin is None): 
            return None
        if (sits[0].termin.acronym == "МКАД"): 
            str0_ = StreetReferent()
            str0_.kind = StreetKind.ROAD
            str0_.add_slot(StreetReferent.ATTR_TYPE, "автодорога", False, 0)
            str0_.add_slot(StreetReferent.ATTR_NAME, "МОСКОВСКАЯ КОЛЬЦЕВАЯ", False, 0)
            t0 = sits[0].begin_token
            t1 = sits[0].end_token
            if (len(sits) > 1 and sits[1].typ == StreetItemType.NUMBER): 
                num = (sits[1].value if sits[1].number is None else str(sits[1].number.int_value))
                if (t0.previous is not None and ((t0.previous.is_value("КИЛОМЕТР", None) or t0.previous.is_value("КМ", None)))): 
                    t0 = t0.previous
                    str0_.add_slot(StreetReferent.ATTR_NUMBER, num + "км", False, 0)
                    t1 = sits[1].end_token
                elif (sits[1].is_number_km): 
                    str0_.add_slot(StreetReferent.ATTR_NUMBER, num + "км", False, 0)
                    t1 = sits[1].end_token
            return AddressItemToken._new231(AddressItemType.STREET, t0, t1, str0_)
        if (MiscLocationHelper.check_geo_object_before(sits[0].begin_token, False) or AddressItemToken.check_house_after(sits[0].end_token.next0_, False, True)): 
            str0_ = StreetReferent()
            str0_.add_slot(StreetReferent.ATTR_TYPE, "улица", False, 0)
            str0_.add_slot(StreetReferent.ATTR_NAME, sits[0].termin.canonic_text, False, 0)
            return AddressItemToken._new231(AddressItemType.STREET, sits[0].begin_token, sits[0].end_token, str0_)
        return None
    
    @staticmethod
    def _try_parse_second_street(t1 : 'Token', t2 : 'Token') -> 'AddressItemToken':
        sli = StreetItemToken.try_parse_list(t1, 10, None)
        if (sli is None or (len(sli) < 1) or sli[0].typ != StreetItemType.NOUN): 
            return None
        sli2 = StreetItemToken.try_parse_list(t2, 10, None)
        if (sli2 is None or len(sli2) == 0): 
            return None
        sli2.insert(0, sli[0])
        res = StreetDefineHelper._try_parse_street(sli2, True, False, False)
        if (res is None): 
            return None
        res.begin_token = sli2[1].begin_token
        return res