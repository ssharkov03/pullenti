# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.unisharp.Streams import MemoryStream
from pullenti.unisharp.Streams import Stream

from pullenti.address.internal.FiasHelper import FiasHelper
from pullenti.address.internal.gar.HTreeNode import HTreeNode

class HTreeRoot:
    
    def __init__(self) -> None:
        self.children = dict()
    
    def add(self, path : str, id0_ : int, actual : bool) -> 'HTreeNode':
        if (Utils.isNullOrEmpty(path)): 
            return None
        res = None
        wrapres54 = RefOutArgWrapper(None)
        inoutres55 = Utils.tryGetValue(self.children, path[0], wrapres54)
        res = wrapres54.value
        if (not inoutres55): 
            res = HTreeNode()
            self.children[path[0]] = res
        i = 1
        while i < len(path): 
            rr = None
            if (res.children is None): 
                res.children = dict()
            wraprr52 = RefOutArgWrapper(None)
            inoutres53 = Utils.tryGetValue(res.children, path[i], wraprr52)
            rr = wraprr52.value
            if (not inoutres53): 
                rr = HTreeNode()
                res.children[path[i]] = rr
            res = rr
            i += 1
        if (res.id0_ == 0): 
            res.id0_ = id0_
        elif (actual): 
            if (res.other_ids is None): 
                res.other_ids = list()
            res.other_ids.append(res.id0_)
            res.id0_ = id0_
        else: 
            if (res.other_ids is None): 
                res.other_ids = list()
            res.other_ids.append(id0_)
        return res
    
    def find(self, path : str) -> 'HTreeNode':
        if (Utils.isNullOrEmpty(path)): 
            return None
        res = None
        wrapres58 = RefOutArgWrapper(None)
        inoutres59 = Utils.tryGetValue(self.children, path[0], wrapres58)
        res = wrapres58.value
        if (not inoutres59): 
            return None
        i = 1
        while i < len(path): 
            rr = None
            if (res.children is None): 
                return None
            wraprr56 = RefOutArgWrapper(None)
            inoutres57 = Utils.tryGetValue(res.children, path[i], wraprr56)
            rr = wraprr56.value
            if (not inoutres57): 
                return None
            res = rr
            i += 1
        return res
    
    def save(self, f : Stream) -> None:
        FiasHelper.serialize_int(f, len(self.children))
        for kp in self.children.items(): 
            FiasHelper.serialize_short(f, ord(kp[0]))
            HTreeRoot.__serialize_node(f, kp[1])
    
    @staticmethod
    def __serialize_node(f : Stream, nod : 'HTreeNode') -> None:
        cou = 0
        if (nod.id0_ > 0): 
            cou += 1
        if (nod.other_ids is not None): 
            cou += len(nod.other_ids)
        FiasHelper.serialize_short(f, cou)
        if (nod.id0_ > 0): 
            FiasHelper.serialize_int(f, nod.id0_)
            if (nod.other_ids is not None): 
                for ii in nod.other_ids: 
                    FiasHelper.serialize_int(f, ii)
        FiasHelper.serialize_short(f, ((0 if nod.children is None else len(nod.children))))
        if (nod.children is not None): 
            for kp in nod.children.items(): 
                FiasHelper.serialize_short(f, ord(kp[0]))
                HTreeRoot.__serialize_node(f, kp[1])
    
    def load(self, dat : bytearray) -> None:
        with MemoryStream(dat) as f: 
            f.position = 0
            cou = FiasHelper.deserialize_int(f)
            if (cou == 0): 
                return
            i = 0
            while i < cou: 
                sh = FiasHelper.deserialize_short(f)
                ch = chr(sh)
                tn = HTreeRoot.__deserialize_node(f)
                if (tn is not None): 
                    self.children[ch] = tn
                i += 1
    
    @staticmethod
    def __deserialize_node(f : Stream) -> 'HTreeNode':
        res = HTreeNode()
        cou = FiasHelper.deserialize_short(f)
        if (cou > 0): 
            res.id0_ = FiasHelper.deserialize_int(f)
            if (cou > 1): 
                res.other_ids = list()
                i = 1
                while i < cou: 
                    res.other_ids.append(FiasHelper.deserialize_int(f))
                    i += 1
        cou = FiasHelper.deserialize_short(f)
        if (cou == 0): 
            return res
        i = 0
        while i < cou: 
            sh = FiasHelper.deserialize_short(f)
            ch = chr(sh)
            tn = HTreeRoot.__deserialize_node(f)
            if (tn is not None): 
                if (res.children is None): 
                    res.children = dict()
                res.children[ch] = tn
            i += 1
        return res