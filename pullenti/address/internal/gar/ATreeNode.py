# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru


class ATreeNode:
    
    def __init__(self) -> None:
        self.objs = None
        self.parent = None;
        self.children = None
        self.lazy_pos = 0
        self.loaded = False
    
    @staticmethod
    def _new7(_arg1 : 'ATreeNode') -> 'ATreeNode':
        res = ATreeNode()
        res.parent = _arg1
        return res