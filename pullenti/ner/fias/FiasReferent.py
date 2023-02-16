# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.core.ReferentsEqualType import ReferentsEqualType
from pullenti.ner.address.AddressHouseType import AddressHouseType
from pullenti.ner.Referent import Referent
from pullenti.ner.metadata.ReferentClass import ReferentClass
from pullenti.ner.fias.internal.MetaFias import MetaFias

class FiasReferent(Referent):
    """ Обертка над объектом ГИС ФИАС """
    
    def __init__(self) -> None:
        super().__init__(FiasReferent.OBJ_TYPENAME)
        self._can_be_wrong = False
        self.fias_obj = None;
        self.instance_of = MetaFias._global_meta
    
    OBJ_TYPENAME = "FIAS"
    
    ATTR_OWNER = "OWNER"
    
    ATTR_NAME = "NAME"
    
    ATTR_TYPE = "TYPE"
    
    ATTR_LEVEL = "LEV"
    
    ATTR_UNOM = "UNOM"
    
    ATTR_CADNUM = "CADNUM"
    
    ATTR_HOUSENUM = "HOUSENUM"
    
    ATTR_HOUSETYP = "HOUSETYP"
    
    ATTR_STRNUM = "STRNUM"
    
    ATTR_STRTYP = "STRTYP"
    
    ATTR_BUILDNUM = "BUILDNUM"
    
    ATTR_FLATNUM = "FLATNUM"
    
    ATTR_FLATTYP = "FLATTYP"
    
    ATTR_ROOMNUM = "ROOMNUM"
    
    ATTR_ROOMTYP = "ROOMTYP"
    
    ATTR_STATUS = "STATUS"
    
    ATTR_CODE = "CODE"
    
    def _set_by_address_object(self, ao : 'AddressObject') -> None:
        for n in ao.names: 
            self.add_slot(FiasReferent.ATTR_NAME, n, False, 0)
        if (ao.typ is not None): 
            self.add_slot(FiasReferent.ATTR_TYPE, ao.typ.name, False, 0)
        if (ao.old_typ is not None and ao.old_typ != ao.typ and ao.old_typ.name != ao.typ.name): 
            self.add_slot(FiasReferent.ATTR_TYPE, ao.old_typ.name, False, 0)
        if (ao.level != (0)): 
            self.add_slot(FiasReferent.ATTR_LEVEL, str(ao.level), False, 0)
        if (not ao.actual): 
            self.add_slot(FiasReferent.ATTR_STATUS, "expired", True, 0)
        self.tag = (ao)
        self.fias_obj = (ao)
    
    def _set_by_house_object(self, ho : 'HouseObject') -> None:
        if (ho.house_number is not None): 
            self.add_slot(FiasReferent.ATTR_HOUSENUM, ho.house_number, False, 0)
            self.add_slot(FiasReferent.ATTR_HOUSETYP, ho.house_typ, False, 0)
        if (ho.build_number is not None): 
            self.add_slot(FiasReferent.ATTR_BUILDNUM, ho.build_number, False, 0)
        if (ho.struc_number is not None): 
            self.add_slot(FiasReferent.ATTR_STRNUM, ho.struc_number, False, 0)
            self.add_slot(FiasReferent.ATTR_STRTYP, ho.struc_typ, False, 0)
        if (not ho.actual): 
            self.add_slot(FiasReferent.ATTR_STATUS, "expired", True, 0)
        self.fias_obj = (ho)
    
    def _set_by_room_object(self, ho : 'RoomObject') -> None:
        if (ho.flat_number is not None): 
            self.add_slot(FiasReferent.ATTR_FLATNUM, ho.flat_number, False, 0)
            self.add_slot(FiasReferent.ATTR_FLATTYP, ho.flat_typ, False, 0)
        if (ho.room_number is not None): 
            self.add_slot(FiasReferent.ATTR_ROOMNUM, ho.room_typ, False, 0)
            self.add_slot(FiasReferent.ATTR_ROOMTYP, ho.room_typ, False, 0)
        if (not ho.actual): 
            self.add_slot(FiasReferent.ATTR_STATUS, "expired", True, 0)
        self.fias_obj = (ho)
    
    def to_string_ex(self, short_variant : bool, lang : 'MorphLang'=None, lev : int=0) -> str:
        if (not self.is_house and not self.is_room): 
            ty0 = self.get_string_value(FiasReferent.ATTR_TYPE)
            na0 = self.get_string_value(FiasReferent.ATTR_NAME)
            if (ty0 is not None and na0 is not None and ty0 in na0): 
                ty0 = (None)
            res1 = (na0 if ty0 is None else "{0} {1}".format(ty0, Utils.ifNotNull(na0, "")))
            return res1
        res = io.StringIO()
        num = self.get_string_value(FiasReferent.ATTR_HOUSENUM)
        if (num is not None): 
            if (res.tell() > 0): 
                print(' ', end="", file=res)
            ty = self.get_string_value(FiasReferent.ATTR_HOUSETYP)
            if (ty == "1"): 
                print("вл.", end="", file=res)
            elif (ty == "3"): 
                print("двлд.", end="", file=res)
            elif (ty == "4"): 
                print("гар.", end="", file=res)
            elif (ty == "5"): 
                print("уч.", end="", file=res)
            else: 
                print("д.", end="", file=res)
            print(num, end="", file=res)
        num = self.get_string_value(FiasReferent.ATTR_BUILDNUM)
        if ((num) is not None): 
            if (res.tell() > 0): 
                print(' ', end="", file=res)
            print("корп.{0}".format(num), end="", file=res, flush=True)
        num = self.get_string_value(FiasReferent.ATTR_STRNUM)
        if ((num) is not None): 
            if (res.tell() > 0): 
                print(' ', end="", file=res)
            ty = self.get_string_value(FiasReferent.ATTR_STRTYP)
            if (ty == "2"): 
                print("сооруж.", end="", file=res)
            elif (ty == "3"): 
                print("лит.", end="", file=res)
            else: 
                print("стр.", end="", file=res)
            print(num, end="", file=res)
        flat = self.get_string_value(FiasReferent.ATTR_FLATNUM)
        if (flat is not None): 
            if (res.tell() > 0): 
                print(' ', end="", file=res)
            print("кв.{0}".format(flat), end="", file=res, flush=True)
        flat = self.get_string_value(FiasReferent.ATTR_ROOMNUM)
        if ((flat) is not None): 
            if (res.tell() > 0): 
                print(' ', end="", file=res)
            print("комн.{0}".format(flat), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    @property
    def parent_referent(self) -> 'Referent':
        return Utils.asObjectOrNull(self.get_slot_value(FiasReferent.ATTR_OWNER), Referent)
    
    @property
    def unom(self) -> int:
        """ Это для объекта БТИ ставится UNOM, а не GUID """
        str0_ = self.get_string_value(FiasReferent.ATTR_UNOM)
        if (str0_ is None): 
            return 0
        u = 0
        wrapu1044 = RefOutArgWrapper(0)
        inoutres1045 = Utils.tryParseInt(str0_, wrapu1044)
        u = wrapu1044.value
        if (inoutres1045): 
            return u
        return 0
    
    @property
    def is_house(self) -> bool:
        return self.find_slot(FiasReferent.ATTR_HOUSENUM, None, True) is not None or self.find_slot(FiasReferent.ATTR_BUILDNUM, None, True) is not None or self.find_slot(FiasReferent.ATTR_STRNUM, None, True) is not None
    
    @property
    def is_room(self) -> bool:
        return self.find_slot(FiasReferent.ATTR_FLATNUM, None, True) is not None or self.find_slot(FiasReferent.ATTR_ROOMNUM, None, True) is not None
    
    @property
    def is_street(self) -> bool:
        lev = self.get_string_value(FiasReferent.ATTR_LEVEL)
        return lev == "7"
    
    def can_be_equals(self, obj : 'Referent', typ : 'ReferentsEqualType'=ReferentsEqualType.WITHINONETEXT) -> bool:
        f = Utils.asObjectOrNull(obj, FiasReferent)
        if (f is None): 
            return False
        if (f.unom > 0 or self.unom > 0): 
            return f.unom == self.unom
        return f == self
    
    def _calc_equal_coef(self, adr : 'AddressReferent') -> int:
        """ Это используется при отбраковке, если получились несколько вариантов
        
        Args:
            adr(AddressReferent): 
        
        """
        coef = 0
        n1 = adr.house
        n2 = self.get_string_value(FiasReferent.ATTR_HOUSENUM)
        if (n1 is not None or n2 is not None): 
            if (n1 == n2): 
                coef += 1
            typ = adr.house_type
            tt = self.get_string_value(FiasReferent.ATTR_HOUSETYP)
            if (typ == AddressHouseType.HOUSE): 
                if (tt != "2"): 
                    coef -= 1
            elif (typ == AddressHouseType.ESTATE): 
                if (tt != "1"): 
                    coef -= 1
            elif (typ == AddressHouseType.HOUSEESTATE): 
                if (tt != "3"): 
                    coef -= 1
        n1 = adr.corpus
        n2 = self.get_string_value(FiasReferent.ATTR_BUILDNUM)
        if (n1 is not None or n2 is not None): 
            if (n1 == n2): 
                coef += 1
        n1 = adr.building
        n2 = self.get_string_value(FiasReferent.ATTR_STRNUM)
        if (n1 is not None or n2 is not None): 
            if (n2 is not None and n2.endswith("Б/Н")): 
                n2 = n2[0:0+len(n2) - 3]
            if (n1 == n2): 
                coef += 1
            else: 
                coef -= 1
        return coef