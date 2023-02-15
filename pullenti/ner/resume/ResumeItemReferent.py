# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.IntOntologyItem import IntOntologyItem
from pullenti.ner.resume.ResumeItemType import ResumeItemType
from pullenti.ner.metadata.ReferentClass import ReferentClass
from pullenti.ner.resume.MetaResume import MetaResume
from pullenti.ner.Referent import Referent

class ResumeItemReferent(Referent):
    """ Элемент резюме """
    
    def __init__(self) -> None:
        super().__init__(ResumeItemReferent.OBJ_TYPENAME)
        self.instance_of = MetaResume.GLOBAL_META
    
    OBJ_TYPENAME = "RESUME"
    """ Имя типа сущности TypeName ("RESUME") """
    
    ATTR_TYPE = "TYPE"
    """ Имя атрибута - тип элемента (см. ResumeItemType) """
    
    ATTR_VALUE = "VALUE"
    """ Имя атрибута - значение """
    
    ATTR_REF = "REF"
    """ Имя атрибута - ссылка на сущность """
    
    ATTR_EXPIRED = "EXPIRED"
    """ Имя атрибута - признак снятия резюме """
    
    @property
    def typ(self) -> 'ResumeItemType':
        """ Тип элемента """
        str0_ = self.get_string_value(ResumeItemReferent.ATTR_TYPE)
        if (str0_ is None): 
            return ResumeItemType.UNDEFINED
        try: 
            return Utils.valToEnum(str0_, ResumeItemType)
        except Exception as ex2430: 
            pass
        return ResumeItemType.UNDEFINED
    @typ.setter
    def typ(self, value_) -> 'ResumeItemType':
        self.add_slot(ResumeItemReferent.ATTR_TYPE, Utils.enumToString(value_).lower(), True, 0)
        return value_
    
    @property
    def value(self) -> str:
        """ Значение элемента """
        return self.get_string_value(ResumeItemReferent.ATTR_VALUE)
    @value.setter
    def value(self, value_) -> str:
        self.add_slot(ResumeItemReferent.ATTR_VALUE, value_, True, 0)
        return value_
    
    @property
    def ref(self) -> 'Referent':
        """ Ссылка на сущность, если есть """
        return Utils.asObjectOrNull(self.get_slot_value(ResumeItemReferent.ATTR_REF), Referent)
    @ref.setter
    def ref(self, value_) -> 'Referent':
        self.add_slot(ResumeItemReferent.ATTR_REF, value_, True, 0)
        return value_
    
    @property
    def expired(self) -> bool:
        """ Признак снятия вакансии """
        return self.get_string_value(ResumeItemReferent.ATTR_EXPIRED) == "true"
    @expired.setter
    def expired(self, value_) -> bool:
        self.add_slot(ResumeItemReferent.ATTR_EXPIRED, ("true" if value_ else None), True, 0)
        return value_
    
    def to_string_ex(self, short_variant : bool, lang : 'MorphLang'=None, lev : int=0) -> str:
        tmp = io.StringIO()
        print("{0}: ".format(MetaResume.TYPES.convert_inner_value_to_outer_value(self.get_string_value(ResumeItemReferent.ATTR_TYPE), None)), end="", file=tmp, flush=True)
        if (self.value is not None): 
            print(self.value, end="", file=tmp)
        elif (self.ref is not None): 
            print(self.ref.to_string_ex(short_variant, lang, lev + 1), end="", file=tmp)
        if (self.expired): 
            print(" (не актуально)", end="", file=tmp)
        return Utils.toStringStringIO(tmp)
    
    def create_ontology_item(self) -> 'IntOntologyItem':
        oi = IntOntologyItem(self)
        oi.termins.append(Termin(self.value))
        return oi