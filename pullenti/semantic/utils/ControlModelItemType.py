# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class ControlModelItemType(IntEnum):
    """ Тип элемента модели управления """
    UNDEFINED = 0
    WORD = 1
    """ Конкретное слово (не относится ко всем остальным) """
    VERB = 2
    """ Все глаголы (не Reflexive) """
    REFLEXIVE = 3
    """ Возвратные глаголы и страдательный залог """
    NOUN = 4
    """ Существительное, которое можно отглаголить """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)