# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import typing
from pullenti.unisharp.Utils import Utils

from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.Referent import Referent
from pullenti.ner.date.DateReferent import DateReferent
from pullenti.ner.TextToken import TextToken
from pullenti.ner.measure.MeasureKind import MeasureKind
from pullenti.ner.measure.internal.NumberWithUnitParseAttr import NumberWithUnitParseAttr
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.ner.money.MoneyReferent import MoneyReferent
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
from pullenti.ner.core.NumberHelper import NumberHelper
from pullenti.ner.core.VerbPhraseHelper import VerbPhraseHelper
from pullenti.ner.uri.UriReferent import UriReferent
from pullenti.ner.measure.internal.NumbersWithUnitToken import NumbersWithUnitToken
from pullenti.ner.vacance.internal.VacanceTokenType import VacanceTokenType

class VacanceToken(MetaToken):
    
    def __init__(self, b : 'Token', e0_ : 'Token') -> None:
        super().__init__(b, e0_, None)
        self.typ = VacanceTokenType.UNDEFINED
        self.refs = list()
        self.value = None;
        self.value2 = None;
    
    @property
    def __is_skill(self) -> bool:
        return (((self.typ == VacanceTokenType.EXPIERENCE or self.typ == VacanceTokenType.EDUCATION or self.typ == VacanceTokenType.SKILL) or self.typ == VacanceTokenType.LANGUAGE or self.typ == VacanceTokenType.PLUS) or self.typ == VacanceTokenType.MORAL or self.typ == VacanceTokenType.LICENSE) or self.typ == VacanceTokenType.DRIVING
    
    def __str__(self) -> str:
        tmp = io.StringIO()
        if (self.typ != VacanceTokenType.UNDEFINED): 
            print("{0}: ".format(Utils.enumToString(self.typ)), end="", file=tmp, flush=True)
        if (self.value is not None): 
            print("\"{0}\" ".format(self.value), end="", file=tmp, flush=True)
        if (self.value2 is not None): 
            print("\"{0}\" ".format(self.value2), end="", file=tmp, flush=True)
        for r in self.refs: 
            print("[{0}] ".format(str(r)), end="", file=tmp, flush=True)
        print(" {0}".format(self.get_source_text()), end="", file=tmp, flush=True)
        return Utils.toStringStringIO(tmp)
    
    @staticmethod
    def try_parse_list(t : 'Token') -> typing.List['VacanceToken']:
        res = list()
        while t is not None: 
            prev = None
            if (len(res) > 0 and res[len(res) - 1].end_token.next0_ == t): 
                prev = res[len(res) - 1]
            vv = VacanceToken.try_parse(t, prev)
            if (vv is None): 
                break
            if (vv.length_char > 3): 
                res.append(vv)
            t = vv.end_token
            t = t.next0_
        i = 0
        first_pass3053 = True
        while True:
            if first_pass3053: first_pass3053 = False
            else: i += 1
            if (not (i < len(res))): break
            it = res[i]
            if (it.typ == VacanceTokenType.DATE): 
                it.typ = VacanceTokenType.UNDEFINED
                continue
            if (it.typ == VacanceTokenType.DUMMY): 
                continue
            if (it.typ == VacanceTokenType.UNDEFINED and len(it.refs) > 0): 
                if (isinstance(it.refs[0], UriReferent)): 
                    continue
            if (it.typ == VacanceTokenType.SKILL and ((i + 1) < len(res)) and res[i + 1].typ == VacanceTokenType.MONEY): 
                it.typ = VacanceTokenType.UNDEFINED
            if (it.typ == VacanceTokenType.EXPIRED): 
                continue
            if (it.typ != VacanceTokenType.UNDEFINED): 
                break
            it.typ = VacanceTokenType.NAME
            if (((i + 2) < len(res)) and ((res[i + 1].typ == VacanceTokenType.UNDEFINED or res[i + 1].typ == VacanceTokenType.SKILL))): 
                if (res[i + 2].typ == VacanceTokenType.MONEY): 
                    it.end_token = res[i + 1].end_token
                    del res[i + 1]
                elif (res[i + 2].typ == VacanceTokenType.MONEY): 
                    if (res[i + 2].__try_parse_money()): 
                        it.end_token = res[i + 1].end_token
                        del res[i + 1]
            it.__get_value()
            if (((i + 1) < len(res)) and res[i + 1].typ == VacanceTokenType.UNDEFINED): 
                if (res[i + 1].__try_parse_money()): 
                    j = i + 2
                    while j < len(res): 
                        if (res[j].typ == VacanceTokenType.MONEY): 
                            res[j].typ = VacanceTokenType.UNDEFINED
                        j += 1
            break
        i = 1
        first_pass3054 = True
        while True:
            if first_pass3054: first_pass3054 = False
            else: i += 1
            if (not (i < len(res))): break
            it = res[i]
            if (it.typ != VacanceTokenType.UNDEFINED): 
                continue
            if (not res[i - 1].__is_skill): 
                continue
            j = i + 1
            while (j < len(res)) and (j < (i + 2)): 
                if (res[j].__is_skill): 
                    if (res[j].typ == VacanceTokenType.PLUS or res[j].typ == VacanceTokenType.MORAL): 
                        res[i].typ = res[i].typ
                    else: 
                        res[i].typ = VacanceTokenType.SKILL
                    break
                j += 1
        i = 0
        while i < len(res): 
            it = res[i]
            if (it.__is_skill and it.value is None): 
                it.__get_value()
            if (it.typ == VacanceTokenType.SKILL or it.typ == VacanceTokenType.MORAL or it.typ == VacanceTokenType.PLUS): 
                j = i + 1
                while j < len(res): 
                    if (res[j].typ != it.typ): 
                        break
                    else: 
                        it.end_token = res[j].end_token
                        del res[j]
                        j -= 1
                    j += 1
                li = VacanceToken.__try_parse_skills(it.begin_token, it.end_token)
                if (li is not None and len(li) > 0): 
                    del res[i]
                    res[i:i] = li
            i += 1
        return res
    
    @staticmethod
    def try_parse(t : 'Token', prev : 'VacanceToken') -> 'VacanceToken':
        if (t is None): 
            return None
        if (t.is_value2("НА", "ПОСТОЯННУЮ")): 
            pass
        res = VacanceToken(t, t)
        skills = 0
        dummy = 0
        lang = 0
        edu = 0
        moral = 0
        lic = 0
        plus = 0
        tt = t
        first_pass3055 = True
        while True:
            if first_pass3055: first_pass3055 = False
            else: tt = tt.next0_
            if (not (tt is not None)): break
            if (tt.is_newline_before and tt != t): 
                if (MiscHelper.can_be_start_of_sentence(tt)): 
                    break
                if (tt.is_hiphen): 
                    break
                cr = True
                npt = NounPhraseHelper.try_parse(tt.previous, NounPhraseParseAttr.NO, 0, None)
                if (npt is not None and npt.end_char >= tt.begin_char): 
                    cr = False
                elif (tt.previous.get_morph_class_in_dictionary().is_noun and tt.chars.is_all_lower): 
                    npt = NounPhraseHelper.try_parse(tt, NounPhraseParseAttr.NO, 0, None)
                    if (npt is not None and npt.morph.case_.is_genitive and not npt.morph.case_.is_nominative): 
                        cr = False
                elif (isinstance(tt.previous, NumberToken)): 
                    if (tt.is_value("РАЗРЯД", None)): 
                        cr = False
                if (cr): 
                    break
            if (tt.is_char(';')): 
                break
            res.end_token = tt
            tok = VacanceToken.M_TERMINS.try_parse(tt, TerminParseAttr.NO)
            if (tok is not None): 
                ty = Utils.valToEnum(tok.termin.tag, VacanceTokenType)
                if (ty == VacanceTokenType.STOP and tt == res.begin_token): 
                    return None
                tt = tok.end_token
                res.end_token = tt
                if (ty == VacanceTokenType.EXPIRED): 
                    res.typ = VacanceTokenType.EXPIRED
                    continue
                if (ty == VacanceTokenType.DUMMY): 
                    dummy += 1
                    continue
                if (ty == VacanceTokenType.EDUCATION): 
                    edu += 1
                    continue
                if (ty == VacanceTokenType.LANGUAGE): 
                    lang += 1
                    ttt = tt.previous
                    while ttt is not None and ttt.begin_char >= t.begin_char: 
                        if ((ttt.is_value("ПЕДАГОГ", None) or ttt.is_value("УЧИТЕЛЬ", None) or ttt.is_value("РЕПЕТИТОР", None)) or ttt.is_value("ПРЕПОДАВАТЕЛЬ", None)): 
                            lang -= 1
                            break
                        ttt = ttt.previous
                    continue
                if (ty == VacanceTokenType.MORAL): 
                    moral += 1
                    continue
                if (ty == VacanceTokenType.PLUS): 
                    plus += 1
                    continue
                if (ty == VacanceTokenType.LICENSE): 
                    lic += 1
                    ttt = tok.begin_token.previous
                    if (ttt is not None): 
                        if (ttt.is_value("ОФОРМЛЯТЬ", None) or ttt.is_value("ОФОРМИТЬ", None) or ttt.is_value("ОФОРМЛЕНИЕ", None)): 
                            lic -= 1
                    continue
                if (ty == VacanceTokenType.SKILL): 
                    if (tok.termin.tag2 is not None and (tok.begin_char - res.begin_char) > 3): 
                        continue
                    skills += 1
                    if (tt.is_value("ОПЫТ", None) or tt.is_value("СТАЖ", None)): 
                        if (res.__try_parse_exp()): 
                            tt = res.end_token
                        elif (prev is not None and prev.typ == VacanceTokenType.PLUS): 
                            skills -= 1
                            plus += 1
                    continue
                if (ty == VacanceTokenType.EXPIERENCE): 
                    if (res.__try_parse_exp()): 
                        tt = res.end_token
                    else: 
                        skills += 1
                    continue
                if (ty == VacanceTokenType.MONEY): 
                    if (res.__try_parse_money()): 
                        tt = res.end_token
                    continue
                if (ty == VacanceTokenType.DRIVING): 
                    if (res.__try_parse_driving()): 
                        tt = res.end_token
                        break
                    else: 
                        lic += 1
                continue
            r = tt.get_referent()
            if (isinstance(r, DateReferent)): 
                dd = Utils.asObjectOrNull(r, DateReferent)
                if (dd.year > 0 and dd.month > 0 and dd.day > 0): 
                    res.refs.append(dd)
            elif (isinstance(r, UriReferent)): 
                dummy += 1
            elif (r is not None and not r in res.refs): 
                if ((isinstance(r, MoneyReferent)) and (((t.begin_char - res.begin_char)) < 10)): 
                    if (res.__try_parse_money()): 
                        t = res.end_token
                        continue
                res.refs.append(r)
        if (res.typ == VacanceTokenType.UNDEFINED): 
            if (dummy > 0): 
                res.typ = VacanceTokenType.DUMMY
            elif (lang > 0): 
                res.typ = VacanceTokenType.LANGUAGE
            elif (edu > 0): 
                res.typ = VacanceTokenType.EDUCATION
                res.__try_parse_education()
            elif (len(res.refs) > 0 and (isinstance(res.refs[0], DateReferent))): 
                res.typ = VacanceTokenType.DATE
            elif (moral > 0): 
                res.typ = VacanceTokenType.MORAL
            elif (lic > 0): 
                res.typ = VacanceTokenType.LICENSE
            elif (plus > 0): 
                res.typ = VacanceTokenType.PLUS
            elif (skills > 0): 
                res.typ = VacanceTokenType.SKILL
        return res
    
    def __get_value(self) -> None:
        t0 = self.begin_token
        t1 = self.end_token
        t = t0
        first_pass3056 = True
        while True:
            if first_pass3056: first_pass3056 = False
            else: t = t.next0_
            if (not (t is not None and (t.end_char < self.end_char))): break
            if ((isinstance(t, TextToken)) and t.length_char == 1 and not t.chars.is_letter): 
                t0 = t.next0_
            elif (t.is_value("ИМЕТЬ", None) or t.is_value("ВЛАДЕТЬ", None) or t.is_value("ЕСТЬ", None)): 
                t0 = t.next0_
            elif (t.is_value2("У", "ВАС") and t.next0_.next0_ is not None and t.next0_.next0_.is_value("ЕСТЬ", None)): 
                t = t.next0_.next0_.next0_
                t0 = t.next0_
            else: 
                tok = VacanceToken.M_TERMINS.try_parse(t, TerminParseAttr.NO)
                if (tok is not None and tok.termin.tag2 is not None): 
                    t = tok.end_token
                    t0 = t.next0_
                    continue
                break
        if (t1.is_char_of(".;:,") or t1.is_hiphen): 
            t1 = t1.previous
        if (self.typ == VacanceTokenType.NAME): 
            t = t0.next0_
            while t is not None and (t.end_char < self.end_char): 
                if (t.is_char_of("(,") and t.next0_ is not None): 
                    if ((t.next0_.get_referent() is not None or t.next0_.is_value("М", None) or t.next0_.is_value("СТ", None)) or t.next0_.is_value("СТАНЦИЯ", None) or t.next0_.chars.is_capital_upper): 
                        t1 = t.previous
                    break
                t = t.next0_
        else: 
            t = t1
            while t is not None and t.begin_char > t0.begin_char: 
                tok = VacanceToken.M_TERMINS.try_parse(t, TerminParseAttr.NO)
                if (tok is not None and tok.termin.tag2 is not None and tok.end_token == t1): 
                    t1 = t.previous
                    ty = Utils.valToEnum(tok.termin.tag, VacanceTokenType)
                    if (ty == VacanceTokenType.PLUS and self.typ == VacanceTokenType.SKILL): 
                        self.typ = VacanceTokenType.PLUS
                    while t1 is not None and t1 != t0: 
                        if (t1.is_value("БЫТЬ", None) or t1.is_value("ЯВЛЯТЬСЯ", None)): 
                            pass
                        else: 
                            break
                        t1 = t1.previous
                    break
                t = t.previous
        attr = (GetTextAttr.KEEPREGISTER) | (GetTextAttr.KEEPQUOTES)
        if (self.typ == VacanceTokenType.MORAL): 
            tok1 = VacanceToken.M_TERMINS.try_parse(t0, TerminParseAttr.NO)
            if (tok1 is not None and tok1.termin.tag2 is None and (Utils.valToEnum(tok1.termin.tag, VacanceTokenType)) == self.typ): 
                self.value = tok1.termin.canonic_text.lower()
                if (tok1.end_char < t1.end_char): 
                    self.value = "{0} {1}".format(self.value, MiscHelper.get_text_value(tok1.end_token.next0_, t1, Utils.valToEnum(attr, GetTextAttr)))
        if (self.value is None): 
            if (t0.is_value("ПРАВО", None)): 
                pass
            else: 
                (attr) |= (GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE)
            self.value = MiscHelper.get_text_value(t0, t1, Utils.valToEnum(attr, GetTextAttr))
        if (not Utils.isNullOrEmpty(self.value) and not t0.chars.is_all_upper and str.islower(self.value[0])): 
            self.value = "{0}{1}".format(str.upper(self.value[0]), self.value[1:])
    
    def __try_parse_exp(self) -> bool:
        t = self.end_token.next0_
        while t is not None: 
            if (t.is_value("РАБОТА", None) or t.is_hiphen or t.is_char(':')): 
                pass
            else: 
                break
            t = t.next0_
        if (t is None): 
            return False
        if (t.is_value2("НЕ", "ТРЕБОВАТЬСЯ")): 
            self.end_token = t.next0_
            self.typ = VacanceTokenType.EXPIERENCE
            self.value = "0"
            return True
        uni = NumbersWithUnitToken.try_parse(t, None, NumberWithUnitParseAttr.NO)
        if (uni is None): 
            return False
        if (len(uni.units) != 1 or uni.units[0].unit is None or uni.units[0].unit.kind != MeasureKind.TIME): 
            return False
        self.end_token = uni.end_token
        self.typ = VacanceTokenType.EXPIERENCE
        if (uni.single_val is not None): 
            self.value = NumberHelper.double_to_string(uni.single_val)
        elif (uni.from_val is not None): 
            self.value = NumberHelper.double_to_string(uni.from_val)
            if (uni.to_val is not None): 
                self.value = NumberHelper.double_to_string(uni.to_val)
                self.value = "{0}-{1}".format(self.value, self.value)
        elif (uni.to_val is not None): 
            self.value = NumberHelper.double_to_string(uni.to_val)
        return True
    
    def __try_parse_money(self) -> bool:
        t = self.begin_token
        while t is not None: 
            m = Utils.asObjectOrNull(t.get_referent(), MoneyReferent)
            if (m is not None): 
                if (t.end_char > self.end_char): 
                    self.end_token = t
                if (not m in self.refs): 
                    self.refs.append(m)
                self.typ = VacanceTokenType.MONEY
                if (t.next0_ is not None and ((t.next0_.is_hiphen or t.next0_.is_value("ДО", None)))): 
                    if (t.next0_.next0_ is not None and (isinstance(t.next0_.next0_.get_referent(), MoneyReferent))): 
                        if (t.next0_.next0_.end_char > self.end_token.end_char): 
                            self.end_token = t.next0_.next0_
                            self.refs.append(self.end_token.get_referent())
                return True
            if (t.is_newline_before and t != self.begin_token): 
                break
            if ((t.begin_char - self.begin_char) > 20): 
                break
            t = t.next0_
        return False
    
    def __try_parse_driving(self) -> bool:
        t = self.end_token.next0_
        first_pass3057 = True
        while True:
            if first_pass3057: first_pass3057 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if ((t.is_hiphen or t.is_char_of(":.") or t.is_value("КАТЕГОРИЯ", None)) or t.is_value("КАТ", None)): 
                continue
            if ((isinstance(t, TextToken)) and t.length_char <= 3 and t.chars.is_letter): 
                self.typ = VacanceTokenType.DRIVING
                self.value = t.term
                self.end_token = t
                t = t.next0_
                first_pass3058 = True
                while True:
                    if first_pass3058: first_pass3058 = False
                    else: t = t.next0_
                    if (not (t is not None)): break
                    if (t.is_char('.') or t.is_comma_and): 
                        continue
                    elif (t.length_char == 1 and t.chars.is_all_upper and t.chars.is_letter): 
                        self.value = "{0}{1}".format(self.value, t.term)
                        self.end_token = t
                    else: 
                        break
                self.value = self.value.replace("А", "A").replace("В", "B").replace("С", "C")
                return True
            break
        return False
    
    def __try_parse_education(self) -> bool:
        hi = False
        middl = False
        prof = False
        spec = False
        tech = False
        t = self.begin_token
        while t is not None and t.end_char <= self.end_char: 
            if (t.is_value("СРЕДНИЙ", None) or t.is_value("СРЕДНЕ", None) or t.is_value("СРЕДН", None)): 
                middl = True
            elif (t.is_value("ВЫСШИЙ", None) or t.is_value("ВЫСШ", None)): 
                hi = True
            elif (t.is_value("ПРОФЕССИОНАЛЬНЫЙ", None) or t.is_value("ПРОФ", None) or t.is_value("ПРОФИЛЬНЫЙ", None)): 
                prof = True
            elif ((t.is_value("СПЕЦИАЛЬНЫЙ", None) or t.is_value("СПЕЦ", None) or t.is_value2("ПО", "СПЕЦИАЛЬНОСТЬ")) or t.is_value2("ПО", "НАПРАВЛЕНИЕ")): 
                spec = True
            elif ((t.is_value("ТЕХНИЧЕСКИЙ", None) or t.is_value("ТЕХ", None) or t.is_value("ТЕХН", None)) or t.is_value("ТЕХНИЧ", None)): 
                tech = True
            t = t.next0_
        if (not hi and not middl): 
            if (spec or prof or tech): 
                middl = True
        if (hi or middl): 
            self.value = ("ВО" if hi else "СО")
            if (spec): 
                self.value += ",спец"
            if (prof): 
                self.value += ",проф"
            if (tech): 
                self.value += ",тех"
            return True
        self.__get_value()
        return False
    
    @staticmethod
    def __try_parse_skills(t0 : 'Token', t1 : 'Token') -> typing.List['VacanceToken']:
        res = list()
        ski = None
        has_verb = False
        ty0 = VacanceTokenType.UNDEFINED
        t = t0
        first_pass3059 = True
        while True:
            if first_pass3059: first_pass3059 = False
            else: t = t.next0_
            if (not (t is not None and t.end_char <= t1.end_char)): break
            keyword_ = False
            tok = VacanceToken.M_TERMINS.try_parse(t, TerminParseAttr.NO)
            if (tok is None): 
                npt1 = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.NO, 0, None)
                if (npt1 is not None and npt1.end_token != t): 
                    tok = VacanceToken.M_TERMINS.try_parse(npt1.end_token, TerminParseAttr.NO)
            if (tok is not None): 
                ty = Utils.valToEnum(tok.termin.tag, VacanceTokenType)
                if (ty == VacanceTokenType.SKILL or ty == VacanceTokenType.MORAL or ty == VacanceTokenType.PLUS): 
                    keyword_ = True
                    ty0 = ty
            if (MiscHelper.can_be_start_of_sentence(t)): 
                ski = (None)
            elif (ski is not None and ski.begin_token != t and keyword_): 
                if (t.chars.is_capital_upper): 
                    ski = (None)
                elif (t.previous is not None and t.previous.is_comma_and): 
                    ski.end_token = ski.end_token.previous
                    ski = (None)
            if (ski is None): 
                ski = VacanceToken._new2520(t, t, (VacanceTokenType.SKILL if ty0 == VacanceTokenType.UNDEFINED else ty0))
                has_verb = False
                res.append(ski)
            npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.NO, 0, None)
            if (npt is not None): 
                t = npt.end_token
                ski.end_token = t
                continue
            verb = VerbPhraseHelper.try_parse(t, False, False, False)
            if (verb is not None): 
                t = verb.end_token
                ski.end_token = t
                has_verb = True
                continue
            if (t.is_char(';')): 
                ski = (None)
                continue
            if (t.is_comma): 
                pass
            ski.end_token = t
        i = 0
        while i < len(res): 
            res[i].__get_value()
            if (res[i].length_char < 5): 
                del res[i]
                i -= 1
            i += 1
        return res
    
    M_TERMINS = None
    
    @staticmethod
    def initialize() -> None:
        if (VacanceToken.M_TERMINS is not None): 
            return
        VacanceToken.M_TERMINS = TerminCollection()
        t = None
        t = Termin._new264("ЗАРАБОТНАЯ ПЛАТА", VacanceTokenType.MONEY)
        t.add_abridge("З/П")
        VacanceToken.M_TERMINS.add(t)
        t = Termin._new264("ОПЫТ РАБОТЫ", VacanceTokenType.EXPIERENCE)
        t.add_variant("СТАЖ РАБОТЫ", False)
        t.add_variant("РАБОЧИЙ СТАЖ", False)
        VacanceToken.M_TERMINS.add(t)
        t = Termin._new264("ОБРАЗОВАНИЕ", VacanceTokenType.EDUCATION)
        VacanceToken.M_TERMINS.add(t)
        for s in ["АНГЛИЙСКИЙ", "НЕМЕЦКИЙ", "ФРАНЦУЗСКИЙ", "ИТАЛЬЯНСКИЙ", "ИСПАНСКИЙ", "КИТАЙСКИЙ"]: 
            VacanceToken.M_TERMINS.add(Termin._new264(s, VacanceTokenType.LANGUAGE))
        for s in ["ВОДИТЕЛЬСКИЕ ПРАВА", "ПРАВА КАТЕГОРИИ", "ВОДИТЕЛЬСКОЕ УДОСТОВЕРЕНИЕ", "УДОСТОВЕРЕНИЕ ВОДИТЕЛЯ", "ПРАВА ВОДИТЕЛЯ"]: 
            VacanceToken.M_TERMINS.add(Termin._new264(s, VacanceTokenType.DRIVING))
        for s in ["УДОСТОВЕРЕНИЕ", "ВОДИТЕЛЬСКАЯ МЕДСПРАВКА", "ВОДИТЕЛЬСКАЯ МЕД.СПРАВКА", "ВОЕННЫЙ БИЛЕТ", "МЕДИЦИНСКАЯ КНИЖКА", "МЕДКНИЖКА", "МЕД.КНИЖКА", "АТТЕСТАТ", "АТТЕСТАЦИЯ", "СЕРТИФИКАТ", "ДОПУСК", "ГРУППА ДОПУСКА"]: 
            VacanceToken.M_TERMINS.add(Termin._new264(s, VacanceTokenType.LICENSE))
        for s in ["ЖЕЛАНИЕ;ЖЕЛАТЬ", "ЖЕЛАНИЕ И СПОСОБНОСТЬ", "ГОТОВНОСТЬ К;ГОТОВЫЙ К", "ДОБРОСОВЕСТНОСТЬ;ДОБРОСОВЕСТНЫЙ", "ГИБКОСТЬ", "РАБОТА В КОМАНДЕ;УМЕНИЕ РАБОТАТЬ В КОМАНДЕ", "ОБЩИТЕЛЬНОСТЬ;ОБЩИТЕЛЬНЫЙ;УМЕНИЕ ОБЩАТЬСЯ С ЛЮДЬМИ;УМЕНИЕ ОБЩАТЬСЯ;КОНТАКТ С ЛЮДЬМИ", "ОТВЕТСТВЕННОСТЬ;ОТВЕТСТВЕННЫЙ", "АКТИВНАЯ ЖИЗНЕННАЯ ПОЗИЦИЯ", "КОММУНИКАБЕЛЬНОСТЬ;КОММУНИКАБЕЛЬНЫЙ", "ЛОЯЛЬНОСТЬ;ЛОЯЛЬНЫЙ", "ИСПОЛНИТЕЛЬНОСТЬ;ИСПОЛНИТЕЛЬНЫЙ", "РЕЗУЛЬТАТИВНОСТЬ;РЕЗУЛЬТАТИВНЫЙ", "ПУНКТУАЛЬНОСТЬ;ПУНКТУАЛЬНЫЙ", "ДИСЦИПЛИНИРОВАННОСТЬ;ДИСЦИПЛИНИРОВАННЫЙ", "ТРУДОЛЮБИЕ;ТРУДОЛЮБИВЫЙ", "ЦЕЛЕУСТРЕМЛЕННОСТЬ;ЦЕЛЕУСТРЕМЛЕННЫЙ", "РАБОТОСПОСОБНОСТЬ;РАБОТОСПОСОБНЫЙ", "ОПРЯТНОСТЬ;ОПРЯТНЫЙ", "ВЕЖЛИВОСТЬ;ВЕЖЛИВЫЙ", "ВЫНОСЛИВОСТЬ;ВЫНОСЛИВЫЙ", "АКТИВНОСТЬ;АКТИВНЫЙ", "ОБУЧАЕМОСТЬ;ОБУЧАЕМЫЙ;СПОСОБНОСТЬ К ОБУЧЕНИЮ;ЛЕГКО ОБУЧАЕМЫЙ;ЛЕГКООБУЧАЕМЫЙ;БЫСТРО ОБУЧАТЬСЯ", "ОБРАЗОВАННОСТЬ", "ОТЛИЧНОЕ НАСТРОЕНИЕ", "ХОРОШЕЕ НАСТРОЕНИЕ", "ГРАМОТНАЯ РЕЧЬ", "ГРАМОТНОЕ ПИСЬМО", "ГРАМОТНОЕ ПИСЬМО И РЕЧЬ", "НАЦЕЛЕННОСТЬ НА РЕЗУЛЬТАТ;НАЦЕЛЕННЫЙ НА РЕЗУЛЬТАТ", "ОПТИМИЗМ;ОПТИМИСТИЧНЫЙ", "КОММУНИКАБЕЛЬНОСТЬ;КОММУНИКАБЕЛЬНЫЙ", "ПРИВЕТЛИВОСТЬ;ПРИВЕТЛИВЫЙ", "ЖЕЛАНИЕ РАБОТАТЬ;ЖЕЛАТЬ РАБОТАТЬ", "ЖЕЛАНИЕ ЗАРАБАТЫВАТЬ;ЖЕЛАТЬ ЗАРАБАТЫВАТЬ", "ОБЯЗАТЕЛЬНОСТЬ", "ПУНКТУАЛЬНОСТЬ;ПУНКТУАЛЬНЫЙ", "ГРАМОТНОСТЬ", "ИНИЦИАТИВНОСТЬ;ИНИЦИАТИВНЫЙ", "ОРГАНИЗОВАННОСТЬ", "АККУРАТНОСТЬ;АККУРАТНЫЙ", "ВНИМАТЕЛЬНОСТЬ;ВНИМАТЕЛЬНЫЙ", "ДИСЦИПЛИНИРОВАННОСТЬ;ДИСЦИПЛИНИРОВАННЫЙ;ПОВЫШЕННЫЕ ТРЕБОВАНИЯ К ДИСЦИПЛИНЕ", "БЕЗ ВРЕДНЫХ ПРИВЫЧЕК;ОТСУТСТВИЕ ВРЕДНЫХ ПРИВЫЧЕК;ВРЕДНЫЕ ПРИВЫЧКИ ОТСУТСТВУЮТ"]: 
            pp = Utils.splitString(s, ';', False)
            te = Termin._new264(pp[0], VacanceTokenType.MORAL)
            ii = 1
            while ii < len(pp): 
                te.add_variant(pp[ii], False)
                ii += 1
            VacanceToken.M_TERMINS.add(te)
        for s in ["ОПЫТ", "ЗНАНИЕ", "ВЛАДЕНИЕ", "НАВЫК", "УМЕНИЕ", "ПОНИМАНИЕ", "ОРГАНИЗАТОРСКИЕ НАВЫКИ", "ОРГАНИЗАТОРСКИЕ СПОСОБНОСТИ", "ПОЛЬЗОВАТЕЛЬ ПК"]: 
            VacanceToken.M_TERMINS.add(Termin._new264(s, VacanceTokenType.SKILL))
        for s in ["НУЖНО", "НЕОБХОДИМО", "ТРЕБОВАТЬСЯ", "НАЛИЧИЕ", "ДЛЯ РАБОТЫ ТРЕБУЕТСЯ", "ОБЯЗАТЕЛЬНО", "ОБЯЗАТЕЛЕН"]: 
            VacanceToken.M_TERMINS.add(Termin._new266(s, VacanceTokenType.SKILL, True))
        for s in ["ЖЕЛАТЕЛЬНО", "ПРИВЕТСТВОВАТЬСЯ", "ЯВЛЯТЬСЯ ПРЕИМУЩЕСТВОМ", "КАК ПЛЮС", "БУДЕТ ПРЕИМУЩЕСТВОМ", "БУДЕТ ЯВЛЯТЬСЯ ПРЕИМУЩЕСТВОМ", "МЫ ЦЕНИМ"]: 
            VacanceToken.M_TERMINS.add(Termin._new2530(s, VacanceTokenType.PLUS, True, True))
        for s in ["НЕЗАМЕНИМЫЙ ОПЫТ", "ОСТАВИТЬ ОТЗЫВ", "КЛЮЧЕВЫЕ НАВЫКИ", "ПОЛНАЯ ЗАНЯТОСТЬ", "КОРПОРАТИВНЫЕ ЗАНЯТИЯ", "КОМПЕНСАЦИЯ", "ОПЛАТА БОЛЬНИЧНЫХ", "ПРЕМИЯ", "ВОЗМОЖНОСТЬ ПОЛУЧИТЬ", "УСЛОВИЯ ДЛЯ", "СПЕЦИАЛЬНЫЕ НАВЫКИ И ЗНАНИЯ", "ПРОГРАММА ЛОЯЛЬНОСТИ", "СИСТЕМА ЛОЯЛЬНОСТИ", "КОРПОРАТИВНЫЙ", "ИНТЕРЕСНАЯ РАБОТА", "НА ПОСТОЯННУЮ РАБОТУ", "ПРОФСОЮЗ"]: 
            VacanceToken.M_TERMINS.add(Termin._new264(s, VacanceTokenType.DUMMY))
        for s in ["ВАКАНСИЯ В АРХИВЕ", "В АРХИВЕ С"]: 
            VacanceToken.M_TERMINS.add(Termin._new264(s, VacanceTokenType.EXPIRED))
    
    @staticmethod
    def _new2520(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'VacanceTokenType') -> 'VacanceToken':
        res = VacanceToken(_arg1, _arg2)
        res.typ = _arg3
        return res