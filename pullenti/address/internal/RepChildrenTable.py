# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing

from pullenti.util.repository.KeyBaseTable import KeyBaseTable

class RepChildrenTable(KeyBaseTable):
    
    def __init__(self, base_dir : str, name_ : str="chils") -> None:
        super().__init__(None, name_, base_dir)
    
    def add(self, id0_ : int, li : typing.List[int]) -> None:
        if (li is None or len(li) == 0): 
            self.write_key_data(id0_, None)
        else: 
            res = bytearray()
            for i in li: 
                res.extend((i).to_bytes(4, byteorder="little"))
            self.write_key_data(id0_, bytearray(res))
    
    def get(self, id0_ : int) -> typing.List[int]:
        dat = self.read_key_data(id0_, 0)
        if (dat is None): 
            return None
        res = list()
        ind = 0
        while ind < len(dat): 
            res.append(int.from_bytes(dat[ind:ind+4], byteorder="little"))
            ind += 4
        return res