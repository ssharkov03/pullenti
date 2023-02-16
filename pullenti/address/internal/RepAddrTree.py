# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.unisharp.Streams import Stream

from pullenti.address.GarLevel import GarLevel
from pullenti.address.internal.FiasHelper import FiasHelper
from pullenti.address.internal.RepAddrTreeNode import RepAddrTreeNode
from pullenti.address.internal.RepAddrTreeNodeObj import RepAddrTreeNodeObj

class RepAddrTree:
    
    def __init__(self) -> None:
        self.__m_data = None
        self.__children = dict()
    
    def clear(self) -> None:
        for kp in self.__children.items(): 
            kp[1].unload()
        self.__children.clear()
        self.__m_data = (None)
    
    def open0_(self, dat : bytearray) -> None:
        self.__m_data = dat
        self.__children.clear()
        ind = 0
        cou = int.from_bytes(dat[ind:ind+4], byteorder="little")
        ind += 4
        if (cou == 0): 
            return
        i = 0
        while i < cou: 
            ch = chr(int.from_bytes(dat[ind:ind+2], byteorder="little"))
            ind += 2
            tn = RepAddrTreeNode()
            wrapind120 = RefOutArgWrapper(ind)
            self.__deserialize_node(tn, wrapind120)
            ind = wrapind120.value
            self.__children[ch] = tn
            i += 1
    
    def __deserialize_node(self, res : 'RepAddrTreeNode', ind : int) -> None:
        cou = int.from_bytes(self.__m_data[ind.value:ind.value+2], byteorder="little")
        ind.value += 2
        if (cou > 0): 
            res.objs = list()
            while cou > 0: 
                o = RepAddrTreeNodeObj()
                o.id0_ = int.from_bytes(self.__m_data[ind.value:ind.value+4], byteorder="little")
                ind.value += 4
                o.lev = (Utils.valToEnum(self.__m_data[ind.value], GarLevel))
                ind.value += 1
                tt = self.__m_data[ind.value]
                ind.value += 1
                while tt > 0: 
                    o.typ_ids.append(int.from_bytes(self.__m_data[ind.value:ind.value+2], byteorder="little"))
                    ind.value += 2
                    tt -= 1
                cc = int.from_bytes(self.__m_data[ind.value:ind.value+2], byteorder="little")
                ind.value += 2
                while cc > 0: 
                    if (o.parents is None): 
                        o.parents = list()
                    o.parents.append(int.from_bytes(self.__m_data[ind.value:ind.value+4], byteorder="little"))
                    ind.value += 4
                    cc -= 1
                res.objs.append(o)
                cou -= 1
        cou = (int.from_bytes(self.__m_data[ind.value:ind.value+2], byteorder="little"))
        ind.value += 2
        while cou > 0: 
            ch = chr(int.from_bytes(self.__m_data[ind.value:ind.value+2], byteorder="little"))
            ind.value += 2
            tn = RepAddrTreeNode()
            tn.lazy_pos = ind.value
            tn.loaded = False
            len0_ = int.from_bytes(self.__m_data[ind.value:ind.value+4], byteorder="little")
            ind.value += 4
            if (res.children is None): 
                res.children = dict()
            res.children[ch] = tn
            ind.value = (tn.lazy_pos + len0_)
            cou -= 1
        res.loaded = True
    
    def __load_node(self, res : 'RepAddrTreeNode') -> None:
        if (not res.loaded and res.lazy_pos > 0): 
            ind = res.lazy_pos + 4
            wrapind121 = RefOutArgWrapper(ind)
            self.__deserialize_node(res, wrapind121)
            ind = wrapind121.value
        res.loaded = True
    
    def save(self, f : Stream) -> None:
        FiasHelper.serialize_int(f, len(self.__children))
        for kp in self.__children.items(): 
            FiasHelper.serialize_short(f, ord(kp[0]))
            self.__serialize_node(f, kp[1])
    
    def __serialize_node(self, s : Stream, tn : 'RepAddrTreeNode') -> None:
        if (not tn.loaded): 
            ind = tn.lazy_pos
            len0_ = int.from_bytes(self.__m_data[ind:ind+4], byteorder="little")
            ind += 4
            len0_ -= 4
            s.write(self.__m_data, ind, len0_)
            return
        if (tn.objs is None or len(tn.objs) == 0): 
            FiasHelper.serialize_short(s, 0)
        else: 
            FiasHelper.serialize_short(s, len(tn.objs))
            for o in tn.objs: 
                FiasHelper.serialize_int(s, o.id0_)
                FiasHelper.serialize_byte(s, o.lev)
                FiasHelper.serialize_byte(s, len(o.typ_ids))
                for ii in o.typ_ids: 
                    FiasHelper.serialize_short(s, ii)
                if (o.parents is None or len(o.parents) == 0): 
                    FiasHelper.serialize_short(s, 0)
                else: 
                    FiasHelper.serialize_short(s, len(o.parents))
                    for p in o.parents: 
                        FiasHelper.serialize_int(s, p)
        FiasHelper.serialize_short(s, ((0 if tn.children is None else len(tn.children))))
        if (tn.children is not None): 
            for ch in tn.children.items(): 
                FiasHelper.serialize_short(s, ord(ch[0]))
                p0 = s.position
                FiasHelper.serialize_int(s, 0)
                self.__serialize_node(s, ch[1])
                p1 = s.position
                s.position = p0
                FiasHelper.serialize_int(s, p1 - p0)
                s.position = p1
    
    def find(self, path : str) -> typing.List['RepAddrTreeNodeObj']:
        dic = self.__children
        gtn = None
        i = 0
        while i < len(path): 
            if (dic is None): 
                return None
            tn = None
            ch = path[i]
            wraptn122 = RefOutArgWrapper(None)
            inoutres123 = Utils.tryGetValue(dic, ch, wraptn122)
            tn = wraptn122.value
            if (not inoutres123): 
                return None
            if (not tn.loaded): 
                self.__load_node(tn)
            if ((i + 1) == len(path)): 
                gtn = tn
                break
            if (tn.children is None or len(tn.children) == 0): 
                return None
            dic = tn.children
            i += 1
        if (gtn is None): 
            return None
        return gtn.objs
    
    def add(self, path : str, obj : 'RepAddrTreeNodeObj') -> bool:
        dic = self.__children
        gtn = None
        i = 0
        while i < len(path): 
            tn = None
            ch = path[i]
            wraptn124 = RefOutArgWrapper(None)
            inoutres125 = Utils.tryGetValue(dic, ch, wraptn124)
            tn = wraptn124.value
            if (not inoutres125): 
                tn = RepAddrTreeNode()
                tn.loaded = True
                dic[ch] = tn
            if (not tn.loaded): 
                self.__load_node(tn)
            if ((i + 1) == len(path)): 
                gtn = tn
                break
            if (tn.children is None): 
                tn.children = dict()
            dic = tn.children
            i += 1
        if (gtn.objs is None): 
            gtn.objs = list()
        for o in gtn.objs: 
            if (o.id0_ == obj.id0_): 
                ret = False
                if (obj.parents is not None): 
                    if (o.parents is None): 
                        o.parents = obj.parents
                        ret = True
                    else: 
                        for p in obj.parents: 
                            if (not p in o.parents): 
                                o.parents = obj.parents
                                ret = True
                return ret
        gtn.objs.append(obj)
        return True