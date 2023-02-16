# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class FioTemplateType(IntEnum):
    UNDEFINED = 0
    SURNAMEII = 1
    IISURNAME = 2
    SURNAMEI = 3
    ISURNAME = 4
    SURNAMENAME = 5
    SURNAMENAMESECNAME = 6
    NAMESURNAME = 7
    NAMESECNAMESURNAME = 8
    NAMEISURNAME = 9
    NAMESECNAME = 10
    KING = 11
    ASIANNAME = 12
    ASIANSURNAMENAME = 13
    ARABICLONG = 14
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)