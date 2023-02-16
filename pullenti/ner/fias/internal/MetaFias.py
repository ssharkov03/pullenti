# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils

from pullenti.ner.metadata.ReferentClass import ReferentClass

class MetaFias(ReferentClass):
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.fias.FiasReferent import FiasReferent
        MetaFias._global_meta = MetaFias()
        MetaFias._global_meta.add_feature(FiasReferent.ATTR_NAME, "Название", 1, 1)
        MetaFias._global_meta.add_feature(FiasReferent.ATTR_TYPE, "Тип", 1, 1)
    
    @property
    def name(self) -> str:
        from pullenti.ner.fias.FiasReferent import FiasReferent
        return FiasReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Объект ФИАС"
    
    OBJ_IMAGE_ID = "fiasobj"
    
    HOUSE_IMAGE_ID = "fiashouse"
    
    ROOM_IMAGE_ID = "fiasroom"
    
    STREET_IMAGE_ID = "fiasstreet"
    
    def get_image_id(self, obj : 'Referent'=None) -> str:
        from pullenti.ner.fias.FiasReferent import FiasReferent
        dat = Utils.asObjectOrNull(obj, FiasReferent)
        if (dat is not None): 
            if (dat.is_house): 
                return MetaFias.HOUSE_IMAGE_ID
            if (dat.is_room): 
                return MetaFias.ROOM_IMAGE_ID
            if (dat.is_street): 
                return MetaFias.STREET_IMAGE_ID
        return MetaFias.OBJ_IMAGE_ID
    
    _global_meta = None