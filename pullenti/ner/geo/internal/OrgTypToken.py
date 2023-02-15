# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import typing
from pullenti.unisharp.Utils import Utils

from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.geo.internal.NameTokenType import NameTokenType
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.address.internal.AddressItemToken import AddressItemToken
from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.ner.geo.internal.GeoTokenData import GeoTokenData
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
from pullenti.ner.geo.internal.MiscLocationHelper import MiscLocationHelper
from pullenti.ner.geo.internal.TerrItemToken import TerrItemToken
from pullenti.ner.address.internal.StreetItemToken import StreetItemToken
from pullenti.ner.geo.GeoAnalyzer import GeoAnalyzer
from pullenti.ner.geo.internal.NameToken import NameToken

class OrgTypToken(MetaToken):
    
    def __init__(self, b : 'Token', e0_ : 'Token') -> None:
        super().__init__(b, e0_, None)
        self.is_doubt = False
        self.is_massiv = False
        self.vals = list()
    
    def clone(self) -> 'OrgTypToken':
        res = OrgTypToken(self.begin_token, self.end_token)
        res.vals.extend(self.vals)
        res.is_doubt = self.is_doubt
        res.is_massiv = self.is_massiv
        return res
    
    def __str__(self) -> str:
        tmp = io.StringIO()
        if (self.is_doubt): 
            print("? ", end="", file=tmp)
        i = 0
        while i < len(self.vals): 
            if (i > 0): 
                print(" / ", end="", file=tmp)
            print(self.vals[i], end="", file=tmp)
            i += 1
        return Utils.toStringStringIO(tmp)
    
    SPEED_REGIME = False
    
    @staticmethod
    def _prepare_all_data(t0 : 'Token') -> None:
        if (not OrgTypToken.SPEED_REGIME): 
            return
        ad = GeoAnalyzer._get_data(t0)
        if (ad is None): 
            return
        ad.otregime = False
        t = t0
        while t is not None: 
            after_terr = False
            tt = MiscLocationHelper.check_territory(t)
            if (tt is not None and tt.next0_ is not None): 
                after_terr = True
                t = tt.next0_
            d = Utils.asObjectOrNull(t.tag, GeoTokenData)
            ty = OrgTypToken.try_parse(t, after_terr, ad)
            if (ty is not None): 
                if (d is None): 
                    d = GeoTokenData(t)
                d.org_typ = ty
                t = ty.end_token
            t = t.next0_
        ad.otregime = True
    
    @staticmethod
    def try_parse(t : 'Token', after_terr : bool, ad : 'GeoAnalyzerData'=None) -> 'OrgTypToken':
        if (not (isinstance(t, TextToken))): 
            return None
        if (t.length_char == 1 and not t.chars.is_letter): 
            return None
        if (ad is None): 
            ad = GeoAnalyzer._get_data(t)
        if (ad is None): 
            return None
        if (ad is not None and OrgTypToken.SPEED_REGIME and ((ad.otregime or ad.all_regime))): 
            d = Utils.asObjectOrNull(t.tag, GeoTokenData)
            if (d is not None): 
                return d.org_typ
            return None
        if (ad.olevel > 2): 
            return None
        ad.olevel += 1
        res = OrgTypToken.__try_parse(t, after_terr, 0)
        ad.olevel -= 1
        return res
    
    @staticmethod
    def __try_parse(t : 'Token', after_terr : bool, lev : int=0) -> 'OrgTypToken':
        if (t is None): 
            return None
        if (t.is_value("СП", None)): 
            if (not after_terr and t.chars.is_all_lower): 
                return None
        if (t.is_value("НП", None)): 
            if (not after_terr and t.chars.is_all_lower): 
                return None
        if ((t.is_value("ОФИС", None) or t.is_value("ФАД", None) or t.is_value("АД", None)) or t.is_value("КОРПУС", None)): 
            return None
        if (t.is_value("ФЕДЕРАЦИЯ", None) or t.is_value("СОЮЗ", None) or t.is_value("ПРЕФЕКТУРА", None)): 
            return None
        t1 = None
        typs = None
        doubt = False
        massiv = False
        morph_ = None
        tok = OrgTypToken._m_org_ontology.try_parse(t, TerminParseAttr.NO)
        if (tok is not None): 
            t1 = tok.end_token
            typs = list()
            morph_ = tok.morph
            massiv = tok.termin.tag2 is not None
            typs.append(tok.termin.canonic_text.lower())
            if (tok.termin.acronym is not None): 
                typs.append(tok.termin.acronym)
            if (tok.end_token == t): 
                if ((t.length_char < 4) and (isinstance(t, TextToken)) and LanguageHelper.ends_with(t.term, "К")): 
                    oi = TerrItemToken.check_onto_item(t.next0_)
                    if (oi is not None): 
                        if (t.next0_.get_morph_class_in_dictionary().is_adjective and oi.begin_token == oi.end_token): 
                            pass
                        else: 
                            return None
                    if ((not after_terr and t.chars.is_all_upper and t.next0_ is not None) and t.next0_.chars.is_all_upper and t.next0_.length_char > 1): 
                        return None
            if (tok.termin.canonic_text == "МЕСТОРОЖДЕНИЕ" and (isinstance(tok.end_token.next0_, TextToken)) and tok.end_token.next0_.chars.is_all_lower): 
                npt = NounPhraseHelper.try_parse(tok.end_token.next0_, NounPhraseParseAttr.NO, 0, None)
                if (npt is not None and npt.chars.is_all_lower): 
                    tok.end_token = npt.end_token
            if ((((t.chars.is_all_upper and t.length_char == 1 and t.next0_ is not None) and t.next0_.is_char('.') and (isinstance(t.next0_.next0_, TextToken))) and t.next0_.next0_.length_char == 1 and t.next0_.next0_.chars.is_all_upper) and t.next0_.next0_.next0_ == tok.end_token and tok.end_token.is_char('.')): 
                return None
        else: 
            if (StreetItemToken.check_keyword(t)): 
                return None
            rtok = t.kit.process_referent("ORGANIZATION", t, "MINTYPE")
            if (rtok is not None): 
                if (rtok.end_token == t and t.is_value("ТК", None)): 
                    if (TerrItemToken.check_onto_item(t.next0_) is not None): 
                        return None
                    if (t.chars.is_all_upper and t.next0_ is not None and t.next0_.chars.is_all_upper): 
                        return None
                prof = rtok.referent.get_string_value("PROFILE")
                if (Utils.compareStrings(Utils.ifNotNull(prof, ""), "UNIT", True) == 0): 
                    doubt = True
                t1 = rtok.end_token
                typs = rtok.referent.get_string_values("TYPE")
                morph_ = rtok.morph
        if (((t1 is None and (isinstance(t, TextToken)) and t.length_char >= 2) and t.length_char <= 4 and t.chars.is_all_upper) and t.chars.is_cyrillic_letter): 
            if (AddressItemToken.try_parse_pure_item(t, None, None) is not None): 
                return None
            if (t.length_char == 2): 
                return None
            if (TerrItemToken.check_onto_item(t) is not None): 
                return None
            typs = list()
            typs.append(t.term)
            t1 = t
            doubt = True
        if (t1 is None and after_terr): 
            pt = AddressItemToken.M_PLOT.try_parse(t, TerminParseAttr.NO)
            if (pt is not None): 
                typs = list()
                typs.append("участок")
                t1 = pt.end_token
                doubt = True
            else: 
                pt = AddressItemToken.M_OWNER.try_parse(t, TerminParseAttr.NO)
                if ((pt) is not None): 
                    typs = list()
                    typs.append("владение")
                    t1 = pt.end_token
                    doubt = True
        if (t1 is None): 
            return None
        if (morph_ is None): 
            morph_ = t1.morph
        res = OrgTypToken._new1119(t, t1, doubt, typs, morph_, massiv)
        if ((t == t1 and (t.length_char < 3) and t.next0_ is not None) and t.next0_.is_char('.')): 
            res.end_token = t1.next0_
        if ((lev < 2) and (res.whitespaces_after_count < 3)): 
            next0__ = OrgTypToken.try_parse(res.end_token.next0_, after_terr, None)
            if (next0__ is not None and not next0__.begin_token.chars.is_all_lower): 
                nam = NameToken.try_parse(next0__.end_token.next0_, NameTokenType.ORG, 0, False)
                if (nam is None or next0__.whitespaces_after_count > 3): 
                    next0__ = (None)
                elif ((nam.number is not None and nam.name is None and next0__.length_char > 2) and next0__.is_doubt): 
                    next0__ = (None)
            if (next0__ is not None): 
                if (not next0__.is_doubt): 
                    res.is_doubt = False
                res.merge_with(next0__)
        return res
    
    def merge_with(self, ty : 'OrgTypToken') -> None:
        for v in ty.vals: 
            if (not v in self.vals): 
                self.vals.append(v)
        if (ty.is_massiv): 
            self.is_massiv = True
        self.end_token = ty.end_token
    
    @staticmethod
    def find_termin_by_acronym(abbr : str) -> typing.List['Termin']:
        te = Termin._new1113(abbr, abbr)
        return OrgTypToken._m_org_ontology.find_termins_by_termin(te)
    
    @staticmethod
    def initialize() -> None:
        OrgTypToken._m_org_ontology = TerminCollection()
        t = Termin._new1113("САДОВОЕ ТОВАРИЩЕСТВО", "СТ")
        t.add_variant("САДОВОДЧЕСКОЕ ТОВАРИЩЕСТВО", False)
        t.acronym = "СТ"
        t.add_abridge("С/ТОВ")
        t.add_abridge("ПК СТ")
        t.add_abridge("САД.ТОВ.")
        t.add_abridge("САДОВ.ТОВ.")
        t.add_abridge("С/Т")
        t.add_variant("ВЕДЕНИЕ ГРАЖДАНАМИ САДОВОДСТВА ИЛИ ОГОРОДНИЧЕСТВА ДЛЯ СОБСТВЕННЫХ НУЖД", False)
        OrgTypToken._m_org_ontology.add(t)
        t = Termin("ДАЧНОЕ ТОВАРИЩЕСТВО")
        t.add_abridge("Д/Т")
        t.add_abridge("ДАЧ/Т")
        t.acronym = "ДТ"
        t.acronym_can_be_lower = True
        OrgTypToken._m_org_ontology.add(t)
        t = Termin("ЖИЛИЩНОЕ ТОВАРИЩЕСТВО")
        t.add_abridge("Ж/Т")
        t.add_abridge("ЖИЛ/Т")
        t.acronym = "ЖТ"
        t.acronym_can_be_lower = True
        OrgTypToken._m_org_ontology.add(t)
        t = Termin("САДОВЫЙ КООПЕРАТИВ")
        t.add_abridge("С/К")
        t.acronym = "СК"
        t.acronym_can_be_lower = True
        OrgTypToken._m_org_ontology.add(t)
        t = Termin("ПОТРЕБИТЕЛЬСКИЙ КООПЕРАТИВ")
        t.add_variant("ПОТРЕБКООПЕРАТИВ", False)
        t.acronym = "ПК"
        t.acronym_can_be_lower = True
        OrgTypToken._m_org_ontology.add(t)
        t = Termin("САДОВОЕ ОБЩЕСТВО")
        t.add_abridge("С/О")
        t.acronym = "СО"
        t.acronym_can_be_lower = True
        OrgTypToken._m_org_ontology.add(t)
        t = Termin("САДОВОДЧЕСКОЕ ДАЧНОЕ ТОВАРИЩЕСТВО")
        t.add_variant("САДОВОЕ ДАЧНОЕ ТОВАРИЩЕСТВО", False)
        t.acronym = "СДТ"
        t.acronym_can_be_lower = True
        OrgTypToken._m_org_ontology.add(t)
        t = Termin("ДАЧНОЕ НЕКОММЕРЧЕСКОЕ ОБЪЕДИНЕНИЕ")
        t.add_variant("ДАЧНОЕ НЕКОММЕРЧЕСКОЕ ОБЪЕДИНЕНИЕ ГРАЖДАН", False)
        t.acronym = "ДНО"
        t.acronym_can_be_lower = True
        OrgTypToken._m_org_ontology.add(t)
        t = Termin("ДАЧНОЕ НЕКОММЕРЧЕСКОЕ ПАРТНЕРСТВО")
        t.add_variant("ДАЧНОЕ НЕКОММЕРЧЕСКОЕ ПАРТНЕРСТВО ГРАЖДАН", False)
        t.acronym = "ДНП"
        t.acronym_can_be_lower = True
        OrgTypToken._m_org_ontology.add(t)
        t = Termin("ДАЧНОЕ НЕКОММЕРЧЕСКОЕ ТОВАРИЩЕСТВО")
        t.acronym = "ДНТ"
        t.acronym_can_be_lower = True
        OrgTypToken._m_org_ontology.add(t)
        t = Termin("ДАЧНЫЙ ПОТРЕБИТЕЛЬСКИЙ КООПЕРАТИВ")
        t.acronym = "ДПК"
        t.acronym_can_be_lower = True
        OrgTypToken._m_org_ontology.add(t)
        t = Termin("ДАЧНО СТРОИТЕЛЬНЫЙ КООПЕРАТИВ")
        t.add_variant("ДАЧНЫЙ СТРОИТЕЛЬНЫЙ КООПЕРАТИВ", False)
        t.acronym = "ДСК"
        t.acronym_can_be_lower = True
        OrgTypToken._m_org_ontology.add(t)
        t = Termin("СТРОИТЕЛЬНО ПРОИЗВОДСТВЕННЫЙ КООПЕРАТИВ")
        t.acronym = "СПК"
        t.acronym_can_be_lower = True
        OrgTypToken._m_org_ontology.add(t)
        t = Termin("САДОВОДЧЕСКОЕ НЕКОММЕРЧЕСКОЕ ТОВАРИЩЕСТВО")
        t.add_variant("САДОВОЕ НЕКОММЕРЧЕСКОЕ ТОВАРИЩЕСТВО", False)
        t.add_variant("ТСНСТ", False)
        t.acronym = "СНТ"
        t.acronym_can_be_lower = True
        t.add_abridge("САДОВОЕ НЕКОМ-Е ТОВАРИЩЕСТВО")
        OrgTypToken._m_org_ontology.add(t)
        t = Termin._new1061("САДОВОДЧЕСКОЕ НЕКОММЕРЧЕСКОЕ ОБЪЕДИНЕНИЕ", "СНО", True)
        t.add_variant("САДОВОЕ НЕКОММЕРЧЕСКОЕ ОБЪЕДИНЕНИЕ", False)
        OrgTypToken._m_org_ontology.add(t)
        t = Termin._new1061("САДОВОДЧЕСКОЕ НЕКОММЕРЧЕСКОЕ ПАРТНЕРСТВО", "СНП", True)
        t.add_variant("САДОВОЕ НЕКОММЕРЧЕСКОЕ ПАРТНЕРСТВО", False)
        OrgTypToken._m_org_ontology.add(t)
        t = Termin._new1124("САДОВОДЧЕСКОЕ НЕКОММЕРЧЕСКОЕ ТОВАРИЩЕСТВО", "СНТ", "СНТ", True)
        t.add_variant("САДОВОЕ НЕКОММЕРЧЕСКОЕ ТОВАРИЩЕСТВО", False)
        OrgTypToken._m_org_ontology.add(t)
        t = Termin._new1061("САДОВОДЧЕСКОЕ ОГОРОДНИЧЕСКОЕ ТОВАРИЩЕСТВО", "СОТ", True)
        t.add_variant("САДОВОЕ ОГОРОДНИЧЕСКОЕ ТОВАРИЩЕСТВО", False)
        OrgTypToken._m_org_ontology.add(t)
        t = Termin._new1061("ДАЧНОЕ НЕКОММЕРЧЕСКОЕ ТОВАРИЩЕСТВО", "ДНТ", True)
        t.add_variant("ДАЧНО НЕКОММЕРЧЕСКОЕ ТОВАРИЩЕСТВО", False)
        OrgTypToken._m_org_ontology.add(t)
        t = Termin._new1061("НЕКОММЕРЧЕСКОЕ САДОВОДЧЕСКОЕ ТОВАРИЩЕСТВО", "НСТ", True)
        t.add_variant("НЕКОММЕРЧЕСКОЕ САДОВОЕ ТОВАРИЩЕСТВО", False)
        OrgTypToken._m_org_ontology.add(t)
        t = Termin._new1061("ОБЪЕДИНЕННОЕ НЕКОММЕРЧЕСКОЕ САДОВОДЧЕСКОЕ ТОВАРИЩЕСТВО", "ОНСТ", True)
        t.add_variant("ОБЪЕДИНЕННОЕ НЕКОММЕРЧЕСКОЕ САДОВОЕ ТОВАРИЩЕСТВО", False)
        OrgTypToken._m_org_ontology.add(t)
        t = Termin._new1061("САДОВОДЧЕСКАЯ ПОТРЕБИТЕЛЬСКАЯ КООПЕРАЦИЯ", "СПК", True)
        t.add_variant("САДОВАЯ ПОТРЕБИТЕЛЬСКАЯ КООПЕРАЦИЯ", False)
        t.add_variant("САДОВОДЧЕСКИЙ ПОТРЕБИТЕЛЬНЫЙ КООПЕРАТИВ", False)
        t.add_variant("САДОВОДЧЕСКИЙ ПОТРЕБИТЕЛЬСКИЙ КООПЕРАТИВ", False)
        OrgTypToken._m_org_ontology.add(t)
        t = Termin._new1061("ДАЧНО СТРОИТЕЛЬНЫЙ КООПЕРАТИВ", "ДСК", True)
        t.add_variant("ДАЧНЫЙ СТРОИТЕЛЬНЫЙ КООПЕРАТИВ", False)
        OrgTypToken._m_org_ontology.add(t)
        OrgTypToken._m_org_ontology.add(Termin._new1061("ДАЧНО СТРОИТЕЛЬНО ПРОИЗВОДСТВЕННЫЙ КООПЕРАТИВ", "ДСПК", True))
        OrgTypToken._m_org_ontology.add(Termin._new1061("ЖИЛИЩНЫЙ СТРОИТЕЛЬНО ПРОИЗВОДСТВЕННЫЙ КООПЕРАТИВ", "ЖСПК", True))
        OrgTypToken._m_org_ontology.add(Termin._new1061("ЖИЛИЩНЫЙ СТРОИТЕЛЬНЫЙ КООПЕРАТИВ", "ЖСК", True))
        OrgTypToken._m_org_ontology.add(Termin._new1061("ЖИЛИЩНЫЙ СТРОИТЕЛЬНЫЙ КООПЕРАТИВ ИНДИВИДУАЛЬНЫХ ЗАСТРОЙЩИКОВ", "ЖСКИЗ", True))
        t = Termin._new1061("ОГОРОДНИЧЕСКОЕ НЕКОММЕРЧЕСКОЕ ОБЪЕДИНЕНИЕ", "ОНО", True)
        t.add_variant("ОГОРОДНИЧЕСКОЕ ОБЪЕДИНЕНИЕ", False)
        OrgTypToken._m_org_ontology.add(t)
        t = Termin._new1061("ОГОРОДНИЧЕСКОЕ НЕКОММЕРЧЕСКОЕ ПАРТНЕРСТВО", "ОНП", True)
        t.add_variant("ОГОРОДНИЧЕСКОЕ ПАРТНЕРСТВО", False)
        OrgTypToken._m_org_ontology.add(t)
        t = Termin._new1061("ОГОРОДНИЧЕСКОЕ НЕКОММЕРЧЕСКОЕ ТОВАРИЩЕСТВО", "ОНТ", True)
        t.add_variant("ОГОРОДНИЧЕСКОЕ ТОВАРИЩЕСТВО", False)
        OrgTypToken._m_org_ontology.add(t)
        t = Termin._new1061("ОГОРОДНИЧЕСКИЙ ПОТРЕБИТЕЛЬСКИЙ КООПЕРАТИВ", "ОПК", True)
        t.add_variant("ОГОРОДНИЧЕСКИЙ КООПЕРАТИВ", False)
        OrgTypToken._m_org_ontology.add(t)
        OrgTypToken._m_org_ontology.add(Termin._new1061("ТОВАРИЩЕСТВО СОБСТВЕННИКОВ НЕДВИЖИМОСТИ", "СТСН", True))
        OrgTypToken._m_org_ontology.add(Termin._new1061("САДОВОДЧЕСКОЕ ТОВАРИЩЕСТВО СОБСТВЕННИКОВ НЕДВИЖИМОСТИ", "ТСН", True))
        OrgTypToken._m_org_ontology.add(Termin._new1061("ТОВАРИЩЕСТВО СОБСТВЕННИКОВ ЖИЛЬЯ", "ТСЖ", True))
        OrgTypToken._m_org_ontology.add(Termin._new1061("САДОВЫЕ ЗЕМЕЛЬНЫЕ УЧАСТКИ", "СЗУ", True))
        OrgTypToken._m_org_ontology.add(Termin._new1061("ТОВАРИЩЕСТВО ИНДИВИДУАЛЬНЫХ ЗАСТРОЙЩИКОВ", "ТИЗ", True))
        t = Termin._new1061("КОЛЛЕКТИВ ИНДИВИДУАЛЬНЫХ ЗАСТРОЙЩИКОВ", "КИЗ", True)
        t.add_variant("КИЗК", False)
        OrgTypToken._m_org_ontology.add(t)
        t = Termin._new1061("САДОВОЕ НЕКОММЕРЧЕСКОЕ ТОВАРИЩЕСТВО СОБСТВЕННИКОВ НЕДВИЖИМОСТИ", "СНТСН", True)
        t.add_variant("САДОВОДЧЕСКОЕ НЕКОММЕРЧЕСКОЕ ТОВАРИЩЕСТВО СОБСТВЕННИКОВ НЕДВИЖИМОСТИ", False)
        t.add_variant("СНТ СН", False)
        OrgTypToken._m_org_ontology.add(t)
        t = Termin._new1061("НЕКОММЕРЧЕСКОЕ ПАРТНЕРСТВО СОБСТВЕННИКОВ", "НПС", True)
        OrgTypToken._m_org_ontology.add(t)
        t = Termin._new1061("ЛИЧНОЕ ПОДСОБНОЕ ХОЗЯЙСТВО", "ЛПХ", True)
        OrgTypToken._m_org_ontology.add(t)
        t = Termin("ИНДИВИДУАЛЬНОЕ САДОВОДСТВО")
        OrgTypToken._m_org_ontology.add(t)
        t = Termin("ОБЪЕДИНЕНИЕ")
        OrgTypToken._m_org_ontology.add(t)
        t = Termin("ИМУЩЕСТВЕННЫЙ КОМПЛЕКС")
        OrgTypToken._m_org_ontology.add(t)
        t = Termin("СОВМЕСТНОЕ ПРЕДПРИЯТИЕ")
        t.acronym = "СП"
        t.acronym_can_be_lower = True
        OrgTypToken._m_org_ontology.add(t)
        t = Termin("НЕКОММЕРЧЕСКОЕ ПАРТНЕРСТВО")
        t.acronym = "НП"
        t.acronym_can_be_lower = True
        OrgTypToken._m_org_ontology.add(t)
        t = Termin("АВТОМОБИЛЬНЫЙ КООПЕРАТИВ")
        t.add_abridge("А/К")
        t.acronym = "АК"
        t.acronym_can_be_lower = True
        OrgTypToken._m_org_ontology.add(t)
        t = Termin("ГАРАЖНЫЙ КООПЕРАТИВ")
        t.add_abridge("Г/К")
        t.add_abridge("ГР.КОП.")
        t.add_abridge("ГАР.КОП.")
        t.add_abridge("ГАР.КООП.")
        t.add_variant("ГАРАЖНЫЙ КООП", False)
        t.acronym = "ГК"
        t.acronym_can_be_lower = True
        OrgTypToken._m_org_ontology.add(t)
        t = Termin("ПРОИЗВОДСТВЕННЫЙ СЕЛЬСКОХОЗЯЙСТВЕННЫЙ КООПЕРАТИВ")
        t.add_variant("ПРОИЗВОДСТВЕННО СЕЛЬСКОХОЗЯЙСТВЕННЫЙ КООПЕРАТИВ", False)
        t.acronym = "ПСК"
        t.acronym_can_be_lower = True
        OrgTypToken._m_org_ontology.add(t)
        OrgTypToken._m_org_ontology.add(Termin._new1061("ГАРАЖНО СТРОИТЕЛЬНЫЙ КООПЕРАТИВ", "ГСК", True))
        OrgTypToken._m_org_ontology.add(Termin._new1061("ГАРАЖНО ЭКСПЛУАТАЦИОННЫЙ КООПЕРАТИВ", "ГЭК", True))
        OrgTypToken._m_org_ontology.add(Termin._new1061("ГАРАЖНО ПОТРЕБИТЕЛЬСКИЙ КООПЕРАТИВ", "ГПК", True))
        OrgTypToken._m_org_ontology.add(Termin._new1061("ПОТРЕБИТЕЛЬСКИЙ ГАРАЖНО СТРОИТЕЛЬНЫЙ КООПЕРАТИВ", "ПГСК", True))
        OrgTypToken._m_org_ontology.add(Termin._new1061("ГАРАЖНЫЙ СТРОИТЕЛЬНО ПОТРЕБИТЕЛЬСКИЙ КООПЕРАТИВ", "ГСПК", True))
        OrgTypToken._m_org_ontology.add(Termin._new1061("ПОТРЕБИТЕЛЬСКИЙ ГАРАЖНЫЙ КООПЕРАТИВ", "ПГК", True))
        OrgTypToken._m_org_ontology.add(Termin._new1061("ИНДИВИДУАЛЬНОЕ ЖИЛИЩНОЕ СТРОИТЕЛЬСТВО", "ИЖС", True))
        OrgTypToken._m_org_ontology.add(Termin("ЖИВОТНОВОДЧЕСКАЯ ТОЧКА"))
        t = Termin._new1061("СТАНЦИЯ ТЕХНИЧЕСКОГО ОБСЛУЖИВАНИЯ", "СТО", True)
        t.add_variant("СТАНЦИЯ ТЕХОБСЛУЖИВАНИЯ", False)
        OrgTypToken._m_org_ontology.add(t)
        t = Termin._new1061("АВТО ЗАПРАВОЧНАЯ СТАНЦИЯ", "АЗС", True)
        t.add_variant("АВТОЗАПРАВОЧНАЯ СТАНЦИЯ", False)
        OrgTypToken._m_org_ontology.add(t)
        t = Termin._new1157("ДАЧНАЯ ЗАСТРОЙКА", "ДЗ", True, 1)
        t.add_variant("КВАРТАЛ ДАЧНОЙ ЗАСТРОЙКИ", False)
        t.add_variant("ЗОНА ДАЧНОЙ ЗАСТРОЙКИ", False)
        OrgTypToken._m_org_ontology.add(t)
        t = Termin._new1061("КОТТЕДЖНЫЙ ПОСЕЛОК", "КП", True)
        OrgTypToken._m_org_ontology.add(t)
        t = Termin._new1157("ДАЧНЫЙ ПОСЕЛОК", "ДП", True, 1)
        t.add_abridge("Д/П")
        t.add_variant("ДАЧНЫЙ ПОСЕЛОК МАССИВ", False)
        t.add_variant("ДП МАССИВ", False)
        OrgTypToken._m_org_ontology.add(t)
        t = Termin._new1160("САДОВОДЧЕСКИЙ МАССИВ", 1)
        t.add_variant("САД. МАССИВ", False)
        t.add_variant("САДОВЫЙ МАССИВ", False)
        OrgTypToken._m_org_ontology.add(t)
        t = Termin("САНАТОРИЙ")
        t.add_abridge("САН.")
        OrgTypToken._m_org_ontology.add(t)
        t = Termin("ДЕТСКИЙ ГОРОДОК")
        t.add_abridge("ДЕТ.ГОРОДОК")
        OrgTypToken._m_org_ontology.add(t)
        t = Termin("ДОМ ОТДЫХА")
        t.add_abridge("Д/О")
        OrgTypToken._m_org_ontology.add(t)
        t = Termin("БАЗА ОТДЫХА")
        t.add_abridge("Б/О")
        t.add_variant("БАЗА ОТДЫХА РЫБАКА И ОХОТНИКА", False)
        t.add_variant("БАЗА ОТДЫХА СЕМЕЙНОГО ТИПА", False)
        OrgTypToken._m_org_ontology.add(t)
        t = Termin._new1061("ФЕРМЕРСКОЕ ХОЗЯЙСТВО", "ФХ", True)
        t.add_abridge("Ф/Х")
        OrgTypToken._m_org_ontology.add(t)
        t = Termin._new1061("КРЕСТЬЯНСКОЕ ХОЗЯЙСТВО", "КФХ", True)
        t.add_variant("КРЕСТЬЯНСКОЕ ФЕРМЕРСКОЕ ХОЗЯЙСТВО", False)
        t.add_abridge("Ф/Х")
        OrgTypToken._m_org_ontology.add(t)
        t = Termin("СОВХОЗ")
        t.add_abridge("С-ЗА")
        t.add_abridge("С/ЗА")
        t.add_abridge("С/З")
        t.add_abridge("СХ.")
        t.add_abridge("С/Х")
        OrgTypToken._m_org_ontology.add(t)
        t = Termin("ПИОНЕРСКИЙ ЛАГЕРЬ")
        t.add_abridge("П/Л")
        t.add_abridge("П.Л.")
        t.add_abridge("ПИОНЕР.ЛАГ.")
        OrgTypToken._m_org_ontology.add(t)
        t = Termin("КУРОРТ")
        OrgTypToken._m_org_ontology.add(t)
        t = Termin._new1061("КОЛЛЕКТИВ ИНДИВИДУАЛЬНЫХ ВЛАДЕЛЬЦЕВ", "КИВ", True)
        OrgTypToken._m_org_ontology.add(t)
        t = Termin("ПОДСОБНОЕ ХОЗЯЙСТВО")
        t.add_abridge("ПОДСОБНОЕ Х-ВО")
        t.add_abridge("ПОДСОБНОЕ ХОЗ-ВО")
        OrgTypToken._m_org_ontology.add(t)
        t = Termin._new1061("БИЗНЕС ЦЕНТР", "БЦ", True)
        t.add_variant("БІЗНЕС ЦЕНТР", False)
        OrgTypToken._m_org_ontology.add(t)
        t = Termin._new1061("ТОРГОВЫЙ ЦЕНТР", "ТЦ", True)
        t.add_variant("ТОРГОВИЙ ЦЕНТР", False)
        OrgTypToken._m_org_ontology.add(t)
        t = Termin._new1061("ТОРГОВО РАЗВЛЕКАТЕЛЬНЫЙ ЦЕНТР", "ТРЦ", True)
        t.add_variant("ТОРГОВО РОЗВАЖАЛЬНИЙ ЦЕНТР", False)
        OrgTypToken._m_org_ontology.add(t)
        t = Termin._new1061("ТОРГОВО РАЗВЛЕКАТЕЛЬНЫЙ КОМПЛЕКС", "ТРК", True)
        t.add_variant("ТОРГОВО РОЗВАЖАЛЬНИЙ КОМПЛЕКС", False)
        OrgTypToken._m_org_ontology.add(t)
        t = Termin("АЭРОПОРТ")
        OrgTypToken._m_org_ontology.add(t)
        t = Termin("АЭРОДРОМ")
        OrgTypToken._m_org_ontology.add(t)
        t = Termin("ГИДРОУЗЕЛ")
        OrgTypToken._m_org_ontology.add(t)
        t = Termin("ВОДОЗАБОР")
        OrgTypToken._m_org_ontology.add(t)
        t = Termin("ПОЛЕВОЙ СТАН")
        OrgTypToken._m_org_ontology.add(t)
        t = Termin("ЧАБАНСКАЯ СТОЯНКА")
        OrgTypToken._m_org_ontology.add(t)
        t = Termin._new1061("ВОЙСКОВАЯ ЧАСТЬ", "ВЧ", True)
        t.add_variant("ВОИНСКАЯ ЧАСТЬ", False)
        t.add_abridge("В/Ч")
        OrgTypToken._m_org_ontology.add(t)
        t = Termin._new1061("КВАРТИРНО ЭКСПЛУАТАЦИОННАЯ ЧАСТЬ", "КЭЧ", True)
        OrgTypToken._m_org_ontology.add(t)
        OrgTypToken._m_org_ontology.add(Termin("КАРЬЕР"))
        OrgTypToken._m_org_ontology.add(Termin("РУДНИК"))
        OrgTypToken._m_org_ontology.add(Termin("ПРИИСК"))
        OrgTypToken._m_org_ontology.add(Termin("ЛЕСНОЙ ТЕРМИНАЛ"))
        OrgTypToken._m_org_ontology.add(Termin("МОЛОЧНЫЙ КОМПЛЕКС"))
        t = Termin("МЕСТОРОЖДЕНИЕ")
        t.add_abridge("МЕСТОРОЖД.")
        OrgTypToken._m_org_ontology.add(t)
    
    _m_org_ontology = None
    
    @staticmethod
    def _new1119(_arg1 : 'Token', _arg2 : 'Token', _arg3 : bool, _arg4 : typing.List[str], _arg5 : 'MorphCollection', _arg6 : bool) -> 'OrgTypToken':
        res = OrgTypToken(_arg1, _arg2)
        res.is_doubt = _arg3
        res.vals = _arg4
        res.morph = _arg5
        res.is_massiv = _arg6
        return res