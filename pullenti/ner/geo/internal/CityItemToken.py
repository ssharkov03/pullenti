# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import xml.etree
import typing
import io
import math
from enum import IntEnum
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Streams import MemoryStream
from pullenti.unisharp.Streams import Stream

from pullenti.morph.MorphNumber import MorphNumber
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.address.internal.AddressItemType import AddressItemType
from pullenti.ner.address.internal.StreetItemType import StreetItemType
from pullenti.ner.address.internal.AddressItemToken import AddressItemToken
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.morph.MorphWordForm import MorphWordForm
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.morph.MorphLang import MorphLang
from pullenti.ner.core.ReferentsEqualType import ReferentsEqualType
from pullenti.ner.Referent import Referent
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
from pullenti.ner.date.DateReferent import DateReferent
from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.core.NumberExType import NumberExType
from pullenti.ner.geo.internal.Condition import Condition
from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.NumberHelper import NumberHelper
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.Token import Token
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.address.internal.PullentiNerAddressInternalResourceHelper import PullentiNerAddressInternalResourceHelper
from pullenti.ner.geo.internal.MiscLocationHelper import MiscLocationHelper
from pullenti.ner.geo.internal.GeoTokenData import GeoTokenData
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.core.IntOntologyCollection import IntOntologyCollection
from pullenti.ner.geo.GeoAnalyzer import GeoAnalyzer
from pullenti.ner.geo.internal.OrgItemToken import OrgItemToken
from pullenti.ner.geo.internal.CityAttachHelper import CityAttachHelper
from pullenti.ner.core.IntOntologyItem import IntOntologyItem
from pullenti.ner.address.internal.StreetItemToken import StreetItemToken
from pullenti.ner.MorphCollection import MorphCollection

