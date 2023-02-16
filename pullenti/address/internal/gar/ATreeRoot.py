# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import threading
import typing
import gc
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.unisharp.Streams import MemoryStream
from pullenti.unisharp.Streams import FileStream
from pullenti.unisharp.Streams import Stream

from pullenti.address.internal.FiasHelper import FiasHelper
from pullenti.util.FileHelper import FileHelper
from pullenti.address.internal.gar.ATreeNode import ATreeNode
from pullenti.address.internal.gar.AddrInfo import AddrInfo

class ATreeRoot:
    
    def __init__(self) -> None:
        self.children = dict()
        self.m_lock = threading.Lock()
        self.__m_data = None;
    
    def close0_(self) -> None:
        self.children.clear()
        if (self.__m_data is not None): 
            self.__m_data.close()
            self.__m_data = (None)
    
    def collect(self) -> None:
        for ch in self.children.items(): 
            ch[1].children.clear()
            ch[1].loaded = False
    
    def add(self, path : str, id0_ : int, typ_id : int, parents : typing.List[int], alt_parent_id : int, region : int) -> 'ATreeNode':
        if (Utils.isNullOrEmpty(path)): 
            return None
        res = None
        wrapres12 = RefOutArgWrapper(None)
        inoutres13 = Utils.tryGetValue(self.children, path[0], wrapres12)
        res = wrapres12.value
        if (not inoutres13): 
            res = ATreeNode()
            self.children[path[0]] = res
        i = 1
        while i < len(path): 
            rr = None
            if (res.children is None): 
                res.children = dict()
            wraprr8 = RefOutArgWrapper(None)
            inoutres9 = Utils.tryGetValue(res.children, path[i], wraprr8)
            rr = wraprr8.value
            if (not inoutres9): 
                rr = ATreeNode._new7(res)
                res.children[path[i]] = rr
            res = rr
            i += 1
        if (res.objs is None): 
            res.objs = list()
        i = 0
        while i < len(res.objs): 
            if (res.objs[i].id0_ == id0_): 
                res.objs[i] = AddrInfo._new10(id0_, typ_id, parents, alt_parent_id, region)
                return res
            i += 1
        res.objs.append(AddrInfo._new10(id0_, typ_id, parents, alt_parent_id, region))
        if (len(res.objs) > 0x7000): 
            pass
        return res
    
    def find(self, path : str, correct : bool=False, for_search : bool=False) -> 'ATreeNode':
        if (Utils.isNullOrEmpty(path)): 
            return None
        res = self.__find(None, path, 0)
        if (res is not None): 
            if (((res.objs is not None and len(res.objs) > 0)) or for_search): 
                return res
        if (not correct or (len(path) < 4)): 
            return None
        wrapres16 = RefOutArgWrapper(None)
        inoutres17 = Utils.tryGetValue(self.children, path[0], wrapres16)
        res = wrapres16.value
        if (not inoutres17): 
            return None
        j = 1
        res1 = None
        while j < len(path): 
            rr = None
            if (not res.loaded): 
                self.load_node(res)
            if (res.children is None): 
                break
            if (((j + 1) < len(path)) and not str.isdigit(path[j])): 
                for ch in res.children.items(): 
                    rr = self.__find(ch[1], path, j)
                    if (rr is None or rr.objs is None or len(rr.objs) == 0): 
                        if (j > 2): 
                            rr = self.__find(ch[1], path, j - 1)
                    if (rr is None or rr.objs is None or len(rr.objs) == 0): 
                        continue
                    if (res1 is None): 
                        res1 = rr
                    else: 
                        res2 = ATreeNode()
                        res2.objs = list(res1.objs)
                        res2.objs.extend(rr.objs)
                        res1 = res2
            wraprr14 = RefOutArgWrapper(None)
            inoutres15 = Utils.tryGetValue(res.children, path[j], wraprr14)
            rr = wraprr14.value
            if (not inoutres15): 
                break
            res = rr
            j += 1
        if (res1 is not None): 
            return res1
        return None
    
    def __find(self, tn : 'ATreeNode', path : str, i : int) -> 'ATreeNode':
        res = None
        if (tn is None): 
            wrapres18 = RefOutArgWrapper(None)
            inoutres19 = Utils.tryGetValue(self.children, path[i], wrapres18)
            res = wrapres18.value
            if (not inoutres19): 
                return None
        else: 
            res = tn
        j = i + 1
        while j < len(path): 
            rr = None
            if (not res.loaded): 
                self.load_node(res)
            if (res.children is None): 
                return None
            wraprr20 = RefOutArgWrapper(None)
            inoutres21 = Utils.tryGetValue(res.children, path[j], wraprr20)
            rr = wraprr20.value
            if (not inoutres21): 
                return None
            res = rr
            j += 1
        if (not res.loaded): 
            self.load_node(res)
        return res
    
    def load_node(self, res : 'ATreeNode') -> None:
        if (not res.loaded and res.lazy_pos > 0): 
            self.__m_data.position = res.lazy_pos
            self.__deserialize_node(res)
        res.loaded = True
    
    def save(self, fname : str) -> None:
        if (self.__m_data is not None): 
            self.__m_data.close()
            self.__m_data = (None)
        with FileStream(fname, "wb") as f: 
            FiasHelper.serialize_int(f, len(self.children))
            for kp in self.children.items(): 
                FiasHelper.serialize_short(f, ord(kp[0]))
                ATreeRoot.__serialize_node(f, kp[1])
        self.close0_()
        gc.collect()
    
    @staticmethod
    def __serialize_node(f : Stream, nod : 'ATreeNode') -> None:
        FiasHelper.serialize_short(f, ((0 if nod.objs is None else len(nod.objs))))
        if (nod.objs is not None): 
            for v in nod.objs: 
                FiasHelper.serialize_int(f, v.id0_)
                FiasHelper.serialize_short(f, v.typ_id)
                f.writebyte(v.region)
                FiasHelper.serialize_short(f, (0 if v.parents_id is None else len(v.parents_id)))
                if (v.parents_id is not None): 
                    for p in v.parents_id: 
                        FiasHelper.serialize_int(f, p)
                    if (len(v.parents_id) > 0): 
                        FiasHelper.serialize_int(f, v.alt_parent_id)
        FiasHelper.serialize_short(f, ((0 if nod.children is None else len(nod.children))))
        if (nod.children is not None): 
            if (len(nod.children) > 0x1000): 
                pass
            for kp in nod.children.items(): 
                FiasHelper.serialize_short(f, ord(kp[0]))
                p0 = f.position
                FiasHelper.serialize_int(f, 0)
                ATreeRoot.__serialize_node(f, kp[1])
                p1 = f.position
                f.position = p0
                FiasHelper.serialize_int(f, p1)
                f.position = p1
    
    def load(self, fname : str) -> None:
        dat = FileHelper.load_data_from_file(fname, 0)
        self.__m_data = (MemoryStream(dat))
        self.__m_data.position = 0
        cou = FiasHelper.deserialize_int(self.__m_data)
        if (cou == 0): 
            return
        i = 0
        while i < cou: 
            ch = chr(FiasHelper.deserialize_short(self.__m_data))
            tn = ATreeNode()
            self.__deserialize_node(tn)
            self.children[ch] = tn
            i += 1
    
    def __deserialize_node(self, res : 'ATreeNode') -> None:
        cou = FiasHelper.deserialize_short(self.__m_data)
        if (cou > 0x1000 or (cou < 0)): 
            pass
        if (cou > 0): 
            res.objs = list()
            i = 0
            while i < cou: 
                id0_ = FiasHelper.deserialize_int(self.__m_data)
                tid = FiasHelper.deserialize_short(self.__m_data)
                reg = self.__m_data.readbyte()
                cou1 = FiasHelper.deserialize_short(self.__m_data)
                pars = list()
                alt = 0
                if (cou1 > 0): 
                    while cou1 > 0: 
                        pars.append(FiasHelper.deserialize_int(self.__m_data))
                        cou1 -= 1
                    alt = FiasHelper.deserialize_int(self.__m_data)
                res.objs.append(AddrInfo._new10(id0_, tid, pars, alt, reg))
                i += 1
        cou = FiasHelper.deserialize_short(self.__m_data)
        if (cou == 0): 
            return
        if (cou > 0x1000 or (cou < 0)): 
            pass
        i = 0
        while i < cou: 
            ch = chr(FiasHelper.deserialize_short(self.__m_data))
            p1 = FiasHelper.deserialize_int(self.__m_data)
            tn = ATreeNode()
            tn.lazy_pos = (self.__m_data.position)
            tn.loaded = False
            if (res.children is None): 
                res.children = dict()
            res.children[ch] = tn
            tn.parent = res
            self.__m_data.position = p1
            i += 1
        res.loaded = True