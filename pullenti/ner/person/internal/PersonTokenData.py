# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

class PersonTokenData:
    
    def __init__(self, t : 'Token') -> None:
        self.tok = None;
        self.attr = None;
        self.tok = t
        t.tag = (self)
    
    def __str__(self) -> str:
        tmp = io.StringIO()
        print(str(self.tok), end="", file=tmp)
        if (self.attr is not None): 
            print(" \r\nAttr: {0}".format(str(self.attr)), end="", file=tmp, flush=True)
        return Utils.toStringStringIO(tmp)