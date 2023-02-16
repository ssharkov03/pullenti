# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

class AbbrTreeNode:
    
    def __init__(self) -> None:
        self.children = None;
        self.len0_ = 0
        self.corrs = None
    
    def __str__(self) -> str:
        if (self.corrs is not None): 
            for kp in self.corrs.items(): 
                return "{0}->{1}".format(kp[0], kp[1])
        return "?"
    
    def find(self, str0_ : str, i : int) -> 'AbbrTreeNode':
        tn = self
        j = i
        while j < len(str0_): 
            if (tn.children is None): 
                break
            tn1 = None
            wraptn172 = RefOutArgWrapper(None)
            inoutres73 = Utils.tryGetValue(tn.children, str0_[j], wraptn172)
            tn1 = wraptn172.value
            if (not inoutres73): 
                break
            tn = tn1
            j += 1
        if (tn.corrs is not None): 
            return tn
        return None
    
    def add(self, str0_ : str, i : int, corr : str, ty : str) -> None:
        if (i < len(str0_)): 
            tn = None
            if (self.children is not None): 
                wraptn74 = RefOutArgWrapper(None)
                inoutres75 = Utils.tryGetValue(self.children, str0_[i], wraptn74)
                tn = wraptn74.value
                if (not inoutres75): 
                    tn = (None)
            if (tn is None): 
                if (self.children is None): 
                    self.children = dict()
                tn = AbbrTreeNode._new76(i + 1)
                self.children[str0_[i]] = tn
            tn.add(str0_, i + 1, corr, ty)
        else: 
            if (self.corrs is None): 
                self.corrs = dict()
            if (not ty in self.corrs): 
                self.corrs[ty] = corr
    
    @staticmethod
    def _new76(_arg1 : int) -> 'AbbrTreeNode':
        res = AbbrTreeNode()
        res.len0_ = _arg1
        return res