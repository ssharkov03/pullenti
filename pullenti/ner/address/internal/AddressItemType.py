# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class AddressItemType(IntEnum):
    PREFIX = 0
    STREET = 1
    HOUSE = 2
    BUILDING = 3
    CORPUS = 4
    POTCH = 5
    FLOOR = 6
    FLAT = 7
    CORPUSORFLAT = 8
    OFFICE = 9
    ROOM = 10
    PLOT = 11
    FIELD = 12
    PAVILION = 13
    BLOCK = 14
    BOX = 15
    CITY = 16
    REGION = 17
    COUNTRY = 18
    NUMBER = 19
    NONUMBER = 20
    KILOMETER = 21
    ZIP = 22
    POSTOFFICEBOX = 23
    CSP = 24
    DETAIL = 25
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)