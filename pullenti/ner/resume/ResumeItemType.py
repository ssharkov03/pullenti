# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class ResumeItemType(IntEnum):
    """ Тип элемента резюме """
    UNDEFINED = 0
    POSITION = 1
    """ Искомая рабочая позиция """
    SEX = 2
    """ Пол """
    AGE = 3
    """ Возраст """
    MONEY = 4
    """ Ожидаемая зарплата """
    EDUCATION = 5
    """ Образование """
    EXPERIENCE = 6
    """ Опыт работы """
    LANGUAGE = 7
    """ Язык(и) """
    DRIVINGLICENSE = 8
    """ Водительские права """
    LICENSE = 9
    """ Какое-то иное удостоверение или права на что-либо """
    SPECIALITY = 10
    """ Специализация """
    SKILL = 11
    """ Навык """
    MORAL = 12
    """ Моральное качество """
    HOBBY = 13
    """ Хобби """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)