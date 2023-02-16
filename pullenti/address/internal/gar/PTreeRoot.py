# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import threading
import gc
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.unisharp.Streams import FileStream
from pullenti.unisharp.Streams import Stream

from pullenti.address.internal.FiasHelper import FiasHelper
from pullenti.address.internal.gar.PTreeNode import PTreeNode

class PTreeRoot:
    
    def __init__(self) -> None:
        self.max_length = 6
        self.children = dict()
        self.__m_lock = threading.Lock()
        self.__m_data = None;
    
    def close0_(self) -> None:
        self.children.clear()
        if (self.__m_data is not None): 
            self.__m_data.close()
            self.__m_data = (None)
    
    def collect(self) -> None:
        with self.__m_lock: 
            for ch in self.children.items(): 
                ch[1].children.clear()
                ch[1].loaded = False
    
    def add(self, path : str, id0_ : int) -> 'PTreeNode':
        if (Utils.isNullOrEmpty(path)): 
            return None
        res = None
        wrapres66 = RefOutArgWrapper(None)
        inoutres67 = Utils.tryGetValue(self.children, path[0], wrapres66)
        res = wrapres66.value
        if (not inoutres67): 
            res = PTreeNode()
            self.children[path[0]] = res
        j = 1
        i = 1
        first_pass2714 = True
        while True:
            if first_pass2714: first_pass2714 = False
            else: i += 1
            if (not ((i < len(path)) and (j < self.max_length))): break
            if (not str.isalnum(path[i]) or path[i] == '0'): 
                continue
            rr = None
            if (res.children is None): 
                res.children = dict()
            wraprr64 = RefOutArgWrapper(None)
            inoutres65 = Utils.tryGetValue(res.children, path[i], wraprr64)
            rr = wraprr64.value
            if (not inoutres65): 
                rr = PTreeNode()
                res.children[path[i]] = rr
            j += 1
            res = rr
        if (res.ids is None): 
            res.ids = list()
        if (len(res.ids) >= 10000): 
            pass
        elif (not id0_ in res.ids): 
            res.ids.append(id0_)
        return res
    
    def find(self, path : str) -> 'PTreeNode':
        if (Utils.isNullOrEmpty(path)): 
            return None
        res = None
        wrapres70 = RefOutArgWrapper(None)
        inoutres71 = Utils.tryGetValue(self.children, path[0], wrapres70)
        res = wrapres70.value
        if (not inoutres71): 
            return None
        j = 1
        i = 1
        first_pass2715 = True
        while True:
            if first_pass2715: first_pass2715 = False
            else: i += 1
            if (not ((i < len(path)) and (j < self.max_length))): break
            if (not str.isalnum(path[i]) or path[i] == '0'): 
                continue
            if (not res.loaded): 
                self.load_node(res)
            rr = None
            if (res.children is None): 
                return None
            wraprr68 = RefOutArgWrapper(None)
            inoutres69 = Utils.tryGetValue(res.children, path[i], wraprr68)
            rr = wraprr68.value
            if (not inoutres69): 
                return None
            res = rr
            j += 1
        if (not res.loaded): 
            self.load_node(res)
        return res
    
    def load_node(self, res : 'PTreeNode') -> None:
        with self.__m_lock: 
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
                PTreeRoot.__serialize_node(f, kp[1])
        self.close0_()
        gc.collect()
    
    @staticmethod
    def __serialize_node(f : Stream, nod : 'PTreeNode') -> None:
        FiasHelper.serialize_short(f, ((0 if nod.ids is None else len(nod.ids))))
        if (nod.ids is not None): 
            nod.ids.sort()
            for v in nod.ids: 
                FiasHelper.serialize_int(f, v)
        FiasHelper.serialize_int(f, (0 if nod.children is None else len(nod.children)))
        if (nod.children is not None): 
            if (len(nod.children) > 0x1000): 
                pass
            for kp in nod.children.items(): 
                FiasHelper.serialize_short(f, ord(kp[0]))
                p0 = f.position
                FiasHelper.serialize_int(f, 0)
                PTreeRoot.__serialize_node(f, kp[1])
                p1 = f.position
                f.position = p0
                FiasHelper.serialize_int(f, p1)
                f.position = p1
    
    def load(self, fname : str) -> None:
        self.__m_data = (FileStream(fname, "rb"))
        self.__m_data.position = 0
        cou = FiasHelper.deserialize_int(self.__m_data)
        if (cou == 0): 
            return
        i = 0
        while i < cou: 
            ch = chr(FiasHelper.deserialize_short(self.__m_data))
            tn = PTreeNode()
            self.__deserialize_node(tn)
            self.children[ch] = tn
            i += 1
    
    def __deserialize_node(self, res : 'PTreeNode') -> None:
        cou = FiasHelper.deserialize_short(self.__m_data)
        if (cou > 0x1000 or (cou < 0)): 
            pass
        if (cou > 0): 
            res.ids = list()
            i = 0
            while i < cou: 
                id0_ = FiasHelper.deserialize_int(self.__m_data)
                res.ids.append(id0_)
                i += 1
        cou = FiasHelper.deserialize_int(self.__m_data)
        if (cou == 0): 
            return
        if (cou > 0x1000 or (cou < 0)): 
            pass
        i = 0
        while i < cou: 
            ch = chr(FiasHelper.deserialize_short(self.__m_data))
            p1 = FiasHelper.deserialize_int(self.__m_data)
            tn = PTreeNode()
            tn.lazy_pos = (self.__m_data.position)
            tn.loaded = False
            if (res.children is None): 
                res.children = dict()
            res.children[ch] = tn
            self.__m_data.position = p1
            i += 1
        res.loaded = True