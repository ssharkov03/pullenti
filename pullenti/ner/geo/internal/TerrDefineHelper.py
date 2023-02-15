# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
import io
from pullenti.unisharp.Utils import Utils

from pullenti.morph.MorphClass import MorphClass
from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphCase import MorphCase
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.morph.MorphBaseInfo import MorphBaseInfo
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.core.ProperNameHelper import ProperNameHelper
from pullenti.ner.MorphCollection import MorphCollection
from pullenti.ner.geo.internal.OrgItemToken import OrgItemToken
from pullenti.ner.address.internal.StreetItemType import StreetItemType
from pullenti.ner.address.internal.AddressItemType import AddressItemType
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.Referent import Referent
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
from pullenti.ner.Token import Token
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.address.internal.AddressItemToken import AddressItemToken
from pullenti.ner.geo.internal.MiscLocationHelper import MiscLocationHelper
from pullenti.ner.geo.internal.TerrItemToken import TerrItemToken
from pullenti.ner.address.internal.StreetItemToken import StreetItemToken
from pullenti.ner.geo.internal.CityAttachHelper import CityAttachHelper
from pullenti.ner.geo.internal.CityItemToken import CityItemToken

class TerrDefineHelper:
    
    @staticmethod
    def __try_attach_moscowao(li : typing.List['TerrItemToken'], ad : 'AnalyzerData') -> 'ReferentToken':
        if (li[0].termin_item is None or not li[0].termin_item.is_moscow_region): 
            return None
        if (li[0].is_doubt): 
            ok = False
            if (CityAttachHelper.check_city_after(li[0].end_token.next0_)): 
                ok = True
            else: 
                ali = AddressItemToken.try_parse_list(li[0].end_token.next0_, 2)
                if (ali is not None and len(ali) > 0 and ali[0].typ == AddressItemType.STREET): 
                    ok = True
            if (not ok): 
                return None
        reg = GeoReferent()
        typ = "АДМИНИСТРАТИВНЫЙ ОКРУГ"
        reg._add_typ(typ)
        name = li[0].termin_item.canonic_text
        if (LanguageHelper.ends_with(name, typ)): 
            name = name[0:0+len(name) - len(typ) - 1].strip()
        reg._add_name(name)
        return ReferentToken(reg, li[0].begin_token, li[0].end_token)
    
    @staticmethod
    def try_define(li : typing.List['TerrItemToken'], ad : 'AnalyzerData', attach_always : bool=False, cits : typing.List['CityItemToken']=None, exists : typing.List['GeoReferent']=None) -> 'ReferentToken':
        if (li is None or len(li) == 0): 
            return None
        ex_obj = None
        new_name = None
        adj_list = list()
        noun = None
        add_noun = None
        rt = TerrDefineHelper.__try_attach_moscowao(li, ad)
        if (rt is not None): 
            return rt
        can_be_city_before = False
        adj_terr_before = False
        if (cits is not None): 
            if (cits[0].typ == CityItemToken.ItemType.CITY): 
                can_be_city_before = True
            elif (cits[0].typ == CityItemToken.ItemType.NOUN and len(cits) > 1): 
                can_be_city_before = True
        k = 0
        k = 0
        while k < len(li): 
            if (li[k].onto_item is not None): 
                if (ex_obj is not None or new_name is not None): 
                    break
                if (noun is not None): 
                    if (k == 1): 
                        if (noun.termin_item.canonic_text == "РАЙОН" or noun.termin_item.canonic_text == "ОБЛАСТЬ" or noun.termin_item.canonic_text == "СОЮЗ"): 
                            if (isinstance(li[k].onto_item.referent, GeoReferent)): 
                                if (li[k].onto_item.referent.is_state): 
                                    break
                            ok = False
                            tt = li[k].end_token.next0_
                            if (tt is None): 
                                ok = True
                            elif (tt.is_char_of(",.")): 
                                ok = True
                            if ((not ok and len(li) >= 4 and li[2].termin_item is not None) and li[3].termin_item is None): 
                                ok = True
                            if (not ok): 
                                ok = MiscLocationHelper.check_geo_object_before(li[0].begin_token, False)
                            if (not ok): 
                                ok = MiscLocationHelper.check_geo_object_after(li[1].end_token, False, False)
                            if (not ok): 
                                adr = AddressItemToken.try_parse(tt, False, None, None)
                                if (adr is not None): 
                                    if (adr.typ == AddressItemType.STREET): 
                                        ok = True
                            if (not ok): 
                                break
                        if (li[k].onto_item is not None): 
                            if (noun.begin_token.is_value("МО", None) or noun.begin_token.is_value("ЛО", None)): 
                                return None
                ex_obj = li[k]
            elif (li[k].termin_item is not None): 
                if (noun is not None): 
                    break
                if (li[k].termin_item.is_always_prefix and k > 0): 
                    break
                if (k > 0 and li[k].is_doubt): 
                    if (li[k].begin_token == li[k].end_token and li[k].begin_token.is_value("ЗАО", None)): 
                        break
                if (li[k].termin_item.is_adjective or li[k].is_geo_in_dictionary): 
                    adj_list.append(li[k])
                else: 
                    if (ex_obj is not None): 
                        geo_ = Utils.asObjectOrNull(ex_obj.onto_item.referent, GeoReferent)
                        if (geo_ is None): 
                            break
                        if (ex_obj.is_adjective and ((li[k].termin_item.canonic_text == "СОЮЗ" or li[k].termin_item.canonic_text == "ФЕДЕРАЦИЯ"))): 
                            str0_ = str(ex_obj.onto_item)
                            if (not li[k].termin_item.canonic_text in str0_): 
                                break
                        if (li[k].termin_item.canonic_text == "РАЙОН" or li[k].termin_item.canonic_text == "ОКРУГ" or li[k].termin_item.canonic_text == "КРАЙ"): 
                            tmp = io.StringIO()
                            for s in geo_.slots: 
                                if (s.type_name == GeoReferent.ATTR_TYPE): 
                                    print("{0};".format(s.value), end="", file=tmp, flush=True)
                            if (not li[k].termin_item.canonic_text in Utils.toStringStringIO(tmp).upper()): 
                                if (k != 1 or new_name is not None): 
                                    break
                                new_name = li[0]
                                new_name.is_adjective = True
                                new_name.onto_item = (None)
                                ex_obj = (None)
                    noun = li[k]
                    if (k == 0 and not li[k].is_newline_before): 
                        tt = TerrItemToken.try_parse(li[k].begin_token.previous, None, None)
                        if (tt is not None and tt.morph.class0_.is_adjective): 
                            adj_terr_before = True
            else: 
                if (ex_obj is not None): 
                    break
                if (new_name is not None): 
                    if ((k == 2 and new_name == li[1] and len(li) == 3) and noun is not None): 
                        cit = CityItemToken.try_parse(new_name.begin_token, None, False, None)
                        if (cit is not None and cit.typ == CityItemToken.ItemType.NOUN and cit.end_token.next0_ == li[k].begin_token): 
                            if ("МУНИЦИПАЛ" in noun.termin_item.canonic_text): 
                                nam = CityItemToken.try_parse(cit.end_token.next0_, None, False, None)
                                if (nam is not None and ((nam.typ == CityItemToken.ItemType.PROPERNAME or nam.typ == CityItemToken.ItemType.CITY))): 
                                    if (nam.end_token.next0_ is not None and nam.end_token.next0_.is_and): 
                                        li2 = TerrItemToken.try_parse_list(nam.end_token.next0_.next0_, 4, None)
                                        if (li2 is not None and len(li2) >= 2 and ((li2[0].termin_item is not None or li2[1].termin_item is not None))): 
                                            geo1 = GeoReferent()
                                            rt1 = ReferentToken(geo1, li[0].begin_token, li2[1].end_token)
                                            geo1._add_typ(noun.termin_item.canonic_text)
                                            geo1.add_slot(GeoReferent.ATTR_NAME, MiscHelper.get_text_value(li[1].begin_token, rt1.end_token, GetTextAttr.NO), False, 0)
                                            return rt1
                        else: 
                            break
                    else: 
                        break
                new_name = li[k]
            k += 1
        name = None
        alt_name = None
        full_name = None
        morph_ = None
        typ_var = None
        if (ex_obj is not None and noun is not None): 
            geo_ = Utils.asObjectOrNull(ex_obj.onto_item.referent, GeoReferent)
            if (geo_ is not None and not geo_.is_city and ((geo_.is_state or (len(noun.termin_item.canonic_text) < 3) or geo_._contains_type(noun.termin_item.canonic_text)))): 
                pass
            else: 
                new_name = ex_obj
                ex_obj = (None)
        if (ex_obj is not None): 
            if (ex_obj.is_adjective and not ex_obj.morph.language.is_en and noun is None): 
                if (attach_always and ex_obj.end_token.next0_ is not None): 
                    npt = MiscLocationHelper._try_parse_npt(ex_obj.begin_token)
                    if (ex_obj.end_token.next0_.is_comma_and): 
                        pass
                    elif (npt is None): 
                        pass
                    else: 
                        str0_ = StreetItemToken.try_parse(ex_obj.end_token.next0_, None, False, None)
                        if (str0_ is not None): 
                            if (str0_.typ == StreetItemType.NOUN and str0_.end_token == npt.end_token): 
                                return None
                elif (ex_obj.begin_token.is_value("ПОДНЕБЕСНЫЙ", None)): 
                    pass
                else: 
                    ttt = ex_obj.end_token.next0_
                    if (ttt is not None and ttt.is_comma and len(li) == 1): 
                        ttt = ttt.next0_
                    elif (AddressItemToken.check_street_after(ex_obj.begin_token.previous, False)): 
                        return None
                    cit = CityItemToken.try_parse_list(ttt, 5, None)
                    if (cit is not None and ((cit[0].typ == CityItemToken.ItemType.NOUN or cit[0].typ == CityItemToken.ItemType.CITY))): 
                        npt = MiscLocationHelper._try_parse_npt(ex_obj.begin_token)
                        if (npt is not None and npt.end_token == cit[0].end_token): 
                            pass
                        elif (not MiscLocationHelper.is_user_param_address(ex_obj)): 
                            return None
                        elif (cit[0].typ == CityItemToken.ItemType.NOUN and ((len(cit) == 2 or len(cit) == 4)) and ((cit[1].typ == CityItemToken.ItemType.CITY or cit[1].typ == CityItemToken.ItemType.PROPERNAME))): 
                            if (AddressItemToken.check_street_after(cit[1].begin_token, False)): 
                                return None
                        elif (cit[0].typ == CityItemToken.ItemType.CITY): 
                            pass
                        else: 
                            return None
                    elif ((cit is not None and cit[0].typ == CityItemToken.ItemType.PROPERNAME and len(cit) == 2) and cit[1].typ == CityItemToken.ItemType.NOUN and ex_obj.end_token.next0_.is_comma): 
                        pass
                    elif (ttt is None or ttt.whitespaces_before_count > 4): 
                        return None
                    elif (MiscLocationHelper.check_geo_object_after(ttt.previous, False, False)): 
                        pass
                    elif (not MiscLocationHelper.is_user_param_address(ex_obj)): 
                        return None
                    elif (AddressItemToken.check_house_after(ex_obj.end_token.next0_, True, False)): 
                        return None
            if (noun is None and ((ex_obj.can_be_city or ex_obj.can_be_surname))): 
                cit0 = CityItemToken.try_parse_back(ex_obj.begin_token.previous, False)
                if (cit0 is not None and cit0.typ != CityItemToken.ItemType.PROPERNAME): 
                    return None
            if (ex_obj.is_doubt and noun is None): 
                ok2 = False
                if (TerrDefineHelper.__can_be_geo_after(ex_obj.end_token.next0_)): 
                    ok2 = True
                elif (not ex_obj.can_be_surname and not ex_obj.can_be_city): 
                    if ((ex_obj.end_token.next0_ is not None and ex_obj.end_token.next0_.is_char(')') and ex_obj.begin_token.previous is not None) and ex_obj.begin_token.previous.is_char('(')): 
                        ok2 = True
                    elif (ex_obj.chars.is_latin_letter and ex_obj.begin_token.previous is not None): 
                        if (ex_obj.begin_token.previous.is_value("IN", None)): 
                            ok2 = True
                        elif (ex_obj.begin_token.previous.is_value("THE", None) and ex_obj.begin_token.previous.previous is not None and ex_obj.begin_token.previous.previous.is_value("IN", None)): 
                            ok2 = True
                if (not ok2): 
                    cit0 = CityItemToken.try_parse_back(ex_obj.begin_token.previous, False)
                    if (cit0 is not None and cit0.typ != CityItemToken.ItemType.PROPERNAME): 
                        pass
                    elif (MiscLocationHelper.check_geo_object_before(ex_obj.begin_token.previous, False)): 
                        pass
                    else: 
                        return None
            name = ex_obj.onto_item.canonic_text
            morph_ = ex_obj.morph
        elif (new_name is not None and noun is None): 
            if (not MiscLocationHelper.is_user_param_address(new_name)): 
                return None
            if (len(li) != 1 or not MiscLocationHelper.check_geo_object_before(li[0].begin_token, False)): 
                return None
            if (li[0].end_token.next0_ is None or not li[0].end_token.next0_.is_comma): 
                return None
            if (li[0].begin_token.previous is None or not li[0].begin_token.previous.is_comma): 
                return None
            if (not li[0].morph.class0_.is_adjective): 
                return None
            str0_ = li[0].get_source_text()
            if (Utils.endsWithString(str0_, "О", True)): 
                return None
            if (Utils.endsWithString(str0_, "ОЕ", True)): 
                return None
            cit = CityItemToken.try_parse(li[0].begin_token, None, False, None)
            if (cit is not None and ((cit.typ == CityItemToken.ItemType.CITY or cit.typ == CityItemToken.ItemType.NOUN))): 
                return None
            name = MiscHelper.get_text_value_of_meta_token(li[0], GetTextAttr.NO)
            morph_ = li[0].morph
            typ_var = "район"
        elif (new_name is not None): 
            j = 1
            while j < k: 
                if (li[j].is_newline_before and ((not li[0].is_newline_before or not li[j].is_newline_after))): 
                    if (BracketHelper.can_be_start_of_sequence(li[j].begin_token, False, False)): 
                        pass
                    else: 
                        if (j < (k - 1)): 
                            return None
                        if (len(li) == 2 and k == 2): 
                            pass
                        else: 
                            li2 = list(li)
                            del li2[0:0+k]
                            rt2 = TerrDefineHelper.try_define(li2, ad, False, None, None)
                            if (rt2 is not None and rt2.end_token == li2[len(li2) - 1].end_token): 
                                pass
                            else: 
                                return None
                j += 1
            morph_ = noun.morph
            if (new_name.is_adjective): 
                if (noun.termin_item.acronym == "АО"): 
                    if (noun.begin_token != noun.end_token): 
                        return None
                    if (new_name.morph.gender != MorphGender.FEMINIE): 
                        return None
                geo_before = None
                tt0 = li[0].begin_token.previous
                if (tt0 is not None and tt0.is_comma_and): 
                    tt0 = tt0.previous
                if (not li[0].is_newline_before and tt0 is not None): 
                    geo_before = (Utils.asObjectOrNull(tt0.get_referent(), GeoReferent))
                if (Utils.indexOfList(li, noun, 0) < Utils.indexOfList(li, new_name, 0)): 
                    if (noun.termin_item.is_state): 
                        return None
                    if (new_name.can_be_surname and geo_before is None): 
                        if (((noun.morph.case_) & new_name.morph.case_).is_undefined): 
                            return None
                    dont_check = False
                    if (MiscHelper.is_exists_in_dictionary(new_name.begin_token, new_name.end_token, (MorphClass.ADJECTIVE) | MorphClass.PRONOUN | MorphClass.VERB)): 
                        if (noun.begin_token != new_name.begin_token): 
                            if (geo_before is None): 
                                if (len(li) == 2 and TerrDefineHelper.__can_be_geo_after(li[1].end_token.next0_)): 
                                    pass
                                elif (len(li) == 3 and li[2].termin_item is not None and TerrDefineHelper.__can_be_geo_after(li[2].end_token.next0_)): 
                                    pass
                                elif (len(li) == 4 and li[2].termin_item is not None and li[3].termin_item is None): 
                                    pass
                                elif (new_name.is_geo_in_dictionary): 
                                    pass
                                elif (new_name.end_token.is_newline_after): 
                                    pass
                                elif (AddressItemToken.check_street_after(new_name.end_token.next0_, False)): 
                                    pass
                                elif (new_name.end_token.next0_ is not None and new_name.end_token.next0_.is_value("КИЛОМЕТР", None)): 
                                    pass
                                elif (OrgItemToken.try_parse(new_name.end_token.next0_, None) is not None): 
                                    pass
                                else: 
                                    return None
                                dont_check = True
                    if (not dont_check): 
                        npt = NounPhraseHelper.try_parse(new_name.end_token, NounPhraseParseAttr.PARSEPRONOUNS, 0, None)
                        if (npt is not None and npt.end_token != new_name.end_token): 
                            if (len(li) == 3 and li[2].termin_item is not None and npt.end_token == li[2].end_token): 
                                add_noun = li[2]
                            elif (len(li) == 4 and li[2].termin_item is not None and npt.end_token == li[2].end_token): 
                                pass
                            elif (AddressItemToken.check_street_after(npt.end_token, False)): 
                                pass
                            elif (MiscLocationHelper.check_geo_object_after(new_name.end_token, False, False)): 
                                pass
                            elif (npt.end_token.is_value("КИЛОМЕТР", None)): 
                                pass
                            elif (OrgItemToken.try_parse(new_name.end_token.next0_, None) is not None): 
                                pass
                            else: 
                                return None
                    rtp = new_name.kit.process_referent("PERSON", new_name.begin_token, None)
                    if (rtp is not None): 
                        return None
                    name = ProperNameHelper.get_name_ex(new_name.begin_token, new_name.end_token, MorphClass.ADJECTIVE, MorphCase.UNDEFINED, noun.termin_item.gender, False, False)
                    vvv = MiscHelper.get_text_value_of_meta_token(new_name, GetTextAttr.NO)
                    if (vvv.endswith("ВО")): 
                        name = vvv
                else: 
                    ok = False
                    if (((k + 1) < len(li)) and li[k].termin_item is None and li[k + 1].termin_item is not None): 
                        ok = True
                    elif ((k < len(li)) and li[k].onto_item is not None): 
                        ok = True
                    elif (k == len(li) and not new_name.is_adj_in_dictionary): 
                        ok = True
                        if (noun.termin_item.canonic_text == "ТЕРРИТОРИЯ"): 
                            cit1 = CityItemToken.try_parse_back(li[0].begin_token.previous, False)
                            if (cit1 is not None and cit1.typ == CityItemToken.ItemType.NOUN): 
                                return None
                    elif (MiscLocationHelper.check_geo_object_before(li[0].begin_token, False) or can_be_city_before): 
                        ok = True
                    elif (MiscLocationHelper.check_geo_object_after(li[k - 1].end_token, False, False)): 
                        ok = True
                    elif (len(li) == 3 and k == 2): 
                        cit = CityItemToken.try_parse(li[2].begin_token, None, False, None)
                        if (cit is not None): 
                            if (cit.typ == CityItemToken.ItemType.CITY or cit.typ == CityItemToken.ItemType.NOUN): 
                                ok = True
                    elif (len(li) == 2): 
                        ok = TerrDefineHelper.__can_be_geo_after(li[len(li) - 1].end_token.next0_)
                    if (not ok and not li[0].is_newline_before and not li[0].chars.is_all_lower): 
                        rt00 = li[0].kit.process_referent("PERSONPROPERTY", li[0].begin_token.previous, None)
                        if (rt00 is not None): 
                            ok = True
                    if (noun.termin_item is not None and noun.termin_item.is_strong and new_name.is_adjective): 
                        ok = True
                    if (noun.is_doubt and len(adj_list) == 0 and geo_before is None): 
                        return None
                    name = ProperNameHelper.get_name_ex(new_name.begin_token, new_name.end_token, MorphClass.ADJECTIVE, MorphCase.UNDEFINED, noun.termin_item.gender, False, False)
                    vvv = MiscHelper.get_text_value_of_meta_token(new_name, GetTextAttr.NO)
                    if (vvv.endswith("ВО")): 
                        name = vvv
                    if (not ok and not attach_always): 
                        if (MiscHelper.is_exists_in_dictionary(new_name.begin_token, new_name.end_token, (MorphClass.ADJECTIVE) | MorphClass.PRONOUN | MorphClass.VERB)): 
                            if (exists is not None): 
                                for e0_ in exists: 
                                    if (e0_.find_slot(GeoReferent.ATTR_NAME, name, True) is not None): 
                                        ok = True
                                        break
                            if (not ok): 
                                return None
                    full_name = "{0} {1}".format(ProperNameHelper.get_name_ex(li[0].begin_token, noun.begin_token.previous, MorphClass.ADJECTIVE, MorphCase.UNDEFINED, noun.termin_item.gender, False, False), noun.termin_item.canonic_text)
            else: 
                if (not attach_always or ((noun.termin_item is not None and noun.termin_item.canonic_text == "ФЕДЕРАЦИЯ"))): 
                    is_latin = noun.chars.is_latin_letter and new_name.chars.is_latin_letter
                    if (Utils.indexOfList(li, noun, 0) > Utils.indexOfList(li, new_name, 0)): 
                        if (not is_latin): 
                            return None
                    if (not new_name.is_district_name and not BracketHelper.can_be_start_of_sequence(new_name.begin_token, False, False)): 
                        if (len(adj_list) == 0 and MiscHelper.is_exists_in_dictionary(new_name.begin_token, new_name.end_token, (MorphClass.NOUN) | MorphClass.PRONOUN)): 
                            if (len(li) == 2 and noun.is_city_region and (noun.whitespaces_after_count < 2)): 
                                pass
                            elif (MiscLocationHelper.check_geo_object_after(new_name.end_token, False, False)): 
                                pass
                            elif (len(li) < 3): 
                                return None
                            else: 
                                ii = Utils.indexOfList(li, new_name, 0)
                                li2 = list(li)
                                del li2[0:0+ii + 1]
                                rt2 = TerrDefineHelper.try_define(li2, ad, False, None, None)
                                if (rt2 is None): 
                                    return None
                        if (not is_latin): 
                            if ((noun.termin_item.is_region and not attach_always and ((not adj_terr_before or new_name.is_doubt))) and not noun.is_city_region and not noun.termin_item.is_specific_prefix): 
                                if (not MiscLocationHelper.check_geo_object_before(noun.begin_token, False)): 
                                    if (not noun.is_doubt and noun.begin_token != noun.end_token): 
                                        pass
                                    elif ((noun.termin_item.is_always_prefix and len(li) == 2 and li[0] == noun) and li[1] == new_name): 
                                        pass
                                    else: 
                                        return None
                            if (noun.is_doubt and len(adj_list) == 0): 
                                if (noun.termin_item.acronym == "МО" or noun.termin_item.acronym == "ЛО"): 
                                    if (k == (len(li) - 1) and li[k].termin_item is not None): 
                                        add_noun = li[k]
                                        k += 1
                                    elif (len(li) == 2 and noun == li[0] and str(new_name).endswith("совет")): 
                                        pass
                                    else: 
                                        return None
                                else: 
                                    return None
                            if (new_name.begin_token.is_value("КОРОЛЕВ", None)): 
                                pass
                            else: 
                                pers = new_name.kit.process_referent("PERSON", new_name.begin_token, None)
                                if (pers is not None): 
                                    return None
                name = MiscHelper.get_text_value(new_name.begin_token, new_name.end_token, GetTextAttr.NO)
                if (new_name.begin_token != new_name.end_token): 
                    ttt = new_name.begin_token.next0_
                    while ttt is not None and ttt.end_char <= new_name.end_char: 
                        if (ttt.chars.is_letter): 
                            ty = TerrItemToken.try_parse(ttt, None, None)
                            if ((ty is not None and ty.termin_item is not None and noun is not None) and ((noun.termin_item.canonic_text in ty.termin_item.canonic_text or ty.termin_item.canonic_text in noun.termin_item.canonic_text))): 
                                name = MiscHelper.get_text_value(new_name.begin_token, ttt.previous, GetTextAttr.NO)
                                break
                        ttt = ttt.next0_
                if (len(adj_list) > 0): 
                    npt = MiscLocationHelper._try_parse_npt(adj_list[0].begin_token)
                    if (npt is not None and npt.end_token == noun.end_token): 
                        alt_name = "{0} {1}".format(npt.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False), name)
        else: 
            if ((len(li) == 1 and noun is not None and noun.end_token.next0_ is not None) and (isinstance(noun.end_token.next0_.get_referent(), GeoReferent))): 
                g = Utils.asObjectOrNull(noun.end_token.next0_.get_referent(), GeoReferent)
                if (noun.termin_item is not None): 
                    tyy = noun.termin_item.canonic_text.lower()
                    ooo = False
                    if (g.find_slot(GeoReferent.ATTR_TYPE, tyy, True) is not None): 
                        ooo = True
                    elif (tyy.endswith("район") and g.find_slot(GeoReferent.ATTR_TYPE, "район", True) is not None): 
                        ooo = True
                    if (ooo): 
                        return ReferentToken._new956(g, noun.begin_token, noun.end_token.next0_, noun.begin_token.morph)
            if ((len(li) == 1 and noun == li[0] and li[0].termin_item is not None) and TerrItemToken.try_parse(li[0].end_token.next0_, None, None) is None and TerrItemToken.try_parse(li[0].begin_token.previous, None, None) is None): 
                if (li[0].morph.number == MorphNumber.PLURAL): 
                    return None
                cou = 0
                str0_ = li[0].termin_item.canonic_text.lower()
                tt = li[0].begin_token.previous
                first_pass2889 = True
                while True:
                    if first_pass2889: first_pass2889 = False
                    else: tt = tt.previous
                    if (not (tt is not None)): break
                    if (tt.is_newline_after): 
                        cou += 10
                    else: 
                        cou += 1
                    if (cou > 500): 
                        break
                    g = Utils.asObjectOrNull(tt.get_referent(), GeoReferent)
                    if (g is None): 
                        continue
                    ok = True
                    cou = 0
                    tt = li[0].end_token.next0_
                    first_pass2890 = True
                    while True:
                        if first_pass2890: first_pass2890 = False
                        else: tt = tt.next0_
                        if (not (tt is not None)): break
                        if (tt.is_newline_before): 
                            cou += 10
                        else: 
                            cou += 1
                        if (cou > 500): 
                            break
                        tee = TerrItemToken.try_parse(tt, None, None)
                        if (tee is None): 
                            continue
                        ok = False
                        break
                    if (ok): 
                        ii = 0
                        while g is not None and (ii < 3): 
                            if (g.find_slot(GeoReferent.ATTR_TYPE, str0_, True) is not None): 
                                return ReferentToken._new956(g, li[0].begin_token, li[0].end_token, noun.begin_token.morph)
                            g = g.higher; ii += 1
                    break
            return None
        ter = None
        if (ex_obj is not None and (isinstance(ex_obj.tag, GeoReferent))): 
            ter = (Utils.asObjectOrNull(ex_obj.tag, GeoReferent))
        else: 
            ter = GeoReferent()
            if (ex_obj is not None): 
                geo_ = Utils.asObjectOrNull(ex_obj.onto_item.referent, GeoReferent)
                if (geo_ is not None and not geo_.is_city and (((geo_.is_state or noun is None or (len(noun.termin_item.canonic_text) < 3)) or geo_._contains_type(noun.termin_item.canonic_text)))): 
                    ter._merge_slots2(geo_, li[0].kit.base_language)
                else: 
                    ter._add_name(name)
                if (noun is None and ex_obj.can_be_city): 
                    ter._add_typ_city(li[0].kit.base_language, True)
                else: 
                    pass
            elif (new_name is not None): 
                ter._add_name(name)
                if (alt_name is not None): 
                    ter._add_name(alt_name)
            if (typ_var is not None): 
                ter._add_typ(typ_var)
            if (noun is not None): 
                if (noun.termin_item.canonic_text == "АО"): 
                    ter._add_typ(("АВТОНОМНИЙ ОКРУГ" if li[0].kit.base_language.is_ua else "АВТОНОМНЫЙ ОКРУГ"))
                elif (noun.termin_item.canonic_text == "МУНИЦИПАЛЬНОЕ СОБРАНИЕ" or noun.termin_item.canonic_text == "МУНІЦИПАЛЬНЕ ЗБОРИ"): 
                    ter._add_typ(("МУНІЦИПАЛЬНЕ УТВОРЕННЯ" if li[0].kit.base_language.is_ua else "МУНИЦИПАЛЬНОЕ ОБРАЗОВАНИЕ"))
                elif (noun.termin_item.acronym == "МО" and add_noun is not None): 
                    ter._add_typ(add_noun.termin_item.canonic_text)
                else: 
                    if (noun.termin_item.canonic_text == "СОЮЗ" and ex_obj is not None and ex_obj.end_char > noun.end_char): 
                        return ReferentToken._new956(ter, ex_obj.begin_token, ex_obj.end_token, ex_obj.morph)
                    ter._add_typ(noun.termin_item.canonic_text)
                    if (noun.termin_item.is_region and ter.is_state): 
                        ter._add_typ_reg(li[0].kit.base_language)
                if (noun.termin_item2 is not None): 
                    ter._add_typ(noun.termin_item2.canonic_text)
            if (ter.is_state and ter.is_region): 
                for a in adj_list: 
                    if (a.termin_item.is_region): 
                        ter._add_typ_reg(li[0].kit.base_language)
                        break
            if (ter.is_state): 
                if (full_name is not None): 
                    ter._add_name(full_name)
        if (noun is None): 
            while k > 1 and li[k - 1] in adj_list:
                k -= 1
        res = ReferentToken(ter, li[0].begin_token, li[k - 1].end_token)
        if (noun is not None and noun.morph.class0_.is_noun): 
            res.morph = noun.morph
        else: 
            res.morph = MorphCollection()
            ii = 0
            while ii < k: 
                for v in li[ii].morph.items: 
                    bi = MorphBaseInfo()
                    bi.copy_from(v)
                    if (noun is not None): 
                        if (bi.class0_.is_adjective): 
                            bi.class0_ = MorphClass.NOUN
                    res.morph.add_item(bi)
                ii += 1
        if (li[0].termin_item is not None and li[0].termin_item.is_specific_prefix): 
            res.begin_token = li[0].end_token.next0_
        if (add_noun is not None and add_noun.end_char > res.end_char): 
            res.end_token = add_noun.end_token
        if ((isinstance(res.begin_token.previous, TextToken)) and (res.whitespaces_before_count < 2)): 
            tt = Utils.asObjectOrNull(res.begin_token.previous, TextToken)
            if (tt.term == "АР"): 
                for ty in ter.typs: 
                    if ("республика" in ty or "республіка" in ty): 
                        res.begin_token = tt
                        break
        if (len(li) == 3 and li[1] == noun): 
            if (li[2].termin_item == noun.termin_item): 
                res.end_token = li[2].end_token
        if (noun is not None and "МЕЖСЕЛЕН" in noun.termin_item.canonic_text): 
            tt = res.end_token.next0_
            if (tt is not None and tt.is_comma): 
                tt = tt.next0_
            if ((tt is not None and tt.is_value("НАХОДИТЬСЯ", None) and tt.next0_ is not None) and tt.next0_.is_value("ВНЕ", None)): 
                tt = tt.next0_.next0_
                first_pass2891 = True
                while True:
                    if first_pass2891: first_pass2891 = False
                    else: tt = tt.next0_
                    if (not (tt is not None)): break
                    mc = tt.get_morph_class_in_dictionary()
                    if (not mc.is_noun): 
                        continue
                    if (tt.is_value("ГРАНИЦА", None) or tt.is_value("ПРЕДЕЛ", None) or tt.is_value("ПОСЕЛЕНИЕ", None)): 
                        res.end_token = tt
                    elif (not mc.is_adjective): 
                        break
        return res
    
    @staticmethod
    def __can_be_geo_after(tt : 'Token') -> bool:
        while tt is not None and ((tt.is_comma or BracketHelper.is_bracket(tt, True))):
            tt = tt.next0_
        if (tt is None): 
            return False
        if (isinstance(tt.get_referent(), GeoReferent)): 
            return True
        tli = TerrItemToken.try_parse_list(tt, 2, None)
        if (tli is not None and len(tli) > 1): 
            if (tli[0].termin_item is None and tli[1].termin_item is not None): 
                return True
            elif (tli[0].termin_item is not None and tli[1].termin_item is None): 
                return True
        if (CityAttachHelper.check_city_after(tt)): 
            return True
        if (TerrDefineHelper.try_attach_stateusaterritory(tt) is not None): 
            return True
        return False
    
    @staticmethod
    def try_attach_stateusaterritory(t : 'Token') -> 'ReferentToken':
        if (t is None or not t.chars.is_latin_letter): 
            return None
        tok = TerrItemToken._m_geo_abbrs.try_parse(t, TerminParseAttr.NO)
        if (tok is None): 
            return None
        g = Utils.asObjectOrNull(tok.termin.tag, GeoReferent)
        if (g is None): 
            return None
        if (tok.end_token.next0_ is not None and tok.end_token.next0_.is_char('.')): 
            tok.end_token = tok.end_token.next0_
        gg = g.clone()
        gg.occurrence.clear()
        return ReferentToken(gg, tok.begin_token, tok.end_token)