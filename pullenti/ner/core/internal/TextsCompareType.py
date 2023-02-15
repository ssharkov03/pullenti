# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class TextsCompareType(IntEnum):
    NONCOMPARABLE = 0
    EQUIVALENT = 1
    EARLY = 2
    LATER = 3
    IN = 4
    CONTAINS = 5
    INTERSECT = 6
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)