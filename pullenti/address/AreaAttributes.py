# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import xml.etree
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.unisharp.Xml import XmlWriter

from pullenti.address.GarLevel import GarLevel
from pullenti.address.BaseAttributes import BaseAttributes

class AreaAttributes(BaseAttributes):
    """ Атрибуты города, региона, района, квартала, улиц и т.п. """
    
    def __init__(self) -> None:
        super().__init__()
        self.types = list()
        self.names = list()
        self.number = None;
    
    def __str__(self) -> str:
        res = (self.types[0] if len(self.types) > 0 else "?")
        out_num = False
        if (self.number is not None and self.level == GarLevel.STREET and not self.number.endswith("км")): 
            res = "{0} {1}".format(res, self.number)
            out_num = True
        if (len(self.names) > 0): 
            res = "{0} {1}".format(res, self.names[0])
        if (self.number is not None and not out_num): 
            nnn = 0
            wrapnnn148 = RefOutArgWrapper(0)
            inoutres149 = Utils.tryParseInt(self.number, wrapnnn148)
            nnn = wrapnnn148.value
            if (inoutres149): 
                res = "{0}-{1}".format(res, self.number)
            else: 
                res = "{0} {1}".format(res, self.number)
        return res
    
    def out_info(self, res : io.StringIO) -> None:
        for ty in self.types: 
            print("Тип: {0}\r\n".format(ty), end="", file=res, flush=True)
        if (len(self.names) > 0): 
            print("Наименование: {0}".format(self.names[0]), end="", file=res, flush=True)
            i = 1
            while i < len(self.names): 
                print(" / {0}".format(self.names[i]), end="", file=res, flush=True)
                i += 1
            print("\r\n", end="", file=res)
        if (self.number is not None): 
            print("Номер: {0}\r\n".format(self.number), end="", file=res, flush=True)
    
    def serialize(self, xml0_ : XmlWriter) -> None:
        xml0_.write_start_element("area")
        xml0_.write_element_string("level", Utils.enumToString(self.level).lower())
        for ty in self.types: 
            xml0_.write_element_string("type", ty)
        for nam in self.names: 
            xml0_.write_element_string("name", nam)
        if (self.number is not None): 
            xml0_.write_element_string("num", self.number)
        xml0_.write_end_element()
    
    def deserialize(self, xml0_ : xml.etree.ElementTree.Element) -> None:
        for x in xml0_: 
            if (Utils.getXmlLocalName(x) == "type"): 
                self.types.append(Utils.getXmlInnerText(x))
            elif (Utils.getXmlLocalName(x) == "name"): 
                self.names.append(Utils.getXmlInnerText(x))
            elif (Utils.getXmlLocalName(x) == "num"): 
                self.number = Utils.getXmlInnerText(x)
            elif (Utils.getXmlLocalName(x) == "level"): 
                try: 
                    self.level = (Utils.valToEnum(Utils.getXmlInnerText(x), GarLevel))
                except Exception as ex150: 
                    pass