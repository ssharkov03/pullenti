# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class ChatType(IntEnum):
    """ Типы диалоговых элементов """
    UNDEFINED = 0
    """ Неопределённый """
    THANKS = 1
    """ Благодарность """
    MISC = 2
    """ Вводные слова, мусор и пр., на что не стоит обращать внимание """
    HELLO = 3
    """ Привет """
    BYE = 4
    """ Пока """
    ACCEPT = 5
    """ Согласие """
    CANCEL = 6
    """ Отказ """
    BUSY = 7
    """ Занят """
    VERB = 8
    """ Глагольная группа """
    LATER = 9
    """ Позже - (например, перезвонить позже) """
    DATE = 10
    """ дата (возможно, относительная) """
    DATERANGE = 11
    """ диапазон дат """
    REPEAT = 12
    """ Просьба повторить """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)