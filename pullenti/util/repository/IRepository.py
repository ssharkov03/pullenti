# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru


class IRepository(object):
    
    @property
    def base_dir(self) -> str:
        return None
    
    def initialize(self, dir_name : str) -> None:
        pass
    
    def clear(self) -> None:
        pass
    
    @property
    def out_log(self) -> bool:
        return None
    @out_log.setter
    def out_log(self, value) -> bool:
        return value
    def __enter__(self): return self
    def __exit__(self, typ, val, traceback): pass # ERROR: Dispose method not found in class