# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru


class RepObjTreeNode:
    
    def __init__(self) -> None:
        self.objs = None
        self.lazy_pos = 0
        self.loaded = False
        self.children = None
    
    def unload(self) -> None:
        if (self.lazy_pos == 0): 
            return
        if (self.children is not None): 
            self.children.clear()
        self.children = (None)
        if (self.objs is not None): 
            self.objs.clear()
        self.objs = (None)
        self.loaded = False