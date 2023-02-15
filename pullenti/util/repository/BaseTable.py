# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import threading
import pathlib
import shutil
import datetime
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Streams import FileStream
from pullenti.unisharp.Streams import Stream

class BaseTable(object):
    
    def __init__(self, index_ : 'IRepository') -> None:
        self.index = None;
        self.name = None;
        self.m_lock = threading.Lock()
        self.index = index_
    
    def __str__(self) -> str:
        return Utils.ifNotNull(self.name, str(super()))
    
    @property
    def records_count(self) -> int:
        return 0
    
    @property
    def size(self) -> int:
        return 0
    
    def close(self) -> None:
        self._close()
    
    def open0_(self, read_only : bool, index_in_memory_max_length : int=0) -> bool:
        return False
    
    def _close(self) -> None:
        pass
    
    def clear(self) -> None:
        pass
    
    def flush(self) -> None:
        pass
    
    def optimize(self, min_percent : int=10) -> bool:
        return False
    
    def need_optimize(self, min_percent : int=10, analyze_disk_space : bool=True) -> bool:
        return False
    
    @staticmethod
    def _backup_file(fname : str, path : str) -> bool:
        try: 
            if (not pathlib.Path(fname).is_file()): 
                return True
            shutil.copy(fname, pathlib.PurePath(path).joinpath(pathlib.PurePath(fname).name))
            return True
        except Exception as ex: 
            return False
    
    @staticmethod
    def _restore_file(fname : str, path : str, remove : bool) -> bool:
        try: 
            src = pathlib.PurePath(path).joinpath(pathlib.PurePath(fname).name)
            if (not pathlib.Path(src).is_file()): 
                return True
            shutil.copy(src, fname)
            if (remove): 
                pathlib.Path(src).unlink()
            return True
        except Exception as ex: 
            return False
    
    def backup(self, path : str) -> bool:
        return True
    
    def restore(self, path : str, remove : bool) -> bool:
        return True
    
    def _create_file_stream(self, file_name : str, read_only : bool, buf_len : int=-1) -> FileStream:
        res_ex = None
        for k in range(5):
            try: 
                if (read_only): 
                    if (buf_len > 0): 
                        return FileStream(file_name, "rb")
                    else: 
                        return FileStream(file_name, "rb")
                elif (buf_len > 0): 
                    return FileStream(file_name, "r+b")
                else: 
                    return FileStream(file_name, "r+b")
            except Exception as ex: 
                res_ex = ex
            if (k == 0): 
                if (not pathlib.Path(file_name).is_file()): 
                    if (buf_len > 0): 
                        return FileStream(file_name, "r+b")
                    else: 
                        return FileStream(file_name, "r+b")
        raise res_ex
    
    @staticmethod
    def get_bytes_for_string(res : bytearray, str0_ : str, enc : str=None) -> None:
        if (Utils.isNullOrEmpty(str0_)): 
            res.extend((0).to_bytes(2, byteorder="little"))
        else: 
            b = (str0_.encode("UTF-8", 'ignore') if enc is None else str0_.encode(enc, 'ignore'))
            res.extend((len(b)).to_bytes(2, byteorder="little"))
            res.extend(b)
    
    @staticmethod
    def get_string_for_bytes(data : bytearray, ind : int, dont_create : bool=False, enc : str=None) -> str:
        if ((ind.value + 2) > len(data)): 
            return None
        len0_ = int.from_bytes(data[ind.value:ind.value+2], byteorder="little")
        ind.value += 2
        if (len0_ <= (0)): 
            return None
        if ((ind.value + (len0_)) > len(data)): 
            return None
        res = None
        if (not dont_create): 
            if (enc is None): 
                res = data[ind.value:ind.value+len0_].decode("UTF-8", 'ignore')
            else: 
                res = data[ind.value:ind.value+len0_].decode(enc, 'ignore')
        ind.value += (len0_)
        return res
    
    @staticmethod
    def _get_bytes_for_date0(res : bytearray, dt : datetime.datetime) -> None:
        if (dt is not None): 
            BaseTable._get_bytes_for_date(res, dt)
        else: 
            res.extend((0).to_bytes(2, byteorder="little"))
    
    @staticmethod
    def _get_bytes_for_date(res : bytearray, dt : datetime.datetime) -> None:
        res.extend((dt.year).to_bytes(2, byteorder="little"))
        res.append(dt.month)
        res.append(dt.day)
        res.append(dt.hour)
        res.append(dt.minute)
        res.append(dt.second)
        res.append(0)
    
    @staticmethod
    def _to_date(data : bytearray, ind : int) -> datetime.datetime:
        if ((ind.value + 2) > len(data)): 
            return None
        year = int.from_bytes(data[ind.value:ind.value+2], byteorder="little")
        ind.value += 2
        if (year == 0): 
            return None
        if ((ind.value + 8) > len(data)): 
            return None
        mon = data[ind.value]
        ind.value += 1
        day = data[ind.value]
        ind.value += 1
        hour = data[ind.value]
        ind.value += 1
        min0_ = data[ind.value]
        ind.value += 1
        sec = data[ind.value]
        ind.value += 1
        ind.value += 1
        if (year == 0): 
            return None
        try: 
            return datetime.datetime(year, mon, day, hour, min0_, sec)
        except Exception as ex2676: 
            return None
    def __enter__(self): return self
    def __exit__(self, typ, val, traceback): self.close()