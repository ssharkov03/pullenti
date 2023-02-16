# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
import pathlib
import xml.etree
from enum import IntEnum
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.unisharp.Streams import MemoryStream
from pullenti.unisharp.Streams import FileStream
from pullenti.unisharp.Streams import Stream
from pullenti.unisharp.Xml import XmlWriter
from pullenti.unisharp.Xml import XmlWriterSettings

from pullenti.util.FileHelper import FileHelper
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.address.StreetKind import StreetKind
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.address.StreetReferent import StreetReferent
from pullenti.address.internal.FiasHelper import FiasHelper

class AddrTyp:
    
    class Typs(IntEnum):
        UNDEFINED = 0
        REGION = 1
        CITY = 2
        VILLAGE = 3
        ORG = 4
        STREET = 5
        
        @classmethod
        def has_value(cls, value):
            return any(value == item.value for item in cls)
    
    def __init__(self) -> None:
        self.name = None;
        self.typ = AddrTyp.Typs.UNDEFINED
        self.id0_ = 0
        self.count = 0
        self.stat = dict()
    
    def __str__(self) -> str:
        return "{0}: {1}".format(Utils.enumToString(self.typ), self.name)
    
    def add_stat(self, r : 'Referent') -> None:
        ty = AddrTyp.Typs.UNDEFINED
        if (r is not None and r.type_name == "ORGANIZATION"): 
            ty = AddrTyp.Typs.ORG
        elif (isinstance(r, StreetReferent)): 
            ty = AddrTyp.Typs.STREET
        elif (isinstance(r, GeoReferent)): 
            g = Utils.asObjectOrNull(r, GeoReferent)
            if (g.is_state): 
                pass
            elif (g.is_city and not g.is_region): 
                if ("город" in g.typs): 
                    ty = AddrTyp.Typs.CITY
                else: 
                    ty = AddrTyp.Typs.VILLAGE
            elif (g.is_region and not g.is_city): 
                ty = AddrTyp.Typs.REGION
        if (ty != AddrTyp.Typs.UNDEFINED): 
            if (ty in self.stat): 
                self.stat[ty] += 1
            else: 
                self.stat[ty] = 1
    
    def calc_typ(self) -> None:
        if (self.name == "территория"): 
            return
        max0_ = 10
        for s in self.stat.items(): 
            if (s[1] > max0_): 
                max0_ = s[1]
                self.typ = s[0]
    
    def can_be_equal(self, name_ : str) -> bool:
        if (name_ is None): 
            return False
        if (Utils.compareStrings(name_, self.name, True) == 0): 
            return True
        if (Utils.startsWithString(name_, self.name, True)): 
            return True
        if (Utils.startsWithString(self.name, name_, True)): 
            return True
        if (self.name == "километр"): 
            if ("шоссе" in name_ or "дорога" in name_ or "трасса" in name_): 
                return True
        if (self.name == "город" and "муницип" in name_): 
            return True
        if (self.name.startswith("сельск") and name_.startswith("сельск")): 
            return True
        return False
    
    def check_type(self, r : 'Referent') -> int:
        if (r.type_name == "ORGANIZATION"): 
            if (self.typ == AddrTyp.Typs.ORG): 
                return 1
            if (self.name == "территория"): 
                return 1
            return -1
        if (isinstance(r, StreetReferent)): 
            st = Utils.asObjectOrNull(r, StreetReferent)
            ki = st.kind
            typs1 = st.typs
            for t in typs1: 
                if (Utils.compareStrings(t, self.name, True) == 0): 
                    return 1
                elif (((self.name == "километр" or self.name.endswith("трасса"))) and ki == StreetKind.ROAD): 
                    return 1
                elif (t.endswith(self.name) or t.startswith(self.name) or self.name.startswith(t)): 
                    return 1
            if (self.typ == AddrTyp.Typs.ORG): 
                return (1 if ki == StreetKind.AREA else 0)
            if (self.typ == AddrTyp.Typs.VILLAGE and ki == StreetKind.ORG): 
                return 0
            if (self.typ != AddrTyp.Typs.STREET): 
                if (((self.typ == AddrTyp.Typs.VILLAGE or self.typ == AddrTyp.Typs.CITY)) and ki == StreetKind.AREA): 
                    return 0
                return -1
            if (self.name == "территория" or self.name == "сад"): 
                if (ki != StreetKind.UNDEFINED): 
                    return 1
            if (self.name == "улица"): 
                return 0
            if (len(typs1) == 1 and typs1[0] == "улица"): 
                return 0
            return -1
        g = Utils.asObjectOrNull(r, GeoReferent)
        if (g is None): 
            return -1
        if (self.typ == AddrTyp.Typs.STREET): 
            return -1
        typs = g.typs
        if (self.name in typs): 
            return 1
        for t in typs: 
            if (t.startswith(self.name) or self.name.startswith(t)): 
                return 1
        for t in typs: 
            if (LanguageHelper.ends_with(t, self.name) or LanguageHelper.ends_with(self.name, t)): 
                return 1
        if (self.name == "город"): 
            for t in typs: 
                if ("муницип" in t): 
                    return 1
        if (self.typ == AddrTyp.Typs.VILLAGE): 
            if (self.name.startswith("сельск")): 
                for t in typs: 
                    if (t.startswith("сельск")): 
                        return 1
            if (not g.is_city): 
                return -1
            if (not "город" in typs): 
                return 1
            return 0
        if (self.typ == AddrTyp.Typs.CITY): 
            if (not g.is_city): 
                return -1
            if (self.name == "автодорога"): 
                return -1
            if (self.name == "город" and not "город" in typs): 
                return 0
            if (self.name != "город" and "город" in typs): 
                return 0
            return 1
        if (self.typ == AddrTyp.Typs.ORG): 
            if (g.is_city): 
                return 0
        if (self.typ == AddrTyp.Typs.REGION): 
            if (self.name == "край" and "область" in typs): 
                return 1
            if (self.name == "область" and "край" in typs): 
                return 1
        return -1
    
    @staticmethod
    def _save(fname : str, typs : typing.List[tuple], id0__ : str, dt : str) -> None:
        if (pathlib.PurePath(fname).suffix == ".xml"): 
            settings = XmlWriterSettings()
            settings.indent = True
            settings.indentChars = (" ")
            settings.encoding = "UTF-8"
            with FileStream(fname, "wb") as f: 
                xml0_ = XmlWriter.create_stream(f, settings)
                xml0_.write_start_document()
                xml0_.write_start_element("types")
                if (id0__ is not None): 
                    xml0_.write_attribute_string("guid", id0__)
                if (dt is not None): 
                    xml0_.write_attribute_string("date", dt)
                for ty in typs.values(): 
                    xml0_.write_start_element("type")
                    xml0_.write_attribute_string("id", str(ty.id0_))
                    xml0_.write_attribute_string("class", Utils.enumToString(ty.typ))
                    xml0_.write_attribute_string("name", Utils.ifNotNull(ty.name, "?"))
                    xml0_.write_attribute_string("count", str(ty.count))
                    xml0_.write_end_element()
                xml0_.write_end_element()
                xml0_.write_end_document()
                xml0_.close()
            return
        with FileStream(fname, "r+b") as f: 
            FiasHelper.serialize_int(f, len(typs))
            for kp in typs.items(): 
                FiasHelper.serialize_short(f, kp[1].id0_)
                FiasHelper.serialize_byte(f, kp[1].typ)
                FiasHelper.serialize_string(f, kp[1].name, False)
                FiasHelper.serialize_string(f, None, False)
            FiasHelper.serialize_string(f, id0__, False)
            FiasHelper.serialize_string(f, dt, False)
    
    @staticmethod
    def _load(fname : str, id0__ : str, dt : str) -> typing.List[tuple]:
        res = dict()
        if (pathlib.PurePath(fname).suffix == ".xml"): 
            xdoc = None # new XmlDocument
            with FileStream(fname, "rb") as f: 
                xdoc = Utils.parseXmlFromStream(f)
            for a in xdoc.getroot().attrib.items(): 
                if (Utils.getXmlAttrLocalName(a) == "guid"): 
                    id0__.value = a[1]
                elif (Utils.getXmlAttrLocalName(a) == "date"): 
                    dt.value = a[1]
            for x in xdoc.getroot(): 
                if (Utils.getXmlLocalName(x) == "type"): 
                    ty = AddrTyp()
                    for a in x.attrib.items(): 
                        if (Utils.getXmlAttrLocalName(a) == "id"): 
                            n = 0
                            wrapn1 = RefOutArgWrapper(0)
                            inoutres2 = Utils.tryParseInt(a[1], wrapn1)
                            n = wrapn1.value
                            if (inoutres2): 
                                ty.id0_ = n
                        elif (Utils.getXmlAttrLocalName(a) == "name"): 
                            ty.name = a[1]
                        elif (Utils.getXmlAttrLocalName(a) == "count"): 
                            n = 0
                            wrapn3 = RefOutArgWrapper(0)
                            inoutres4 = Utils.tryParseInt(a[1], wrapn3)
                            n = wrapn3.value
                            if (inoutres4): 
                                ty.count = n
                        elif (Utils.getXmlAttrLocalName(a) == "class"): 
                            try: 
                                ty.typ = (Utils.valToEnum(a[1], AddrTyp.Typs))
                            except Exception as ex5: 
                                pass
                    if (ty.id0_ > 0 and not ty.id0_ in res): 
                        res[ty.id0_] = ty
            return res
        dat = FileHelper.load_data_from_file(fname, 0)
        with MemoryStream(dat) as f: 
            f.position = 0
            cou = FiasHelper.deserialize_int(f)
            if (cou == 0): 
                return None
            i = 0
            while i < cou: 
                while cou > 0: 
                    sh = FiasHelper.deserialize_short(f)
                    ty = AddrTyp._new6(sh)
                    ty.typ = (Utils.valToEnum(FiasHelper.deserialize_byte(f), AddrTyp.Typs))
                    ty.name = FiasHelper.deserialize_string(f)
                    FiasHelper.deserialize_string(f)
                    if (not sh in res): 
                        res[sh] = ty
                    cou -= 1
                i += 1
            id0__.value = FiasHelper.deserialize_string(f)
            dt.value = FiasHelper.deserialize_string(f)
        return res
    
    @staticmethod
    def _new6(_arg1 : int) -> 'AddrTyp':
        res = AddrTyp()
        res.id0_ = _arg1
        return res
    
    @staticmethod
    def _new34(_arg1 : int, _arg2 : str) -> 'AddrTyp':
        res = AddrTyp()
        res.id0_ = _arg1
        res.name = _arg2
        return res