# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import xml.etree
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Xml import XmlWriter

from pullenti.address.BaseAttributes import BaseAttributes
from pullenti.address.HouseAttributes import HouseAttributes
from pullenti.address.RoomAttributes import RoomAttributes
from pullenti.address.AreaAttributes import AreaAttributes
from pullenti.address.SpecialAttributes import SpecialAttributes
from pullenti.address.GarObject import GarObject

class TextObject:
    """ Адресный объект, выделяемый из текста
    
    Адресный объект из текста
    """
    
    def __init__(self, attrs_ : 'BaseAttributes') -> None:
        self.attrs = None;
        self.gars = list()
        self.rep_object = None;
        self.tag = None;
        self._tag2 = None;
        self.attrs = attrs_
    
    def __str__(self) -> str:
        if (self.attrs is None): 
            return "?"
        return str(self.attrs)
    
    def _find_gar_by_id(self, id0_ : str) -> 'GarObject':
        for g in self.gars: 
            if (g.id0_ == id0_): 
                return g
        return None
    
    def out_info(self, res : io.StringIO) -> None:
        """ Вывести подробную текстовую информацию об объекте (для отладки)
        
        Args:
            res(io.StringIO): 
        """
        self.attrs.out_info(res)
        if (self.rep_object is not None): 
            print("\r\nОбъект адрессария: {0} (ID={1})".format(self.rep_object.spelling, self.rep_object.id0_), end="", file=res, flush=True)
        print("\r\nПривязка к ГАР: ".format(), end="", file=res, flush=True)
        if (len(self.gars) == 0): 
            print("НЕТ\r\n", end="", file=res)
        else: 
            i = 0
            while i < len(self.gars): 
                if (i > 0): 
                    print("; ", end="", file=res)
                print(str(self.gars[i]), end="", file=res)
                i += 1
    
    def serialize(self, xml0_ : XmlWriter) -> None:
        xml0_.write_start_element("textobj")
        self.attrs.serialize(xml0_)
        for g in self.gars: 
            g.serialize(xml0_)
        xml0_.write_end_element()
    
    def deserialize(self, xml0_ : xml.etree.ElementTree.Element) -> None:
        for x in xml0_: 
            if (Utils.getXmlLocalName(x) == "gar"): 
                g = GarObject(None)
                g.deserialize(x)
                self.gars.append(g)
            elif (Utils.getXmlLocalName(x) == "area"): 
                self.attrs = (AreaAttributes())
                self.attrs.deserialize(x)
            elif (Utils.getXmlLocalName(x) == "house"): 
                self.attrs = (HouseAttributes())
                self.attrs.deserialize(x)
            elif (Utils.getXmlLocalName(x) == "room"): 
                self.attrs = (RoomAttributes())
                self.attrs.deserialize(x)
            elif (Utils.getXmlLocalName(x) == "spec"): 
                self.attrs = (SpecialAttributes())
                self.attrs.deserialize(x)