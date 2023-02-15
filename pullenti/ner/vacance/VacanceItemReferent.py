# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

from pullenti.ner.vacance.VacanceItemType import VacanceItemType
from pullenti.ner.Referent import Referent
from pullenti.ner.metadata.ReferentClass import ReferentClass
from pullenti.ner.vacance.MetaVacance import MetaVacance

class VacanceItemReferent(Referent):
    """ Элемент вакансии """
    
    def __init__(self) -> None:
        super().__init__(VacanceItemReferent.OBJ_TYPENAME)
        self.instance_of = MetaVacance.GLOBAL_META
    
    OBJ_TYPENAME = "VACANCY"
    """ Имя типа сущности TypeName ("VACANCY") """
    
    ATTR_TYPE = "TYPE"
    """ Имя атрибута - тип элемента (см. VacanceItemType) """
    
    ATTR_VALUE = "VALUE"
    """ Имя атрибута - значение """
    
    ATTR_REF = "REF"
    """ Имя атрибута - ссылка на сущность """
    
    ATTR_EXPIRED = "EXPIRED"
    """ Имя атрибута - признак снятия вакансии """
    
    @property
    def typ(self) -> 'VacanceItemType':
        """ Тип элемента """
        str0_ = self.get_string_value(VacanceItemReferent.ATTR_TYPE)
        if (str0_ is None): 
            return VacanceItemType.UNDEFINED
        try: 
            return Utils.valToEnum(str0_, VacanceItemType)
        except Exception as ex2533: 
            pass
        return VacanceItemType.UNDEFINED
    @typ.setter
    def typ(self, value_) -> 'VacanceItemType':
        self.add_slot(VacanceItemReferent.ATTR_TYPE, Utils.enumToString(value_).lower(), True, 0)
        return value_
    
    @property
    def value(self) -> str:
        """ Значение элемента """
        return self.get_string_value(VacanceItemReferent.ATTR_VALUE)
    @value.setter
    def value(self, value_) -> str:
        self.add_slot(VacanceItemReferent.ATTR_VALUE, value_, True, 0)
        return value_
    
    @property
    def ref(self) -> 'Referent':
        """ Ссылка на сущность, если есть """
        return Utils.asObjectOrNull(self.get_slot_value(VacanceItemReferent.ATTR_REF), Referent)
    @ref.setter
    def ref(self, value_) -> 'Referent':
        self.add_slot(VacanceItemReferent.ATTR_REF, value_, True, 0)
        return value_
    
    @property
    def expired(self) -> bool:
        """ Признак снятия вакансии """
        return self.get_string_value(VacanceItemReferent.ATTR_EXPIRED) == "true"
    @expired.setter
    def expired(self, value_) -> bool:
        self.add_slot(VacanceItemReferent.ATTR_EXPIRED, ("true" if value_ else None), True, 0)
        return value_
    
    def to_string_ex(self, short_variant : bool, lang : 'MorphLang'=None, lev : int=0) -> str:
        tmp = io.StringIO()
        print("{0}: ".format(MetaVacance.TYPES.convert_inner_value_to_outer_value(self.get_string_value(VacanceItemReferent.ATTR_TYPE), None)), end="", file=tmp, flush=True)
        if (self.value is not None): 
            print(self.value, end="", file=tmp)
        elif (self.ref is not None): 
            print(self.ref.to_string_ex(short_variant, lang, lev + 1), end="", file=tmp)
            if (self.typ == VacanceItemType.MONEY): 
                for s in self.slots: 
                    if (s.type_name == VacanceItemReferent.ATTR_REF and s.value != self.ref): 
                        print("-{0}".format(s.value.to_string_ex(short_variant, lang, lev + 1)), end="", file=tmp, flush=True)
                        break
        if (self.expired): 
            print(" (не актуальна)", end="", file=tmp)
        return Utils.toStringStringIO(tmp)