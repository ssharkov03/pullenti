# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import pathlib
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.util.repository.BaseTable import BaseTable

class StringDictionaryTable(BaseTable):
    
    def __init__(self, index_ : 'IRepository', name_ : str) -> None:
        super().__init__(index_)
        self.__m_hash = dict()
        self.__m_strings = list()
        self.__m_new = list()
        self.__m_file_name = None;
        self.__m_stream = None;
        self.__m_file_name = pathlib.PurePath(index_.base_dir).joinpath(name_ + ".dic")
        self.name = name_
    
    @property
    def is_exists(self) -> bool:
        if (not pathlib.Path(self.__m_file_name).is_file()): 
            return False
        return True
    
    @property
    def size(self) -> int:
        fi = pathlib.Path(self.__m_file_name)
        if (fi.is_file()): 
            return fi.stat().st_size
        else: 
            return 0
    
    def backup(self, path : str) -> bool:
        self._close()
        if (not BaseTable._backup_file(self.__m_file_name, path)): 
            return False
        return super().backup(path)
    
    def restore(self, path : str, remove : bool) -> bool:
        self._close()
        if (not BaseTable._restore_file(self.__m_file_name, path, remove)): 
            return False
        return super().restore(path, remove)
    
    def _close(self) -> None:
        self.__save_new()
        if (self.__m_stream is not None): 
            self.__m_stream.close()
            self.__m_stream = (None)
        self.__m_hash.clear()
        self.__m_strings.clear()
    
    def flush(self) -> None:
        self.__save_new()
        super().flush()
        if (self.__m_stream is not None): 
            self.__m_stream.flush()
    
    def __save_new(self) -> None:
        if (len(self.__m_new) < 1): 
            return
        buf = bytearray()
        for s in self.__m_new: 
            BaseTable.get_bytes_for_string(buf, s, None)
        self.__m_stream.position = self.__m_stream.length
        self.__m_stream.write(bytearray(buf), 0, len(buf))
        self.__m_new.clear()
    
    def clear(self) -> None:
        self._close()
        if (pathlib.Path(self.__m_file_name).is_file()): 
            pathlib.Path(self.__m_file_name).unlink()
    
    def open0_(self, read_only : bool, index_in_memory_max_length : int=0) -> bool:
        if (self.__m_stream is not None): 
            if (read_only or self.__m_stream.writable): 
                return True
        self._close()
        if (read_only): 
            if (not pathlib.Path(self.__m_file_name).is_file()): 
                return False
        self.__m_stream = (self._create_file_stream(self.__m_file_name, read_only, -1))
        if (self.__m_stream.length > (0)): 
            buf = Utils.newArrayOfBytes(self.__m_stream.length, 0)
            self.__m_stream.position = 0
            self.__m_stream.read(buf, 0, len(buf))
            self.__restore(buf)
        return True
    
    def __restore(self, data : bytearray) -> None:
        ind = 0
        while ind < len(data):
            wrapind2700 = RefOutArgWrapper(ind)
            s = BaseTable.get_string_for_bytes(data, wrapind2700, False, None)
            ind = wrapind2700.value
            if (s is None): 
                break
            if (not s in self.__m_hash): 
                self.__m_hash[s] = len(self.__m_hash) + 1
                self.__m_strings.append(s)
    
    def get_code_by_string(self, val : str, add_if_not_exist : bool) -> int:
        if (Utils.isNullOrEmpty(val)): 
            return 0
        id0_ = 0
        wrapid2701 = RefOutArgWrapper(0)
        inoutres2702 = Utils.tryGetValue(self.__m_hash, val, wrapid2701)
        id0_ = wrapid2701.value
        if (inoutres2702): 
            return id0_
        if (not add_if_not_exist): 
            return 0
        id0_ = (len(self.__m_hash) + 1)
        self.__m_hash[val] = id0_
        self.__m_strings.append(val)
        self.__m_new.append(val)
        return id0_
    
    def get_string_by_code(self, id0_ : int) -> str:
        if ((id0_ < 1) or id0_ > len(self.__m_strings)): 
            return None
        else: 
            return self.__m_strings[id0_ - 1]