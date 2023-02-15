# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class GarLevel(IntEnum):
    """ Уровень адресного объекта """
    UNDEFINED = 0
    REGION = 1
    """ Субъект РФ (регион) """
    ADMINAREA = 2
    """ Административный район """
    MUNICIPALAREA = 3
    """ Муниципальный район """
    SETTLEMENT = 4
    """ Сельское/городское поселение """
    CITY = 5
    """ Город """
    LOCALITY = 6
    """ Населенный пункт """
    AREA = 7
    """ Элемент планировочной структуры """
    STREET = 8
    """ Элемент улично-дорожной сети """
    PLOT = 9
    """ Земельный участок """
    BUILDING = 10
    """ Здание (сооружение) """
    ROOM = 11
    """ Помещение """
    CARPLACE = 17
    """ Машино-место """
    COUNTRY = 100
    """ Страна (в ГАР нет, но нужно в других местах) """
    SPECIAL = 200
    """ Специфический объект (например, пересечение улиц или указатель на что-то) """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)