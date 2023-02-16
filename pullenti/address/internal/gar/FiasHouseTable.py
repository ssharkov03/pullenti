# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.util.repository.BaseTable import BaseTable
from pullenti.util.repository.KeyBaseTable import KeyBaseTable

class FiasHouseTable(KeyBaseTable):
    
    def __init__(self, rep : 'IRepository', name_ : str="houseobjects") -> None:
        super().__init__(rep, name_, None)
    
    def add(self, id0_ : int, doc : 'HouseObject') -> None:
        dat = self.__store(doc)
        self.write_key_data(id0_, dat)
    
    def __store(self, ao : 'HouseObject') -> bytearray:
        res = bytearray()
        attr = ((0 if ao.actual else 1))
        if (ao.unom > 0): 
            attr |= (2)
        res.append(attr)
        res.extend((ao.parent_id).to_bytes(4, byteorder="little"))
        res.append(ao.house_typ)
        res.append(ao.struc_typ)
        BaseTable.get_bytes_for_string(res, ao.house_number, None)
        BaseTable.get_bytes_for_string(res, ao.build_number, None)
        BaseTable.get_bytes_for_string(res, ao.struc_number, None)
        res.extend(((0 if ao.room_ids is None else len(ao.room_ids))).to_bytes(4, byteorder="little"))
        if (ao.room_ids is not None): 
            for ii in ao.room_ids: 
                res.extend((ii).to_bytes(4, byteorder="little"))
        if (ao.unom > 0): 
            res.extend((ao.unom).to_bytes(4, byteorder="little"))
        BaseTable.get_bytes_for_string(res, ao.guid, None)
        return bytearray(res)
    
    def get(self, id0_ : int, ao : 'HouseObject') -> bool:
        dat = self.read_key_data(id0_, 0)
        if (dat is None): 
            return False
        ao.id0_ = id0_
        return self.__restore(dat, ao)
    
    def get_parent_id(self, id0_ : int) -> int:
        data = self.read_key_data(id0_, 5)
        if (data is None): 
            return 0
        ind = 1
        return int.from_bytes(data[ind:ind+4], byteorder="little")
    
    def get_actual(self, id0_ : int) -> int:
        data = self.read_key_data(id0_, 1)
        if (data is None): 
            return -1
        return (0 if ((((data[0]) & 1)) != 0) else 1)
    
    def __restore(self, data : bytearray, ao : 'HouseObject') -> bool:
        if ((((data[0]) & 1)) != 0): 
            ao.actual = False
        else: 
            ao.actual = True
        is_unom = (((data[0]) & 2)) != 0
        ind = 1
        ao.parent_id = int.from_bytes(data[ind:ind+4], byteorder="little")
        ind += 4
        ao.house_typ = data[ind]
        ind += 1
        ao.struc_typ = data[ind]
        ind += 1
        wrapind50 = RefOutArgWrapper(ind)
        ao.house_number = BaseTable.get_string_for_bytes(data, wrapind50, False, None)
        ind = wrapind50.value
        wrapind49 = RefOutArgWrapper(ind)
        ao.build_number = BaseTable.get_string_for_bytes(data, wrapind49, False, None)
        ind = wrapind49.value
        wrapind48 = RefOutArgWrapper(ind)
        ao.struc_number = BaseTable.get_string_for_bytes(data, wrapind48, False, None)
        ind = wrapind48.value
        cou = int.from_bytes(data[ind:ind+4], byteorder="little")
        ind += 4
        if (cou > 0): 
            ao.room_ids = list()
            while cou > 0: 
                ao.room_ids.append(int.from_bytes(data[ind:ind+4], byteorder="little"))
                ind += 4
                cou -= 1
        if (is_unom): 
            ao.unom = int.from_bytes(data[ind:ind+4], byteorder="little")
            ind += 4
        if (ind < len(data)): 
            wrapind47 = RefOutArgWrapper(ind)
            ao.guid = BaseTable.get_string_for_bytes(data, wrapind47, False, None)
            ind = wrapind47.value
        return True