# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import typing
from pullenti.unisharp.Utils import Utils

class AddrInfo(object):
    
    def __init__(self) -> None:
        self.id0_ = 0
        self.typ_id = 0
        self.alt_typ_id = 0
        self.parents_id = list()
        self.alt_parent_id = 0
        self.region = 0
    
    def __str__(self) -> str:
        tmp = io.StringIO()
        print("{0} ({1}".format(self.id0_, self.typ_id), end="", file=tmp, flush=True)
        if (self.alt_typ_id > (0)): 
            print("/{0}".format(self.alt_typ_id), end="", file=tmp, flush=True)
        print(')', end="", file=tmp)
        for p in self.parents_id: 
            print(" {0}".format(p), end="", file=tmp, flush=True)
        if (self.alt_parent_id != 0): 
            print(" / alt={0}".format(self.alt_parent_id), end="", file=tmp, flush=True)
        print(",r={0}".format(self.region), end="", file=tmp, flush=True)
        return Utils.toStringStringIO(tmp)
    
    def compareTo(self, other : 'AddrInfo') -> int:
        if (self.id0_ < other.id0_): 
            return -1
        if (self.id0_ > other.id0_): 
            return 1
        return 0
    
    @staticmethod
    def _new10(_arg1 : int, _arg2 : int, _arg3 : typing.List[int], _arg4 : int, _arg5 : int) -> 'AddrInfo':
        res = AddrInfo()
        res.id0_ = _arg1
        res.typ_id = _arg2
        res.parents_id = _arg3
        res.alt_parent_id = _arg4
        res.region = _arg5
        return res