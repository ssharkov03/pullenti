# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import xml.etree
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Xml import XmlWriter

from pullenti.address.GarLevel import GarLevel
from pullenti.address.BaseAttributes import BaseAttributes
from pullenti.address.StroenType import StroenType
from pullenti.address.HouseType import HouseType
from pullenti.address.AddressHelper import AddressHelper

class HouseAttributes(BaseAttributes):
    """ Атрибуты строений и участков """
    
    def __init__(self) -> None:
        super().__init__()
        self.typ = HouseType.UNDEFINED
        self.number = None;
        self.build_number = None;
        self.stroen_typ = StroenType.UNDEFINED
        self.stroen_number = None;
    
    def __str__(self) -> str:
        res = io.StringIO()
        if (self.number is not None or self.typ != HouseType.UNDEFINED): 
            if (self.typ != HouseType.UNDEFINED): 
                print("{0}{1}".format(AddressHelper.get_house_type_string(self.typ, self.number is not None), Utils.ifNotNull(self.number, "б/н")), end="", file=res, flush=True)
            else: 
                print(self.number, end="", file=res)
        if (self.build_number is not None): 
            if (res.tell() > 0): 
                print(" ", end="", file=res)
            print("корп.{0}".format(self.build_number), end="", file=res, flush=True)
        if (self.stroen_number is not None): 
            if (res.tell() > 0): 
                print(" ", end="", file=res)
            print("{0}{1}".format(AddressHelper.get_stroen_type_string(self.stroen_typ, True), self.stroen_number), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    def out_info(self, res : io.StringIO) -> None:
        if (self.number is not None or self.typ != HouseType.UNDEFINED): 
            if (self.typ != HouseType.UNDEFINED): 
                typ_ = AddressHelper.get_house_type_string(self.typ, False)
                print("{0}{1}: {2}\r\n".format(str.upper(typ_[0]), typ_[1:], Utils.ifNotNull(self.number, "б/н")), end="", file=res, flush=True)
            else: 
                print("Номер: {0}\r\n".format(self.number), end="", file=res, flush=True)
        if (self.build_number is not None): 
            print("Корпус: {0}\r\n".format(self.build_number), end="", file=res, flush=True)
        if (self.stroen_number is not None): 
            typ_ = AddressHelper.get_stroen_type_string(self.stroen_typ, False)
            print("{0}{1}: {2}\r\n".format(str.upper(typ_[0]), typ_[1:], self.stroen_number), end="", file=res, flush=True)
    
    def serialize(self, xml0_ : XmlWriter) -> None:
        xml0_.write_start_element("house")
        xml0_.write_element_string("level", Utils.enumToString(self.level).lower())
        if (self.typ != HouseType.UNDEFINED): 
            xml0_.write_element_string("type", Utils.enumToString(self.typ).lower())
        if (self.number is not None): 
            xml0_.write_element_string("num", self.number)
        if (self.build_number is not None): 
            xml0_.write_element_string("bnum", self.build_number)
        if (self.stroen_number is not None): 
            xml0_.write_element_string("stype", Utils.enumToString(self.stroen_typ).lower())
            xml0_.write_element_string("snum", self.stroen_number)
        xml0_.write_end_element()
    
    def deserialize(self, xml0_ : xml.etree.ElementTree.Element) -> None:
        for x in xml0_: 
            if (Utils.getXmlLocalName(x) == "type"): 
                try: 
                    self.typ = (Utils.valToEnum(Utils.getXmlInnerText(x), HouseType))
                except Exception as ex153: 
                    pass
            elif (Utils.getXmlLocalName(x) == "num"): 
                self.number = Utils.getXmlInnerText(x)
            elif (Utils.getXmlLocalName(x) == "stype"): 
                try: 
                    self.stroen_typ = (Utils.valToEnum(Utils.getXmlInnerText(x), StroenType))
                except Exception as ex154: 
                    pass
            elif (Utils.getXmlLocalName(x) == "snum"): 
                self.stroen_number = Utils.getXmlInnerText(x)
            elif (Utils.getXmlLocalName(x) == "bnum"): 
                self.build_number = Utils.getXmlInnerText(x)
            elif (Utils.getXmlLocalName(x) == "level"): 
                try: 
                    self.level = (Utils.valToEnum(Utils.getXmlInnerText(x), GarLevel))
                except Exception as ex155: 
                    pass