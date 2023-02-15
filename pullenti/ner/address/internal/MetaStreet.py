# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils

from pullenti.ner.metadata.ReferentClass import ReferentClass
from pullenti.ner.address.StreetKind import StreetKind

class MetaStreet(ReferentClass):
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.address.StreetReferent import StreetReferent
        MetaStreet._global_meta = MetaStreet()
        MetaStreet._global_meta.add_feature(StreetReferent.ATTR_TYPE, "Тип", 0, 0)
        MetaStreet._global_meta.add_feature(StreetReferent.ATTR_KIND, "Класс", 0, 1)
        MetaStreet._global_meta.add_feature(StreetReferent.ATTR_NAME, "Наименование", 0, 0)
        MetaStreet._global_meta.add_feature(StreetReferent.ATTR_NUMBER, "Номер", 0, 1)
        MetaStreet._global_meta.add_feature(StreetReferent.ATTR_SECNUMBER, "Доп.номер", 0, 1)
        MetaStreet._global_meta.add_feature(StreetReferent.ATTR_HIGHER, "Вышележащая улица", 0, 1)
        MetaStreet._global_meta.add_feature(StreetReferent.ATTR_GEO, "Географический объект", 0, 1)
        MetaStreet._global_meta.add_feature(StreetReferent.ATTR_REF, "Ссылка на связанную сущность", 0, 0)
        MetaStreet._global_meta.add_feature(StreetReferent.ATTR_FIAS, "Объект ФИАС", 0, 1)
        MetaStreet._global_meta.add_feature(StreetReferent.ATTR_BTI, "Объект БТИ", 0, 1)
        MetaStreet._global_meta.add_feature(StreetReferent.ATTR_OKM, "Код ОКМ УМ", 0, 1)
    
    @property
    def name(self) -> str:
        from pullenti.ner.address.StreetReferent import StreetReferent
        return StreetReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Улица"
    
    IMAGE_ID = "street"
    
    IMAGE_TERR_ID = "territory"
    
    IMAGE_TERR_ORG_ID = "terrorg"
    
    IMAGE_TERR_SPEC_ID = "terrspec"
    
    def get_image_id(self, obj : 'Referent'=None) -> str:
        from pullenti.ner.address.StreetReferent import StreetReferent
        s = Utils.asObjectOrNull(obj, StreetReferent)
        if (s is not None): 
            if (s.kind == StreetKind.ORG): 
                return MetaStreet.IMAGE_TERR_ORG_ID
            if (s.kind == StreetKind.AREA): 
                return MetaStreet.IMAGE_TERR_ID
            if (s.kind == StreetKind.SPEC): 
                return MetaStreet.IMAGE_TERR_SPEC_ID
        return MetaStreet.IMAGE_ID
    
    _global_meta = None