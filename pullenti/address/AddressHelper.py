# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils

from pullenti.address.RoomType import RoomType
from pullenti.address.SpecialType import SpecialType
from pullenti.address.StroenType import StroenType
from pullenti.address.GarLevel import GarLevel
from pullenti.address.HouseType import HouseType

class AddressHelper:
    """ Разные полезные функции """
    
    @staticmethod
    def get_level_string(level : 'GarLevel') -> str:
        if (level == GarLevel.REGION): 
            return "субъект РФ (регион)"
        if (level == GarLevel.ADMINAREA): 
            return "административный район"
        if (level == GarLevel.MUNICIPALAREA): 
            return "муниципальный район"
        if (level == GarLevel.SETTLEMENT): 
            return "сельское/городское поселение"
        if (level == GarLevel.CITY): 
            return "город"
        if (level == GarLevel.LOCALITY): 
            return "населенный пункт"
        if (level == GarLevel.AREA): 
            return "элемент планировочной структуры"
        if (level == GarLevel.STREET): 
            return "элемент улично-дорожной сети"
        if (level == GarLevel.PLOT): 
            return "земельный участок"
        if (level == GarLevel.BUILDING): 
            return "здание (сооружение)"
        if (level == GarLevel.ROOM): 
            return "помещение"
        if (level == GarLevel.CARPLACE): 
            return "машино-место"
        return Utils.enumToString(level)
    
    @staticmethod
    def get_level_image_name(level : 'GarLevel') -> str:
        if (level == GarLevel.REGION or level == GarLevel.COUNTRY): 
            return "region"
        if (level == GarLevel.ADMINAREA): 
            return "admin"
        if (level == GarLevel.MUNICIPALAREA): 
            return "municipal"
        if (level == GarLevel.SETTLEMENT): 
            return "settlement"
        if (level == GarLevel.CITY): 
            return "city"
        if (level == GarLevel.LOCALITY): 
            return "locality"
        if (level == GarLevel.AREA): 
            return "area"
        if (level == GarLevel.STREET): 
            return "street"
        if (level == GarLevel.PLOT): 
            return "plot"
        if (level == GarLevel.BUILDING): 
            return "building"
        if (level == GarLevel.ROOM): 
            return "room"
        if (level == GarLevel.CARPLACE): 
            return "carplace"
        return "undefined"
    
    @staticmethod
    def get_house_type_string(ty : 'HouseType', short_val : bool) -> str:
        if (ty == HouseType.ESTATE): 
            return ("влад." if short_val else "владение")
        if (ty == HouseType.HOUSEESTATE): 
            return ("дмвлд." if short_val else "домовладение")
        if (ty == HouseType.HOUSE): 
            return ("д." if short_val else "дом")
        if (ty == HouseType.PLOT): 
            return ("уч." if short_val else "участок")
        if (ty == HouseType.GARAGE): 
            return ("гар." if short_val else "гараж")
        return "?"
    
    @staticmethod
    def get_stroen_type_string(ty : 'StroenType', short_val : bool) -> str:
        if (ty == StroenType.CONSTRUCTION): 
            return ("сооруж." if short_val else "сооружение")
        if (ty == StroenType.LITER): 
            return ("лит." if short_val else "литера")
        return ("стр." if short_val else "строение")
    
    @staticmethod
    def get_room_type_string(ty : 'RoomType', short_val : bool) -> str:
        if (ty == RoomType.FLAT): 
            return ("кв." if short_val else "квартира")
        if (ty == RoomType.OFFICE): 
            return ("оф." if short_val else "офис")
        if (ty == RoomType.ROOM): 
            return ("комн." if short_val else "комната")
        if (ty == RoomType.SPACE or ty == RoomType.UNDEFINED): 
            return ("помещ." if short_val else "помещение")
        if (ty == RoomType.GARAGE): 
            return ("гар." if short_val else "гараж")
        if (ty == RoomType.CARPLACE): 
            return ("маш.м." if short_val else "машиноместо")
        if (ty == RoomType.PAVILION): 
            return ("пав." if short_val else "павильон")
        return "?"
    
    IMAGES = None
    """ Картинки (иконки) для ГАР-объектов """
    
    @staticmethod
    def find_image(image_id : str) -> 'ImageWrapper':
        """ Найти картинку по идентификатору
        
        Args:
            image_id(str): Id картинки
        
        Returns:
            ImageWrapper: обёртка
        """
        for img in AddressHelper.IMAGES: 
            if (Utils.compareStrings(img.id0_, image_id, True) == 0): 
                return img
        return None
    
    @staticmethod
    def is_spec_type_direction(typ : 'SpecialType') -> bool:
        """ Проверка, что спецтип является направлением
        
        Args:
            typ(SpecialType): 
        
        """
        if ((typ == SpecialType.NORTH or typ == SpecialType.EAST or typ == SpecialType.WEST) or typ == SpecialType.SOUTH): 
            return True
        if ((typ == SpecialType.NORTHEAST or typ == SpecialType.NORTHWEST or typ == SpecialType.SOUTHEAST) or typ == SpecialType.SOUTHWEST): 
            return True
        return False
    
    @staticmethod
    def get_spec_type_string(typ : 'SpecialType') -> str:
        if (typ == SpecialType.NEAR): 
            return "вблизи"
        if (typ == SpecialType.NORTH): 
            return "на север"
        if (typ == SpecialType.WEST): 
            return "на запад"
        if (typ == SpecialType.SOUTH): 
            return "на юг"
        if (typ == SpecialType.EAST): 
            return "на восток"
        if (typ == SpecialType.NORTHEAST): 
            return "на северо-восток"
        if (typ == SpecialType.NORTHWEST): 
            return "на северо-запад"
        if (typ == SpecialType.SOUTHEAST): 
            return "на юго-восток"
        if (typ == SpecialType.SOUTHWEST): 
            return "на юго-запад"
        return Utils.enumToString(typ)
    
    # static constructor for class AddressHelper
    @staticmethod
    def _static_ctor():
        AddressHelper.IMAGES = list()

AddressHelper._static_ctor()