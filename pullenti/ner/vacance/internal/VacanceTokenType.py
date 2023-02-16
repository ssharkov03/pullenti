# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class VacanceTokenType(IntEnum):
    UNDEFINED = 0
    DUMMY = 1
    STOP = 2
    EXPIRED = 3
    NAME = 4
    DATE = 5
    SKILL = 6
    PLUS = 7
    EXPIERENCE = 8
    EDUCATION = 9
    MONEY = 10
    LANGUAGE = 11
    MORAL = 12
    DRIVING = 13
    LICENSE = 14
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)