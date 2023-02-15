# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.unisharp.Streams import Stream

from pullenti.address.internal.FiasHelper import FiasHelper
from pullenti.address.internal.RepObjTreeNode import RepObjTreeNode

class RepObjTree:
    
    def __init__(self) -> None:
        self.__m_data = None
        self.__children = dict()
        self.modified = False
        self.max_length = 8
    
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
            ch = chr(int.from_bytes(self.__m_data[ind:ind+2], byteorder="little"))
            ind += 2
            tn = RepObjTreeNode()
            wrapind127 = RefOutArgWrapper(ind)
            self.__deserialize_node(tn, wrapind127)
            ind = wrapind127.value
            self.__children[ch] = tn
            i += 1
        self.modified = False
    
    def __deserialize_node(self, res : 'RepObjTreeNode', ind : int) -> None:
        cou = int.from_bytes(self.__m_data[ind.value:ind.value+2], byteorder="little")
        ind.value += 2
        if (cou > 0): 
            res.objs = dict()
            while cou > 0: 
                id0_ = int.from_bytes(self.__m_data[ind.value:ind.value+4], byteorder="little")
                ind.value += 4
                rest = FiasHelper.deserialize_string_from_bytes(self.__m_data, ind, True)
                res.objs[rest] = id0_
                cou -= 1
        cou = (int.from_bytes(self.__m_data[ind.value:ind.value+2], byteorder="little"))
        ind.value += 2
        while cou > 0: 
            ch = chr(int.from_bytes(self.__m_data[ind.value:ind.value+2], byteorder="little"))
            ind.value += 2
            tn = RepObjTreeNode()
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
    
    def __load_node(self, res : 'RepObjTreeNode') -> None:
        if (not res.loaded and res.lazy_pos > 0): 
            ind = res.lazy_pos + 4
            wrapind128 = RefOutArgWrapper(ind)
            self.__deserialize_node(res, wrapind128)
            ind = wrapind128.value
        res.loaded = True
    
    def save(self, f : Stream) -> None:
        FiasHelper.serialize_int(f, len(self.__children))
        for kp in self.__children.items(): 
            FiasHelper.serialize_short(f, ord(kp[0]))
            self.__serialize_node(f, kp[1])
        self.modified = False
    
    def __serialize_node(self, s : Stream, tn : 'RepObjTreeNode') -> None:
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
            for o in tn.objs.items(): 
                FiasHelper.serialize_int(s, o[1])
                FiasHelper.serialize_string(s, o[0], True)
        FiasHelper.serialize_short(s, (0 if tn.children is None else len(tn.children)))
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
    
    def find(self, str0_ : str) -> int:
        dic = self.__children
        gtn = None
        i = 0
        i = 0
        while i < len(str0_): 
            if (dic is None): 
                return 0
            tn = None
            ch = str0_[i]
            wraptn129 = RefOutArgWrapper(None)
            inoutres130 = Utils.tryGetValue(dic, ch, wraptn129)
            tn = wraptn129.value
            if (not inoutres130): 
                return 0
            if (not tn.loaded): 
                self.__load_node(tn)
            gtn = tn
            if (tn.children is None or len(tn.children) == 0): 
                i += 1
                break
            dic = tn.children
            i += 1
        if (gtn is None or gtn.objs is None): 
            return 0
        rest = ("" if i >= len(str0_) else str0_[i:])
        res = 0
        wrapres131 = RefOutArgWrapper(0)
        inoutres132 = Utils.tryGetValue(gtn.objs, rest, wrapres131)
        res = wrapres131.value
        if (inoutres132): 
            return res
        return 0
    
    def add(self, str0_ : str, id0_ : int) -> bool:
        dic = self.__children
        gtn = None
        i = 0
        i = 0
        while (i < len(str0_)) and (i < self.max_length): 
            tn = None
            ch = str0_[i]
            wraptn133 = RefOutArgWrapper(None)
            inoutres134 = Utils.tryGetValue(dic, ch, wraptn133)
            tn = wraptn133.value
            if (not inoutres134): 
                tn = RepObjTreeNode()
                tn.loaded = True
                dic[ch] = tn
            elif (not tn.loaded): 
                self.__load_node(tn)
            gtn = tn
            if (tn.children is None): 
                tn.children = dict()
            dic = tn.children
            i += 1
        if (gtn.objs is None): 
            gtn.objs = dict()
        rest = ("" if i >= len(str0_) else str0_[i:])
        if (not rest in gtn.objs): 
            gtn.objs[rest] = id0_
            self.modified = True
        elif (gtn.objs[rest] != id0_): 
            gtn.objs[rest] = id0_
            self.modified = True
        return True