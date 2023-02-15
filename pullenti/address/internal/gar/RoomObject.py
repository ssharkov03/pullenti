# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

class RoomObject(object):
    
    def __init__(self) -> None:
        self.id0_ = 0
        self.house_id = 0
        self.flat_number = None;
        self.room_number = None;
        self.flat_typ = 0
        self.room_typ = 0
        self.actual = False
        self.guid = None;
        self.children_ids = None
    
    def __str__(self) -> str:
        res = io.StringIO()
        if (self.flat_number is not None): 
            print("кв.{0}".format(self.flat_number), end="", file=res, flush=True)
        if (self.room_number is not None): 
            print("комн.{0}".format(self.room_number), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def __get_int(str0_ : str) -> int:
        if (str0_ is None): 
            return 0
        res = 0
        i = 0
        while i < len(str0_): 
            if (str.isdigit(str0_[i])): 
                res = (((res * 10) + (ord(str0_[i]))) - 0x30)
            else: 
                break
            i += 1
        return res
    
    @staticmethod
    def _comp_nums(str1 : str, str2 : str) -> int:
        n1 = RoomObject.__get_int(str1)
        n2 = RoomObject.__get_int(str2)
        if (n1 < n2): 
            return -1
        if (n1 > n2): 
            return 1
        if (str1 is not None and str2 is not None): 
            return Utils.compareStrings(str1, str2, False)
        return 0
    
    def compareTo(self, other : 'RoomObject') -> int:
        i = RoomObject._comp_nums(self.flat_number, other.flat_number)
        if (i != 0): 
            return i
        i = RoomObject._comp_nums(self.room_number, other.room_number)
        if (((i)) != 0): 
            return i
        return 0
    
    def out_info(self, tmp : io.StringIO) -> None:
        if (not self.actual): 
            print("\r\nActual: no", end="", file=tmp)
        if (self.flat_number is not None): 
            print("\r\nFlat: {0} (type {1})".format(self.flat_number, self.flat_typ), end="", file=tmp, flush=True)
        if (self.room_number is not None): 
            print("\r\nRoom: {0} (type {1})".format(self.room_number, self.room_typ), end="", file=tmp, flush=True)