# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class HouseType(IntEnum):
    """ Типы домов """
    UNDEFINED = 0
    """ Не определено """
    ESTATE = 1
    """ Владение """
    HOUSE = 2
    """ Дом """
    HOUSEESTATE = 3
    """ Домовладение """
    GARAGE = 4
    """ Гараж """
    PLOT = 5
    """ Участок """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)