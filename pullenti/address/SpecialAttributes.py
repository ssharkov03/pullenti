# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import xml.etree
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Xml import XmlWriter

from pullenti.address.BaseAttributes import BaseAttributes
from pullenti.address.SpecialType import SpecialType
from pullenti.address.GarLevel import GarLevel
from pullenti.address.AddressHelper import AddressHelper

class SpecialAttributes(BaseAttributes):
    """ Атрибуты специфических адресных объектов (указатели, пересечения и др.) """
    
    def __init__(self) -> None:
        super().__init__()
        self.typ = SpecialType.UNDEFINED
        self.param = None;
        self.level = GarLevel.SPECIAL
    
    def __str__(self) -> str:
        tmp = io.StringIO()
        print(AddressHelper.get_spec_type_string(self.typ), end="", file=tmp)
        if (self.param is not None): 
            print(" {0}".format(self.param), end="", file=tmp, flush=True)
        return Utils.toStringStringIO(tmp)
    
    def serialize(self, xml0_ : XmlWriter) -> None:
        xml0_.write_start_element("spec")
        if (self.typ != SpecialType.UNDEFINED): 
            xml0_.write_element_string("type", Utils.enumToString(self.typ).upper())
        if (self.param is not None): 
            xml0_.write_element_string("param", self.param)
        xml0_.write_end_element()
    
    def deserialize(self, xml0_ : xml.etree.ElementTree.Element) -> None:
        for x in xml0_: 
            if (Utils.getXmlLocalName(x) == "type"): 
                try: 
                    self.typ = (Utils.valToEnum(Utils.getXmlInnerText(x), SpecialType))
                except Exception as ex159: 
                    pass
            elif (Utils.getXmlLocalName(x) == "param"): 
                self.param = Utils.getXmlInnerText(x)