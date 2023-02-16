# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class SpecialType(IntEnum):
    """ Типы спецобъектов """
    UNDEFINED = 0
    NEAR = 1
    """ Около, в районе """
    NORTH = 2
    """ Направление на север """
    EAST = 3
    """ Направление на восток """
    SOUTH = 4
    """ Направление на юг """
    WEST = 5
    """ Направление на запад """
    NORTHWEST = 6
    """ Направление на северо-запад """
    NORTHEAST = 7
    """ Направление на северо-восток """
    SOUTHWEST = 8
    """ Направление на юго-запад """
    SOUTHEAST = 9
    """ Направление на юго-восток """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)