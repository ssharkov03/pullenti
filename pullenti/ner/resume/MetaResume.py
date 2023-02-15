# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils

from pullenti.ner.metadata.ReferentClass import ReferentClass
from pullenti.ner.resume.ResumeItemType import ResumeItemType

class MetaResume(ReferentClass):
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.resume.ResumeItemReferent import ResumeItemReferent
        MetaResume.GLOBAL_META = MetaResume()
        MetaResume.TYPES = MetaResume.GLOBAL_META.add_feature(ResumeItemReferent.ATTR_TYPE, "Тип", 1, 1)
        MetaResume.TYPES.add_value(Utils.enumToString(ResumeItemType.POSITION).lower(), "Позиция", None, None)
        MetaResume.TYPES.add_value(Utils.enumToString(ResumeItemType.AGE).lower(), "Возраст", None, None)
        MetaResume.TYPES.add_value(Utils.enumToString(ResumeItemType.SEX).lower(), "Пол", None, None)
        MetaResume.TYPES.add_value(Utils.enumToString(ResumeItemType.EDUCATION).lower(), "Образование", None, None)
        MetaResume.TYPES.add_value(Utils.enumToString(ResumeItemType.EXPERIENCE).lower(), "Опыт работы", None, None)
        MetaResume.TYPES.add_value(Utils.enumToString(ResumeItemType.LANGUAGE).lower(), "Язык", None, None)
        MetaResume.TYPES.add_value(Utils.enumToString(ResumeItemType.MONEY).lower(), "Зарплата", None, None)
        MetaResume.TYPES.add_value(Utils.enumToString(ResumeItemType.DRIVINGLICENSE).lower(), "Водительские права", None, None)
        MetaResume.TYPES.add_value(Utils.enumToString(ResumeItemType.LICENSE).lower(), "Лицензия", None, None)
        MetaResume.TYPES.add_value(Utils.enumToString(ResumeItemType.SPECIALITY).lower(), "Специальность", None, None)
        MetaResume.TYPES.add_value(Utils.enumToString(ResumeItemType.MORAL).lower(), "Моральное качество", None, None)
        MetaResume.TYPES.add_value(Utils.enumToString(ResumeItemType.SKILL).lower(), "Навык", None, None)
        MetaResume.TYPES.add_value(Utils.enumToString(ResumeItemType.HOBBY).lower(), "Хобби", None, None)
        MetaResume.GLOBAL_META.add_feature(ResumeItemReferent.ATTR_VALUE, "Значение", 0, 1)
        MetaResume.GLOBAL_META.add_feature(ResumeItemReferent.ATTR_REF, "Ссылка", 0, 0)
        MetaResume.GLOBAL_META.add_feature(ResumeItemReferent.ATTR_EXPIRED, "Признак неактуальности", 0, 1)
    
    TYPES = None
    
    @property
    def name(self) -> str:
        from pullenti.ner.resume.ResumeItemReferent import ResumeItemReferent
        return ResumeItemReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Резюме"
    
    IMAGE_ID = "resume"
    
    def get_image_id(self, obj : 'Referent'=None) -> str:
        return MetaResume.IMAGE_ID
    
    GLOBAL_META = None