# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils

from pullenti.ner.metadata.ReferentClass import ReferentClass
from pullenti.ner.vacance.VacanceItemType import VacanceItemType

class MetaVacance(ReferentClass):
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.vacance.VacanceItemReferent import VacanceItemReferent
        MetaVacance.GLOBAL_META = MetaVacance()
        MetaVacance.TYPES = MetaVacance.GLOBAL_META.add_feature(VacanceItemReferent.ATTR_TYPE, "Тип", 1, 1)
        MetaVacance.TYPES.add_value(Utils.enumToString(VacanceItemType.NAME).lower(), "Наименование", None, None)
        MetaVacance.TYPES.add_value(Utils.enumToString(VacanceItemType.DATE).lower(), "Дата", None, None)
        MetaVacance.TYPES.add_value(Utils.enumToString(VacanceItemType.EDUCATION).lower(), "Образование", None, None)
        MetaVacance.TYPES.add_value(Utils.enumToString(VacanceItemType.EXPERIENCE).lower(), "Опыт работы", None, None)
        MetaVacance.TYPES.add_value(Utils.enumToString(VacanceItemType.LANGUAGE).lower(), "Язык", None, None)
        MetaVacance.TYPES.add_value(Utils.enumToString(VacanceItemType.MONEY).lower(), "Зарплата", None, None)
        MetaVacance.TYPES.add_value(Utils.enumToString(VacanceItemType.DRIVINGLICENSE).lower(), "Водительские права", None, None)
        MetaVacance.TYPES.add_value(Utils.enumToString(VacanceItemType.LICENSE).lower(), "Лицензия", None, None)
        MetaVacance.TYPES.add_value(Utils.enumToString(VacanceItemType.MORAL).lower(), "Моральное требование", None, None)
        MetaVacance.TYPES.add_value(Utils.enumToString(VacanceItemType.SKILL).lower(), "Требование", None, None)
        MetaVacance.TYPES.add_value(Utils.enumToString(VacanceItemType.PLUS).lower(), "Пожелание", None, None)
        MetaVacance.GLOBAL_META.add_feature(VacanceItemReferent.ATTR_VALUE, "Значение", 0, 1)
        MetaVacance.GLOBAL_META.add_feature(VacanceItemReferent.ATTR_REF, "Ссылка", 0, 0)
        MetaVacance.GLOBAL_META.add_feature(VacanceItemReferent.ATTR_EXPIRED, "Признак неактуальности", 0, 1)
    
    TYPES = None
    
    @property
    def name(self) -> str:
        from pullenti.ner.vacance.VacanceItemReferent import VacanceItemReferent
        return VacanceItemReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Вакансия"
    
    IMAGE_ID = "vacance"
    
    def get_image_id(self, obj : 'Referent'=None) -> str:
        return MetaVacance.IMAGE_ID
    
    GLOBAL_META = None