class CityItemToken(MetaToken):
    
    class ItemType(IntEnum):
        PROPERNAME = 0
        CITY = 1
        NOUN = 2
        MISC = 3
        
        @classmethod
        def has_value(cls, value):
            return any(value == item.value for item in cls)
    
    @staticmethod
    def initialize() -> None:
        if (CityItemToken.M_ONTOLOGY is not None): 
            return
        CityItemToken.M_ONTOLOGY = IntOntologyCollection()
        CityItemToken.M_ONTOLOGY_EX = IntOntologyCollection()
        CityItemToken.M_CITY_ADJECTIVES = TerminCollection()
        t = None
        t = Termin("ГОРОД")
        t.add_abridge("ГОР.")
        t.add_abridge("Г.")
        t.tag = CityItemToken.ItemType.NOUN
        t.add_variant("ГОРОД ФЕДЕРАЛЬНОГО ЗНАЧЕНИЯ", False)
        t.add_variant("ГОРОД ГОРОДСКОЕ ПОСЕЛЕНИЕ", False)
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("ГОРОДОК")
        t.tag = CityItemToken.ItemType.NOUN
        t.add_variant("ШАХТЕРСКИЙ ГОРОДОК", False)
        t.add_variant("ПРИМОРСКИЙ ГОРОДОК", False)
        t.add_variant("МАЛЕНЬКИЙ ГОРОДОК", False)
        t.add_variant("НЕБОЛЬШОЙ ГОРОДОК", False)
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("CITY")
        t.tag = CityItemToken.ItemType.NOUN
        t.add_variant("TOWN", False)
        t.add_variant("CAPITAL", False)
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("МІСТО", MorphLang.UA)
        t.add_abridge("МІС.")
        t.add_abridge("М.")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin._new1027("ГОРОД-ГЕРОЙ", "ГОРОД")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin._new1058("МІСТО-ГЕРОЙ", MorphLang.UA, "МІСТО")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin._new1027("ГОРОД-КУРОРТ", "ГОРОД")
        t.add_abridge("Г.К.")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin._new1058("МІСТО-КУРОРТ", MorphLang.UA, "МІСТО")
        t.add_abridge("М.К.")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("СЕЛО")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("ДЕРЕВНЯ")
        t.add_abridge("ДЕР.")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("СЕЛЕНИЕ")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("СЕЛО", MorphLang.UA)
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("ПОСЕЛЕНИЕ")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("ПОСЕЛОК")
        t.add_abridge("ПОС.")
        t.tag = CityItemToken.ItemType.NOUN
        t.add_variant("ЖИЛОЙ ПОСЕЛОК", False)
        t.add_variant("КУРОРТНЫЙ ПОСЕЛОК", False)
        t.add_variant("ВАХТОВЫЙ ПОСЕЛОК", False)
        t.add_variant("ШАХТЕРСКИЙ ПОСЕЛОК", False)
        t.add_variant("ПОСЕЛОК СОВХОЗА", False)
        t.add_variant("ПОСЕЛОК КОЛХОЗА", False)
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("СЕЛИЩЕ", MorphLang.UA)
        t.add_abridge("СЕЛ.")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("ПОСЕЛОК ГОРОДСКОГО ТИПА")
        t.acronym_smart = "ПГТ"
        t.acronym = t.acronym_smart
        t.add_abridge("ПГТ.")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("СЕЛИЩЕ МІСЬКОГО ТИПУ", MorphLang.UA)
        t.acronym_smart = "СМТ"
        t.acronym = t.acronym_smart
        t.add_abridge("СМТ.")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("РАБОЧИЙ ПОСЕЛОК")
        t.add_abridge("Р.П.")
        t.tag = CityItemToken.ItemType.NOUN
        t.add_abridge("РАБ.П.")
        t.add_abridge("Р.ПОС.")
        t.add_abridge("РАБ.ПОС.")
        t.add_abridge("РП")
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("РОБОЧЕ СЕЛИЩЕ", MorphLang.UA)
        t.add_abridge("Р.С.")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("ДАЧНЫЙ ПОСЕЛОК")
        t.add_abridge("Д.П.")
        t.tag = CityItemToken.ItemType.NOUN
        t.add_abridge("ДАЧ.П.")
        t.add_abridge("Д.ПОС.")
        t.add_abridge("ДАЧ.ПОС.")
        t.add_variant("ЖИЛИЩНО ДАЧНЫЙ ПОСЕЛОК", False)
        t.add_variant("ДАЧНОЕ ПОСЕЛЕНИЕ", False)
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("ДАЧНЕ СЕЛИЩЕ", MorphLang.UA)
        t.add_abridge("Д.С.")
        t.tag = CityItemToken.ItemType.NOUN
        t.add_abridge("ДАЧ.С.")
        t.add_abridge("Д.СЕЛ.")
        t.add_abridge("ДАЧ.СЕЛ.")
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin._new1061("ГОРОДСКОЕ ПОСЕЛЕНИЕ", "ГП", True)
        t.add_abridge("Г.П.")
        t.tag = CityItemToken.ItemType.NOUN
        t.add_abridge("Г.ПОС.")
        t.add_abridge("ГОР.П.")
        t.add_abridge("ГОР.ПОС.")
        t.add_abridge("ГП.")
        t.add_variant("ГОРОДСКОЙ ПОСЕЛОК", False)
        t.add_abridge("Г.О.Г.")
        t.add_abridge("ГОРОДСКОЙ ОКРУГ Г.")
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin._new290("ПОСЕЛКОВОЕ ПОСЕЛЕНИЕ", "ПОСЕЛОК", CityItemToken.ItemType.NOUN)
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("МІСЬКЕ ПОСЕЛЕННЯ", MorphLang.UA)
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("СЕЛЬСКОЕ ПОСЕЛЕНИЕ")
        t.tag = CityItemToken.ItemType.NOUN
        t.add_abridge("С.ПОС.")
        t.add_abridge("С.П.")
        t.add_variant("СЕЛЬСОВЕТ", False)
        t.add_variant("СЕЛЬСКИЙ ПОСЕЛОК", False)
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("СІЛЬСЬКЕ ПОСЕЛЕННЯ", MorphLang.UA)
        t.add_abridge("С.ПОС.")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("СТАНИЦА")
        t.tag = CityItemToken.ItemType.NOUN
        t.add_abridge("СТ-ЦА")
        t.add_abridge("СТАН-ЦА")
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("СТАНИЦЯ", MorphLang.UA)
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin._new1027("СТОЛИЦА", "ГОРОД")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin._new1058("СТОЛИЦЯ", MorphLang.UA, "МІСТО")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("СТАНЦИЯ")
        t.add_abridge("СТАНЦ.")
        t.add_abridge("СТ.")
        t.add_abridge("СТАН.")
        t.tag = CityItemToken.ItemType.NOUN
        t.add_variant("ПЛАТФОРМА", False)
        t.add_abridge("ПЛАТФ.")
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("СТАНЦІЯ", MorphLang.UA)
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("ЖЕЛЕЗНОДОРОЖНАЯ СТАНЦИЯ")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("ЗАЛІЗНИЧНА СТАНЦІЯ", MorphLang.UA)
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("НАСЕЛЕННЫЙ ПУНКТ")
        t.tag = CityItemToken.ItemType.NOUN
        t.add_abridge("Н.П.")
        t.add_abridge("Б.Н.П.")
        t.add_abridge("НП")
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("НАСЕЛЕНИЙ ПУНКТ", MorphLang.UA)
        t.tag = CityItemToken.ItemType.NOUN
        t.add_abridge("НП")
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin._new1027("РАЙОННЫЙ ЦЕНТР", "НАСЕЛЕННЫЙ ПУНКТ")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin._new1058("РАЙОННИЙ ЦЕНТР", MorphLang.UA, "НАСЕЛЕНИЙ ПУНКТ")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin._new1027("ОБЛАСТНОЙ ЦЕНТР", "НАСЕЛЕННЫЙ ПУНКТ")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin._new1058("ОБЛАСНИЙ ЦЕНТР", MorphLang.UA, "НАСЕЛЕНИЙ ПУНКТ")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("ПОЧИНОК")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("ЗАИМКА")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("ХУТОР")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("АУЛ")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("ААЛ")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("АРБАН")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("ВЫСЕЛКИ")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("МЕСТЕЧКО")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("УСАДЬБА")
        t.tag = CityItemToken.ItemType.NOUN
        t.add_variant("ЦЕНТРАЛЬНАЯ УСАДЬБА", False)
        t.add_abridge("ЦЕНТР.УС.")
        t.add_abridge("ЦЕНТР.УСАДЬБА")
        t.add_abridge("Ц/У")
        t.add_abridge("УС-БА")
        t.add_abridge("ЦЕНТР.УС-БА")
        CityItemToken.M_ONTOLOGY.add(t)
        for s in ["ЖИТЕЛЬ", "МЭР"]: 
            CityItemToken.M_ONTOLOGY.add(Termin._new264(s, CityItemToken.ItemType.MISC))
        for s in ["ЖИТЕЛЬ", "МЕР"]: 
            CityItemToken.M_ONTOLOGY.add(Termin._new572(s, MorphLang.UA, CityItemToken.ItemType.MISC))
        t = Termin._new264("АДМИНИСТРАЦИЯ", CityItemToken.ItemType.MISC)
        t.add_abridge("АДМ.")
        CityItemToken.M_ONTOLOGY.add(t)
        CityItemToken.M_STD_ADJECTIVES = IntOntologyCollection()
        t = Termin("ВЕЛИКИЙ")
        t.add_abridge("ВЕЛ.")
        t.add_abridge("ВЕЛИК.")
        CityItemToken.M_STD_ADJECTIVES.add(t)
        t = Termin("БОЛЬШОЙ")
        t.add_abridge("БОЛ.")
        t.add_abridge("БОЛЬШ.")
        CityItemToken.M_STD_ADJECTIVES.add(t)
        t = Termin("МАЛЫЙ")
        t.add_abridge("МАЛ.")
        CityItemToken.M_STD_ADJECTIVES.add(t)
        t = Termin("ВЕРХНИЙ")
        t.add_abridge("ВЕР.")
        t.add_abridge("ВЕРХ.")
        CityItemToken.M_STD_ADJECTIVES.add(t)
        t = Termin("НИЖНИЙ")
        t.add_abridge("НИЖ.")
        t.add_abridge("НИЖН.")
        CityItemToken.M_STD_ADJECTIVES.add(t)
        t = Termin("СРЕДНИЙ")
        t.add_abridge("СРЕД.")
        t.add_abridge("СРЕДН.")
        t.add_abridge("СР.")
        CityItemToken.M_STD_ADJECTIVES.add(t)
        t = Termin("СТАРЫЙ")
        t.add_abridge("СТ.")
        t.add_abridge("СТАР.")
        CityItemToken.M_STD_ADJECTIVES.add(t)
        t = Termin("НОВЫЙ")
        t.add_abridge("НОВ.")
        CityItemToken.M_STD_ADJECTIVES.add(t)
        t = Termin("ВЕЛИКИЙ", MorphLang.UA)
        t.add_abridge("ВЕЛ.")
        t.add_abridge("ВЕЛИК.")
        CityItemToken.M_STD_ADJECTIVES.add(t)
        t = Termin("МАЛИЙ", MorphLang.UA)
        t.add_abridge("МАЛ.")
        CityItemToken.M_STD_ADJECTIVES.add(t)
        t = Termin("ВЕРХНІЙ", MorphLang.UA)
        t.add_abridge("ВЕР.")
        t.add_abridge("ВЕРХ.")
        t.add_abridge("ВЕРХН.")
        CityItemToken.M_STD_ADJECTIVES.add(t)
        t = Termin("НИЖНІЙ", MorphLang.UA)
        t.add_abridge("НИЖ.")
        t.add_abridge("НИЖН.")
        CityItemToken.M_STD_ADJECTIVES.add(t)
        t = Termin("СЕРЕДНІЙ", MorphLang.UA)
        t.add_abridge("СЕР.")
        t.add_abridge("СЕРЕД.")
        t.add_abridge("СЕРЕДН.")
        CityItemToken.M_STD_ADJECTIVES.add(t)
        t = Termin("СТАРИЙ", MorphLang.UA)
        t.add_abridge("СТ.")
        t.add_abridge("СТАР.")
        CityItemToken.M_STD_ADJECTIVES.add(t)
        t = Termin("НОВИЙ", MorphLang.UA)
        t.add_abridge("НОВ.")
        CityItemToken.M_STD_ADJECTIVES.add(t)
        CityItemToken.M_STD_ADJECTIVES.add(Termin("SAN"))
        CityItemToken.M_STD_ADJECTIVES.add(Termin("LOS"))
        CityItemToken.M_SPEC_NAMES = TerminCollection()
        for s in ["ГОРОДОК ПИСАТЕЛЕЙ ПЕРЕДЕЛКИНО", "ЦЕНТРАЛЬНАЯ УСАДЬБА", "ГОРКИ ЛЕНИНСКИЕ"]: 
            CityItemToken.M_SPEC_NAMES.add(Termin._new1072(s, True))
        CityItemToken.M_SPEC_ABBRS = TerminCollection()
        t = Termin("ЛЕСНИЧЕСТВО")
        t.add_abridge("ЛЕС-ВО")
        t.add_abridge("ЛЕСН-ВО")
        CityItemToken.M_SPEC_ABBRS.add(t)
        t = Termin("ЛЕСОПАРК")
        CityItemToken.M_SPEC_ABBRS.add(t)
        t = Termin("ЛЕСОУЧАСТОК")
        CityItemToken.M_SPEC_ABBRS.add(t)
        t = Termin("РУДНИК")
        CityItemToken.M_SPEC_ABBRS.add(t)
        t = Termin("ПРИИСК")
        CityItemToken.M_SPEC_ABBRS.add(t)
        t = Termin("МЕСТОРОЖДЕНИЯ")
        CityItemToken.M_SPEC_ABBRS.add(t)
        t = Termin("ЗАПОВЕДНИК")
        t.add_abridge("ЗАП-К")
        CityItemToken.M_SPEC_ABBRS.add(t)
        t = Termin("СОВХОЗ")
        t.add_abridge("С/Х")
        t.add_abridge("СВХ")
        CityItemToken.M_SPEC_ABBRS.add(t)
        dat = PullentiNerAddressInternalResourceHelper.get_bytes("c.dat")
        if (dat is None): 
            raise Utils.newException("Not found resource file c.dat in Analyzer.Location", None)
        with MemoryStream(MiscLocationHelper._deflate(dat)) as tmp: 
            tmp.position = 0
            xml0_ = None # new XmlDocument
            xml0_ = Utils.parseXmlFromStream(tmp)
            for x in xml0_.getroot(): 
                if (Utils.getXmlName(x) == "bigcity"): 
                    CityItemToken.__load_big_city(x)
                elif (Utils.getXmlName(x) == "city"): 
                    CityItemToken.__load_city(x)
    
    @staticmethod
    def __load_city(xml0_ : xml.etree.ElementTree.Element) -> None:
        ci = IntOntologyItem(None)
        onto = CityItemToken.M_ONTOLOGY_EX
        lang = MorphLang.RU
        if (Utils.getXmlAttrByName(xml0_.attrib, "l") is not None and Utils.getXmlAttrByName(xml0_.attrib, "l")[1] == "ua"): 
            lang = MorphLang.UA
        for x in xml0_: 
            if (Utils.getXmlName(x) == "n"): 
                v = Utils.getXmlInnerText(x)
                t = Termin()
                t.init_by_normal_text(v, lang)
                ci.termins.append(t)
                t.add_std_abridges()
                if (v.startswith("SAINT ")): 
                    t.add_abridge("ST. " + v[6:])
                elif (v.startswith("SAITNE ")): 
                    t.add_abridge("STE. " + v[7:])
        onto.add_item(ci)
    
    @staticmethod
    def __load_big_city(xml0_ : xml.etree.ElementTree.Element) -> None:
        ci = IntOntologyItem(None)
        ci.misc_attr = (ci)
        adj = None
        onto = CityItemToken.M_ONTOLOGY_EX
        city_adj = CityItemToken.M_CITY_ADJECTIVES
        lang = MorphLang.RU
        if (Utils.getXmlAttrByName(xml0_.attrib, "l") is not None): 
            la = Utils.getXmlAttrByName(xml0_.attrib, "l")[1]
            if (la == "ua"): 
                lang = MorphLang.UA
            elif (la == "en"): 
                lang = MorphLang.EN
        for x in xml0_: 
            if (Utils.getXmlName(x) == "n"): 
                v = Utils.getXmlInnerText(x)
                if (Utils.isNullOrEmpty(v)): 
                    continue
                t = Termin()
                t.init_by_normal_text(v, lang)
                ci.termins.append(t)
                if (v == "САНКТ-ПЕТЕРБУРГ"): 
                    if (CityItemToken.M_ST_PETERBURG is None): 
                        CityItemToken.M_ST_PETERBURG = ci
                    t.acronym = "СПБ"
                    t.add_abridge("С.ПЕТЕРБУРГ")
                    t.add_abridge("СП-Б")
                    t.add_abridge("С-ПБ")
                    ci.termins.append(Termin("ПЕТЕРБУРГ", lang))
                elif (v.startswith("SAINT ")): 
                    t.add_abridge("ST. " + v[6:])
                elif (v.startswith("SAITNE ")): 
                    t.add_abridge("STE. " + v[7:])
                elif (v.startswith("НИЖН") and v.find(' ') > 0): 
                    ii = v.find(' ')
                    vv = v[ii + 1:]
                    t.add_abridge("Н." + vv)
                    t.add_abridge("Н-" + vv)
            elif (Utils.getXmlName(x) == "a"): 
                adj = Utils.getXmlInnerText(x)
        onto.add_item(ci)
        if (not Utils.isNullOrEmpty(adj)): 
            at = Termin()
            at.init_by_normal_text(adj, lang)
            at.tag = (ci)
            city_adj.add(at)
            spb = adj == "САНКТ-ПЕТЕРБУРГСКИЙ" or adj == "САНКТ-ПЕТЕРБУРЗЬКИЙ"
            if (spb): 
                city_adj.add(Termin._new572(adj[6:], lang, ci))
    
    M_ONTOLOGY = None
    
    M_ONTOLOGY_EX = None
    
    M_ST_PETERBURG = None
    
    M_CITY_ADJECTIVES = None
    
    M_STD_ADJECTIVES = None
    
    M_SPEC_NAMES = None
    
    M_SPEC_ABBRS = None
    
    @staticmethod
    def check_onto_item(t : 'Token') -> 'IntOntologyToken':
        if (not (isinstance(t, TextToken))): 
            return None
        li = CityItemToken.M_ONTOLOGY_EX.try_attach(t, None, False)
        if (li is not None): 
            for nt in li: 
                if (nt.item is not None): 
                    return nt
        return None
    
    @staticmethod
    def check_keyword(t : 'Token') -> 'IntOntologyToken':
        if (not (isinstance(t, TextToken))): 
            return None
        li = CityItemToken.M_ONTOLOGY.try_attach(t, None, False)
        if (li is not None): 
            for nt in li: 
                if (nt.item is None): 
                    return nt
        return None
    
    @staticmethod
    def try_parse_list(t : 'Token', max_count : int, ad : 'GeoAnalyzerData'=None) -> typing.List['CityItemToken']:
        ci = CityItemToken.try_parse(t, None, False, ad)
        if (ci is None): 
            if (t is None): 
                return None
            if (((isinstance(t, TextToken)) and t.is_value("МУНИЦИПАЛЬНЫЙ", None) and t.next0_ is not None) and t.next0_.is_value("ОБРАЗОВАНИЕ", None)): 
                t1 = t.next0_.next0_
                br = False
                if (BracketHelper.can_be_start_of_sequence(t1, False, False)): 
                    br = True
                    t1 = t1.next0_
                lii = CityItemToken.try_parse_list(t1, max_count, None)
                if (lii is not None and lii[0].typ == CityItemToken.ItemType.NOUN): 
                    lii[0].begin_token = t
                    lii[0].doubtful = False
                    if (br and BracketHelper.can_be_end_of_sequence(lii[len(lii) - 1].end_token.next0_, False, None, False)): 
                        lii[len(lii) - 1].end_token = lii[len(lii) - 1].end_token.next0_
                    return lii
            return None
        if (ci.chars.is_latin_letter and ci.typ == CityItemToken.ItemType.NOUN and not t.chars.is_all_lower): 
            return None
        li = list()
        li.append(ci)
        t = ci.end_token.next0_
        first_pass2876 = True
        while True:
            if first_pass2876: first_pass2876 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.is_newline_before): 
                if (t.newlines_before_count > 1): 
                    break
                if (len(li) == 1 and li[0].typ == CityItemToken.ItemType.NOUN): 
                    pass
                else: 
                    break
            ci0 = CityItemToken.try_parse(t, ci, False, ad)
            if (ci0 is None): 
                if (t.is_newline_before): 
                    break
                if (ci.typ == CityItemToken.ItemType.NOUN and BracketHelper.can_be_start_of_sequence(t, True, False)): 
                    br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
                    if ((br is not None and (br.length_char < 50) and t.next0_.chars.is_cyrillic_letter) and not t.next0_.chars.is_all_lower): 
                        ci0 = CityItemToken._new1074(br.begin_token, br.end_token, CityItemToken.ItemType.PROPERNAME)
                        tt = br.end_token.previous
                        num = None
                        if (isinstance(tt, NumberToken)): 
                            num = str(tt.value)
                            tt = tt.previous
                            if (tt is not None and tt.is_hiphen): 
                                tt = tt.previous
                        ci0.value = MiscHelper.get_text_value(br.begin_token.next0_, tt, GetTextAttr.NO)
                        if (tt != br.begin_token.next0_): 
                            ci0.alt_value = MiscHelper.get_text_value(br.begin_token.next0_, tt, GetTextAttr.NO)
                        if (Utils.isNullOrEmpty(ci0.value)): 
                            ci0 = (None)
                        elif (num is not None): 
                            ci0.value = "{0}-{1}".format(ci0.value, num)
                            if (ci0.alt_value is not None): 
                                ci0.alt_value = "{0}-{1}".format(ci0.alt_value, num)
                if ((ci0 is None and ((ci.typ == CityItemToken.ItemType.PROPERNAME or ci.typ == CityItemToken.ItemType.CITY)) and t.is_comma) and li[0] == ci): 
                    npt = MiscLocationHelper._try_parse_npt(t.next0_)
                    if (npt is not None): 
                        tt = t.next0_
                        while tt is not None and tt.end_char <= npt.end_char: 
                            ci00 = CityItemToken.try_parse(tt, ci, False, None)
                            if (ci00 is not None and ci00.typ == CityItemToken.ItemType.NOUN): 
                                ci01 = CityItemToken.try_parse(ci00.end_token.next0_, ci, False, None)
                                if (ci01 is None): 
                                    ci0 = ci00
                                    ci0.alt_value = MiscHelper.get_text_value(t.next0_, ci00.end_token, (GetTextAttr.IGNOREARTICLES if t.kit.base_language.is_en else GetTextAttr.FIRSTNOUNGROUPTONOMINATIVESINGLE)).lower()
                                    break
                            if (not tt.chars.is_all_lower): 
                                break
                            tt = tt.next0_
                if (ci0 is None): 
                    break
            if ((ci0.typ == CityItemToken.ItemType.NOUN and ci0.value is not None and LanguageHelper.ends_with(ci0.value, "УСАДЬБА")) and ci.typ == CityItemToken.ItemType.NOUN): 
                ci.doubtful = False
                ci.end_token = ci0.end_token
                t = ci.end_token
                continue
            if (ci0.typ == CityItemToken.ItemType.NOUN and ci.typ == CityItemToken.ItemType.MISC and ci.value == "АДМИНИСТРАЦИЯ"): 
                ci0.doubtful = False
            if (ci.merge_with_next(ci0)): 
                t = ci.end_token
                continue
            ci = ci0
            li.append(ci)
            t = ci.end_token
            if (max_count > 0 and len(li) >= max_count): 
                break
        if (len(li) > 1 and li[0].value == "СОВЕТ"): 
            return None
        if (len(li) > 2 and li[0].typ == CityItemToken.ItemType.NOUN and li[1].typ == CityItemToken.ItemType.NOUN): 
            if (li[0].merge_with_next(li[1])): 
                del li[1]
        if (len(li) > 2 and li[0].is_newline_after): 
            del li[1:1+len(li) - 1]
        if (not li[0].geo_object_before): 
            li[0].geo_object_before = MiscLocationHelper.check_geo_object_before(li[0].begin_token, False)
        if (not li[len(li) - 1].geo_object_after): 
            li[len(li) - 1].geo_object_after = MiscLocationHelper.check_geo_object_after(li[len(li) - 1].end_token, True, False)
        if ((len(li) == 2 and li[0].typ == CityItemToken.ItemType.NOUN and li[1].typ == CityItemToken.ItemType.NOUN) and ((li[0].geo_object_before or li[1].geo_object_after))): 
            if (li[0].chars.is_capital_upper and li[1].chars.is_all_lower): 
                li[0].typ = CityItemToken.ItemType.PROPERNAME
            elif (li[1].chars.is_capital_upper and li[0].chars.is_all_lower): 
                li[1].typ = CityItemToken.ItemType.PROPERNAME
        return li
    
    def __init__(self, begin : 'Token', end : 'Token') -> None:
        super().__init__(begin, end, None)
        self.typ = CityItemToken.ItemType.PROPERNAME
        self.value = None;
        self.alt_value = None;
        self.onto_item = None;
        self.doubtful = False
        self.geo_object_before = False
        self.geo_object_after = False
        self.higher_geo = None;
        self.org_ref = None;
        self.orto_city = None;
        self._cond = None;
    
    def __str__(self) -> str:
        res = io.StringIO()
        if (self._cond is not None): 
            print("[{0}] ".format(str(self._cond)), end="", file=res, flush=True)
        print("{0}".format(Utils.enumToString(self.typ)), end="", file=res, flush=True)
        if (self.value is not None): 
            print(" {0}".format(self.value), end="", file=res, flush=True)
        if (self.onto_item is not None): 
            print(" {0}".format(str(self.onto_item)), end="", file=res, flush=True)
        if (self.doubtful): 
            print(" (?)", end="", file=res)
        if (self.org_ref is not None): 
            print(" (Org: {0})".format(self.org_ref.referent), end="", file=res, flush=True)
        if (self.geo_object_before): 
            print(" GeoBefore", end="", file=res)
        if (self.geo_object_after): 
            print(" GeoAfter", end="", file=res)
        if (self.orto_city is not None): 
            print(" Orto: {0}".format(self.orto_city), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    def merge_with_next(self, ne : 'CityItemToken') -> bool:
        if (self.typ != CityItemToken.ItemType.NOUN or ne.typ != CityItemToken.ItemType.NOUN): 
            return False
        ok = False
        if (self.value == "ГОРОДСКОЕ ПОСЕЛЕНИЕ" and ne.value == "ГОРОД"): 
            ok = True
        if (not ok): 
            return False
        self.end_token = ne.end_token
        self.doubtful = False
        return True
    
    SPEED_REGIME = False
    
    @staticmethod
    def _prepare_all_data(t0 : 'Token') -> None:
        if (not CityItemToken.SPEED_REGIME): 
            return
        ad = GeoAnalyzer._get_data(t0)
        if (ad is None): 
            return
        ad.cregime = False
        t = t0
        while t is not None: 
            d = Utils.asObjectOrNull(t.tag, GeoTokenData)
            cit = CityItemToken.try_parse(t, None, False, ad)
            if (cit is not None): 
                if (d is None): 
                    d = GeoTokenData(t)
                d.cit = cit
            t = t.next0_
        t = t0
        first_pass2877 = True
        while True:
            if first_pass2877: first_pass2877 = False
            else: t = t.next0_
            if (not (t is not None)): break
            d = Utils.asObjectOrNull(t.tag, GeoTokenData)
            if (d is None or d.cit is None or d.cit.typ != CityItemToken.ItemType.NOUN): 
                continue
            tt = d.cit.end_token.next0_
            if (tt is None): 
                continue
            dd = Utils.asObjectOrNull(tt.tag, GeoTokenData)
            if (dd is not None and dd.cit is not None): 
                continue
            cit = CityItemToken.try_parse(tt, d.cit, False, ad)
            if (cit is None): 
                continue
            if (dd is None): 
                dd = GeoTokenData(tt)
            dd.cit = cit
        ad.cregime = True
    
    @staticmethod
    def try_parse(t : 'Token', prev : 'CityItemToken'=None, dont_normalize : bool=False, ad : 'GeoAnalyzerData'=None) -> 'CityItemToken':
        if (t is None): 
            return None
        if (ad is None): 
            ad = GeoAnalyzer._get_data(t)
        if (ad is None): 
            return None
        d = Utils.asObjectOrNull(t.tag, GeoTokenData)
        if (t.is_value("НП", None)): 
            pass
        if (d is not None and d.no_geo): 
            return None
        if (CityItemToken.SPEED_REGIME and ((ad.cregime or ad.all_regime)) and not dont_normalize): 
            if (d is None): 
                return None
            if (d.cit is None): 
                return None
            if (d.cit._cond is not None): 
                if (ad.check_regime): 
                    return None
                ad.check_regime = True
                b = d.cit._cond.check()
                ad.check_regime = False
                if (not b): 
                    return None
            return d.cit
        if (ad.clevel > 1): 
            return None
        ad.clevel += 1
        res = CityItemToken.__try_parse_int(t, prev, dont_normalize, ad)
        ad.clevel -= 1
        if (res is not None and res.typ == CityItemToken.ItemType.NOUN and (res.whitespaces_after_count < 2)): 
            nn = MiscLocationHelper._try_parse_npt(res.end_token.next0_)
            if (nn is not None and ((nn.end_token.is_value("ЗНАЧЕНИЕ", "ЗНАЧЕННЯ") or nn.end_token.is_value("ТИП", None) or nn.end_token.is_value("ХОЗЯЙСТВО", "ХАЗЯЙСТВО")))): 
                if (OrgItemToken.try_parse(res.end_token.next0_, ad) is None): 
                    res.end_token = nn.end_token
            elif ((res.value == "ГОРОДСКОЕ ПОСЕЛЕНИЕ" or res.value == "СЕЛЬСКОЕ ПОСЕЛЕНИЕ")): 
                ad.clevel += 1
                next0__ = CityItemToken.__try_parse_int(res.end_token.next0_, res, dont_normalize, ad)
                ad.clevel -= 1
                if (next0__ is not None and next0__.typ == CityItemToken.ItemType.NOUN): 
                    res.end_token = next0__.end_token
                    res.alt_value = next0__.value
        if (((res is not None and res.typ == CityItemToken.ItemType.PROPERNAME and res.value is not None) and not res.doubtful and res.begin_token == res.end_token) and len(res.value) > 4): 
            if (LanguageHelper.ends_with_ex(res.value, "ГРАД", "ГОРОД", None, None)): 
                res.alt_value = (None)
                res.typ = CityItemToken.ItemType.CITY
            elif (LanguageHelper.ends_with_ex(res.value, "СК", "ИНО", "ПОЛЬ", None) or LanguageHelper.ends_with_ex(res.value, "ВЛЬ", "АС", "ЕС", None)): 
                sits = StreetItemToken.try_parse_list(res.end_token.next0_, 3, ad)
                if (sits is not None): 
                    if (len(sits) == 1 and sits[0].typ == StreetItemType.NOUN): 
                        return res
                    if (len(sits) == 2 and sits[0].typ == StreetItemType.NUMBER and sits[1].typ == StreetItemType.NOUN): 
                        return res
                mc = res.end_token.get_morph_class_in_dictionary()
                if (mc.is_proper_geo or mc.is_undefined): 
                    res.alt_value = (None)
                    res.typ = CityItemToken.ItemType.CITY
            elif (LanguageHelper.ends_with_ex(res.value, "АНЬ", "TOWN", None, None) or res.value.startswith("SAN")): 
                res.typ = CityItemToken.ItemType.CITY
            elif (isinstance(res.end_token, TextToken)): 
                lem = res.end_token.lemma
                if (LanguageHelper.ends_with_ex(lem, "ГРАД", "ГОРОД", "СК", None) or LanguageHelper.ends_with_ex(lem, "АНЬ", "ПОЛЬ", None, None)): 
                    res.alt_value = res.value
                    res.value = lem
                    ii = res.alt_value.find('-')
                    if (ii >= 0): 
                        res.value = (res.alt_value[0:0+ii + 1] + lem)
                    if (not LanguageHelper.ends_with(res.value, "АНЬ")): 
                        res.alt_value = (None)
        if (res is None): 
            return None
        if ((res.typ != CityItemToken.ItemType.NOUN and res.end_token.next0_ is not None and res.end_token.next0_.is_char('(')) and (res.whitespaces_after_count < 3)): 
            br = BracketHelper.try_parse(res.end_token.next0_, BracketParseAttr.NO, 100)
            if (br is not None and br.end_token.next0_ is not None and (br.whitespaces_after_count < 3)): 
                nn = CityItemToken.try_parse(br.end_token.next0_, res, False, None)
                if (nn is not None and nn.typ == CityItemToken.ItemType.NOUN): 
                    li = CityItemToken.try_parse_list(br.begin_token.next0_, 3, ad)
                    if ((li is not None and len(li) == 2 and li[0].typ != CityItemToken.ItemType.NOUN) and li[1].typ == CityItemToken.ItemType.NOUN and li[1].end_token.next0_ == br.end_token): 
                        res.orto_city = CityAttachHelper.try_define(li, ad, True)
                        res.end_token = br.end_token
        return res
    
    @staticmethod
    def __try_parse_int(t : 'Token', prev : 'CityItemToken', dont_normalize : bool, ad : 'GeoAnalyzerData') -> 'CityItemToken':
        from pullenti.ner.geo.internal.TerrItemToken import TerrItemToken
        if (t is None or (((isinstance(t, TextToken)) and not t.chars.is_letter))): 
            return None
        res = CityItemToken.__try_parse(t, prev, dont_normalize, ad)
        if ((prev is None and t.chars.is_cyrillic_letter and t.chars.is_all_upper) and t.length_char == 2): 
            if (t.is_value("ТА", None)): 
                res = CityItemToken.__try_parse(t.next0_, prev, dont_normalize, ad)
                if (res is not None): 
                    if (res.typ == CityItemToken.ItemType.NOUN): 
                        res.begin_token = t
                        res.doubtful = False
                    else: 
                        res = (None)
        if (prev is not None and prev.typ == CityItemToken.ItemType.NOUN and ((prev.value != "ГОРОД" and prev.value != "МІСТО"))): 
            if (res is None): 
                det = OrgItemToken.try_parse(t, None)
                if (det is not None): 
                    cou = 0
                    ttt = det.begin_token
                    while ttt is not None and ttt.end_char <= det.end_char: 
                        if (ttt.chars.is_letter): 
                            cou += 1
                        ttt = ttt.next0_
                    if (cou < 6): 
                        re = CityItemToken._new1074(det.begin_token, det.end_token, CityItemToken.ItemType.PROPERNAME)
                        if (det.referent.type_name == "ORGANIZATION"): 
                            re.org_ref = (det)
                        else: 
                            re.value = MiscHelper.get_text_value_of_meta_token(det, GetTextAttr.NO)
                            re.alt_value = MiscHelper.get_text_value_of_meta_token(det, GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE)
                        return re
                if ((isinstance(t, NumberToken)) and (t.whitespaces_after_count < 2)): 
                    next0__ = CityItemToken.__try_parse(t.next0_, prev, dont_normalize, ad)
                    if ((next0__ is not None and next0__.typ == CityItemToken.ItemType.PROPERNAME and next0__.value is not None) and next0__.end_token.next0_ is not None): 
                        ok = False
                        if (next0__.end_token.next0_.is_comma): 
                            ok = True
                        elif (AddressItemToken.check_street_after(next0__.end_token.next0_, False)): 
                            ok = True
                        if (ok): 
                            next0__.begin_token = t
                            next0__.value = "{0}-{1}".format(next0__.value, t.value)
                            if (next0__.alt_value is not None): 
                                next0__.alt_value = "{0}-{1}".format(next0__.alt_value, t.value)
                            res = next0__
        if (res is not None and res.typ == CityItemToken.ItemType.NOUN and (res.whitespaces_after_count < 3)): 
            npt = MiscLocationHelper._try_parse_npt(res.end_token.next0_)
            if (npt is not None): 
                if (npt.end_token.is_value("ПОДЧИНЕНИЕ", "ПІДПОРЯДКУВАННЯ")): 
                    res.end_token = npt.end_token
            if (res.value == "НАСЕЛЕННЫЙ ПУНКТ"): 
                next0__ = CityItemToken.__try_parse(res.end_token.next0_, prev, dont_normalize, ad)
                if (next0__ is not None and next0__.typ == CityItemToken.ItemType.NOUN): 
                    next0__.begin_token = res.begin_token
                    return next0__
        if (res is not None and t.chars.is_all_upper and res.typ == CityItemToken.ItemType.PROPERNAME): 
            tt = t.previous
            if (tt is not None and tt.is_comma): 
                tt = tt.previous
            geo_prev = None
            if (tt is not None and (isinstance(tt.get_referent(), GeoReferent))): 
                geo_prev = (Utils.asObjectOrNull(tt.get_referent(), GeoReferent))
            if (geo_prev is not None and ((geo_prev.is_region or geo_prev.is_city))): 
                det = OrgItemToken.try_parse(t, None)
                if (det is not None): 
                    res = (None)
        if (res is not None and res.typ == CityItemToken.ItemType.PROPERNAME): 
            if ((t.is_value("ДУМА", "РАДА") or t.is_value("ГЛАВА", "ГОЛОВА") or t.is_value("АДМИНИСТРАЦИЯ", "АДМІНІСТРАЦІЯ")) or t.is_value("МЭР", "МЕР") or t.is_value("ПРЕДСЕДАТЕЛЬ", "ГОЛОВА")): 
                return None
        if (res is not None and res.value == "НАСЕЛЕННЫЙ ПУНКТ" and (res.whitespaces_after_count < 2)): 
            s = StreetItemToken.try_parse(res.end_token.next0_, None, False, None)
            if (s is not None and s.typ == StreetItemType.NOUN and s.termin.canonic_text == "ПОЧТОВОЕ ОТДЕЛЕНИЕ"): 
                res.end_token = s.end_token
        geo_after = None
        if (res is None): 
            if (BracketHelper.can_be_start_of_sequence(t, True, False)): 
                br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
                if (br is not None): 
                    res = CityItemToken.__try_parse(t.next0_, None, False, ad)
                    if (res is not None and ((res.typ == CityItemToken.ItemType.PROPERNAME or res.typ == CityItemToken.ItemType.CITY))): 
                        res.begin_token = t
                        res.typ = CityItemToken.ItemType.PROPERNAME
                        res.end_token = br.end_token
                        if (res.end_token.next0_ != br.end_token): 
                            res.value = MiscHelper.get_text_value(t, br.end_token, GetTextAttr.NO)
                            res.alt_value = (None)
                        return res
            if (isinstance(t, TextToken)): 
                txt = t.term
                if (txt == "НЕТ"): 
                    return None
                if (txt == "ИМ" or txt == "ИМЕНИ"): 
                    t1 = t.next0_
                    if (t1 is not None and t1.is_char('.')): 
                        t1 = t1.next0_
                    res = CityItemToken.__try_parse(t1, None, False, ad)
                    if (res is not None and ((((res.typ == CityItemToken.ItemType.CITY and res.doubtful)) or res.typ == CityItemToken.ItemType.PROPERNAME))): 
                        res.begin_token = t
                        res.morph = MorphCollection()
                        return res
                if (t.chars.is_cyrillic_letter and t.length_char == 1 and t.chars.is_all_upper): 
                    if ((t.next0_ is not None and not t.is_whitespace_after and ((t.next0_.is_hiphen or t.next0_.is_char('.')))) and (t.next0_.whitespaces_after_count < 2)): 
                        if (prev is not None and prev.typ == CityItemToken.ItemType.NOUN and (((not prev.doubtful or prev.geo_object_before or MiscLocationHelper.check_geo_object_before(prev.begin_token, False)) or MiscLocationHelper.check_geo_object_before_brief(prev.begin_token, ad)))): 
                            res1 = CityItemToken.__try_parse(t.next0_.next0_, None, False, ad)
                            if (res1 is not None and ((res1.typ == CityItemToken.ItemType.PROPERNAME or res1.typ == CityItemToken.ItemType.CITY))): 
                                adjs = MiscLocationHelper.get_std_adj_full_str(txt, res1.morph.gender, res1.morph.number, True)
                                if (adjs is None and prev is not None and prev.typ == CityItemToken.ItemType.NOUN): 
                                    adjs = MiscLocationHelper.get_std_adj_full_str(txt, prev.morph.gender, MorphNumber.UNDEFINED, True)
                                if (adjs is None): 
                                    adjs = MiscLocationHelper.get_std_adj_full_str(txt, res1.morph.gender, res1.morph.number, False)
                                if (adjs is not None): 
                                    if (res1.value is None): 
                                        res1.value = res1.get_source_text().upper()
                                    if (res1.alt_value is not None): 
                                        res1.alt_value = "{0} {1}".format(adjs[0], res1.alt_value)
                                    elif (len(adjs) > 1): 
                                        res1.alt_value = "{0} {1}".format(adjs[1], res1.value)
                                    res1.value = "{0} {1}".format(adjs[0], res1.value)
                                    res1.begin_token = t
                                    res1.typ = CityItemToken.ItemType.PROPERNAME
                                    return res1
            tt = (t.previous if prev is None else prev.begin_token.previous)
            while tt is not None and tt.is_char_of(",."):
                tt = tt.previous
            geo_prev = None
            if (tt is not None and (isinstance(tt.get_referent(), GeoReferent))): 
                geo_prev = (Utils.asObjectOrNull(tt.get_referent(), GeoReferent))
            cond = None
            tt0 = t
            ooo = False
            has_geo_after = False
            if (geo_prev is not None): 
                ooo = True
            elif (MiscLocationHelper.check_near_before(t, ad) is not None): 
                ooo = True
            elif (MiscLocationHelper.check_geo_object_before(t, False)): 
                ooo = True
            elif (t.chars.is_letter): 
                tt = t.next0_
                if (tt is not None and tt.is_char('.')): 
                    tt = tt.next0_
                if ((isinstance(tt, TextToken)) and not tt.chars.is_all_lower): 
                    if (MiscLocationHelper.check_geo_object_after_brief(tt, ad)): 
                        has_geo_after = True
                        ooo = has_geo_after
                    elif (MiscLocationHelper.check_geo_object_after(tt, True, False)): 
                        has_geo_after = True
                        ooo = has_geo_after
                    elif (AddressItemToken.check_street_after(tt.next0_, False)): 
                        ooo = True
                    elif (ad.clevel == 0): 
                        cit2 = CityItemToken.try_parse(tt, None, False, ad)
                        if (cit2 is not None and cit2.begin_token != cit2.end_token and ((cit2.typ == CityItemToken.ItemType.PROPERNAME or cit2.typ == CityItemToken.ItemType.CITY))): 
                            if (AddressItemToken.check_street_after(cit2.end_token.next0_, False)): 
                                ooo = True
                        if (cit2 is not None and cit2.typ == CityItemToken.ItemType.CITY and tt.previous.is_char('.')): 
                            if (cit2.is_whitespace_after or ((cit2.end_token.next0_ is not None and cit2.end_token.next0_.length_char == 1))): 
                                ooo = True
                                if (cit2.onto_item is not None): 
                                    geo_after = (Utils.asObjectOrNull(cit2.onto_item.referent, GeoReferent))
            if ((ad is not None and not ooo and not ad.cregime) and CityItemToken.SPEED_REGIME): 
                if (cond is None): 
                    cond = Condition()
                cond.geo_before_token = t
                ooo = True
            if (ooo): 
                tt = t
                ttt = tt
                first_pass2878 = True
                while True:
                    if first_pass2878: first_pass2878 = False
                    else: ttt = ttt.next0_
                    if (not (ttt is not None)): break
                    if (ttt.is_char_of(",.")): 
                        tt = ttt.next0_
                        continue
                    if (ttt.is_newline_before): 
                        break
                    det = AddressItemToken.try_parse_pure_item(ttt, None, ad)
                    if (det is not None and det.typ == AddressItemType.DETAIL): 
                        ttt = det.end_token
                        tt0 = det.end_token.next0_
                        tt = tt0
                        continue
                    org0_ = OrgItemToken.try_parse(ttt, None)
                    if (org0_ is not None and org0_.is_gsk): 
                        ttt = org0_.end_token
                        tt = org0_.end_token.next0_
                        tt0 = tt
                        continue
                    ait = AddressItemToken.try_parse_pure_item(ttt, None, None)
                    if (ait is not None and ait.typ == AddressItemType.PLOT): 
                        ttt = ait.end_token
                        tt = ait.end_token.next0_
                        tt0 = tt
                        continue
                    break
                if (isinstance(tt, TextToken)): 
                    if (tt0.is_comma and tt0.next0_ is not None): 
                        tt0 = tt0.next0_
                    txt = tt.term
                    if ((((txt == "Д" or txt == "С" or txt == "C") or txt == "П" or txt == "Х")) and ((tt.chars.is_all_lower or MiscLocationHelper.is_user_param_address(tt) or ((tt.next0_ is not None and tt.next0_.is_char_of(".,")))))): 
                        tt1 = tt
                        if (tt1.next0_ is not None and tt1.next0_.is_char_of(",.")): 
                            tt1 = tt1.next0_
                        elif (txt == "С" and tt1.next0_ is not None and ((tt1.next0_.morph.case_.is_instrumental or tt1.next0_.morph.case_.is_genitive))): 
                            if (not (isinstance(tt1.next0_, TextToken))): 
                                return None
                            if (MiscLocationHelper.is_user_param_address(tt1)): 
                                pass
                            else: 
                                if (not tt.chars.is_all_lower or not tt1.next0_.chars.is_capital_upper): 
                                    return None
                                if (tt1.next0_.is_newline_after): 
                                    pass
                                elif (AddressItemToken.check_street_after(tt1.next0_.next0_, False)): 
                                    pass
                                else: 
                                    return None
                        tt2 = tt1.next0_
                        if ((tt2 is not None and tt2.length_char == 1 and tt2.chars.is_cyrillic_letter) and tt2.chars.is_all_upper): 
                            if (tt2.next0_ is not None and ((tt2.next0_.is_char('.') or tt2.next0_.is_hiphen)) and not tt2.is_whitespace_after): 
                                if (tt.chars.is_all_upper): 
                                    return None
                                tt2 = tt2.next0_.next0_
                        else: 
                            while tt2 is not None and tt2.is_comma:
                                tt2 = tt2.next0_
                        ok = False
                        if ((txt == "Д" and (isinstance(tt2, NumberToken)) and not tt2.is_newline_before) and not tt2.previous.is_comma): 
                            ok = False
                        elif (((txt == "С" or txt == "C")) and (isinstance(tt2, TextToken)) and ((tt2.is_value("О", None) or tt2.is_value("O", None)))): 
                            ok = False
                        elif (tt2 is None or tt2.is_value("ДОМ", None)): 
                            ok = True
                        elif (not tt2.chars.is_cyrillic_letter and (isinstance(tt2, TextToken))): 
                            ok = False
                        elif (tt2.is_newline_before and tt2.previous.is_comma): 
                            ok = True
                        elif (tt2.chars.is_capital_upper and (tt2.whitespaces_before_count < 2)): 
                            ok = tt.chars.is_all_lower
                        elif (AddressItemToken.check_street_after(tt2, False)): 
                            ok = True
                        elif (AddressItemToken.check_house_after(tt2, False, True)): 
                            ok = True
                        elif (tt2.chars.is_all_upper and (tt2.whitespaces_before_count < 2)): 
                            ok = True
                            if (tt.chars.is_all_upper): 
                                rtt = tt.kit.process_referent("PERSON", tt, None)
                                if (rtt is not None): 
                                    ok = False
                                    ttt2 = rtt.end_token.next0_
                                    if (ttt2 is not None and ttt2.is_comma): 
                                        ttt2 = ttt2.next0_
                                    if (AddressItemToken.check_house_after(ttt2, False, False) or AddressItemToken.check_street_after(ttt2, False)): 
                                        ok = True
                                elif (tt.previous is not None and tt.previous.is_char('.')): 
                                    ok = False
                            elif (tt1 == tt): 
                                ok = False
                            if (not ok and tt1.next0_ is not None): 
                                ttt2 = tt1.next0_.next0_
                                if (ttt2 is not None and ttt2.is_comma): 
                                    ttt2 = ttt2.next0_
                                if (AddressItemToken.check_house_after(ttt2, False, False) or AddressItemToken.check_street_after(ttt2, False)): 
                                    if (OrgItemToken.try_parse(tt1.next0_, None) is not None): 
                                        pass
                                    else: 
                                        ok = True
                        elif ((isinstance(tt2, NumberToken)) and tt2.previous.is_comma): 
                            ok = True
                        elif (prev is not None and prev.typ == CityItemToken.ItemType.PROPERNAME and (tt.whitespaces_before_count < 2)): 
                            if (MiscLocationHelper.check_geo_object_before(prev.begin_token.previous, False)): 
                                ok = True
                            if (txt == "П" and tt.next0_ is not None and ((tt.next0_.is_hiphen or tt.next0_.is_char_of("\\/")))): 
                                sit = StreetItemToken.try_parse(tt, None, False, None)
                                if (sit is not None and sit.typ == StreetItemType.NOUN): 
                                    ok = False
                        elif (prev is None): 
                            if (MiscLocationHelper.check_geo_object_before(tt.previous, False)): 
                                if (tt1.is_newline_after): 
                                    pass
                                else: 
                                    ok = True
                            elif (geo_after is not None or has_geo_after): 
                                ok = True
                            elif (MiscLocationHelper.is_user_param_address(tt)): 
                                ok = True
                        if (tt.previous is not None and tt.previous.is_hiphen and not tt.is_whitespace_before): 
                            if (tt.next0_ is not None and tt.next0_.is_char('.')): 
                                pass
                            else: 
                                ok = False
                        if (ok): 
                            ii = 0
                            ttt = t.previous
                            while ttt is not None and (ii < 4): 
                                oo = OrgItemToken.try_parse(ttt, None)
                                if (oo is not None and oo.end_char > tt.end_char): 
                                    ok = False
                                ttt = ttt.previous; ii += 1
                        if (ok): 
                            res = CityItemToken._new1074(tt0, tt1, CityItemToken.ItemType.NOUN)
                            if (tt1.is_comma): 
                                res.end_token = tt1.previous
                            res.value = ("ДЕРЕВНЯ" if txt == "Д" else (("ПОСЕЛОК" if txt == "П" else (("ХУТОР" if txt == "Х" else "СЕЛО")))))
                            if (txt == "П"): 
                                res.alt_value = "ПОСЕЛЕНИЕ"
                            elif (txt == "С" or txt == "C"): 
                                res.alt_value = "СЕЛЕНИЕ"
                                if (tt0 == tt1): 
                                    npt = NounPhraseHelper.try_parse(tt1.next0_, NounPhraseParseAttr.PARSEPRONOUNS, 0, None)
                                    if (npt is not None and npt.morph.case_.is_instrumental): 
                                        return None
                            res.doubtful = True
                            return res
                    if ((txt == "СП" or txt == "РП" or txt == "ГП") or txt == "ДП"): 
                        if (tt.next0_ is not None and tt.next0_.is_char('.')): 
                            tt = tt.next0_
                        if (tt.next0_ is not None and tt.next0_.chars.is_capital_upper): 
                            return CityItemToken._new1078(tt0, tt, CityItemToken.ItemType.NOUN, True, Condition._new1077(t), ("РАБОЧИЙ ПОСЕЛОК" if txt == "РП" else (("ГОРОДСКОЕ ПОСЕЛЕНИЕ" if txt == "ГП" else (("ДАЧНЫЙ ПОСЕЛОК" if txt == "ДП" else "СЕЛЬСКОЕ ПОСЕЛЕНИЕ"))))))
                    if (tt0 != tt and CityItemToken.check_keyword(tt) is not None): 
                        res = CityItemToken.try_parse(tt, None, False, ad)
                        if (res is not None and res.typ == CityItemToken.ItemType.NOUN): 
                            res.geo_object_before = True
                            res.begin_token = tt0
                            return res
                    if (tt.chars.is_all_upper and tt.length_char > 2 and tt.chars.is_cyrillic_letter): 
                        return CityItemToken._new1079(tt, tt, CityItemToken.ItemType.PROPERNAME, tt.term)
            if ((isinstance(t, NumberToken)) and t.next0_ is not None): 
                net = NumberHelper.try_parse_number_with_postfix(t)
                if (net is not None and net.ex_typ == NumberExType.KILOMETER): 
                    return CityItemToken._new1079(t, net.end_token, CityItemToken.ItemType.PROPERNAME, "{0}КМ".format(math.floor(net.real_value)))
            rt = Utils.asObjectOrNull(t, ReferentToken)
            if ((rt is not None and (isinstance(rt.referent, GeoReferent)) and rt.begin_token == rt.end_token) and rt.referent.is_state): 
                if (t.previous is None): 
                    return None
                if (t.previous.morph.number == MorphNumber.SINGULAR and t.morph.case_.is_nominative and not t.morph.case_.is_genitive): 
                    return CityItemToken._new1079(t, t, CityItemToken.ItemType.PROPERNAME, rt.get_source_text().upper())
            return None
        if (res.typ == CityItemToken.ItemType.NOUN): 
            if (res.value == "СЕЛО" and (isinstance(t, TextToken))): 
                if (t.previous is None): 
                    pass
                elif (t.previous.morph.class0_.is_preposition): 
                    pass
                else: 
                    res.doubtful = True
                res.morph.gender = MorphGender.NEUTER
            if (LanguageHelper.ends_with(res.value, "УСАДЬБА") and res.alt_value is None): 
                res.alt_value = "НАСЕЛЕННЫЙ ПУНКТ"
            if (res.value == "СТАНЦИЯ" or res.value == "СТАНЦІЯ"): 
                res.doubtful = True
            if (res.end_token.is_value("СТОЛИЦА", None) or res.end_token.is_value("СТОЛИЦЯ", None)): 
                res.doubtful = True
                if (res.end_token.next0_ is not None): 
                    geo_ = Utils.asObjectOrNull(res.end_token.next0_.get_referent(), GeoReferent)
                    if (geo_ is not None and ((geo_.is_region or geo_.is_state))): 
                        res.higher_geo = geo_
                        res.end_token = res.end_token.next0_
                        res.doubtful = False
                        res.value = "ГОРОД"
                        for it in TerrItemToken._m_capitals_by_state.termins: 
                            ge = Utils.asObjectOrNull(it.tag, GeoReferent)
                            if (ge is None or not ge.can_be_equals(geo_, ReferentsEqualType.WITHINONETEXT)): 
                                continue
                            tok = TerrItemToken._m_capitals_by_state.try_parse(res.end_token.next0_, TerminParseAttr.NO)
                            if (tok is not None and tok.termin == it): 
                                break
                            res.typ = CityItemToken.ItemType.CITY
                            res.value = it.canonic_text
                            return res
            if ((res.begin_token.length_char == 1 and res.begin_token.chars.is_all_upper and res.begin_token.next0_ is not None) and res.begin_token.next0_.is_char('.')): 
                ne = CityItemToken.__try_parse_int(res.begin_token.next0_.next0_, None, False, ad)
                if (ne is not None and ne.typ == CityItemToken.ItemType.CITY and not ne.doubtful): 
                    pass
                elif (ne is not None and ne.typ == CityItemToken.ItemType.PROPERNAME and ((LanguageHelper.ends_with_ex(ne.value, "К", "О", None, None) or AddressItemToken.check_street_after(ne.end_token.next0_, False)))): 
                    pass
                elif (ne is None or ne.typ != CityItemToken.ItemType.PROPERNAME): 
                    return None
                elif (MiscLocationHelper.check_geo_object_after(ne.end_token.next0_, False, True)): 
                    pass
                else: 
                    return None
        if (res.typ == CityItemToken.ItemType.PROPERNAME or res.typ == CityItemToken.ItemType.CITY): 
            val = Utils.ifNotNull(res.value, ((None if res.onto_item is None else res.onto_item.canonic_text)))
            t1 = res.end_token
            if (((not t1.is_whitespace_after and t1.next0_ is not None and t1.next0_.is_hiphen) and not t1.next0_.is_whitespace_after and (isinstance(t1.next0_.next0_, NumberToken))) and t1.next0_.next0_.int_value is not None and (t1.next0_.next0_.int_value < 30)): 
                res.end_token = t1.next0_.next0_
                res.value = "{0}-{1}".format(val, t1.next0_.next0_.value)
                if (res.alt_value is not None): 
                    res.alt_value = "{0}-{1}".format(res.alt_value, t1.next0_.next0_.value)
                res.typ = CityItemToken.ItemType.PROPERNAME
            elif (t1.whitespaces_after_count == 1 and (isinstance(t1.next0_, NumberToken)) and t1.next0_.morph.class0_.is_adjective): 
                ok = False
                if (t1.next0_.next0_ is None or t1.next0_.is_newline_after): 
                    ok = True
                elif (not t1.next0_.is_whitespace_after and t1.next0_.next0_ is not None and t1.next0_.next0_.is_char_of(",")): 
                    ok = True
                elif (StreetItemToken.check_keyword(t1.next0_.next0_) and t1.whitespaces_after_count <= t1.next0_.whitespaces_after_count): 
                    if (AddressItemToken.check_street_after(t1.next0_.next0_, False)): 
                        ok = True
                elif (AddressItemToken.check_house_after(t1.next0_.next0_, False, False)): 
                    ok = True
                if (ok): 
                    res.end_token = t1.next0_
                    res.value = "{0}-{1}".format(val, t1.next0_.value)
                    if (res.alt_value is not None): 
                        res.alt_value = "{0}-{1}".format(res.alt_value, t1.next0_.value)
                    res.typ = CityItemToken.ItemType.PROPERNAME
        if (res.typ == CityItemToken.ItemType.CITY and res.begin_token == res.end_token): 
            if (res.begin_token.get_morph_class_in_dictionary().is_adjective and (isinstance(res.end_token.next0_, TextToken))): 
                ok = False
                t1 = None
                npt = MiscLocationHelper._try_parse_npt(res.begin_token)
                if (npt is not None and npt.end_token == res.end_token.next0_): 
                    t1 = npt.end_token
                    mc = t1.get_morph_class_in_dictionary()
                    if (mc.is_noun): 
                        if (res.end_token.next0_.chars.equals(res.begin_token.chars)): 
                            ok = True
                            if (res.begin_token.chars.is_all_upper): 
                                cii = CityItemToken.__try_parse_int(res.end_token.next0_, None, dont_normalize, ad)
                                if (cii is not None and cii.typ == CityItemToken.ItemType.NOUN): 
                                    ok = False
                        elif (res.end_token.next0_.chars.is_all_lower): 
                            ttt = res.end_token.next0_.next0_
                            if (ttt is None or ttt.is_char_of(",.")): 
                                ok = True
                elif (res.end_token.next0_.chars.equals(res.begin_token.chars) and res.begin_token.chars.is_capital_upper): 
                    ttt = res.end_token.next0_.next0_
                    if (ttt is None or ttt.is_char_of(",.")): 
                        ok = True
                    t1 = res.end_token.next0_
                    npt = (None)
                if (ok and t1 is not None): 
                    res.typ = CityItemToken.ItemType.PROPERNAME
                    res.onto_item = (None)
                    res.end_token = t1
                    if (npt is not None): 
                        res.value = npt.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False)
                        res.morph = npt.morph
                    else: 
                        res.value = MiscHelper.get_text_value(res.begin_token, res.end_token, GetTextAttr.NO)
            if ((res.end_token.next0_ is not None and res.end_token.next0_.is_hiphen and not res.end_token.next0_.is_whitespace_after) and not res.end_token.next0_.is_whitespace_before): 
                res1 = CityItemToken.__try_parse(res.end_token.next0_.next0_, None, False, ad)
                if ((res1 is not None and res1.typ == CityItemToken.ItemType.PROPERNAME and res1.begin_token == res1.end_token) and res1.begin_token.chars.equals(res.begin_token.chars)): 
                    if (res1.onto_item is None and res.onto_item is None): 
                        res.typ = CityItemToken.ItemType.PROPERNAME
                        res.value = "{0}-{1}".format((res.value if res.onto_item is None else res.onto_item.canonic_text), res1.value)
                        if (res.alt_value is not None): 
                            res.alt_value = "{0}-{1}".format(res.alt_value, res1.value)
                        res.onto_item = (None)
                        res.end_token = res1.end_token
                        res.doubtful = False
                elif ((isinstance(res.end_token.next0_.next0_, NumberToken)) and res.end_token.next0_.next0_.int_value is not None and (res.end_token.next0_.next0_.int_value < 30)): 
                    res.typ = CityItemToken.ItemType.PROPERNAME
                    res.value = "{0}-{1}".format((res.value if res.onto_item is None else res.onto_item.canonic_text), res.end_token.next0_.next0_.value)
                    if (res.alt_value is not None): 
                        res.alt_value = "{0}-{1}".format(res.alt_value, res.end_token.next0_.next0_.value)
                    res.onto_item = (None)
                    res.end_token = res.end_token.next0_.next0_
            elif (res.begin_token.get_morph_class_in_dictionary().is_proper_name): 
                if (res.begin_token.is_value("КИЇВ", None) or res.begin_token.is_value("АСТАНА", None) or res.begin_token.is_value("АЛМАТЫ", None)): 
                    pass
                elif ((isinstance(res.end_token, TextToken)) and LanguageHelper.ends_with(res.end_token.term, "ВО")): 
                    pass
                else: 
                    res.doubtful = True
                    tt = res.begin_token.previous
                    if (tt is not None and tt.previous is not None): 
                        if (tt.is_char(',') or tt.morph.class0_.is_conjunction): 
                            geo_ = Utils.asObjectOrNull(tt.previous.get_referent(), GeoReferent)
                            if (geo_ is not None and geo_.is_city): 
                                res.doubtful = False
                    if (tt is not None and tt.is_value("В", None) and tt.chars.is_all_lower): 
                        npt1 = MiscLocationHelper._try_parse_npt(res.begin_token)
                        if (npt1 is None or npt1.end_char <= res.end_char): 
                            res.doubtful = False
            if ((res.begin_token == res.end_token and res.typ == CityItemToken.ItemType.CITY and res.onto_item is not None) and res.onto_item.canonic_text == "САНКТ - ПЕТЕРБУРГ"): 
                tt = res.begin_token.previous
                first_pass2879 = True
                while True:
                    if first_pass2879: first_pass2879 = False
                    else: tt = tt.previous
                    if (not (tt is not None)): break
                    if (tt.is_hiphen or tt.is_char('.')): 
                        continue
                    if (tt.is_value("С", None) or tt.is_value("C", None) or tt.is_value("САНКТ", None)): 
                        res.begin_token = tt
                    break
        if ((res.begin_token == res.end_token and res.typ == CityItemToken.ItemType.PROPERNAME and res.whitespaces_after_count == 1) and (isinstance(res.end_token.next0_, TextToken)) and res.end_token.chars.equals(res.end_token.next0_.chars)): 
            ok = False
            t1 = res.end_token
            if (t1.next0_.next0_ is None or t1.next0_.is_newline_after): 
                ok = True
            elif (not t1.next0_.is_whitespace_after and t1.next0_.next0_ is not None and t1.next0_.next0_.is_char_of(",.")): 
                ok = True
            if (ok): 
                pp = CityItemToken.__try_parse(t1.next0_, None, False, ad)
                if (pp is not None and pp.typ == CityItemToken.ItemType.NOUN): 
                    ok = False
                if (ok): 
                    te = TerrItemToken.try_parse(t1.next0_, None, None)
                    if (te is not None): 
                        if (te.termin_item is not None): 
                            ok = False
                        elif (te.onto_item is not None and not te.morph.case_.is_genitive): 
                            ok = False
                    if (ok): 
                        if (StreetItemToken.check_keyword(t1.next0_)): 
                            ok = False
            if (ok): 
                res.end_token = t1.next0_
                res.value = MiscHelper.get_text_value(res.begin_token, res.end_token, GetTextAttr.NO)
                res.alt_value = (None)
                res.typ = CityItemToken.ItemType.PROPERNAME
        return res
    
    @staticmethod
    def __try_parse(t : 'Token', prev : 'CityItemToken', dont_normalize : bool, ad : 'GeoAnalyzerData') -> 'CityItemToken':
        from pullenti.ner.geo.internal.TerrItemToken import TerrItemToken
        if (not (isinstance(t, TextToken))): 
            if ((isinstance(t, ReferentToken)) and (isinstance(t.get_referent(), DateReferent))): 
                aii = StreetItemToken._try_parse_spec(t, None)
                if (aii is not None): 
                    if (len(aii) > 1 and aii[0].typ == StreetItemType.NUMBER and aii[1].typ == StreetItemType.STDNAME): 
                        res2 = CityItemToken._new1074(t, aii[1].end_token, CityItemToken.ItemType.PROPERNAME)
                        res2.value = "{0} {1}".format((aii[0].value if aii[0].number is None else str(aii[0].number.int_value)), aii[1].value)
                        return res2
            if ((((isinstance(t, NumberToken)) and prev is not None and prev.typ == CityItemToken.ItemType.NOUN) and (t.whitespaces_before_count < 3) and (t.whitespaces_after_count < 3)) and (isinstance(t.next0_, TextToken)) and t.next0_.chars.is_capital_upper): 
                if (prev.begin_token.is_value("СТ", None) or prev.begin_token.is_value("П", None)): 
                    return None
                cit1 = CityItemToken.try_parse(t.next0_, None, False, ad)
                if (cit1 is not None and cit1.typ == CityItemToken.ItemType.PROPERNAME and cit1.value is not None): 
                    cit1.begin_token = t
                    cit1.value = "{0}-{1}".format(cit1.value, t.value)
                    return cit1
            return None
        spec = CityItemToken.__try_parse_spec(t)
        if (spec is not None): 
            return spec
        li = None
        li0 = None
        is_in_loc_onto = False
        if (t.kit.ontology is not None and li is None): 
            li0 = t.kit.ontology.attach_token(GeoReferent.OBJ_TYPENAME, t)
            if ((li0) is not None): 
                li = li0
                is_in_loc_onto = True
        if (li is None): 
            li = CityItemToken.M_ONTOLOGY.try_attach(t, None, False)
            if (li is None): 
                li = CityItemToken.M_ONTOLOGY_EX.try_attach(t, None, False)
        elif (prev is None): 
            stri = StreetItemToken.try_parse(t.previous, None, False, ad)
            if (stri is not None and stri.typ == StreetItemType.NOUN): 
                return None
            stri = StreetItemToken.try_parse(li[0].end_token.next0_, None, False, ad)
            if (stri is not None and stri.typ == StreetItemType.NOUN): 
                return None
        if (li is not None and len(li) > 0): 
            if (isinstance(t, TextToken)): 
                for i in range(len(li) - 1, -1, -1):
                    if (li[i].item is not None): 
                        g = Utils.asObjectOrNull(li[i].item.referent, GeoReferent)
                        if (g is not None): 
                            if (not g.is_city): 
                                del li[i]
                                continue
                tt = Utils.asObjectOrNull(t, TextToken)
                for nt in li: 
                    if (nt.item is not None and nt.item.canonic_text == tt.term): 
                        if (MiscLocationHelper.is_user_param_address(nt) or not MiscHelper.is_all_characters_lower(nt.begin_token, nt.end_token, False)): 
                            ci = CityItemToken._new1083(nt.begin_token, nt.end_token, CityItemToken.ItemType.CITY, nt.item, nt.morph)
                            if (nt.begin_token == nt.end_token and not is_in_loc_onto): 
                                ci.doubtful = CityItemToken.__check_doubtful(Utils.asObjectOrNull(nt.begin_token, TextToken))
                            tt1 = nt.end_token.next0_
                            if ((((tt1 is not None and tt1.is_hiphen and not tt1.is_whitespace_before) and not tt1.is_whitespace_after and prev is not None) and prev.typ == CityItemToken.ItemType.NOUN and (isinstance(tt1.next0_, TextToken))) and tt1.previous.chars.equals(tt1.next0_.chars)): 
                                li = (None)
                                break
                            return ci
                if (li is not None): 
                    for nt in li: 
                        if (nt.item is not None): 
                            if (not MiscHelper.is_all_characters_lower(nt.begin_token, nt.end_token, False)): 
                                ci = CityItemToken._new1083(nt.begin_token, nt.end_token, CityItemToken.ItemType.CITY, nt.item, nt.morph)
                                if (nt.begin_token == nt.end_token and (isinstance(nt.begin_token, TextToken))): 
                                    ci.doubtful = CityItemToken.__check_doubtful(Utils.asObjectOrNull(nt.begin_token, TextToken))
                                    str0_ = nt.begin_token.term
                                    if (str0_ != nt.item.canonic_text): 
                                        if (LanguageHelper.ends_with_ex(str0_, "О", "А", None, None)): 
                                            ci.alt_value = str0_
                                return ci
            if (li is not None): 
                for nt in li: 
                    if (nt.item is None): 
                        ty = (CityItemToken.ItemType.NOUN if nt.termin.tag is None else Utils.valToEnum(nt.termin.tag, CityItemToken.ItemType))
                        ci = CityItemToken._new1085(nt.begin_token, nt.end_token, ty, nt.morph)
                        ci.value = nt.termin.canonic_text
                        if (ty == CityItemToken.ItemType.MISC and ci.value == "ЖИТЕЛЬ" and t.previous is not None): 
                            if (t.previous.is_value("МЕСТНЫЙ", "МІСЦЕВИЙ")): 
                                return None
                            if (t.previous.morph.class0_.is_pronoun): 
                                return None
                        if (ty == CityItemToken.ItemType.NOUN and not t.chars.is_all_lower): 
                            if (t.morph.class0_.is_proper_surname): 
                                ci.doubtful = True
                        if (nt.begin_token == nt.end_token): 
                            if (t.is_value("СТ", None)): 
                                if (OrgItemToken.try_parse(t, None) is not None): 
                                    return None
                        if (nt.begin_token.kit.base_language.is_ua): 
                            if (nt.begin_token.is_value("М", None) or nt.begin_token.is_value("Г", None)): 
                                if (not nt.begin_token.chars.is_all_lower): 
                                    return None
                                ci.doubtful = True
                            elif (nt.begin_token.is_value("МІС", None)): 
                                if (t.term != "МІС"): 
                                    return None
                                ci.doubtful = True
                        if (nt.begin_token.kit.base_language.is_ru): 
                            if (nt.begin_token.is_value("Г", None) and not MiscLocationHelper.is_user_param_address(nt)): 
                                if (nt.begin_token.previous is not None and nt.begin_token.previous.morph.class0_.is_preposition): 
                                    pass
                                else: 
                                    ok = True
                                    if (not nt.begin_token.chars.is_all_lower): 
                                        ok = False
                                    elif ((nt.end_token == nt.begin_token and nt.end_token.next0_ is not None and not nt.end_token.is_whitespace_after) and ((nt.end_token.next0_.is_char_of("\\/") or nt.end_token.next0_.is_hiphen))): 
                                        ok = False
                                    elif (not t.is_whitespace_before and t.previous is not None and ((t.previous.is_char_of("\\/") or t.previous.is_hiphen))): 
                                        return None
                                    if (not ok): 
                                        nex = CityItemToken.try_parse(nt.end_token.next0_, None, False, None)
                                        if (nex is not None and nex.typ == CityItemToken.ItemType.CITY and (nt.end_token.whitespaces_after_count < 4)): 
                                            pass
                                        elif (nt.end_token.next0_ is not None and AddressItemToken.check_street_after(nt.end_token.next0_.next0_, False)): 
                                            pass
                                        else: 
                                            if (nex is None or nex.typ != CityItemToken.ItemType.PROPERNAME): 
                                                return None
                                            if (AddressItemToken.check_street_after(nex.end_token.next0_, False)): 
                                                pass
                                            elif (MiscLocationHelper.check_geo_object_after(nex.end_token, False, True)): 
                                                pass
                                            else: 
                                                return None
                                ci.doubtful = True
                            elif (nt.begin_token.is_value("ГОР", None)): 
                                if (t.term != "ГОР"): 
                                    if (t.chars.is_capital_upper): 
                                        ci = (None)
                                        break
                                    return None
                                ci.doubtful = True
                            elif (nt.begin_token.is_value("ПОС", None)): 
                                if (t.term != "ПОС"): 
                                    return None
                                ci.doubtful = True
                                ci.alt_value = "ПОСЕЛЕНИЕ"
                        npt1 = MiscLocationHelper._try_parse_npt(t.previous)
                        if (npt1 is not None and len(npt1.adjectives) > 0): 
                            s = npt1.adjectives[0].get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False)
                            if ((s == "РОДНОЙ" or s == "ЛЮБИМЫЙ" or s == "РІДНИЙ") or s == "КОХАНИЙ"): 
                                return None
                        if (t.is_value("ПОСЕЛЕНИЕ", None)): 
                            if (t.next0_ is not None and t.next0_.is_value("СТАНЦИЯ", None)): 
                                ci1 = CityItemToken.try_parse(t.next0_.next0_, None, False, None)
                                if (ci1 is not None and ((ci1.typ == CityItemToken.ItemType.PROPERNAME or ci1.typ == CityItemToken.ItemType.CITY))): 
                                    ci.end_token = t.next0_
                        if ((ci.length_char < 3) and ci.end_token.next0_ is not None and ci.end_token.next0_.is_char('.')): 
                            ci.end_token = ci.end_token.next0_
                        return ci
        if (not (isinstance(t, TextToken))): 
            return None
        if (t.term == "СПБ" and not t.chars.is_all_lower and CityItemToken.M_ST_PETERBURG is not None): 
            return CityItemToken._new1086(t, t, CityItemToken.ItemType.CITY, CityItemToken.M_ST_PETERBURG, CityItemToken.M_ST_PETERBURG.canonic_text)
        if (t.term == "НЕТ"): 
            return None
        if (t.chars.is_all_lower): 
            if (t.length_char < 4): 
                return None
            if (not MiscLocationHelper.is_user_param_address(t)): 
                return None
            if (StreetItemToken.check_keyword(t)): 
                return None
            if (t.previous is not None and t.previous.is_comma): 
                pass
            elif (prev is not None and prev.typ == CityItemToken.ItemType.NOUN): 
                pass
            else: 
                return None
        stds = CityItemToken.M_STD_ADJECTIVES.try_attach(t, None, False)
        if (stds is not None): 
            cit = CityItemToken.try_parse(stds[0].end_token.next0_, None, False, ad)
            if (cit is not None and ((((cit.typ == CityItemToken.ItemType.PROPERNAME and cit.value is not None)) or cit.typ == CityItemToken.ItemType.CITY))): 
                adj = stds[0].termin.canonic_text
                if (stds[0].end_token.is_value(adj, None) or MiscLocationHelper.is_user_param_address(t)): 
                    adj = MiscHelper.get_text_value_of_meta_token(stds[0], GetTextAttr.NO)
                cit.value = "{0} {1}".format(adj, Utils.ifNotNull(cit.value, (cit.onto_item.canonic_text if cit is not None and cit.onto_item is not None else None)))
                if (cit.alt_value is not None): 
                    cit.alt_value = "{0} {1}".format(adj, cit.alt_value)
                cit.begin_token = t
                npt0 = MiscLocationHelper._try_parse_npt(t)
                if (npt0 is not None and npt0.end_token == cit.end_token): 
                    if (npt0.end_token.morph.contains_attr("кач.прил.", None) or MiscLocationHelper.is_user_param_address(t)): 
                        pass
                    else: 
                        cit.morph = npt0.morph
                        cit.alt_value = cit.value
                        cit.value = npt0.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False)
                cit.typ = CityItemToken.ItemType.PROPERNAME
                cit.doubtful = False
                return cit
        t1 = t
        doubt = False
        name = io.StringIO()
        altname = None
        k = 0
        is_prep = False
        tt = t
        while tt is not None: 
            if (not (isinstance(tt, TextToken))): 
                break
            if (not tt.chars.is_letter or ((tt.chars.is_cyrillic_letter != t.chars.is_cyrillic_letter and not tt.is_value("НА", None)))): 
                break
            if (tt != t): 
                si = StreetItemToken.try_parse(tt, None, False, None)
                if (si is not None and si.typ == StreetItemType.NOUN): 
                    if (si.end_token.next0_ is None or si.end_token.next0_.is_char_of(",.")): 
                        pass
                    else: 
                        break
                if (tt.length_char < 2): 
                    break
                if ((tt.length_char < 3) and not tt.is_value("НА", None)): 
                    if (tt.is_whitespace_before): 
                        break
            if (name.tell() > 0): 
                print('-', end="", file=name)
                if (altname is not None): 
                    print('-', end="", file=altname)
            if ((isinstance(tt, TextToken)) and ((is_prep or ((k > 0 and not tt.get_morph_class_in_dictionary().is_proper_geo))))): 
                print(tt.term, end="", file=name)
                if (altname is not None): 
                    print(tt.term, end="", file=altname)
            else: 
                ss = (tt.term if dont_normalize else CityItemToken.__get_normal_geo(tt))
                if (ss == "ПОЛ" and tt.is_value("ПОЛЕ", None)): 
                    ss = "ПОЛЕ"
                if (ss != tt.term): 
                    if (altname is None): 
                        altname = io.StringIO()
                    print(Utils.toStringStringIO(name), end="", file=altname)
                    print(tt.term, end="", file=altname)
                elif (altname is not None): 
                    print(ss, end="", file=altname)
                print(ss, end="", file=name)
            t1 = tt
            is_prep = tt.morph.class0_.is_preposition
            if (tt.next0_ is None or tt.next0_.next0_ is None): 
                break
            if (not tt.next0_.is_hiphen): 
                break
            if (dont_normalize): 
                break
            if (tt.is_whitespace_after or tt.next0_.is_whitespace_after): 
                if (tt.whitespaces_after_count > 1 or tt.next0_.whitespaces_after_count > 1): 
                    break
                if (not tt.next0_.next0_.chars.equals(tt.chars)): 
                    break
                ttt = tt.next0_.next0_.next0_
                if (ttt is not None and not ttt.is_newline_after): 
                    if (ttt.chars.is_letter): 
                        break
            tt = tt.next0_
            k += 1
            tt = tt.next0_
        if (k > 0): 
            if (k > 2): 
                return None
            reee = CityItemToken._new1087(t, t1, CityItemToken.ItemType.PROPERNAME, Utils.toStringStringIO(name), doubt)
            if (altname is not None): 
                reee.alt_value = Utils.toStringStringIO(altname)
            return reee
        if (t is None): 
            return None
        npt = (None if t.chars.is_latin_letter else NounPhraseHelper.try_parse(t, NounPhraseParseAttr.REFERENTCANBENOUN, 0, None))
        if (npt is not None and (isinstance(npt.end_token, ReferentToken)) and npt.end_token.begin_token != npt.end_token.end_token): 
            npt = (None)
        if ((npt is not None and npt.end_token != t and len(npt.adjectives) > 0) and not npt.adjectives[0].end_token.next0_.is_comma): 
            cit = CityItemToken.try_parse(t.next0_, None, False, None)
            if (cit is not None and cit.typ == CityItemToken.ItemType.NOUN and ((LanguageHelper.ends_with_ex(cit.value, "ПУНКТ", "ПОСЕЛЕНИЕ", "ПОСЕЛЕННЯ", "ПОСЕЛОК") or t.next0_.is_value("ГОРОДОК", None) or t.next0_.is_value("СЕЛО", None)))): 
                ok2 = False
                mc = t.get_morph_class_in_dictionary()
                if (not mc.is_adjective): 
                    ok2 = True
                elif (not MiscHelper.can_be_start_of_sentence(t)): 
                    ok2 = True
                elif (MiscLocationHelper.check_geo_object_before(t, False)): 
                    ok2 = True
                if (ok2): 
                    return CityItemToken._new1088(t, t, CityItemToken.ItemType.CITY, t.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False), npt.morph)
            check_ = True
            if (not npt.end_token.chars.equals(t.chars)): 
                if (npt.end_token.is_value("КИЛОМЕТР", None)): 
                    npt = (None)
                elif (OrgItemToken.try_parse(t.next0_, None) is not None): 
                    npt = (None)
                elif (npt.end_token.chars.is_all_lower and ((npt.end_token.next0_ is None or npt.end_token.next0_.is_comma or AddressItemToken.check_street_after(npt.end_token.next0_, False)))): 
                    pass
                else: 
                    aid = AddressItemToken.try_parse(t.next0_, False, None, None)
                    if (aid is not None): 
                        npt = (None)
                    elif (prev is not None and prev.typ == CityItemToken.ItemType.NOUN and CityAttachHelper.check_city_after(t.next0_)): 
                        check_ = False
                    else: 
                        rt1 = t.kit.process_referent("NAMEDENTITY", t, None)
                        if (rt1 is not None and rt1.end_token == npt.end_token): 
                            pass
                        else: 
                            npt = (None)
            if (check_ and not dont_normalize and npt is not None): 
                org1 = OrgItemToken.try_parse(t.next0_, None)
                if (org1 is not None and not org1.is_doubt): 
                    org0 = OrgItemToken.try_parse(t, None)
                    if (org0 is not None and org0.is_doubt): 
                        npt = (None)
            if (check_ and not dont_normalize and npt is not None): 
                if (len(npt.adjectives) != 1): 
                    return None
                ter = TerrItemToken.check_onto_item(npt.noun.begin_token)
                if (ter is not None): 
                    npt = (None)
                elif (MiscLocationHelper.check_territory(npt.end_token) is not None): 
                    npt = (None)
                if (npt is not None): 
                    npt1 = MiscLocationHelper._try_parse_npt(npt.end_token)
                    if (npt1 is None or len(npt1.adjectives) == 0): 
                        si = StreetItemToken.try_parse(npt.end_token, None, False, None)
                        if ((si is None or si.typ != StreetItemType.NOUN or si.termin.canonic_text == "МОСТ") or si.termin.canonic_text == "ПАРК" or si.termin.canonic_text == "САД"): 
                            t1 = npt.end_token
                            doubt = CityItemToken.__check_doubtful(Utils.asObjectOrNull(t1, TextToken))
                            return CityItemToken._new1089(t, t1, CityItemToken.ItemType.PROPERNAME, npt.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False), doubt, npt.morph)
        if (t.next0_ is not None and t.next0_.chars.equals(t.chars) and not t.is_newline_after): 
            ok = False
            if (TerrItemToken.check_onto_item(t.next0_) is not None): 
                pass
            elif (t.next0_.next0_ is None or not t.next0_.next0_.chars.equals(t.chars)): 
                ok = True
            elif (isinstance(t.next0_.next0_.get_referent(), GeoReferent)): 
                ok = True
            else: 
                tis = TerrItemToken.try_parse_list(t.next0_.next0_, 2, None)
                if (tis is not None and len(tis) > 1): 
                    if (tis[0].is_adjective and tis[1].termin_item is not None): 
                        ok = True
            if (ok and (((isinstance(t.next0_, TextToken)) or (((isinstance(t.next0_, ReferentToken)) and t.next0_.begin_token == t.next0_.end_token))))): 
                if (isinstance(t.next0_, TextToken)): 
                    doubt = CityItemToken.__check_doubtful(Utils.asObjectOrNull(t.next0_, TextToken))
                stat = t.kit.statistics.get_bigramm_info(t, t.next0_)
                ok1 = False
                if ((stat is not None and stat.pair_count >= 2 and stat.pair_count == stat.second_count) and not stat.second_has_other_first): 
                    if (stat.pair_count > 2): 
                        doubt = False
                    ok1 = True
                elif (CityItemToken.M_STD_ADJECTIVES.try_attach(t, None, False) is not None and (isinstance(t.next0_, TextToken))): 
                    ok1 = True
                elif (((t.next0_.next0_ is None or t.next0_.next0_.is_comma)) and t.morph.class0_.is_noun and ((t.next0_.morph.class0_.is_adjective or t.next0_.morph.class0_.is_noun))): 
                    ok1 = True
                if (not ok1 and t.next0_.chars.value == t.chars.value): 
                    if (t.next0_.morph.case_.is_genitive or (((((LanguageHelper.ends_with(Utils.toStringStringIO(name), "ОВ") or LanguageHelper.ends_with(Utils.toStringStringIO(name), "ВО"))) and (isinstance(t.next0_, TextToken)) and not t.next0_.chars.is_all_lower) and t.next0_.length_char > 1 and not t.next0_.get_morph_class_in_dictionary().is_undefined))): 
                        if (t.next0_.is_newline_after): 
                            ok1 = True
                        elif (MiscLocationHelper.check_geo_object_after(t.next0_, False, False)): 
                            ok1 = True
                        else: 
                            aid = AddressItemToken.try_parse(t.next0_.next0_, False, None, None)
                            if (aid is not None): 
                                if (aid.typ == AddressItemType.STREET or aid.typ == AddressItemType.PLOT or aid.typ == AddressItemType.HOUSE): 
                                    ok1 = True
                if (ok1): 
                    tne = CityItemToken.__try_parse_int(t.next0_, None, False, ad)
                    if (tne is not None and tne.typ == CityItemToken.ItemType.NOUN): 
                        pass
                    else: 
                        if (isinstance(t.next0_, TextToken)): 
                            print(" {0}".format(t.next0_.term), end="", file=name, flush=True)
                            if (altname is not None): 
                                print(" {0}".format(t.next0_.term), end="", file=altname, flush=True)
                        else: 
                            print(" {0}".format(MiscHelper.get_text_value_of_meta_token(Utils.asObjectOrNull(t.next0_, ReferentToken), GetTextAttr.NO)), end="", file=name, flush=True)
                            if (altname is not None): 
                                print(" {0}".format(MiscHelper.get_text_value_of_meta_token(Utils.asObjectOrNull(t.next0_, ReferentToken), GetTextAttr.NO)), end="", file=altname, flush=True)
                        t1 = t.next0_
                        return CityItemToken._new1090(t, t1, CityItemToken.ItemType.PROPERNAME, Utils.toStringStringIO(name), (None if altname is None else Utils.toStringStringIO(altname)), doubt, t.next0_.morph)
        if (t.length_char < 2): 
            return None
        t1 = t
        doubt = CityItemToken.__check_doubtful(Utils.asObjectOrNull(t, TextToken))
        if (((t.next0_ is not None and prev is not None and prev.typ == CityItemToken.ItemType.NOUN) and t.next0_.chars.is_cyrillic_letter and t.next0_.chars.is_all_lower) and t.whitespaces_after_count == 1): 
            tt = t.next0_
            ok = False
            if (tt.next0_ is None or tt.next0_.is_char_of(",;")): 
                ok = True
            if (ok and AddressItemToken.try_parse(tt.next0_, False, None, None) is None): 
                t1 = tt
                print(" {0}".format(t1.get_source_text().upper()), end="", file=name, flush=True)
        if (MiscHelper.is_eng_article(t)): 
            return None
        res = CityItemToken._new1090(t, t1, CityItemToken.ItemType.PROPERNAME, Utils.toStringStringIO(name), (None if altname is None else Utils.toStringStringIO(altname)), doubt, t.morph)
        if (t1 == t and (isinstance(t1, TextToken)) and t1.term0 is not None): 
            res.alt_value = t1.term0
        sog = False
        glas = False
        for ch in res.value: 
            if (LanguageHelper.is_cyrillic_vowel(ch) or LanguageHelper.is_latin_vowel(ch)): 
                glas = True
            else: 
                sog = True
        if (t.chars.is_all_upper and t.length_char > 2): 
            if (not glas or not sog): 
                res.doubtful = True
        elif (not glas or not sog): 
            return None
        if (t == t1 and (isinstance(t, TextToken))): 
            if (t.term != res.value): 
                res.alt_value = t.term
        if ((res.whitespaces_after_count < 2) and (isinstance(res.end_token.next0_, TextToken))): 
            abbr = CityItemToken.M_SPEC_ABBRS.try_parse(res.end_token.next0_, TerminParseAttr.NO)
            if (abbr is not None): 
                res.end_token = abbr.end_token
                res.value = "{0} {1}".format(res.value, abbr.termin.canonic_text)
                if (res.alt_value is not None): 
                    res.alt_value = "{0} {1}".format(res.alt_value, abbr.termin.canonic_text)
            elif (not res.end_token.next0_.chars.is_all_lower): 
                abbr = CityItemToken.M_SPEC_ABBRS.try_parse(res.begin_token, TerminParseAttr.NO)
                if (abbr is not None and abbr.end_token == res.end_token): 
                    next0__ = CityItemToken.__try_parse_int(res.end_token.next0_, None, dont_normalize, ad)
                    if (next0__ is not None and ((next0__.typ == CityItemToken.ItemType.PROPERNAME or next0__.typ == CityItemToken.ItemType.CITY))): 
                        res.end_token = next0__.end_token
                        res.alt_value = "{0} {1}".format(next0__.value, res.value)
                        res.value = "{0} {1}".format(res.value, next0__.value)
        return res
    
    @staticmethod
    def __try_parse_spec(t : 'Token') -> 'CityItemToken':
        if (t is None): 
            return None
        tok1 = CityItemToken.M_SPEC_NAMES.try_parse(t, TerminParseAttr.NO)
        if (tok1 is not None): 
            res = CityItemToken._new1079(t, tok1.end_token, CityItemToken.ItemType.PROPERNAME, tok1.termin.canonic_text)
            if (res.value == "ЦЕНТРАЛЬНАЯ УСАДЬБА"): 
                res1 = CityItemToken.__try_parse_spec(res.end_token.next0_)
                if (res1 is not None): 
                    res.value = "{0} {1}".format(res1.value, res.value)
                    res.end_token = res1.end_token
            return res
        tok1 = CityItemToken.M_SPEC_ABBRS.try_parse(t, TerminParseAttr.NO)
        if (tok1 is not None and tok1.termin.canonic_text == "СОВХОЗ"): 
            tt = tok1.end_token.next0_
            res = None
            if (BracketHelper.can_be_start_of_sequence(tt, True, False)): 
                br = BracketHelper.try_parse(tt, BracketParseAttr.NO, 100)
                if (br is not None): 
                    res = CityItemToken._new1074(t, br.end_token, CityItemToken.ItemType.PROPERNAME)
                    res.value = MiscHelper.get_text_value_of_meta_token(br, GetTextAttr.NO)
            else: 
                cit = CityItemToken.try_parse(tt, None, False, None)
                if (cit is not None and ((cit.typ == CityItemToken.ItemType.PROPERNAME or cit.typ == CityItemToken.ItemType.CITY))): 
                    res = cit
            if (res is not None): 
                res.typ = CityItemToken.ItemType.PROPERNAME
                tok1 = CityItemToken.M_SPEC_NAMES.try_parse(res.end_token.next0_, TerminParseAttr.NO)
                if (tok1 is not None and tok1.termin.canonic_text == "ЦЕНТРАЛЬНАЯ УСАДЬБА"): 
                    res.value = "{0} {1}".format(res.value, tok1.termin.canonic_text)
                    res.end_token = tok1.end_token
                return res
        return None
    
    @staticmethod
    def try_parse_back(t : 'Token', only_noun : bool=False) -> 'CityItemToken':
        while t is not None and ((t.is_char_of("(,") or t.is_and)):
            t = t.previous
        if (not (isinstance(t, TextToken))): 
            return None
        cou = 0
        tt = t
        first_pass2880 = True
        while True:
            if first_pass2880: first_pass2880 = False
            else: tt = tt.previous
            if (not (tt is not None)): break
            if (not (isinstance(tt, TextToken))): 
                return None
            if (not tt.chars.is_letter): 
                continue
            if (only_noun): 
                vv = CityItemToken.check_keyword(tt)
                if (vv is not None and vv.end_token == t): 
                    return CityItemToken._new1079(tt, t, CityItemToken.ItemType.NOUN, vv.termin.canonic_text)
            else: 
                res = CityItemToken.try_parse(tt, None, False, None)
                if (res is not None and res.end_token == t): 
                    return res
            cou += 1
            if (cou > 2): 
                break
        return None
    
    @staticmethod
    def __get_normal_geo(t : 'Token') -> str:
        tt = Utils.asObjectOrNull(t, TextToken)
        if (tt is None): 
            return None
        ch = tt.term[len(tt.term) - 1]
        if (((ch == 'О' or ch == 'В' or ch == 'Ы') or ch == 'Х' or ch == 'Ь') or ch == 'Й'): 
            return tt.term
        for wf in tt.morph.items: 
            if (wf.class0_.is_proper_geo and wf.is_in_dictionary): 
                return wf.normal_case
        geo_eq_term = False
        for wf in tt.morph.items: 
            if (wf.class0_.is_proper_geo): 
                ggg = wf.normal_case
                if (ggg == tt.term): 
                    geo_eq_term = True
                elif (not wf.case_.is_nominative): 
                    return ggg
        if (geo_eq_term): 
            return tt.term
        if (tt.morph.items_count > 0): 
            return tt.morph.get_indexer_item(0).normal_case
        else: 
            return tt.term
    
    @staticmethod
    def __check_doubtful(tt : 'TextToken') -> bool:
        if (tt is None): 
            return True
        if (tt.chars.is_all_lower): 
            return True
        if (tt.length_char < 3): 
            return True
        if (((tt.term == "СОЧИ" or tt.is_value("КИЕВ", None) or tt.is_value("ПСКОВ", None)) or tt.is_value("БОСТОН", None) or tt.is_value("РИГА", None)) or tt.is_value("АСТАНА", None) or tt.is_value("АЛМАТЫ", None)): 
            return False
        if (LanguageHelper.ends_with(tt.term, "ВО")): 
            return False
        if ((isinstance(tt.next0_, TextToken)) and (tt.whitespaces_after_count < 2) and not tt.next0_.chars.is_all_lower): 
            if (tt.chars.equals(tt.next0_.chars) and not tt.chars.is_latin_letter and ((not tt.morph.case_.is_genitive and not tt.morph.case_.is_accusative))): 
                mc = tt.next0_.get_morph_class_in_dictionary()
                if (mc.is_proper_surname or mc.is_proper_secname): 
                    return True
        if ((isinstance(tt.previous, TextToken)) and (tt.whitespaces_before_count < 2) and not tt.previous.chars.is_all_lower): 
            mc = tt.previous.get_morph_class_in_dictionary()
            if (mc.is_proper_surname): 
                return True
        ok = False
        for wff in tt.morph.items: 
            wf = Utils.asObjectOrNull(wff, MorphWordForm)
            if (wf.is_in_dictionary): 
                if (not wf.class0_.is_proper): 
                    ok = True
                if (wf.class0_.is_proper_surname or wf.class0_.is_proper_name or wf.class0_.is_proper_secname): 
                    if (wf.normal_case != "ЛОНДОН" and wf.normal_case != "ЛОНДОНЕ"): 
                        ok = True
            elif (wf.class0_.is_proper_surname): 
                val = Utils.ifNotNull(wf.normal_full, Utils.ifNotNull(wf.normal_case, ""))
                if (LanguageHelper.ends_with_ex(val, "ОВ", "ЕВ", "ИН", None)): 
                    if (val != "БЕРЛИН"): 
                        if (tt.previous is not None and tt.previous.is_value("В", None)): 
                            pass
                        else: 
                            return True
        if (not ok): 
            return False
        t0 = tt.previous
        if (t0 is not None and ((t0.is_char(',') or t0.morph.class0_.is_conjunction))): 
            t0 = t0.previous
        if (t0 is not None and (isinstance(t0.get_referent(), GeoReferent))): 
            return False
        if (MiscLocationHelper.check_geo_object_after_brief(tt, None)): 
            return False
        return True
    
    @staticmethod
    def _new1074(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType') -> 'CityItemToken':
        res = CityItemToken(_arg1, _arg2)
        res.typ = _arg3
        return res
    
    @staticmethod
    def _new1078(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : bool, _arg5 : 'Condition', _arg6 : str) -> 'CityItemToken':
        res = CityItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.doubtful = _arg4
        res._cond = _arg5
        res.value = _arg6
        return res
    
    @staticmethod
    def _new1079(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : str) -> 'CityItemToken':
        res = CityItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        return res
    
    @staticmethod
    def _new1083(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : 'IntOntologyItem', _arg5 : 'MorphCollection') -> 'CityItemToken':
        res = CityItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.onto_item = _arg4
        res.morph = _arg5
        return res
    
    @staticmethod
    def _new1085(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : 'MorphCollection') -> 'CityItemToken':
        res = CityItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.morph = _arg4
        return res
    
    @staticmethod
    def _new1086(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : 'IntOntologyItem', _arg5 : str) -> 'CityItemToken':
        res = CityItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.onto_item = _arg4
        res.value = _arg5
        return res
    
    @staticmethod
    def _new1087(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : str, _arg5 : bool) -> 'CityItemToken':
        res = CityItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        res.doubtful = _arg5
        return res
    
    @staticmethod
    def _new1088(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : str, _arg5 : 'MorphCollection') -> 'CityItemToken':
        res = CityItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        res.morph = _arg5
        return res
    
    @staticmethod
    def _new1089(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : str, _arg5 : bool, _arg6 : 'MorphCollection') -> 'CityItemToken':
        res = CityItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        res.doubtful = _arg5
        res.morph = _arg6
        return res
    
    @staticmethod
    def _new1090(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : str, _arg5 : str, _arg6 : bool, _arg7 : 'MorphCollection') -> 'CityItemToken':
        res = CityItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        res.alt_value = _arg5
        res.doubtful = _arg6
        res.morph = _arg7
        return res