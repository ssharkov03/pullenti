# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

from pullenti.address.GarLevel import GarLevel

class RepAddrTreeNodeObj:
    
    def __init__(self) -> None:
        self.id0_ = 0
        self.parents = None
        self.lev = GarLevel.UNDEFINED
        self.typ_ids = list()
    
    def __str__(self) -> str:
        tmp = io.StringIO()
        print("{0} ({1}".format(self.id0_, Utils.enumToString(self.lev)), end="", file=tmp, flush=True)
        i = 0
        while i < len(self.typ_ids): 
            print("{0}{1}".format(("," if i > 0 else ":"), self.typ_ids[i]), end="", file=tmp, flush=True)
            i += 1
        print(")", end="", file=tmp)
        if (self.parents is not None): 
            for p in self.parents: 
                print(", {0}".format(p), end="", file=tmp, flush=True)
        return Utils.toStringStringIO(tmp)
    
    def correct(self, o : 'RepaddrObject', typs : 'RepTypTable', p : 'RepaddrObject') -> bool:
        ret = False
        for ty in o.types: 
            tid = typs.get_id(ty)
            if (tid != (0) and not tid in self.typ_ids): 
                self.typ_ids.append(tid)
                ret = True
        for id0__ in self.typ_ids: 
            ty = typs.get_typ(id0__)
            if (ty is not None and not ty in o.types): 
                o.types.append(ty)
                ret = True
        if (p is not None): 
            if (self.parents is None): 
                self.parents = list()
            if (not p.id0_ in self.parents): 
                self.parents.append(p.id0_)
                ret = True
            if (o.parents is None): 
                o.parents = list()
            if (not p.id0_ in o.parents): 
                o.parents.append(p.id0_)
                ret = True
        return ret