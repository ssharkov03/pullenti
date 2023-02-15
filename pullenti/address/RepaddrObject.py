# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

from pullenti.address.GarLevel import GarLevel
from pullenti.address.AddressHelper import AddressHelper

class RepaddrObject(object):
    """ Адресный элемент из Адрессария
    
    """
    
    def __init__(self) -> None:
        self.id0_ = 0
        self.parents = None
        self.children = None
        self.spelling = None;
        self.level = GarLevel.UNDEFINED
        self.types = list()
        self.gar_guids = None;
    
    def __str__(self) -> str:
        return self.spelling
    
    def out_info(self, res : io.StringIO) -> None:
        print("Уникальный ID: {0}\r\n".format(self.id0_), end="", file=res, flush=True)
        print("Нормализация: {0}\r\n".format(self.spelling), end="", file=res, flush=True)
        if (self.level != GarLevel.UNDEFINED): 
            print("Уровень: {0} - {1}\r\n".format(self.level, AddressHelper.get_level_string(self.level)), end="", file=res, flush=True)
        if (self.gar_guids is not None): 
            for g in self.gar_guids: 
                print("ГАР-объект: {0}\r\n".format(g), end="", file=res, flush=True)
    
    def compareTo(self, other : 'RepaddrObject') -> int:
        l1 = self.level
        if (self.level == GarLevel.COUNTRY): 
            l1 = 0
        l2 = other.level
        if (other.level == GarLevel.COUNTRY): 
            l2 = 0
        if (l1 < l2): 
            return -1
        if (l1 > l2): 
            return 1
        return Utils.compareStrings(self.spelling, other.spelling, False)