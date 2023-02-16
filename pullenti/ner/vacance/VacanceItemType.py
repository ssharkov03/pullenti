# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class VacanceItemType(IntEnum):
    """ Тип элемента вакансии """
    UNDEFINED = 0
    NAME = 1
    """ Наименование вакансии """
    DATE = 2
    """ Актуальная дата """
    MONEY = 3
    """ Предлагаемая зарплата """
    EDUCATION = 4
    """ Требуемое образование """
    EXPERIENCE = 5
    """ Требуемый опыт работы """
    LANGUAGE = 6
    """ Язык(и) """
    DRIVINGLICENSE = 7
    """ Водительские права """
    LICENSE = 8
    """ Какое-то иное удостоверение или права на что-либо """
    MORAL = 9
    """ Моральное качество """
    SKILL = 10
    """ Требуемый навык """
    PLUS = 11
    """ Дополнительный навык (пожелание) """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)