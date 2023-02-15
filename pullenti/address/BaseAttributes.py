# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import xml.etree
from pullenti.unisharp.Xml import XmlWriter

from pullenti.address.GarLevel import GarLevel

class BaseAttributes:
    """ Базовый класс для атрибутивных классов: AreaAttributes, HouseAttributes, RoomAttributes, SpecialAttributes
    
    Базовый класс атрибутов
    """
    
    def __init__(self) -> None:
        self.level = GarLevel.UNDEFINED
    
    def out_info(self, res : io.StringIO) -> None:
        """ Вывести детальную информацию об атрибутах в текстовом виде
        
        Args:
            res(io.StringIO): 
        """
        pass
    
    def serialize(self, xml0_ : XmlWriter) -> None:
        pass
    
    def deserialize(self, xml0_ : xml.etree.ElementTree.Element) -> None:
        pass