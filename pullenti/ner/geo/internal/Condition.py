# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

from pullenti.ner.geo.internal.MiscLocationHelper import MiscLocationHelper

class Condition:
    
    def __init__(self) -> None:
        self.geo_before_token = None;
        self.pure_geo_before = False
    
    def __str__(self) -> str:
        tmp = io.StringIO()
        if (self.geo_before_token is not None): 
            print("GeoBefore={0}".format(self.geo_before_token), end="", file=tmp, flush=True)
        return Utils.toStringStringIO(tmp)
    
    def check(self) -> bool:
        if (self.geo_before_token is not None): 
            if (MiscLocationHelper.check_geo_object_before(self.geo_before_token, self.pure_geo_before)): 
                return True
        return False
    
    @staticmethod
    def _new377(_arg1 : 'Token', _arg2 : bool) -> 'Condition':
        res = Condition()
        res.geo_before_token = _arg1
        res.pure_geo_before = _arg2
        return res
    
    @staticmethod
    def _new1077(_arg1 : 'Token') -> 'Condition':
        res = Condition()
        res.geo_before_token = _arg1
        return res