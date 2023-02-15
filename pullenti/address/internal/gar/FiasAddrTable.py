# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.util.repository.KeyBaseTable import KeyBaseTable
from pullenti.address.internal.FiasHelper import FiasHelper
from pullenti.address.internal.gar.AddressObjectStatus import AddressObjectStatus

class FiasAddrTable(KeyBaseTable):
    
    def __init__(self, rep : 'IRepository', name_ : str="addressobjects") -> None:
        super().__init__(rep, name_, None)
    
    def add(self, id0_ : int, doc : 'AddressObject', only_attrs : bool) -> None:
        dat = self.__store(doc)
        self.write_key_data(id0_, dat)
    
    def __store(self, ao : 'AddressObject') -> bytearray:
        res = bytearray()
        attr = ((0 if ao.actual else 1))
        if (ao.status == AddressObjectStatus.WARNING): 
            attr |= (2)
        elif (ao.status == AddressObjectStatus.ERROR): 
            attr |= (4)
        if (ao.has_sec_object): 
            attr |= (8)
        res.append(attr)
        res.extend((((0 if ao.typ is None else ao.typ.id0_))).to_bytes(2, byteorder="little"))
        res.extend((((0 if ao.old_typ is None else ao.old_typ.id0_))).to_bytes(2, byteorder="little"))
        res.extend((len(ao.parents_id)).to_bytes(2, byteorder="little"))
        if (len(ao.parents_id) > 0): 
            for id0_ in ao.parents_id: 
                res.extend((id0_).to_bytes(4, byteorder="little"))
            res.extend((ao.alt_parent_id).to_bytes(4, byteorder="little"))
            if (ao.alt_parent_id > 0): 
                pass
        res.extend((ao.level).to_bytes(2, byteorder="little"))
        res.extend((len(ao.names)).to_bytes(2, byteorder="little"))
        for n in ao.names: 
            FiasAddrTable.__get_bytes_for_string1251(res, n)
        res.extend((len(ao.children_ids)).to_bytes(4, byteorder="little"))
        for id0_ in ao.children_ids: 
            res.extend((id0_).to_bytes(4, byteorder="little"))
        res.extend((ao.unom).to_bytes(4, byteorder="little"))
        res.append(ao.region)
        FiasAddrTable.__get_bytes_for_string1251(res, ao.guid)
        return bytearray(res)
    
    def get(self, id0_ : int, ao : 'AddressObject', typs : typing.List[tuple]) -> bool:
        dat = self.read_key_data(id0_, 0)
        if (dat is None): 
            return False
        ao.id0_ = id0_
        return self.__restore(dat, ao, typs)
    
    def get_parent_id(self, id0_ : int) -> int:
        data = self.read_key_data(id0_, 11)
        if (data is None): 
            return 0
        ind = 5
        cou = int.from_bytes(data[ind:ind+2], byteorder="little")
        ind += 2
        if (cou == 0): 
            return 0
        return int.from_bytes(data[ind:ind+4], byteorder="little")
    
    def get_actual(self, id0_ : int) -> int:
        data = self.read_key_data(id0_, 1)
        if (data is None): 
            return -1
        return (0 if ((((data[0]) & 1)) != 0) else 1)
    
    def __restore(self, data : bytearray, ao : 'AddressObject', typs : typing.List[tuple]) -> bool:
        if ((((data[0]) & 1)) != 0): 
            ao.actual = False
        else: 
            ao.actual = True
        if ((((data[0]) & 2)) != 0): 
            ao.status = AddressObjectStatus.WARNING
        if ((((data[0]) & 4)) != 0): 
            ao.status = AddressObjectStatus.ERROR
        if ((((data[0]) & 8)) != 0): 
            ao.has_sec_object = True
        ind = 1
        id0_ = int.from_bytes(data[ind:ind+2], byteorder="little")
        ind += 2
        ty = None
        wrapty27 = RefOutArgWrapper(None)
        inoutres28 = Utils.tryGetValue(typs, id0_, wrapty27)
        ty = wrapty27.value
        if (inoutres28): 
            ao.typ = ty
        id0_ = (int.from_bytes(data[ind:ind+2], byteorder="little"))
        ind += 2
        if (id0_ != 0): 
            wrapty23 = RefOutArgWrapper(None)
            inoutres24 = Utils.tryGetValue(typs, id0_, wrapty23)
            ty = wrapty23.value
            if (inoutres24): 
                ao.old_typ = ty
        cou = int.from_bytes(data[ind:ind+2], byteorder="little")
        ind += 2
        if (cou > 0): 
            while cou > 0: 
                ao.parents_id.append(int.from_bytes(data[ind:ind+4], byteorder="little"))
                ind += 4
                cou -= 1
            ao.alt_parent_id = int.from_bytes(data[ind:ind+4], byteorder="little")
            ind += 4
            if (ao.alt_parent_id > 0): 
                pass
        ao.level = int.from_bytes(data[ind:ind+2], byteorder="little")
        ind += 2
        cou = (int.from_bytes(data[ind:ind+2], byteorder="little"))
        ind += 2
        while cou > 0: 
            wrapind25 = RefOutArgWrapper(ind)
            ao.names.append(FiasAddrTable.__to_string1251(data, wrapind25))
            ind = wrapind25.value
            cou -= 1
        cou = int.from_bytes(data[ind:ind+4], byteorder="little")
        ind += 4
        while cou > 0: 
            ao.children_ids.append(int.from_bytes(data[ind:ind+4], byteorder="little"))
            ind += 4
            cou -= 1
        ao.unom = int.from_bytes(data[ind:ind+4], byteorder="little")
        ind += 4
        ao.region = data[ind]
        ind += 1
        if (ind < len(data)): 
            wrapind26 = RefOutArgWrapper(ind)
            ao.guid = FiasAddrTable.__to_string1251(data, wrapind26)
            ind = wrapind26.value
        return True
    
    @staticmethod
    def __to_string1251(data : bytearray, ind : int) -> str:
        if ((ind.value + 2) > len(data)): 
            return None
        len0_ = int.from_bytes(data[ind.value:ind.value+2], byteorder="little")
        ind.value += 2
        if (len0_ <= (0)): 
            return None
        if ((ind.value + (len0_)) > len(data)): 
            return None
        res = FiasHelper.decode_string1251(data, ind.value, len0_)
        ind.value += (len0_)
        return res
    
    @staticmethod
    def __get_bytes_for_string1251(res : bytearray, str0_ : str) -> None:
        if (Utils.isNullOrEmpty(str0_)): 
            res.extend((0).to_bytes(2, byteorder="little"))
        else: 
            b = FiasHelper.encode_string1251(str0_)
            res.extend((len(b)).to_bytes(2, byteorder="little"))
            res.extend(b)