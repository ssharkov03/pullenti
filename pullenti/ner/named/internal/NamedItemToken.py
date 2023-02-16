# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import typing
from pullenti.unisharp.Utils import Utils

from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.morph.MorphClass import MorphClass
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.named.NamedEntityKind import NamedEntityKind
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.geo.internal.MiscLocationHelper import MiscLocationHelper
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
from pullenti.ner.core.NumberHelper import NumberHelper

class NamedItemToken(MetaToken):
    
    def __init__(self, b : 'Token', e0_ : 'Token') -> None:
        super().__init__(b, e0_, None)
        self.kind = NamedEntityKind.UNDEFINED
        self.name_value = None;
        self.type_value = None;
        self.ref = None;
        self.is_wellknown = False
        self.is_in_bracket = False
    
    def __str__(self) -> str:
        res = io.StringIO()
        if (self.kind != NamedEntityKind.UNDEFINED): 
            print(" [{0}]".format(Utils.enumToString(self.kind)), end="", file=res, flush=True)
        if (self.is_wellknown): 
            print(" (!)".format(), end="", file=res, flush=True)
        if (self.is_in_bracket): 
            print(" [br]".format(), end="", file=res, flush=True)
        if (self.type_value is not None): 
            print(" {0}".format(self.type_value), end="", file=res, flush=True)
        if (self.name_value is not None): 
            print(" \"{0}\"".format(self.name_value), end="", file=res, flush=True)
        if (self.ref is not None): 
            print(" -> {0}".format(str(self.ref)), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def try_parse_list(t : 'Token', loc_onto : 'IntOntologyCollection') -> typing.List['NamedItemToken']:
        ne = NamedItemToken.try_parse(t, loc_onto, None)
        if (ne is None): 
            return None
        res = list()
        res.append(ne)
        t = ne.end_token.next0_
        while t is not None: 
            if (t.whitespaces_before_count > 2): 
                break
            ne = NamedItemToken.try_parse(t, loc_onto, res[len(res) - 1])
            if (ne is None): 
                break
            if (t.is_value("НЕТ", None)): 
                break
            res.append(ne)
            t = ne.end_token
            t = t.next0_
        return res
    
    @staticmethod
    def try_parse(t : 'Token', loc_onto : 'IntOntologyCollection', prev : 'NamedItemToken') -> 'NamedItemToken':
        if (t is None): 
            return None
        if (isinstance(t, ReferentToken)): 
            r = t.get_referent()
            if ((r.type_name == "PERSON" or r.type_name == "PERSONPROPERTY" or (isinstance(r, GeoReferent))) or r.type_name == "ORGANIZATION"): 
                return NamedItemToken._new1469(t, t, r, t.morph)
            return None
        typ = NamedItemToken.__m_types.try_parse(t, TerminParseAttr.NO)
        nam = NamedItemToken.__m_names.try_parse(t, TerminParseAttr.NO)
        if (typ is not None): 
            if (not (isinstance(t, TextToken))): 
                return None
            res = NamedItemToken._new1470(typ.begin_token, typ.end_token, typ.morph, typ.chars)
            res.kind = (Utils.valToEnum(typ.termin.tag, NamedEntityKind))
            res.type_value = typ.termin.canonic_text
            if ((nam is not None and nam.end_token == typ.end_token and not t.chars.is_all_lower) and (Utils.valToEnum(nam.termin.tag, NamedEntityKind)) == res.kind): 
                res.name_value = nam.termin.canonic_text
                res.is_wellknown = True
            return res
        if (nam is not None): 
            if (nam.begin_token.chars.is_all_lower): 
                return None
            res = NamedItemToken._new1470(nam.begin_token, nam.end_token, nam.morph, nam.chars)
            res.kind = (Utils.valToEnum(nam.termin.tag, NamedEntityKind))
            res.name_value = nam.termin.canonic_text
            ok = True
            if (not t.is_whitespace_before and t.previous is not None): 
                ok = False
            elif (not t.is_whitespace_after and t.next0_ is not None): 
                if (t.next0_.is_char_of(",.;!?") and t.next0_.is_whitespace_after): 
                    pass
                else: 
                    ok = False
            if (ok and nam.termin.tag3 is None): 
                res.is_wellknown = True
                res.type_value = (Utils.asObjectOrNull(nam.termin.tag2, str))
            return res
        adj = MiscLocationHelper.try_attach_nord_west(t)
        if (adj is not None): 
            if (adj.morph.class0_.is_noun): 
                if (adj.end_token.is_value("ВОСТОК", None)): 
                    if (adj.begin_token == adj.end_token): 
                        return None
                    re = NamedItemToken._new1472(t, adj.end_token, adj.morph)
                    re.kind = NamedEntityKind.LOCATION
                    re.name_value = MiscHelper.get_text_value(t, adj.end_token, GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE)
                    re.is_wellknown = True
                    return re
                return None
            if (adj.whitespaces_after_count > 2): 
                return None
            if ((isinstance(adj.end_token.next0_, ReferentToken)) and (isinstance(adj.end_token.next0_.get_referent(), GeoReferent))): 
                re = NamedItemToken._new1472(t, adj.end_token.next0_, adj.end_token.next0_.morph)
                re.kind = NamedEntityKind.LOCATION
                re.name_value = MiscHelper.get_text_value(t, adj.end_token.next0_, GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE)
                re.is_wellknown = True
                re.ref = adj.end_token.next0_.get_referent()
                return re
            res = NamedItemToken.try_parse(adj.end_token.next0_, loc_onto, prev)
            if (res is not None and res.kind == NamedEntityKind.LOCATION): 
                s = adj.get_normal_case_text(MorphClass.ADJECTIVE, MorphNumber.SINGULAR, res.morph.gender, False)
                if (s is not None): 
                    if (res.name_value is None): 
                        res.name_value = s.upper()
                    else: 
                        res.name_value = "{0} {1}".format(s.upper(), res.name_value)
                        res.type_value = (None)
                    res.begin_token = t
                    res.chars = t.chars
                    res.is_wellknown = True
                    return res
        if (t.chars.is_capital_upper and not MiscHelper.can_be_start_of_sentence(t)): 
            npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.NO, 0, None)
            if (npt is not None and len(npt.adjectives) > 0): 
                test = NamedItemToken.try_parse(npt.noun.begin_token, loc_onto, None)
                if (test is not None and test.end_token == npt.end_token and test.type_value is not None): 
                    if (test.type_value == "ДОМ"): 
                        return None
                    test.begin_token = t
                    tmp = io.StringIO()
                    for a in npt.adjectives: 
                        s = a.get_normal_case_text(MorphClass.ADJECTIVE, MorphNumber.SINGULAR, test.morph.gender, False)
                        if (tmp.tell() > 0): 
                            print(' ', end="", file=tmp)
                        print(s, end="", file=tmp)
                    test.name_value = Utils.toStringStringIO(tmp)
                    test.chars = t.chars
                    if (test.kind == NamedEntityKind.LOCATION or test.kind == NamedEntityKind.BUILDING or test.kind == NamedEntityKind.MONUMENT): 
                        test.is_wellknown = True
                    return test
        if (BracketHelper.is_bracket(t, True) and t.next0_ is not None and not t.next0_.chars.is_all_lower): 
            br = BracketHelper.try_parse(t, BracketParseAttr.CANCONTAINSVERBS, 100)
            if (br is not None and br.length_char > 3): 
                res = NamedItemToken(t, br.end_token)
                res.is_in_bracket = True
                res.name_value = MiscHelper.get_text_value(t, br.end_token, GetTextAttr.NO)
                nam = NamedItemToken.__m_names.try_parse(t.next0_, TerminParseAttr.NO)
                if (nam is not None and nam.end_token == br.end_token.previous): 
                    res.kind = (Utils.valToEnum(nam.termin.tag, NamedEntityKind))
                    res.is_wellknown = True
                    res.name_value = nam.termin.canonic_text
                return res
        if (((isinstance(t, TextToken)) and t.chars.is_letter and not t.chars.is_all_lower) and t.length_char > 2): 
            res = NamedItemToken._new1472(t, t, t.morph)
            str0_ = t.term
            if (str0_.endswith("О") or str0_.endswith("И") or str0_.endswith("Ы")): 
                res.name_value = str0_
            else: 
                res.name_value = t.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False)
            res.chars = t.chars
            if (((not t.is_whitespace_after and t.next0_ is not None and t.next0_.is_hiphen) and (isinstance(t.next0_.next0_, TextToken)) and not t.next0_.is_whitespace_after) and t.chars.is_cyrillic_letter == t.next0_.next0_.chars.is_cyrillic_letter): 
                res.end_token = t.next0_.next0_
                t = res.end_token
                res.name_value = "{0}-{1}".format(res.name_value, t.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False))
            elif (prev is not None and prev.kind == NamedEntityKind.MONUMENT): 
                npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.NO, 0, None)
                if (npt is not None and npt.end_char > res.end_char): 
                    res.name_value = MiscHelper.get_text_value_of_meta_token(npt, GetTextAttr.NO)
                    res.end_token = npt.end_token
            return res
        if (prev is not None and prev.kind == NamedEntityKind.MONUMENT and (t.whitespaces_before_count < 3)): 
            t1 = None
            nnn = NumberHelper.try_parse_anniversary(t)
            if (nnn is not None): 
                t1 = nnn.end_token
            elif ((isinstance(t, NumberToken)) and (t.whitespaces_before_count < 2)): 
                t1 = t
                nnn = (Utils.asObjectOrNull(t, NumberToken))
            elif (t.is_value("ГЕРОЙ", None)): 
                t1 = t
            else: 
                rt1 = t.kit.process_referent("PERSON", t, None)
                if (rt1 is not None): 
                    t1 = rt1.end_token
            if (t1 is None): 
                return None
            next0__ = NamedItemToken.try_parse(t1.next0_, loc_onto, prev)
            if (next0__ is not None and next0__.type_value is None and next0__.name_value is not None): 
                next0__.begin_token = t
                if (nnn is not None): 
                    next0__.name_value = "{0} ЛЕТ {1}".format(nnn.value, next0__.name_value)
                else: 
                    next0__.name_value = MiscHelper.get_text_value_of_meta_token(next0__, GetTextAttr.NO)
                return next0__
        return None
    
    @staticmethod
    def _initialize() -> None:
        if (NamedItemToken.__m_types is not None): 
            return
        NamedItemToken.__m_types = TerminCollection()
        NamedItemToken.__m_names = TerminCollection()
        t = None
        for s in ["ПЛАНЕТА", "ЗВЕЗДА", "КОМЕТА", "МЕТЕОРИТ", "СОЗВЕЗДИЕ", "ГАЛАКТИКА"]: 
            t = Termin()
            t.init_by_normal_text(s, None)
            t.tag = NamedEntityKind.PLANET
            NamedItemToken.__m_types.add(t)
        for s in ["СОЛНЦЕ", "МЕРКУРИЙ", "ВЕНЕРА", "ЗЕМЛЯ", "МАРС", "ЮПИТЕР", "САТУРН", "УРАН", "НЕПТУН", "ПЛУТОН", "ЛУНА", "ДЕЙМОС", "ФОБОС", "Ио", "Ганимед", "Каллисто"]: 
            t = Termin()
            t.init_by_normal_text(s.upper(), None)
            t.tag = NamedEntityKind.PLANET
            NamedItemToken.__m_names.add(t)
        for s in ["РЕКА", "ОЗЕРО", "МОРЕ", "ОКЕАН", "ЗАЛИВ", "ПРОЛИВ", "ПОБЕРЕЖЬЕ", "КОНТИНЕНТ", "ОСТРОВ", "ПОЛУОСТРОВ", "МЫС", "ГОРА", "ГОРНЫЙ ХРЕБЕТ", "ПЕРЕВАЛ", "ПАДЬ", "ЛЕС", "САД", "ЗАПОВЕДНИК", "ЗАКАЗНИК", "ДОЛИНА", "УЩЕЛЬЕ", "РАВНИНА", "БЕРЕГ"]: 
            t = Termin()
            t.init_by_normal_text(s, None)
            t.tag = NamedEntityKind.LOCATION
            NamedItemToken.__m_types.add(t)
        for s in ["ТИХИЙ", "АТЛАНТИЧЕСКИЙ", "ИНДИЙСКИЙ", "СЕВЕРО-ЛЕДОВИТЫЙ"]: 
            t = Termin()
            t.init_by_normal_text(s, None)
            t.tag = NamedEntityKind.LOCATION
            t.tag2 = ("океан")
            NamedItemToken.__m_names.add(t)
        for s in ["ЕВРАЗИЯ", "АФРИКА", "АМЕРИКА", "АВСТРАЛИЯ", "АНТАРКТИДА"]: 
            t = Termin()
            t.init_by_normal_text(s, None)
            t.tag = NamedEntityKind.LOCATION
            t.tag2 = ("континент")
            NamedItemToken.__m_names.add(t)
        for s in ["ВОЛГА", "НЕВА", "АМУР", "ОБЪ", "АНГАРА", "ЛЕНА", "ИРТЫШ", "ДНЕПР", "ДОН", "ДНЕСТР", "РЕЙН", "АМУДАРЬЯ", "СЫРДАРЬЯ", "ТИГР", "ЕВФРАТ", "ИОРДАН", "МИССИСИПИ", "АМАЗОНКА", "ТЕМЗА", "СЕНА", "НИЛ", "ЯНЦЗЫ", "ХУАНХЭ", "ПАРАНА", "МЕКОНГ", "МАККЕНЗИ", "НИГЕР", "ЕНИСЕЙ", "МУРРЕЙ", "САЛУИН", "ИНД", "РИО-ГРАНДЕ", "БРАХМАПУТРА", "ДАРЛИНГ", "ДУНАЙ", "ЮКОН", "ГАНГ", "МАРРАМБИДЖИ", "ЗАМБЕЗИ", "ТОКАНТИС", "ОРИНОКО", "СИЦЗЯН", "КОЛЫМА", "КАМА", "ОКА", "ЭЛЬЮА", "ВИСЛА", "ДАУГАВА", "ЗАПАДНАЯ ДВИНА", "НЕМАН", "МЕЗЕНЬ", "КУБАНЬ", "ЮЖНЫЙ БУГ"]: 
            t = Termin()
            t.init_by_normal_text(s, None)
            t.tag = NamedEntityKind.LOCATION
            t.tag2 = ("река")
            NamedItemToken.__m_names.add(t)
        for s in ["ЕВРОПА", "АЗИЯ", "АРКТИКА", "КАВКАЗ", "ПРИБАЛТИКА", "СИБИРЬ", "ЗАПОЛЯРЬЕ", "ЧУКОТКА", "ПРИБАЛТИКА", "БАЛКАНЫ", "СКАНДИНАВИЯ", "ОКЕАНИЯ", "АЛЯСКА", "УРАЛ", "ПОВОЛЖЬЕ", "ПРИМОРЬЕ", "КУРИЛЫ", "ТИБЕТ", "ГИМАЛАИ", "АЛЬПЫ", "САХАРА", "ГОБИ", "СИНАЙ", "БАЙКОНУР", "ЧЕРНОБЫЛЬ", "САДОВОЕ КОЛЬЦО", "СТАРЫЙ ГОРОД", "НОВЫЙ ГОРОД"]: 
            t = Termin()
            t.init_by_normal_text(s, None)
            t.tag = NamedEntityKind.LOCATION
            NamedItemToken.__m_names.add(t)
        for s in ["ПАМЯТНИК", "МОНУМЕНТ", "МЕМОРИАЛ", "БЮСТ", "ОБЕЛИСК", "МОГИЛА", "МАВЗОЛЕЙ", "ЗАХОРОНЕНИЕ", "ПАМЯТНАЯ ДОСКА", "ПАМЯТНЫЙ ЗНАК"]: 
            t = Termin()
            t.init_by_normal_text(s, None)
            t.add_variant(s + " В ЧЕСТЬ", False)
            t.tag = NamedEntityKind.MONUMENT
            NamedItemToken.__m_types.add(t)
        b = Termin.ASSIGN_ALL_TEXTS_AS_NORMAL
        Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = False
        for s in ["ВЕЧНЫЙ ОГОНЬ", "НЕИЗВЕСТНЫЙ СОЛДАТ", "ПОКЛОННАЯ ГОРА", "МЕДНЫЙ ВСАДНИК", "ЛЕНИН"]: 
            t = Termin(s)
            t.tag = NamedEntityKind.MONUMENT
            t.tag3 = (NamedItemToken.__m_names)
            NamedItemToken.__m_names.add(t)
        t = Termin._new1475("ПОБЕДА В ВЕЛИКОЙ ОТЕЧЕСТВЕННОЙ ВОЙНЕ", NamedEntityKind.MONUMENT, NamedItemToken.__m_names)
        t.add_variant("ПОБЕДА В ВОВ", False)
        NamedItemToken.__m_names.add(t)
        for s in ["ФИЛЬМ", "КИНОФИЛЬМ", "ТЕЛЕФИЛЬМ", "СЕРИАЛ", "ТЕЛЕСЕРИАЛ", "БЛОКБАСТЕР", "СИКВЕЛ", "КОМЕДИЯ", "ТЕЛЕКОМЕДИЯ", "БОЕВИК", "АЛЬБОМ", "ДИСК", "ПЕСНЯ", "СИНГЛ", "СПЕКТАКЛЬ", "МЮЗИКЛ", "ТЕЛЕСПЕКТАКЛЬ", "ТЕЛЕШОУ", "КНИГА", "РАССКАЗ", "РОМАН", "ПОЭМА", "СТИХ", "СТИХОТВОРЕНИЕ"]: 
            t = Termin(s)
            t.tag = NamedEntityKind.ART
            NamedItemToken.__m_types.add(t)
        Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = b
        for s in ["ДВОРЕЦ", "КРЕМЛЬ", "ЗАМОК", "КРЕПОСТЬ", "УСАДЬБА", "ДОМ", "ЗДАНИЕ", "ШТАБ-КВАРТИРА", "ЖЕЛЕЗНОДОРОЖНЫЙ ВОКЗАЛ", "ВОКЗАЛ", "АВТОВОКЗАЛ", "АЭРОВОКЗАЛ", "АЭРОПОРТ", "АЭРОДРОМ", "БИБЛИОТЕКА", "СОБОР", "МЕЧЕТЬ", "СИНАГОГА", "ЛАВРА", "ХРАМ", "ЦЕРКОВЬ"]: 
            t = Termin()
            t.init_by_normal_text(s, None)
            t.tag = NamedEntityKind.BUILDING
            NamedItemToken.__m_types.add(t)
        for s in ["КРЕМЛЬ", "КАПИТОЛИЙ", "БЕЛЫЙ ДОМ", "БИГ БЕН", "ХРАМОВАЯ ГОРА"]: 
            t = Termin()
            t.init_by_normal_text(s, None)
            t.tag = NamedEntityKind.BUILDING
            NamedItemToken.__m_names.add(t)
        t = Termin._new264("МЕЖДУНАРОДНАЯ КОСМИЧЕСКАЯ СТАНЦИЯ", NamedEntityKind.BUILDING)
        t.acronym = "МКС"
        NamedItemToken.__m_names.add(t)
    
    __m_types = None
    
    __m_names = None
    
    @staticmethod
    def _new1469(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'Referent', _arg4 : 'MorphCollection') -> 'NamedItemToken':
        res = NamedItemToken(_arg1, _arg2)
        res.ref = _arg3
        res.morph = _arg4
        return res
    
    @staticmethod
    def _new1470(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'MorphCollection', _arg4 : 'CharsInfo') -> 'NamedItemToken':
        res = NamedItemToken(_arg1, _arg2)
        res.morph = _arg3
        res.chars = _arg4
        return res
    
    @staticmethod
    def _new1472(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'MorphCollection') -> 'NamedItemToken':
        res = NamedItemToken(_arg1, _arg2)
        res.morph = _arg3
        return res