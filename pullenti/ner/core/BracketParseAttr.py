# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class BracketParseAttr(IntEnum):
    """ Атрибуты выделения последовательности между скобок-кавычек. Битовая маска.
    Атрибуты выделения скобок и кавычек
    """
    NO = 0
    """ Нет """
    CANCONTAINSVERBS = 2
    """ По умолчанию, посл-ть не должна содержать чистых глаголов (если есть, то null).
    Почему так? Да потому, что это используется в основном для имён у именованных
    сущностей, а там не может быть глаголов.
    Если же этот ключ указан, то глаголы не проверяются. """
    NEARCLOSEBRACKET = 4
    """ Брать первую же подходящую закрывающую кавычку. Если не задано, то может искать сложные
    случаи вложенных кавычек. """
    CANBEMANYLINES = 8
    """ Внутри могут быть переходы на новую строку (многострочный) """
    INTERNALUSAGE = 0x10
    # Для внутреннего использования
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)