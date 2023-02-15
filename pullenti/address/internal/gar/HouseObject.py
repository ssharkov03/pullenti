# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

class HouseObject(object):
    
    def __init__(self) -> None:
        self.id0_ = 0
        self.parent_id = 0
        self.guid = None;
        self.unom = 0
        self.house_number = None;
        self.build_number = None;
        self.struc_number = None;
        self.house_typ = 0
        self.struc_typ = 0
        self.actual = False
        self.room_ids = None
        self.tag = None;
    
    def __str__(self) -> str:
        res = io.StringIO()
        if (self.house_number is not None): 
            print("{0}{1}".format(("уч." if self.house_typ == (5) else ("д." if self.house_typ == (2) else ("влад." if self.house_typ == (1) else ("дмвлд." if self.house_typ == (3) else ("гараж" if self.house_typ == (4) else "?"))))), ("б/н" if Utils.isNullOrEmpty(self.house_number) else self.house_number)), end="", file=res, flush=True)
        if (self.build_number is not None): 
            if (res.tell() > 0): 
                print(' ', end="", file=res)
            print("корп.{0}".format(("б/н" if Utils.isNullOrEmpty(self.build_number) else self.build_number)), end="", file=res, flush=True)
        if (self.struc_number is not None): 
            if (res.tell() > 0): 
                print(' ', end="", file=res)
            if (self.struc_typ == (2)): 
                print("сооруж.", end="", file=res)
            elif (self.struc_typ == (3)): 
                print("лит.", end="", file=res)
            else: 
                print("стр.", end="", file=res)
            print(("б/н" if Utils.isNullOrEmpty(self.struc_number) else self.struc_number), end="", file=res)
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
        n1 = HouseObject.__get_int(str1)
        n2 = HouseObject.__get_int(str2)
        if (n1 < n2): 
            return -1
        if (n1 > n2): 
            return 1
        if (str1 is not None and str2 is not None): 
            return Utils.compareStrings(str1, str2, False)
        return 0
    
    def compareTo(self, other : 'HouseObject') -> int:
        i = HouseObject._comp_nums(self.house_number, other.house_number)
        if (i != 0): 
            return i
        i = HouseObject._comp_nums(self.build_number, other.build_number)
        if (((i)) != 0): 
            return i
        i = HouseObject._comp_nums(self.struc_number, other.struc_number)
        if (((i)) != 0): 
            return i
        return 0
    
    def out_info(self, tmp : io.StringIO, db : 'FiasDatabase'=None) -> None:
        if (not self.actual): 
            print("\r\nActual: no", end="", file=tmp)
        print("\r\n{0}".format(str(self)), end="", file=tmp, flush=True)
        print("\r\nGUID: {0}".format(Utils.ifNotNull(self.guid, "?")), end="", file=tmp, flush=True)
        if (db is not None): 
            pars = db.get_house_params(self.id0_)
            if (pars is not None): 
                for kp in pars.items(): 
                    print("\r\n{0}: {1} ".format(Utils.enumToString(kp[0]), kp[1]), end="", file=tmp, flush=True)
    
    @staticmethod
    def _new46(_arg1 : int) -> 'HouseObject':
        res = HouseObject()
        res.id0_ = _arg1
        return res