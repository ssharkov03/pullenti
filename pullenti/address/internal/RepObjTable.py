# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.address.GarLevel import GarLevel
from pullenti.util.repository.KeyBaseTable import KeyBaseTable
from pullenti.util.repository.BaseTable import BaseTable
from pullenti.address.RepaddrObject import RepaddrObject

class RepObjTable(KeyBaseTable):
    
    def __init__(self, typs : 'RepTypTable', base_dir : str, name_ : str="objs") -> None:
        super().__init__(None, name_, base_dir)
        self.__m_typs = None;
        self.__m_typs = typs
    
    def add(self, id0_ : int, r : 'RepaddrObject') -> None:
        r.id0_ = id0_
        res = bytearray()
        self.__store(res, r)
        dat = bytearray(res)
        self.write_key_data(id0_, dat)
    
    def __store(self, res : bytearray, ao : 'RepaddrObject') -> None:
        attr = 0
        res.append(attr)
        res.append(ao.level)
        BaseTable.get_bytes_for_string(res, ao.spelling, None)
        res.extend((len(ao.types)).to_bytes(2, byteorder="little"))
        for ty in ao.types: 
            res.extend((self.__m_typs.get_id(ty)).to_bytes(2, byteorder="little"))
        if (ao.parents is None or len(ao.parents) == 0): 
            res.extend((0).to_bytes(2, byteorder="little"))
        else: 
            res.extend((len(ao.parents)).to_bytes(2, byteorder="little"))
            for p in ao.parents: 
                res.extend((p).to_bytes(4, byteorder="little"))
        if (ao.gar_guids is None or len(ao.gar_guids) == 0): 
            res.extend((0).to_bytes(2, byteorder="little"))
        else: 
            res.extend((len(ao.gar_guids)).to_bytes(2, byteorder="little"))
            for p in ao.gar_guids: 
                BaseTable.get_bytes_for_string(res, p, None)
    
    def get(self, id0_ : int) -> 'RepaddrObject':
        dat = self.read_key_data(id0_, 0)
        if (dat is None): 
            return None
        r = RepaddrObject()
        r.id0_ = id0_
        ind = 0
        wrapind126 = RefOutArgWrapper(ind)
        self.__restore(dat, r, wrapind126)
        ind = wrapind126.value
        return r
    
    def __restore(self, data : bytearray, ao : 'RepaddrObject', ind : int) -> bool:
        attr = data[ind.value]
        ind.value += 1
        cou = data[ind.value]
        ind.value += 1
        ao.level = (Utils.valToEnum(cou, GarLevel))
        ao.spelling = BaseTable.get_string_for_bytes(data, ind, False, None)
        cou = (int.from_bytes(data[ind.value:ind.value+2], byteorder="little"))
        ind.value += 2
        while cou > 0: 
            id0_ = int.from_bytes(data[ind.value:ind.value+2], byteorder="little")
            ind.value += 2
            ty = self.__m_typs.get_typ(id0_)
            if (ty is not None): 
                ao.types.append(ty)
            cou -= 1
        cou = (int.from_bytes(data[ind.value:ind.value+2], byteorder="little"))
        ind.value += 2
        while cou > 0: 
            if (ao.parents is None): 
                ao.parents = list()
            ao.parents.append(int.from_bytes(data[ind.value:ind.value+4], byteorder="little"))
            ind.value += 4
            cou -= 1
        cou = (int.from_bytes(data[ind.value:ind.value+2], byteorder="little"))
        ind.value += 2
        while cou > 0: 
            if (ao.gar_guids is None): 
                ao.gar_guids = list()
            s = BaseTable.get_string_for_bytes(data, ind, False, None)
            ao.gar_guids.append(s)
            cou -= 1
        return True