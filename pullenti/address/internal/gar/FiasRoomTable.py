# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.util.repository.KeyBaseTable import KeyBaseTable
from pullenti.address.internal.gar.RoomObject import RoomObject
from pullenti.util.repository.BaseTable import BaseTable

class FiasRoomTable(KeyBaseTable):
    
    def __init__(self, rep : 'IRepository', name_ : str="roomobjects") -> None:
        super().__init__(rep, name_, None)
    
    def add(self, id0_ : int, r : 'RoomObject') -> None:
        res = bytearray()
        self.__store(res, r)
        dat = bytearray(res)
        self.write_key_data(id0_, dat)
    
    def __store(self, res : bytearray, ao : 'RoomObject') -> None:
        attr = ((0 if ao.actual else 1))
        res.append(attr)
        res.extend((ao.house_id).to_bytes(4, byteorder="little"))
        res.append(ao.flat_typ)
        res.append(ao.room_typ)
        BaseTable.get_bytes_for_string(res, ao.flat_number, None)
        BaseTable.get_bytes_for_string(res, ao.room_number, None)
        res.extend((((0 if ao.children_ids is None else len(ao.children_ids)))).to_bytes(4, byteorder="little"))
        if (ao.children_ids is not None): 
            for id0_ in ao.children_ids: 
                res.extend((id0_).to_bytes(4, byteorder="little"))
        BaseTable.get_bytes_for_string(res, ao.guid, None)
    
    def get(self, id0_ : int) -> 'RoomObject':
        dat = self.read_key_data(id0_, 0)
        if (dat is None): 
            return None
        r = RoomObject()
        r.id0_ = id0_
        ind = 0
        wrapind51 = RefOutArgWrapper(ind)
        self.__restore(dat, r, wrapind51)
        ind = wrapind51.value
        return r
    
    def get_parent_id(self, id0_ : int) -> int:
        data = self.read_key_data(id0_, 11)
        if (data is None): 
            return 0
        ind = 1
        return int.from_bytes(data[ind:ind+4], byteorder="little")
    
    def get_actual(self, id0_ : int) -> int:
        data = self.read_key_data(id0_, 1)
        if (data is None): 
            return -1
        return (0 if ((((data[0]) & 1)) != 0) else 1)
    
    def __restore(self, data : bytearray, ao : 'RoomObject', ind : int) -> bool:
        if ((((data[ind.value]) & 1)) != 0): 
            ao.actual = False
        else: 
            ao.actual = True
        ind.value += 1
        ao.house_id = int.from_bytes(data[ind.value:ind.value+4], byteorder="little")
        ind.value += 4
        ao.flat_typ = data[ind.value]
        ind.value += 1
        ao.room_typ = data[ind.value]
        ind.value += 1
        ao.flat_number = BaseTable.get_string_for_bytes(data, ind, False, None)
        ao.room_number = BaseTable.get_string_for_bytes(data, ind, False, None)
        cou = int.from_bytes(data[ind.value:ind.value+4], byteorder="little")
        ind.value += 4
        while cou > 0: 
            if (ao.children_ids is None): 
                ao.children_ids = list()
            ao.children_ids.append(int.from_bytes(data[ind.value:ind.value+4], byteorder="little"))
            ind.value += 4
            cou -= 1
        if (ind.value < len(data)): 
            ao.guid = BaseTable.get_string_for_bytes(data, ind, False, None)
        return True