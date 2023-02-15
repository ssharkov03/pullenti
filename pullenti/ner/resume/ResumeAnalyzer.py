# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
import math
import threading
from pullenti.unisharp.Utils import Utils

from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.vacance.internal.VacanceTokenType import VacanceTokenType
from pullenti.ner.Referent import Referent
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.address.AddressReferent import AddressReferent
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.money.MoneyReferent import MoneyReferent
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.core.NumberHelper import NumberHelper
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.address.StreetReferent import StreetReferent
from pullenti.ner.resume.ResumeItemReferent import ResumeItemReferent
from pullenti.ner.Analyzer import Analyzer
from pullenti.ner.resume.MetaResume import MetaResume
from pullenti.ner.core.internal.PullentiNerCoreInternalResourceHelper import PullentiNerCoreInternalResourceHelper
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.vacance.internal.VacanceToken import VacanceToken
from pullenti.ner.Token import Token
from pullenti.ner.resume.ResumeItemType import ResumeItemType

class ResumeAnalyzer(Analyzer):
    """ Анализатор резюме (специфический анализатор) """
    
    ANALYZER_NAME = "RESUME"
    """ Имя анализатора ("RESUME") """
    
    @property
    def name(self) -> str:
        return ResumeAnalyzer.ANALYZER_NAME
    
    @property
    def caption(self) -> str:
        return "Резюме"
    
    @property
    def description(self) -> str:
        return "Текст содержит одно резюме"
    
    def clone(self) -> 'Analyzer':
        return ResumeAnalyzer()
    
    @property
    def is_specific(self) -> bool:
        """ Специфический анализатор """
        return True
    
    @property
    def type_system(self) -> typing.List['ReferentClass']:
        return [MetaResume.GLOBAL_META]
    
    @property
    def images(self) -> typing.List[tuple]:
        res = dict()
        res[str(MetaResume.IMAGE_ID)] = PullentiNerCoreInternalResourceHelper.get_bytes("resume.png")
        return res
    
    def create_referent(self, type0_ : str) -> 'Referent':
        if (type0_ == ResumeItemReferent.OBJ_TYPENAME): 
            return ResumeItemReferent()
        return None
    
    @property
    def progress_weight(self) -> int:
        return 1
    
    def process(self, kit : 'AnalysisKit') -> None:
        ad = kit.get_analyzer_data(self)
        has_sex = False
        has_money = False
        has_pos = False
        has_spec = False
        has_skills = False
        has_exp = False
        has_edu = False
        has_about = False
        rt = None
        t = kit.first_token
        first_pass3020 = True
        while True:
            if first_pass3020: first_pass3020 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (not t.is_newline_before): 
                continue
            if (not has_sex): 
                rt = ResumeAnalyzer.__parse_sex(t, ad)
                if (rt is not None): 
                    has_sex = True
                    t = (rt)
                    continue
            if (ResumeAnalyzer.__check_geo(t)): 
                continue
            if (not has_money and (isinstance(t.get_referent(), MoneyReferent))): 
                money_ = ResumeItemReferent()
                has_money = True
                money_.typ = ResumeItemType.MONEY
                money_.ref = t.get_referent()
                rt = ReferentToken(ad.register_referent(money_), t, t)
                kit.embed_token(rt)
                t = (rt)
                continue
            if (not has_exp): 
                rt = ResumeAnalyzer.__parse_experience(t, ad)
                if (rt is not None): 
                    has_exp = True
                    t = (rt)
                    continue
            if (not has_spec and t.is_value("СПЕЦИАЛИЗАЦИЯ", None)): 
                if (t.next0_ is not None and t.next0_.is_char(':')): 
                    t = t.next0_
                rt = ResumeAnalyzer.__parse_list(t.next0_, ad, ResumeItemType.SPECIALITY)
                if (rt is not None): 
                    has_spec = True
                    t = (rt)
                    continue
            if (not has_skills and t.is_value2("КЛЮЧЕВЫЕ", "НАВЫКИ")): 
                rt = ResumeAnalyzer.__parse_list(t.next0_.next0_, ad, ResumeItemType.SKILL)
                if (rt is not None): 
                    has_skills = True
                    t = (rt)
                    continue
            if (not has_about and ((t.is_value2("О", "МНЕ") or t.is_value2("О", "СЕБЕ")))): 
                rt = ResumeAnalyzer.__parse_about_me(t.next0_.next0_, ad)
                if (rt is not None): 
                    has_about = True
                    t = (rt)
                    continue
            if (not has_spec and has_sex and not has_pos): 
                rt = ResumeAnalyzer.__parse_list(t, ad, ResumeItemType.POSITION)
                if (rt is not None): 
                    has_pos = True
                    t = (rt)
                    continue
            if (not has_edu): 
                mt = ResumeAnalyzer.__parse_education(t)
                if (mt is not None): 
                    edu = ResumeItemReferent()
                    has_edu = True
                    edu.typ = ResumeItemType.EDUCATION
                    edu.value = Utils.asObjectOrNull(mt.tag, str)
                    rt = ReferentToken(ad.register_referent(edu), mt.begin_token, mt.end_token)
                    kit.embed_token(rt)
                    t = (rt)
                    continue
            rt = ResumeAnalyzer.__parse_driving(t, ad)
            if (rt is not None): 
                t = (rt)
                continue
    
    @staticmethod
    def __parse_sex(t : 'Token', ad : 'AnalyzerData') -> 'ReferentToken':
        if (not t.is_value("МУЖЧИНА", None) and not t.is_value("ЖЕНЩИНА", None)): 
            return None
        sex = ResumeItemReferent()
        sex.typ = ResumeItemType.SEX
        sex.value = ("муж" if t.is_value("МУЖЧИНА", None) else "жен")
        rt = ReferentToken(ad.register_referent(sex), t, t)
        t.kit.embed_token(rt)
        t = (rt)
        tt = t.next0_
        while tt is not None: 
            if (tt.is_newline_before): 
                break
            if ((isinstance(tt, NumberToken)) and tt.next0_ is not None): 
                if (tt.next0_.is_value("ГОД", None) or tt.next0_.is_value("ЛЕТ", None)): 
                    age = ResumeItemReferent()
                    age.typ = ResumeItemType.AGE
                    age.value = tt.value
                    rt = ReferentToken(ad.register_referent(age), tt, tt.next0_)
                    t.kit.embed_token(rt)
                    t = (rt)
                    break
            tt = tt.next0_
        return rt
    
    @staticmethod
    def __parse_experience(t : 'Token', ad : 'AnalyzerData') -> 'ReferentToken':
        if (not t.is_value2("ОПЫТ", "РАБОТЫ")): 
            return None
        tt = t.next0_
        while tt is not None: 
            if (tt.is_newline_before): 
                break
            if ((isinstance(tt, NumberToken)) and tt.next0_ is not None): 
                if (tt.next0_.is_value("ГОД", None) or tt.next0_.is_value("ЛЕТ", None)): 
                    experience = ResumeItemReferent()
                    experience.typ = ResumeItemType.EXPERIENCE
                    experience.value = tt.value
                    tt1 = tt.next0_
                    if ((isinstance(tt1.next0_, NumberToken)) and tt1.next0_.next0_ is not None and tt1.next0_.next0_.is_value("МЕСЯЦ", None)): 
                        d = round(tt.real_value + ((tt1.next0_.real_value / (12))), 1)
                        experience.value = NumberHelper.double_to_string(d)
                        tt1 = tt1.next0_.next0_
                    rt = ReferentToken(ad.register_referent(experience), tt, tt1)
                    t.kit.embed_token(rt)
                    return rt
            tt = tt.next0_
        return None
    
    @staticmethod
    def __parse_education(t : 'Token') -> 'MetaToken':
        hi = False
        middl = False
        prof = False
        spec = False
        tech = False
        neok = False
        keyword_ = False
        t0 = t
        t1 = t
        while t is not None: 
            if (t0 != t and t.is_newline_before): 
                break
            if (t.is_value("СРЕДНИЙ", None) or t.is_value("СРЕДНЕ", None) or t.is_value("СРЕДН", None)): 
                middl = True
            elif (t.is_value("ВЫСШИЙ", None) or t.is_value("ВЫСШ", None)): 
                hi = True
            elif (t.is_value("НЕОКОНЧЕННЫЙ", None)): 
                neok = True
            elif (t.is_value("ПРОФЕССИОНАЛЬНЫЙ", None) or t.is_value("ПРОФ", None) or t.is_value("ПРОФИЛЬНЫЙ", None)): 
                prof = True
            elif ((t.is_value("СПЕЦИАЛЬНЫЙ", None) or t.is_value("СПЕЦ", None) or t.is_value2("ПО", "СПЕЦИАЛЬНОСТЬ")) or t.is_value2("ПО", "НАПРАВЛЕНИЕ")): 
                spec = True
            elif ((t.is_value("ТЕХНИЧЕСКИЙ", None) or t.is_value("ТЕХ", None) or t.is_value("ТЕХН", None)) or t.is_value("ТЕХНИЧ", None)): 
                tech = True
            elif (t.is_value("ОБРАЗОВАНИЕ", None)): 
                keyword_ = True
                t1 = t
            else: 
                break
            t = t.next0_
        if (not keyword_): 
            return None
        if (not hi and not middl): 
            if ((spec or prof or tech) or neok): 
                middl = True
            else: 
                return None
        val = ("ВО" if hi else "СО")
        if (spec): 
            val += ",спец"
        if (prof): 
            val += ",проф"
        if (tech): 
            val += ",тех"
        if (neok): 
            val += ",неоконч"
        return MetaToken._new1028(t0, t1, val)
    
    @staticmethod
    def __parse_moral(t : 'Token') -> 'MetaToken':
        tok = VacanceToken.M_TERMINS.try_parse(t, TerminParseAttr.NO)
        if (tok is None or tok.termin.tag2 is not None): 
            return None
        ty = Utils.valToEnum(tok.termin.tag, VacanceTokenType)
        if (ty != VacanceTokenType.MORAL): 
            return None
        val = "{0}{1}".format(tok.termin.canonic_text[0], tok.termin.canonic_text[1:].lower())
        t1 = tok.end_token
        tt = tok.end_token.next0_
        while tt is not None: 
            if (tt.whitespaces_before_count > 2): 
                break
            if (VacanceToken.M_TERMINS.try_parse(tt, TerminParseAttr.NO) is not None): 
                break
            npt = NounPhraseHelper.try_parse(tt, Utils.valToEnum((NounPhraseParseAttr.PARSEPREPOSITION) | (NounPhraseParseAttr.PARSEPRONOUNS), NounPhraseParseAttr), 0, None)
            if (npt is None): 
                break
            t1 = npt.end_token
            tt = t1
            tt = tt.next0_
        if (t1.end_char > tok.end_char): 
            val = "{0} {1}".format(val, MiscHelper.get_text_value(tok.end_token.next0_, t1, Utils.valToEnum((GetTextAttr.KEEPQUOTES) | (GetTextAttr.KEEPREGISTER), GetTextAttr)))
        return MetaToken._new1028(t, t1, val)
    
    @staticmethod
    def __parse_driving(t : 'Token', ad : 'AnalyzerData') -> 'ReferentToken':
        if (t is None): 
            return None
        t1 = None
        if ((t.is_value2("ВОДИТЕЛЬСКИЕ", "ПРАВА") or t.is_value2("ПРАВА", "КАТЕГОРИИ") or t.is_value2("ВОДИТЕЛЬСКОЕ", "УДОСТОВЕРЕНИЕ")) or t.is_value2("УДОСТОВЕРЕНИЕ", "ВОДИТЕЛЯ") or t.is_value2("ПРАВА", "ВОДИТЕЛЯ")): 
            t1 = t.next0_.next0_
        if (t1 is None): 
            return None
        t0 = t
        val = None
        t = t1
        first_pass3021 = True
        while True:
            if first_pass3021: first_pass3021 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if ((t.is_hiphen or t.is_char_of(":.") or t.is_value("КАТЕГОРИЯ", None)) or t.is_value("КАТ", None)): 
                continue
            if ((isinstance(t, TextToken)) and t.length_char <= 3 and t.chars.is_letter): 
                val = t.term
                t1 = t
                t = t.next0_
                first_pass3022 = True
                while True:
                    if first_pass3022: first_pass3022 = False
                    else: t = t.next0_
                    if (not (t is not None)): break
                    if (t.whitespaces_before_count > 2): 
                        break
                    elif (t.is_char('.') or t.is_comma_and): 
                        continue
                    elif (t.length_char == 1 and t.chars.is_all_upper and t.chars.is_letter): 
                        val = "{0}{1}".format(val, t.term)
                        t1 = t
                    else: 
                        break
                val = val.replace("А", "A").replace("В", "B").replace("С", "C")
                break
            break
        if (val is None): 
            return None
        drv = ResumeItemReferent()
        drv.typ = ResumeItemType.DRIVINGLICENSE
        drv.value = val
        rt = ReferentToken(ad.register_referent(drv), t0, t1)
        t0.kit.embed_token(rt)
        return rt
    
    @staticmethod
    def __parse_onto(t : 'Token') -> 'MetaToken':
        if (t is None): 
            return None
        if (t.kit.ontology is None): 
            return None
        lii = t.kit.ontology.attach_token(ResumeAnalyzer.ANALYZER_NAME, t)
        if (lii is None or len(lii) == 0): 
            return None
        if (not (isinstance(lii[0].item.referent, ResumeItemReferent))): 
            return None
        val = lii[0].item.referent.value
        val = "{0}{1}".format(val[0], val[1:].lower())
        return MetaToken._new1028(t, lii[0].end_token, val)
    
    @staticmethod
    def __parse_list(t : 'Token', ad : 'AnalyzerData', typ : 'ResumeItemType') -> 'ReferentToken':
        rt = None
        spec = None
        t0 = t
        first_pass3023 = True
        while True:
            if first_pass3023: first_pass3023 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.is_newline_before): 
                if (t.newlines_before_count > 1 and t != t0): 
                    break
                if (t.is_value2("О", "МНЕ") or t.is_value2("О", "СЕБЕ")): 
                    break
                if (t == t0 and typ == ResumeItemType.POSITION): 
                    pass
                elif (typ == ResumeItemType.SKILL): 
                    pass
                else: 
                    break
            if (t.is_char_of(";,")): 
                continue
            if (BracketHelper.can_be_start_of_sequence(t, True, False)): 
                br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
                if (br is not None): 
                    spec = ResumeItemReferent()
                    spec.typ = typ
                    spec.value = MiscHelper.get_text_value(t.next0_, br.end_token.previous, Utils.valToEnum((GetTextAttr.KEEPQUOTES) | (GetTextAttr.KEEPREGISTER), GetTextAttr)).replace(" - ", "-")
                    rt = ReferentToken(ad.register_referent(spec), t, br.end_token)
                    t.kit.embed_token(rt)
                    t = (rt)
                    continue
            t1 = t
            tt = t.next0_
            while tt is not None: 
                if (tt.is_newline_before): 
                    break
                if (tt.is_char_of(";,")): 
                    break
                t1 = tt
                tt = tt.next0_
            if (t1 is None): 
                break
            rt1 = ResumeAnalyzer.__parse_driving(t, ad)
            if (rt1 is not None): 
                t = (rt1)
                rt = rt1
                continue
            mt = ResumeAnalyzer.__parse_moral(t)
            if (mt is not None): 
                mor = ResumeItemReferent()
                mor.typ = ResumeItemType.MORAL
                mor.value = Utils.asObjectOrNull(mt.tag, str)
                rt = ReferentToken(ad.register_referent(mor), t, mt.end_token)
            else: 
                spec = ResumeItemReferent()
                spec.typ = typ
                spec.value = MiscHelper.get_text_value(t, t1, Utils.valToEnum((GetTextAttr.KEEPQUOTES) | (GetTextAttr.KEEPREGISTER), GetTextAttr)).replace(" - ", "-")
                rt = ReferentToken(ad.register_referent(spec), t, t1)
            t.kit.embed_token(rt)
            t = (rt)
        return rt
    
    @staticmethod
    def __parse_about_me(t : 'Token', ad : 'AnalyzerData') -> 'ReferentToken':
        t0 = t
        rt = None
        first_pass3024 = True
        while True:
            if first_pass3024: first_pass3024 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.is_newline_before): 
                if (ResumeAnalyzer.__parse_education(t) is not None): 
                    break
            mt = ResumeAnalyzer.__parse_moral(t)
            if (mt is not None): 
                mor = ResumeItemReferent()
                mor.typ = ResumeItemType.MORAL
                mor.value = Utils.asObjectOrNull(mt.tag, str)
                rt = ReferentToken(ad.register_referent(mor), t, mt.end_token)
                t.kit.embed_token(rt)
                t = (rt)
                continue
            mt = ResumeAnalyzer.__parse_onto(t)
            if (mt is not None): 
                mor = ResumeItemReferent()
                mor.typ = ResumeItemType.SKILL
                mor.value = Utils.asObjectOrNull(mt.tag, str)
                rt = ReferentToken(ad.register_referent(mor), t, mt.end_token)
                t.kit.embed_token(rt)
                t = (rt)
                continue
        return rt
    
    @staticmethod
    def __check_geo(t : 'Token') -> bool:
        if (t is None): 
            return False
        if (t.is_value2("УКАЗАН", "ПРИМЕРНЫЙ")): 
            return True
        tt = t
        while tt is not None: 
            if (tt != t and tt.is_newline_before): 
                break
            r = tt.get_referent()
            if ((isinstance(r, GeoReferent)) or (isinstance(r, StreetReferent)) or (isinstance(r, AddressReferent))): 
                return True
            if (tt.is_value("ГОТОВ", None) or tt.is_value("ПЕРЕЕЗД", None) or tt.is_value("КОМАНДИРОВКА", None)): 
                return True
            tt = tt.next0_
        return False
    
    def process_ontology_item(self, begin : 'Token') -> 'ReferentToken':
        t = begin
        while t is not None: 
            if (t.next0_ is None): 
                re = ResumeItemReferent()
                re.value = MiscHelper.get_text_value(begin, t, GetTextAttr.NO)
                return ReferentToken(re, begin, t)
            t = t.next0_
        return None
    
    __m_initialized = False
    
    __m_lock = None
    
    @staticmethod
    def initialize() -> None:
        with ResumeAnalyzer.__m_lock: 
            if (ResumeAnalyzer.__m_initialized): 
                return
            ResumeAnalyzer.__m_initialized = True
            MetaResume.initialize()
            VacanceToken.initialize()
            ProcessorService.register_analyzer(ResumeAnalyzer())
    
    # static constructor for class ResumeAnalyzer
    @staticmethod
    def _static_ctor():
        ResumeAnalyzer.__m_lock = threading.Lock()

ResumeAnalyzer._static_ctor()