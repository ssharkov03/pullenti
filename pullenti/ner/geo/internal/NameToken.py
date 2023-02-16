# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.ner.core.NumberExType import NumberExType
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.TextToken import TextToken
from pullenti.ner.address.internal.AddressItemToken import AddressItemToken
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.geo.internal.MiscLocationHelper import MiscLocationHelper
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
from pullenti.ner.core.NumberHelper import NumberHelper
from pullenti.ner.geo.internal.NameTokenType import NameTokenType
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.address.internal.StreetItemToken import StreetItemToken
from pullenti.ner.geo.internal.TerrItemToken import TerrItemToken

class NameToken(MetaToken):
    
    def __init__(self, b : 'Token', e0_ : 'Token') -> None:
        super().__init__(b, e0_, None)
        self.name = None;
        self.number = None;
        self.pref = None;
        self.is_doubt = False
        self.is_eponym = False
        self.__m_lev = 0
        self.__m_typ = NameTokenType.ANY
    
    def __str__(self) -> str:
        res = io.StringIO()
        if (self.is_doubt): 
            print("? ", end="", file=res)
        if (self.pref is not None): 
            print("{0} ".format(self.pref), end="", file=res, flush=True)
        if (self.name is not None): 
            print("\"{0}\"".format(self.name), end="", file=res, flush=True)
        if (self.number is not None): 
            print(" N{0}".format(self.number), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def try_parse(t : 'Token', ty : 'NameTokenType', lev : int, after_typ : bool=False) -> 'NameToken':
        from pullenti.ner.geo.internal.OrgTypToken import OrgTypToken
        if (t is None or lev > 3): 
            return None
        br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
        res = None
        ttt = None
        num = None
        ttok = None
        if (br is not None): 
            if (not BracketHelper.is_bracket(t, True)): 
                return None
            nam = NameToken.try_parse(t.next0_, ty, lev + 1, False)
            if (nam is not None and nam.end_token.next0_ == br.end_token): 
                res = nam
                nam.begin_token = t
                nam.end_token = br.end_token
                res.is_doubt = False
            else: 
                res = NameToken(t, br.end_token)
                tt = br.end_token.previous
                if (isinstance(tt, NumberToken)): 
                    res.number = tt.value
                    tt = tt.previous
                    if (tt is not None and tt.is_hiphen): 
                        tt = tt.previous
                if (tt is not None and tt.begin_char > br.begin_char): 
                    res.name = MiscHelper.get_text_value(t.next0_, tt, GetTextAttr.NO)
        elif ((isinstance(t, ReferentToken)) and t.begin_token == t.end_token and not t.begin_token.chars.is_all_lower): 
            res = NameToken._new1098(t, t, True)
            res.name = MiscHelper.get_text_value_of_meta_token(Utils.asObjectOrNull(t, ReferentToken), GetTextAttr.NO)
        else: 
            ttt = MiscHelper.check_number_prefix(t)
            if (isinstance((ttt), NumberToken)): 
                res = NameToken._new1099(t, ttt, ttt.value)
                if (ttt.whitespaces_after_count < 2): 
                    nam = NameToken.try_parse(ttt.next0_, ty, lev + 1, False)
                    if (nam is not None and nam.name is not None and nam.number is None): 
                        res.name = nam.name
                        res.end_token = nam.end_token
            else: 
                num = NumberHelper.try_parse_age(t)
                if ((num) is not None): 
                    res = NameToken._new1100(t, num.end_token, num.value + " ЛЕТ")
                else: 
                    num = NumberHelper.try_parse_anniversary(t)
                    if ((num) is not None): 
                        res = NameToken._new1100(t, num.end_token, num.value + " ЛЕТ")
                    elif (isinstance(t, NumberToken)): 
                        nn = NumberHelper.try_parse_number_with_postfix(t)
                        if (nn is not None): 
                            if (nn.ex_typ != NumberExType.UNDEFINED): 
                                return None
                        res = NameToken._new1099(t, t, t.value)
                    elif (t.is_hiphen and (isinstance(t.next0_, NumberToken))): 
                        num = NumberHelper.try_parse_age(t.next0_)
                        if (num is None): 
                            num = NumberHelper.try_parse_anniversary(t.next0_)
                        if (num is not None): 
                            res = NameToken._new1100(t, num.end_token, num.value + " ЛЕТ")
                        else: 
                            res = NameToken._new1104(t, t.next0_, t.next0_.value, True)
                    elif ((isinstance(t, ReferentToken)) and t.get_referent().type_name == "DATE"): 
                        year = t.get_referent().get_string_value("YEAR")
                        if (year is not None): 
                            res = NameToken._new1100(t, t, year + " ГОДА")
                        else: 
                            mon = t.get_referent().get_string_value("MONTH")
                            day = t.get_referent().get_string_value("DAY")
                            if (day is not None and mon is None and t.get_referent().parent_referent is not None): 
                                mon = t.get_referent().parent_referent.get_string_value("MONTH")
                            if (mon is not None): 
                                res = NameToken._new1106(t, t, str(t.get_referent()).upper())
                    elif (not (isinstance(t, TextToken))): 
                        return None
                    elif (t.length_char == 1): 
                        if ((t.get_morph_class_in_dictionary().is_preposition and t.chars.is_all_upper and t.whitespaces_after_count > 0) and (t.whitespaces_after_count < 3) and (isinstance(t.next0_, TextToken))): 
                            npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.PARSEPREPOSITION, 0, None)
                            if (npt is not None and npt.end_token != t): 
                                return NameToken._new1107(t, npt.end_token, True, MiscHelper.get_text_value(t, npt.end_token, GetTextAttr.NO))
                        if ((((ty != NameTokenType.ORG and ty != NameTokenType.STRONG)) or not t.chars.is_all_upper or not t.chars.is_letter) or t.is_whitespace_after): 
                            return None
                        next0__ = NameToken.try_parse(t.next0_, ty, lev + 1, False)
                        if (next0__ is not None and next0__.number is not None and next0__.name is None): 
                            res = next0__
                            res.begin_token = t
                            res.name = t.term
                        elif (t.next0_ is not None and t.next0_.is_char('.')): 
                            nam = io.StringIO()
                            print(t.term, end="", file=nam)
                            t1 = t.next0_
                            tt = t1.next0_
                            while tt is not None: 
                                if (not (isinstance(tt, TextToken)) or tt.length_char != 1 or not tt.chars.is_letter): 
                                    break
                                if (tt.next0_ is None or not tt.next0_.is_char('.')): 
                                    break
                                print(tt.term, end="", file=nam)
                                tt = tt.next0_
                                t1 = tt
                                tt = tt.next0_
                            if (nam.tell() >= 3): 
                                res = NameToken._new1106(t, t1, Utils.toStringStringIO(nam))
                            else: 
                                rt = t.kit.process_referent("PERSON", t, None)
                                if (rt is not None): 
                                    res = NameToken._new1106(t, rt.end_token, rt.referent.get_string_value("LASTNAME"))
                                    if (res.name is None): 
                                        res.name = rt.referent.to_string_ex(False, None, 0).upper()
                                    else: 
                                        tt = t
                                        while tt is not None and tt.end_char <= rt.end_char: 
                                            if ((isinstance(tt, TextToken)) and tt.is_value(res.name, None)): 
                                                res.name = tt.term
                                                break
                                            tt = tt.next0_
                    elif (t.term == "ИМЕНИ" or t.term == "ИМ"): 
                        tt = t.next0_
                        if (t.is_value("ИМ", None) and tt is not None and tt.is_char('.')): 
                            tt = tt.next0_
                        nam = NameToken.try_parse(tt, NameTokenType.STRONG, lev + 1, False)
                        if (nam is not None): 
                            nam.begin_token = t
                            nam.is_doubt = False
                            nam.is_eponym = True
                            res = nam
                    else: 
                        ttok = NameToken.__m_onto.try_parse(t, TerminParseAttr.NO)
                        if ((ttok) is not None): 
                            res = NameToken._new1106(t, ttok.end_token, ttok.termin.canonic_text)
                        else: 
                            npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.NO, 0, None)
                            if (npt is not None and npt.begin_token == npt.end_token): 
                                npt = (None)
                            if (npt is not None and npt.end_token.chars.is_all_lower): 
                                if (t.chars.is_all_lower): 
                                    npt = (None)
                                elif (StreetItemToken.check_keyword(npt.end_token)): 
                                    if (npt.morph.number == MorphNumber.PLURAL): 
                                        pass
                                    else: 
                                        npt = (None)
                            if (npt is not None): 
                                res = NameToken._new1111(t, npt.end_token, npt.morph, MiscHelper.get_text_value_of_meta_token(npt, GetTextAttr.NO).replace("-", " "))
                            elif (not t.chars.is_all_lower or t.is_value("МЕСТНОСТЬ", None)): 
                                if (TerrItemToken.check_keyword(t) is not None): 
                                    if (t.chars.is_capital_upper and after_typ): 
                                        pass
                                    else: 
                                        return None
                                res = NameToken._new1112(t, t, t.term, t.morph)
                                if ((((LanguageHelper.ends_with(res.name, "ОВ") or LanguageHelper.ends_with(res.name, "ВО"))) and (isinstance(t.next0_, TextToken)) and not t.next0_.chars.is_all_lower) and t.next0_.length_char > 1 and not t.next0_.get_morph_class_in_dictionary().is_undefined): 
                                    if (StreetItemToken.check_keyword(t.next0_)): 
                                        pass
                                    elif (OrgTypToken.try_parse(t.next0_, False, None) is not None): 
                                        pass
                                    else: 
                                        res.end_token = t.next0_
                                        res.name = "{0} {1}".format(res.name, t.next0_.term)
                                        res.morph = t.next0_.morph
                                if ((t.whitespaces_after_count < 2) and (isinstance(t.next0_, TextToken)) and t.next0_.chars.is_letter): 
                                    ok = False
                                    if (t.next0_.length_char >= 3 and t.next0_.get_morph_class_in_dictionary().is_undefined): 
                                        ok = True
                                    else: 
                                        ok1 = False
                                        if ((((t.next0_.length_char < 4) or t.get_morph_class_in_dictionary().is_undefined)) and t.next0_.chars.equals(t.chars)): 
                                            ok1 = True
                                        elif (t.is_value("МЕСТНОСТЬ", None) and not t.next0_.chars.is_all_lower): 
                                            ok = True
                                        elif (not t.next0_.chars.is_all_lower or not AddressItemToken.check_house_after(t.next0_, False, False)): 
                                            if (MiscLocationHelper.check_territory(t.next0_) is None): 
                                                if (t.next0_.is_newline_after or t.next0_.next0_.is_comma or AddressItemToken.check_house_after(t.next0_.next0_, False, False)): 
                                                    ok = True
                                            if (not ok and t.next0_.next0_ is not None): 
                                                typ = OrgTypToken.try_parse(t.next0_.next0_, False, None)
                                                if (typ is not None and typ.is_massiv): 
                                                    ok = True
                                                elif (t.next0_.next0_.is_value("МАССИВ", None)): 
                                                    ok = True
                                        if (ok1): 
                                            next0__ = NameToken.try_parse(t.next0_, ty, lev + 1, False)
                                            if (next0__ is None or next0__.begin_token == next0__.end_token): 
                                                ok = True
                                    if (not ok and t.next0_.get_morph_class_in_dictionary().is_adjective): 
                                        mc = t.get_morph_class_in_dictionary()
                                        if (mc.is_noun or mc.is_proper_geo): 
                                            if (((t.morph.gender) & (t.next0_.morph.gender)) != (MorphGender.UNDEFINED)): 
                                                tt = t.next0_.next0_
                                                if (tt is None): 
                                                    ok = True
                                                elif (tt.is_comma or tt.is_newline_after): 
                                                    ok = True
                                                elif (AddressItemToken.check_house_after(tt, False, False)): 
                                                    ok = True
                                                elif (AddressItemToken.check_street_after(tt, False)): 
                                                    ok = True
                                    if (ok): 
                                        if (OrgTypToken.try_parse(t.next0_, False, None) is not None): 
                                            ok = False
                                    if (ok): 
                                        res.end_token = t.next0_
                                        res.name = "{0} {1}".format(res.name, t.next0_.term)
                            if (res is not None and res.end_token.is_value("УСАДЬБА", None) and (res.whitespaces_after_count < 2)): 
                                res1 = NameToken.try_parse(res.end_token.next0_, ty, lev + 1, False)
                                if (res1 is not None and res1.name is not None): 
                                    res.end_token = res1.end_token
                                    res.name = "{0} {1}".format(res.name, res1.name)
        if (res is None or res.whitespaces_after_count > 2): 
            return res
        ttt = res.end_token.next0_
        if (ttt is not None and ttt.is_hiphen): 
            num = NumberHelper.try_parse_age(ttt.next0_)
            if (num is None): 
                num = NumberHelper.try_parse_anniversary(ttt.next0_)
            if (num is not None): 
                res.pref = (num.value + " ЛЕТ")
                res.end_token = num.end_token
            elif ((isinstance(ttt.next0_, NumberToken)) and res.number is None): 
                res.number = ttt.next0_.value
                res.end_token = ttt.next0_
            if ((isinstance(ttt.next0_, TextToken)) and not ttt.is_whitespace_after and res.name is not None): 
                res.name = "{0} {1}".format(res.name, ttt.next0_.term)
                res.end_token = ttt.next0_
        else: 
            num = NumberHelper.try_parse_age(ttt)
            if ((num) is not None): 
                res.pref = (num.value + " ЛЕТ")
                res.end_token = num.end_token
            else: 
                num = NumberHelper.try_parse_anniversary(ttt)
                if ((num) is not None): 
                    res.pref = (num.value + " ЛЕТ")
                    res.end_token = num.end_token
                elif (isinstance(ttt, NumberToken)): 
                    ok = False
                    if (ty == NameTokenType.ORG): 
                        ok = True
                    if (ok): 
                        if (StreetItemToken.check_keyword(ttt.next0_)): 
                            ok = False
                        elif (ttt.next0_ is not None): 
                            if (ttt.next0_.is_value("КМ", None) or ttt.next0_.is_value("КИЛОМЕТР", None)): 
                                ok = False
                    if (ok): 
                        res.number = ttt.value
                        res.end_token = ttt
        if (res.number is None): 
            ttt = MiscHelper.check_number_prefix(res.end_token.next0_)
            if (isinstance(ttt, NumberToken)): 
                res.number = ttt.value
                res.end_token = ttt
        if ((res.whitespaces_after_count < 3) and res.name is None and BracketHelper.can_be_start_of_sequence(res.end_token.next0_, False, False)): 
            nam = NameToken.try_parse(res.end_token.next0_, ty, lev + 1, False)
            if (nam is not None): 
                res.name = nam.name
                res.end_token = nam.end_token
                res.is_doubt = False
        if (res.pref is not None and res.name is None and res.number is None): 
            nam = NameToken.try_parse(res.end_token.next0_, ty, lev + 1, False)
            if (nam is not None and nam.name is not None and nam.pref is None): 
                res.name = nam.name
                res.number = nam.number
                res.end_token = nam.end_token
        res.__m_lev = lev
        res.__m_typ = ty
        if (res.whitespaces_after_count < 3): 
            nn = NameToken.__m_onto.try_parse(res.end_token.next0_, TerminParseAttr.NO)
            if (nn is not None): 
                res.end_token = nn.end_token
                res.name = "{0} {1}".format(res.name, MiscHelper.get_text_value_of_meta_token(nn, GetTextAttr.NO))
        res.try_attach_number()
        return res
    
    def try_attach_number(self) -> None:
        if (self.whitespaces_after_count > 2): 
            return
        if (self.number is None): 
            nam2 = NameToken.try_parse(self.end_token.next0_, self.__m_typ, self.__m_lev + 1, False)
            if ((nam2 is not None and nam2.number is not None and nam2.name is None) and nam2.pref is None): 
                if (StreetItemToken.check_keyword(nam2.end_token.next0_)): 
                    pass
                else: 
                    self.number = nam2.number
                    self.end_token = nam2.end_token
            elif (nam2 is not None and nam2.is_eponym): 
                self.end_token = nam2.end_token
                if (self.name is None): 
                    self.name = nam2.name
                else: 
                    self.name = "{0} {1}".format(self.name, nam2.name)
                if (nam2.number is not None): 
                    self.number = nam2.number
        if ((self.__m_typ == NameTokenType.ORG and (isinstance(self.end_token, NumberToken)) and self.number == self.end_token.value) and not self.is_whitespace_after): 
            tmp = Utils.newStringIO(self.number)
            delim = None
            tt = self.end_token.next0_
            first_pass2886 = True
            while True:
                if first_pass2886: first_pass2886 = False
                else: tt = tt.next0_
                if (not (tt is not None)): break
                if (tt.is_whitespace_before): 
                    break
                if (tt.is_char_of(",.") or tt.is_table_control_char): 
                    break
                if (tt.is_char_of("\\/")): 
                    delim = "/"
                    continue
                elif (tt.is_hiphen): 
                    delim = "-"
                    continue
                if ((isinstance(tt, NumberToken)) and tt.typ == NumberSpellingType.DIGIT): 
                    if (delim is not None and str.isdigit(Utils.getCharAtStringIO(tmp, tmp.tell() - 1))): 
                        print(delim, end="", file=tmp)
                    delim = (None)
                    print(tt.value, end="", file=tmp)
                    self.end_token = tt
                    continue
                if ((isinstance(tt, TextToken)) and tt.length_char == 1 and tt.chars.is_letter): 
                    if (delim is not None and str.isalpha(Utils.getCharAtStringIO(tmp, tmp.tell() - 1))): 
                        print(delim, end="", file=tmp)
                    delim = (None)
                    print(tt.term, end="", file=tmp)
                    self.end_token = tt
                    continue
                break
            self.number = Utils.toStringStringIO(tmp)
    
    __m_onto = None
    
    @staticmethod
    def initialize() -> None:
        NameToken.__m_onto = TerminCollection()
        t = Termin("СОВЕТСКОЙ АРМИИ И ВОЕННО МОРСКОГО ФЛОТА")
        t.add_variant("СА И ВМФ", False)
        NameToken.__m_onto.add(t)
        t = Termin._new1113("СОВЕТСКОЙ АРМИИ", "СА")
        NameToken.__m_onto.add(t)
        t = Termin._new1113("МИНИСТЕРСТВО ОБОРОНЫ", "МО")
        NameToken.__m_onto.add(t)
        t = Termin._new1113("ВОЕННО МОРСКОЙ ФЛОТ", "ВМФ")
        NameToken.__m_onto.add(t)
        NameToken.__m_onto.add(Termin("МОЛОДАЯ ГВАРДИЯ"))
        NameToken.__m_onto.add(Termin("ЗАЩИТНИКИ БЕЛОГО ДОМА"))
    
    @staticmethod
    def _new1098(_arg1 : 'Token', _arg2 : 'Token', _arg3 : bool) -> 'NameToken':
        res = NameToken(_arg1, _arg2)
        res.is_doubt = _arg3
        return res
    
    @staticmethod
    def _new1099(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str) -> 'NameToken':
        res = NameToken(_arg1, _arg2)
        res.number = _arg3
        return res
    
    @staticmethod
    def _new1100(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str) -> 'NameToken':
        res = NameToken(_arg1, _arg2)
        res.pref = _arg3
        return res
    
    @staticmethod
    def _new1104(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str, _arg4 : bool) -> 'NameToken':
        res = NameToken(_arg1, _arg2)
        res.number = _arg3
        res.is_doubt = _arg4
        return res
    
    @staticmethod
    def _new1106(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str) -> 'NameToken':
        res = NameToken(_arg1, _arg2)
        res.name = _arg3
        return res
    
    @staticmethod
    def _new1107(_arg1 : 'Token', _arg2 : 'Token', _arg3 : bool, _arg4 : str) -> 'NameToken':
        res = NameToken(_arg1, _arg2)
        res.is_doubt = _arg3
        res.name = _arg4
        return res
    
    @staticmethod
    def _new1111(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'MorphCollection', _arg4 : str) -> 'NameToken':
        res = NameToken(_arg1, _arg2)
        res.morph = _arg3
        res.name = _arg4
        return res
    
    @staticmethod
    def _new1112(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str, _arg4 : 'MorphCollection') -> 'NameToken':
        res = NameToken(_arg1, _arg2)
        res.name = _arg3
        res.morph = _arg4
        return res