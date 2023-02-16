# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import xml.etree
import typing
from pullenti.unisharp.Utils import Utils

from pullenti.morph.MorphLang import MorphLang
from pullenti.ner.core.Termin import Termin
from pullenti.ner.org.OrgProfile import OrgProfile
from pullenti.ner.org.internal.OrgItemTypeTyp import OrgItemTypeTyp

class OrgItemTypeTermin(Termin):
    
    def __init__(self, s : str, lang_ : 'MorphLang'=None, p1 : 'OrgProfile'=OrgProfile.UNDEFINED, p2 : 'OrgProfile'=OrgProfile.UNDEFINED) -> None:
        super().__init__(s, lang_, False)
        self.__m_typ = OrgItemTypeTyp.UNDEFINED
        self.must_be_partof_name = False
        self.is_pure_prefix = False
        self.can_be_normal_dep = False
        self.can_has_number = False
        self.can_has_single_name = False
        self.can_has_latin_name = False
        self.must_has_capital_name = False
        self.is_top = False
        self.can_be_single_geo = False
        self.is_doubt_word = False
        self.coeff = 0
        self.profiles = list()
        if (p1 != OrgProfile.UNDEFINED): 
            self.profiles.append(p1)
        if (p2 != OrgProfile.UNDEFINED): 
            self.profiles.append(p2)
    
    @property
    def typ(self) -> 'OrgItemTypeTyp':
        if (self.is_pure_prefix): 
            return OrgItemTypeTyp.PREFIX
        return self.__m_typ
    @typ.setter
    def typ(self, value) -> 'OrgItemTypeTyp':
        if (value == OrgItemTypeTyp.PREFIX): 
            self.is_pure_prefix = True
            self.__m_typ = OrgItemTypeTyp.ORG
        else: 
            self.__m_typ = value
            if (self.__m_typ == OrgItemTypeTyp.DEP or self.__m_typ == OrgItemTypeTyp.DEPADD): 
                if (not OrgProfile.UNIT in self.profiles): 
                    self.profiles.append(OrgProfile.UNIT)
        return value
    
    @property
    def _profile(self) -> 'OrgProfile':
        return OrgProfile.UNDEFINED
    @_profile.setter
    def _profile(self, value) -> 'OrgProfile':
        self.profiles.append(value)
        return value
    
    def __copy_from(self, it : 'OrgItemTypeTermin') -> None:
        self.profiles.extend(it.profiles)
        self.is_pure_prefix = it.is_pure_prefix
        self.can_be_normal_dep = it.can_be_normal_dep
        self.can_has_number = it.can_has_number
        self.can_has_single_name = it.can_has_single_name
        self.can_has_latin_name = it.can_has_latin_name
        self.must_be_partof_name = it.must_be_partof_name
        self.must_has_capital_name = it.must_has_capital_name
        self.is_top = it.is_top
        self.can_be_normal_dep = it.can_be_normal_dep
        self.can_be_single_geo = it.can_be_single_geo
        self.is_doubt_word = it.is_doubt_word
        self.coeff = it.coeff
    
    @staticmethod
    def deserialize_src(xml0_ : xml.etree.ElementTree.Element, set0_ : 'OrgItemTypeTermin') -> typing.List['OrgItemTypeTermin']:
        res = list()
        is_set = Utils.getXmlLocalName(xml0_) == "set"
        if (is_set): 
            set0_ = OrgItemTypeTermin(None)
            res.append(set0_)
        if (xml0_.attrib is None): 
            return res
        for a in xml0_.attrib.items(): 
            nam = Utils.getXmlAttrLocalName(a)
            if (not nam.startswith("name")): 
                continue
            lang_ = MorphLang.RU
            if (nam == "nameUa"): 
                lang_ = MorphLang.UA
            elif (nam == "nameEn"): 
                lang_ = MorphLang.EN
            it = None
            for s in Utils.splitString(a[1], ';', False): 
                if (not Utils.isNullOrEmpty(s)): 
                    if (it is None): 
                        it = OrgItemTypeTermin(s, lang_)
                        res.append(it)
                        if (set0_ is not None): 
                            it.__copy_from(set0_)
                    else: 
                        it.add_variant(s, False)
        for a in xml0_.attrib.items(): 
            nam = Utils.getXmlAttrLocalName(a)
            if (nam.startswith("name")): 
                continue
            if (nam.startswith("abbr")): 
                lang_ = MorphLang.RU
                if (nam == "abbrUa"): 
                    lang_ = MorphLang.UA
                elif (nam == "abbrEn"): 
                    lang_ = MorphLang.EN
                for r in res: 
                    if (r.lang.equals(lang_)): 
                        r.acronym = a[1]
                continue
            if (nam == "profile"): 
                li = list()
                for s in Utils.splitString(a[1], ';', False): 
                    try: 
                        p = Utils.valToEnum(s, OrgProfile)
                        if (p != OrgProfile.UNDEFINED): 
                            li.append(p)
                    except Exception as ex: 
                        pass
                for r in res: 
                    r.profiles = li
                continue
            if (nam == "coef"): 
                v = float(a[1])
                for r in res: 
                    r.coeff = v
                continue
            if (nam == "partofname"): 
                for r in res: 
                    r.must_be_partof_name = a[1] == "true"
                continue
            if (nam == "top"): 
                for r in res: 
                    r.is_top = a[1] == "true"
                continue
            if (nam == "geo"): 
                for r in res: 
                    r.can_be_single_geo = a[1] == "true"
                continue
            if (nam == "purepref"): 
                for r in res: 
                    r.is_pure_prefix = a[1] == "true"
                continue
            if (nam == "number"): 
                for r in res: 
                    r.can_has_number = a[1] == "true"
                continue
            raise Utils.newException("Unknown Org Type Tag: " + Utils.getXmlAttrName(a), None)
        return res
    
    @staticmethod
    def _new1543(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgProfile', _arg4 : float, _arg5 : 'OrgItemTypeTyp', _arg6 : bool, _arg7 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2, _arg3)
        res.coeff = _arg4
        res.typ = _arg5
        res.is_top = _arg6
        res.can_be_single_geo = _arg7
        return res
    
    @staticmethod
    def _new1546(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : 'OrgProfile', _arg4 : float) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res._profile = _arg3
        res.coeff = _arg4
        return res
    
    @staticmethod
    def _new1547(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : 'OrgProfile', _arg5 : float) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res._profile = _arg4
        res.coeff = _arg5
        return res
    
    @staticmethod
    def _new1548(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : 'OrgProfile', _arg4 : float, _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res._profile = _arg3
        res.coeff = _arg4
        res.can_be_single_geo = _arg5
        return res
    
    @staticmethod
    def _new1551(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res._profile = _arg4
        return res
    
    @staticmethod
    def _new1552(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : 'OrgProfile', _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res._profile = _arg4
        res.can_be_normal_dep = _arg5
        return res
    
    @staticmethod
    def _new1553(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.typ = _arg4
        res._profile = _arg5
        return res
    
    @staticmethod
    def _new1554(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_be_single_geo = _arg4
        return res
    
    @staticmethod
    def _new1555(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_be_single_geo = _arg5
        return res
    
    @staticmethod
    def _new1561(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.is_top = _arg4
        res.can_be_single_geo = _arg5
        return res
    
    @staticmethod
    def _new1563(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.is_top = _arg5
        res.can_be_single_geo = _arg6
        return res
    
    @staticmethod
    def _new1564(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        return res
    
    @staticmethod
    def _new1566(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        return res
    
    @staticmethod
    def _new1569(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res._profile = _arg5
        return res
    
    @staticmethod
    def _new1571(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_be_single_geo = _arg4
        res.can_be_normal_dep = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new1573(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_be_single_geo = _arg4
        res.can_has_number = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new1574(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_be_single_geo = _arg4
        res._profile = _arg5
        return res
    
    @staticmethod
    def _new1575(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_be_single_geo = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new1577(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool, _arg7 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_be_single_geo = _arg5
        res.can_has_number = _arg6
        res._profile = _arg7
        return res
    
    @staticmethod
    def _new1584(_arg1 : str, _arg2 : float, _arg3 : str, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.acronym = _arg3
        res.typ = _arg4
        res.can_has_number = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new1585(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_number = _arg5
        return res
    
    @staticmethod
    def _new1586(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_number = _arg4
        res._profile = _arg5
        return res
    
    @staticmethod
    def _new1589(_arg1 : str, _arg2 : float, _arg3 : 'MorphLang', _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.lang = _arg3
        res.typ = _arg4
        res.can_has_number = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new1598(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : 'OrgProfile', _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res._profile = _arg4
        res.can_be_single_geo = _arg5
        return res
    
    @staticmethod
    def _new1599(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.is_doubt_word = _arg4
        return res
    
    @staticmethod
    def _new1600(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.is_doubt_word = _arg5
        return res
    
    @staticmethod
    def _new1603(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        return res
    
    @staticmethod
    def _new1608(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : str, _arg4 : 'OrgProfile', _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.acronym = _arg3
        res._profile = _arg4
        res.can_be_single_geo = _arg5
        res.can_has_number = _arg6
        return res
    
    @staticmethod
    def _new1612(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : 'OrgProfile', _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res._profile = _arg4
        res.can_has_number = _arg5
        return res
    
    @staticmethod
    def _new1613(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgProfile', _arg5 : 'OrgItemTypeTyp', _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res._profile = _arg4
        res.typ = _arg5
        res.can_has_number = _arg6
        return res
    
    @staticmethod
    def _new1616(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : 'OrgProfile', _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res._profile = _arg4
        res.can_has_number = _arg5
        res.can_has_latin_name = _arg6
        return res
    
    @staticmethod
    def _new1622(_arg1 : str, _arg2 : float, _arg3 : str, _arg4 : 'OrgItemTypeTyp', _arg5 : 'OrgProfile', _arg6 : bool, _arg7 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.acronym = _arg3
        res.typ = _arg4
        res._profile = _arg5
        res.can_be_single_geo = _arg6
        res.can_has_number = _arg7
        return res
    
    @staticmethod
    def _new1623(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : bool, _arg7 : bool, _arg8 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_be_normal_dep = _arg4
        res.can_be_single_geo = _arg5
        res.can_has_single_name = _arg6
        res.can_has_latin_name = _arg7
        res._profile = _arg8
        return res
    
    @staticmethod
    def _new1629(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_number = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new1641(_arg1 : str, _arg2 : float, _arg3 : str, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool, _arg7 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.acronym = _arg3
        res.typ = _arg4
        res.can_has_number = _arg5
        res.can_be_single_geo = _arg6
        res._profile = _arg7
        return res
    
    @staticmethod
    def _new1643(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : 'OrgProfile', _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_number = _arg4
        res._profile = _arg5
        res.can_has_latin_name = _arg6
        return res
    
    @staticmethod
    def _new1649(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.is_doubt_word = _arg3
        return res
    
    @staticmethod
    def _new1652(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : str, _arg5 : bool, _arg6 : 'OrgProfile', _arg7 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.acronym = _arg4
        res.can_has_number = _arg5
        res._profile = _arg6
        res.can_has_latin_name = _arg7
        return res
    
    @staticmethod
    def _new1653(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : str, _arg6 : bool, _arg7 : 'OrgProfile', _arg8 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.acronym = _arg5
        res.can_has_number = _arg6
        res._profile = _arg7
        res.can_has_latin_name = _arg8
        return res
    
    @staticmethod
    def _new1654(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : str, _arg5 : bool, _arg6 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.acronym = _arg4
        res.can_has_number = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new1668(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : str, _arg6 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_number = _arg4
        res.acronym = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new1669(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : str, _arg7 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_number = _arg5
        res.acronym = _arg6
        res._profile = _arg7
        return res
    
    @staticmethod
    def _new1670(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_number = _arg4
        return res
    
    @staticmethod
    def _new1680(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : bool, _arg7 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_number = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        res._profile = _arg7
        return res
    
    @staticmethod
    def _new1681(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool, _arg7 : bool, _arg8 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_number = _arg5
        res.can_has_latin_name = _arg6
        res.can_has_single_name = _arg7
        res._profile = _arg8
        return res
    
    @staticmethod
    def _new1684(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : bool, _arg7 : bool, _arg8 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.is_top = _arg4
        res.can_has_single_name = _arg5
        res.can_has_latin_name = _arg6
        res.can_be_single_geo = _arg7
        res._profile = _arg8
        return res
    
    @staticmethod
    def _new1685(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool, _arg7 : bool, _arg8 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.is_top = _arg5
        res.can_has_single_name = _arg6
        res.can_has_latin_name = _arg7
        res.can_be_single_geo = _arg8
        return res
    
    @staticmethod
    def _new1689(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_latin_name = _arg5
        return res
    
    @staticmethod
    def _new1690(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_number = _arg5
        return res
    
    @staticmethod
    def _new1691(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_number = _arg6
        return res
    
    @staticmethod
    def _new1692(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_single_name = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new1693(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool, _arg7 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        res._profile = _arg7
        return res
    
    @staticmethod
    def _new1694(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.must_be_partof_name = _arg4
        return res
    
    @staticmethod
    def _new1695(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : str) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.canonic_text = _arg4
        return res
    
    @staticmethod
    def _new1697(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.must_be_partof_name = _arg5
        return res
    
    @staticmethod
    def _new1698(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : str) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.canonic_text = _arg5
        return res
    
    @staticmethod
    def _new1704(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_number = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        return res
    
    @staticmethod
    def _new1705(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool, _arg7 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_number = _arg5
        res.can_has_latin_name = _arg6
        res.can_has_single_name = _arg7
        return res
    
    @staticmethod
    def _new1708(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : str, _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.acronym = _arg4
        res.can_has_number = _arg5
        return res
    
    @staticmethod
    def _new1710(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : float, _arg4 : bool, _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.coeff = _arg3
        res.can_be_single_geo = _arg4
        res.can_has_single_name = _arg5
        return res
    
    @staticmethod
    def _new1711(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : float, _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.typ = _arg3
        res.coeff = _arg4
        res.can_be_single_geo = _arg5
        res.can_has_single_name = _arg6
        return res
    
    @staticmethod
    def _new1712(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : str) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.acronym = _arg4
        return res
    
    @staticmethod
    def _new1713(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : str, _arg5 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.acronym = _arg4
        res._profile = _arg5
        return res
    
    @staticmethod
    def _new1715(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.is_doubt_word = _arg4
        res.can_has_number = _arg5
        return res
    
    @staticmethod
    def _new1716(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.typ = _arg4
        res.is_doubt_word = _arg5
        res.can_has_number = _arg6
        return res
    
    @staticmethod
    def _new1717(_arg1 : str, _arg2 : float, _arg3 : str, _arg4 : 'OrgItemTypeTyp', _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.acronym = _arg3
        res.typ = _arg4
        res.can_has_number = _arg5
        return res
    
    @staticmethod
    def _new1718(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : str, _arg5 : 'OrgItemTypeTyp', _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.acronym = _arg4
        res.typ = _arg5
        res.can_has_number = _arg6
        return res
    
    @staticmethod
    def _new1723(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_number = _arg5
        return res
    
    @staticmethod
    def _new1730(_arg1 : str, _arg2 : 'OrgItemTypeTyp') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        return res
    
    @staticmethod
    def _new1731(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        return res
    
    @staticmethod
    def _new1733(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.is_doubt_word = _arg4
        return res
    
    @staticmethod
    def _new1738(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : bool, _arg4 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.is_doubt_word = _arg3
        res.can_has_number = _arg4
        return res
    
    @staticmethod
    def _new1739(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.is_doubt_word = _arg4
        res.can_has_number = _arg5
        return res
    
    @staticmethod
    def _new1740(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : float, _arg4 : bool, _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.coeff = _arg3
        res.can_has_number = _arg4
        res.can_has_single_name = _arg5
        return res
    
    @staticmethod
    def _new1742(_arg1 : str, _arg2 : str, _arg3 : 'OrgItemTypeTyp', _arg4 : float, _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.acronym = _arg2
        res.typ = _arg3
        res.coeff = _arg4
        res.can_has_number = _arg5
        res.can_has_single_name = _arg6
        return res
    
    @staticmethod
    def _new1743(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : float, _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.coeff = _arg4
        res.can_has_number = _arg5
        res.can_has_single_name = _arg6
        return res
    
    @staticmethod
    def _new1744(_arg1 : str, _arg2 : str, _arg3 : 'OrgItemTypeTyp', _arg4 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.acronym = _arg2
        res.typ = _arg3
        res.can_be_normal_dep = _arg4
        return res
    
    @staticmethod
    def _new1747(_arg1 : str, _arg2 : 'MorphLang', _arg3 : str, _arg4 : 'OrgItemTypeTyp', _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.acronym = _arg3
        res.typ = _arg4
        res.can_be_normal_dep = _arg5
        return res
    
    @staticmethod
    def _new1750(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.can_be_normal_dep = _arg3
        return res
    
    @staticmethod
    def _new1751(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.can_be_normal_dep = _arg4
        return res
    
    @staticmethod
    def _new1763(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : bool, _arg4 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.can_be_normal_dep = _arg3
        res._profile = _arg4
        return res
    
    @staticmethod
    def _new1764(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.can_be_normal_dep = _arg4
        res._profile = _arg5
        return res
    
    @staticmethod
    def _new1768(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : bool, _arg4 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.can_has_number = _arg3
        res.is_doubt_word = _arg4
        return res
    
    @staticmethod
    def _new1769(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : bool, _arg4 : bool, _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.can_has_number = _arg3
        res.is_doubt_word = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        return res
    
    @staticmethod
    def _new1770(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : bool, _arg7 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.can_has_number = _arg4
        res.is_doubt_word = _arg5
        res.can_has_latin_name = _arg6
        res.can_has_single_name = _arg7
        return res
    
    @staticmethod
    def _new1777(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.can_has_number = _arg3
        return res
    
    @staticmethod
    def _new1778(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.can_has_number = _arg4
        return res
    
    @staticmethod
    def _new1779(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : 'OrgProfile', _arg4 : str) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res._profile = _arg3
        res.acronym = _arg4
        return res
    
    @staticmethod
    def _new1780(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : 'OrgProfile', _arg5 : str) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res._profile = _arg4
        res.acronym = _arg5
        return res
    
    @staticmethod
    def _new1785(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : str, _arg4 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.acronym = _arg3
        res._profile = _arg4
        return res
    
    @staticmethod
    def _new1786(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : str, _arg5 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.acronym = _arg4
        res._profile = _arg5
        return res
    
    @staticmethod
    def _new1790(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res._profile = _arg3
        return res
    
    @staticmethod
    def _new1807(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : str) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.acronym = _arg3
        return res
    
    @staticmethod
    def _new1809(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : str) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.acronym = _arg4
        return res
    
    @staticmethod
    def _new1901(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : str, _arg4 : bool, _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.acronym = _arg3
        res.acronym_can_be_lower = _arg4
        res.can_be_single_geo = _arg5
        return res
    
    @staticmethod
    def _new1902(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : str, _arg4 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.acronym = _arg3
        res.can_has_latin_name = _arg4
        return res
    
    @staticmethod
    def _new1905(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : bool, _arg4 : str) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.can_has_latin_name = _arg3
        res.acronym = _arg4
        return res
    
    @staticmethod
    def _new1906(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : str) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.acronym = _arg5
        return res
    
    @staticmethod
    def _new1909(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.can_has_latin_name = _arg3
        return res
    
    @staticmethod
    def _new1912(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : bool, _arg4 : str, _arg5 : str) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.can_has_latin_name = _arg3
        res.acronym = _arg4
        res.acronym_smart = _arg5
        return res
    
    @staticmethod
    def _new1923(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : str, _arg6 : str) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.acronym = _arg5
        res.acronym_smart = _arg6
        return res
    
    @staticmethod
    def _new1941(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : str, _arg4 : str) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.acronym = _arg3
        res.acronym_smart = _arg4
        return res
    
    @staticmethod
    def _new1944(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : bool, _arg4 : str, _arg5 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.can_has_latin_name = _arg3
        res.acronym = _arg4
        res._profile = _arg5
        return res
    
    @staticmethod
    def _new1945(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : str, _arg6 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.acronym = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new1948(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : bool, _arg4 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.can_has_latin_name = _arg3
        res._profile = _arg4
        return res
    
    @staticmethod
    def _new1949(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res._profile = _arg5
        return res
    
    @staticmethod
    def _new1951(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        return res
    
    @staticmethod
    def _new1955(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : str, _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.acronym = _arg4
        res.can_has_latin_name = _arg5
        return res
    
    @staticmethod
    def _new1958(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : bool, _arg4 : bool, _arg5 : str) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.can_has_latin_name = _arg3
        res.can_has_number = _arg4
        res.acronym = _arg5
        return res
    
    @staticmethod
    def _new1959(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : str) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_number = _arg5
        res.acronym = _arg6
        return res
    
    @staticmethod
    def _new1964(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : str, _arg4 : bool, _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.acronym = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_number = _arg5
        return res
    
    @staticmethod
    def _new1978(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : str, _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.acronym = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_number = _arg6
        return res
    
    @staticmethod
    def _new1979(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : str, _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.acronym = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        return res
    
    @staticmethod
    def _new1980(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : 'OrgProfile', _arg4 : bool, _arg5 : float) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res._profile = _arg3
        res.can_has_latin_name = _arg4
        res.coeff = _arg5
        return res
    
    @staticmethod
    def _new1981(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_single_name = _arg4
        res.can_has_latin_name = _arg5
        return res
    
    @staticmethod
    def _new1982(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : 'OrgProfile', _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res._profile = _arg4
        res.can_has_single_name = _arg5
        res.can_has_latin_name = _arg6
        return res
    
    @staticmethod
    def _new1983(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : 'OrgProfile', _arg6 : bool, _arg7 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.typ = _arg4
        res._profile = _arg5
        res.can_has_single_name = _arg6
        res.can_has_latin_name = _arg7
        return res
    
    @staticmethod
    def _new1984(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_single_name = _arg5
        res.can_has_latin_name = _arg6
        return res
    
    @staticmethod
    def _new1985(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_single_name = _arg4
        res.can_has_latin_name = _arg5
        res.must_has_capital_name = _arg6
        return res
    
    @staticmethod
    def _new1986(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool, _arg7 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_single_name = _arg5
        res.can_has_latin_name = _arg6
        res.must_has_capital_name = _arg7
        return res
    
    @staticmethod
    def _new1989(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_be_normal_dep = _arg4
        res._profile = _arg5
        return res
    
    @staticmethod
    def _new1991(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.typ = _arg4
        res.can_be_normal_dep = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new1992(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : bool, _arg4 : bool, _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.can_has_single_name = _arg3
        res.can_has_latin_name = _arg4
        res.is_doubt_word = _arg5
        return res
    
    @staticmethod
    def _new1994(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : bool, _arg7 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_single_name = _arg4
        res.can_has_latin_name = _arg5
        res.is_doubt_word = _arg6
        res._profile = _arg7
        return res
    
    @staticmethod
    def _new1995(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : bool, _arg4 : bool, _arg5 : bool, _arg6 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.can_has_single_name = _arg3
        res.can_has_latin_name = _arg4
        res.is_doubt_word = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new1996(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : bool, _arg4 : bool, _arg5 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.can_has_single_name = _arg3
        res.can_has_latin_name = _arg4
        res._profile = _arg5
        return res
    
    @staticmethod
    def _new1997(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.can_has_single_name = _arg4
        res.can_has_latin_name = _arg5
        res.is_doubt_word = _arg6
        return res
    
    @staticmethod
    def _new1998(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : float, _arg4 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.coeff = _arg3
        res.can_has_single_name = _arg4
        return res
    
    @staticmethod
    def _new1999(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : float, _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.coeff = _arg4
        res.can_has_single_name = _arg5
        return res
    
    @staticmethod
    def _new2009(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_single_name = _arg5
        return res
    
    @staticmethod
    def _new2010(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        return res
    
    @staticmethod
    def _new2011(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : str, _arg5 : bool, _arg6 : bool, _arg7 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.acronym = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        res.can_be_single_geo = _arg7
        return res
    
    @staticmethod
    def _new2012(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : str, _arg6 : bool, _arg7 : bool, _arg8 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.typ = _arg4
        res.acronym = _arg5
        res.can_has_latin_name = _arg6
        res.can_has_single_name = _arg7
        res.can_be_single_geo = _arg8
        return res
    
    @staticmethod
    def _new2019(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_single_name = _arg5
        res.must_has_capital_name = _arg6
        return res
    
    @staticmethod
    def _new2020(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_single_name = _arg5
        res.must_has_capital_name = _arg6
        return res
    
    @staticmethod
    def _new2021(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : float, _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.coeff = _arg4
        res.can_has_latin_name = _arg5
        return res
    
    @staticmethod
    def _new2022(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgProfile', _arg4 : 'OrgItemTypeTyp', _arg5 : float, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2, _arg3)
        res.typ = _arg4
        res.coeff = _arg5
        res.can_has_latin_name = _arg6
        return res
    
    @staticmethod
    def _new2030(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgProfile', _arg4 : 'OrgItemTypeTyp', _arg5 : float, _arg6 : bool, _arg7 : str) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2, _arg3)
        res.typ = _arg4
        res.coeff = _arg5
        res.can_has_latin_name = _arg6
        res.acronym = _arg7
        return res
    
    @staticmethod
    def _new2034(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : bool, _arg4 : bool, _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.can_has_latin_name = _arg3
        res.can_has_single_name = _arg4
        res.must_has_capital_name = _arg5
        res.can_has_number = _arg6
        return res
    
    @staticmethod
    def _new2035(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : bool, _arg7 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_single_name = _arg5
        res.must_has_capital_name = _arg6
        res.can_has_number = _arg7
        return res
    
    @staticmethod
    def _new2036(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : bool, _arg7 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_single_name = _arg5
        res.must_has_capital_name = _arg6
        res._profile = _arg7
        return res
    
    @staticmethod
    def _new2037(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool, _arg7 : bool, _arg8 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        res.must_has_capital_name = _arg7
        res._profile = _arg8
        return res
    
    @staticmethod
    def _new2041(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool, _arg7 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        res.must_has_capital_name = _arg7
        return res
    
    @staticmethod
    def _new2042(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : str, _arg5 : bool, _arg6 : bool, _arg7 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.acronym = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        res.must_has_capital_name = _arg7
        return res
    
    @staticmethod
    def _new2044(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : bool, _arg7 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_single_name = _arg5
        res.must_has_capital_name = _arg6
        res.can_has_number = _arg7
        return res
    
    @staticmethod
    def _new2046(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool, _arg7 : bool, _arg8 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        res.must_has_capital_name = _arg7
        res.can_has_number = _arg8
        return res
    
    @staticmethod
    def _new2049(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_single_name = _arg5
        res.can_be_single_geo = _arg6
        return res
    
    @staticmethod
    def _new2050(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool, _arg7 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        res.can_be_single_geo = _arg7
        return res
    
    @staticmethod
    def _new2058(_arg1 : str, _arg2 : float, _arg3 : str, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool, _arg7 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.acronym = _arg3
        res.typ = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        res.can_has_number = _arg7
        return res
    
    @staticmethod
    def _new2059(_arg1 : str, _arg2 : str, _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool, _arg7 : bool, _arg8 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.acronym = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        res.must_has_capital_name = _arg7
        res.can_has_number = _arg8
        return res
    
    @staticmethod
    def _new2064(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_latin_name = _arg5
        return res
    
    @staticmethod
    def _new2065(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_number = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new2069(_arg1 : str, _arg2 : float, _arg3 : bool, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.can_be_normal_dep = _arg3
        res.typ = _arg4
        res.can_has_number = _arg5
        res.can_be_single_geo = _arg6
        return res
    
    @staticmethod
    def _new2081(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgProfile', _arg4 : bool, _arg5 : float) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2, _arg3)
        res.can_has_latin_name = _arg4
        res.coeff = _arg5
        return res
    
    @staticmethod
    def _new2086(_arg1 : str, _arg2 : bool, _arg3 : float) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.can_has_latin_name = _arg2
        res.coeff = _arg3
        return res
    
    @staticmethod
    def _new2090(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : float, _arg4 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.coeff = _arg3
        res.can_has_latin_name = _arg4
        return res