# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class VerbType(IntEnum):
    """ Тип глагольной формы """
    UNDEFINED = 0
    BE = 1
    """ Быть, являться """
    HAVE = 2
    """ Иметь """
    CAN = 3
    """ Могу """
    MUST = 4
    """ Должен """
    SAY = 5
    """ Говорить, произносить ... """
    CALL = 6
    """ Звонить """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)