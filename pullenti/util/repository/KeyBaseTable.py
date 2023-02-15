# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import pathlib
import math
import typing
import shutil
import zlib
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.unisharp.Misc import Stopwatch
from pullenti.unisharp.Streams import Stream

from pullenti.util.ConsoleHelper import ConsoleHelper
from pullenti.util.repository.BaseTable import BaseTable

class KeyBaseTable(BaseTable):
    
    def __init__(self, index_ : 'IRepository', name_ : str, base_dir : str=None) -> None:
        super().__init__(index_)
        self.auto_zip_data = False
        self._index_stream_buf_size = -1
        self._data_stream_buf_size = -1
        self.__m_unique_key_position = 0
        self._m_index_file_name = None;
        self._m_data_file_name = None;
        self._m_index = None;
        self._m_index_buf = None;
        self._m_data = None;
        self.__m_read_ind_buf = None;
        self.__m_fetch_pos = 0
        if (self.index is not None): 
            self._m_index_file_name = pathlib.PurePath(self.index.base_dir).joinpath(name_ + ".ind")
            self._m_data_file_name = pathlib.PurePath(self.index.base_dir).joinpath(name_ + ".dat")
        elif (base_dir is not None): 
            self._m_index_file_name = pathlib.PurePath(base_dir).joinpath(name_ + ".ind")
            self._m_data_file_name = pathlib.PurePath(base_dir).joinpath(name_ + ".dat")
        self.name = name_
    
    @property
    def is_exists(self) -> bool:
        if (not pathlib.Path(self._m_data_file_name).is_file()): 
            return False
        if (not pathlib.Path(self._m_index_file_name).is_file()): 
            return False
        return True
    
    def remove(self) -> None:
        self._close()
        if (pathlib.Path(self._m_data_file_name).is_file()): 
            pathlib.Path(self._m_data_file_name).unlink()
        if (pathlib.Path(self._m_index_file_name).is_file()): 
            pathlib.Path(self._m_index_file_name).unlink()
    
    def backup(self, path : str) -> bool:
        self._close()
        if (not BaseTable._backup_file(self._m_index_file_name, path)): 
            return False
        if (not BaseTable._backup_file(self._m_data_file_name, path)): 
            return False
        return super().backup(path)
    
    def restore(self, path : str, remove_ : bool) -> bool:
        self._close()
        if (not BaseTable._restore_file(self._m_index_file_name, path, remove_)): 
            return False
        if (not BaseTable._restore_file(self._m_data_file_name, path, remove_)): 
            return False
        return super().restore(path, remove_)
    
    def _close(self) -> None:
        if (self._m_data is not None): 
            self._m_data.close()
            self._m_data = (None)
        if (self._m_index is not None): 
            self._m_index.close()
            self._m_index = (None)
        self._m_index_buf = (None)
    
    def flush(self) -> None:
        super().flush()
        if (self._m_data is not None): 
            self._m_data.flush()
        if (self._m_index is not None): 
            self._m_index.flush()
    
    __index_record_size = 12
    
    @property
    def records_count(self) -> int:
        return self.get_max_key()
    
    @property
    def size(self) -> int:
        if (self._m_data is not None): 
            return self._m_data.length + self._m_index.length
        res = 0
        fi = pathlib.Path(self._m_data_file_name)
        if (fi.is_file()): 
            res += fi.stat().st_size
        fi = pathlib.Path(self._m_index_file_name)
        if (fi.is_file()): 
            res += fi.stat().st_size
        return res
    
    def get_max_key(self) -> int:
        res = 0
        if (self._m_index is not None): 
            res = (math.floor(self._m_index.length / (KeyBaseTable.__index_record_size)))
        else: 
            fi = pathlib.Path(self._m_index_file_name)
            if (not fi.is_file()): 
                return 0
            res = (math.floor(fi.stat().st_size / (KeyBaseTable.__index_record_size)))
        if (res > (0)): 
            res -= 1
        return res
    
    def reset_unique_key_pointer(self) -> None:
        self.__m_unique_key_position = 0
    
    def get_unique_key(self) -> int:
        max0_ = self.get_max_key()
        if (self.__m_unique_key_position < 0): 
            return max0_ + 1
        disp = 0
        len0_ = 0
        if (self.__m_unique_key_position == 0): 
            self.__m_unique_key_position = 1
        first_pass3073 = True
        while True:
            if first_pass3073: first_pass3073 = False
            else: self.__m_unique_key_position += 1
            if (not (self.__m_unique_key_position < max0_)): break
            wrapdisp2679 = RefOutArgWrapper(0)
            wraplen2680 = RefOutArgWrapper(0)
            inoutres2681 = self.__read_index_info(self.__m_unique_key_position, wrapdisp2679, wraplen2680)
            disp = wrapdisp2679.value
            len0_ = wraplen2680.value
            if (not inoutres2681): 
                continue
            if (disp == (0) and len0_ == 0): 
                retVal3074 = self.__m_unique_key_position
                self.__m_unique_key_position += 1
                return retVal3074
        self.__m_unique_key_position = -1
        return max0_ + 1
    
    def set_max_key(self, max_key : int) -> None:
        delta = max_key - self.get_max_key()
        if (delta <= 0): 
            return
        buf = Utils.newArrayOfBytes(((delta + 1)) * KeyBaseTable.__index_record_size, 0)
        i = 0
        while i < len(buf): 
            buf[i] = (0)
            i += 1
        if (self._m_index is None): 
            self._m_index = self._create_file_stream(self._m_index_file_name, False, -1)
            self._m_index.position = self._m_index.length
            self._m_index.write(buf, 0, len(buf))
            self._m_index.close()
        else: 
            self._m_index.position = self._m_index.length
            self._m_index.write(buf, 0, len(buf))
    
    def clear(self) -> None:
        self._close()
        if (pathlib.Path(self._m_index_file_name).is_file()): 
            pathlib.Path(self._m_index_file_name).unlink()
        if (pathlib.Path(self._m_data_file_name).is_file()): 
            pathlib.Path(self._m_data_file_name).unlink()
    
    def open0_(self, read_only : bool, index_in_memory_max_length : int=0) -> bool:
        if (self._m_data is not None): 
            if (read_only or self._m_data.writable): 
                return True
        self._close()
        self.__m_unique_key_position = 0
        if (read_only): 
            if (not pathlib.Path(self._m_index_file_name).is_file() or not pathlib.Path(self._m_data_file_name).is_file()): 
                return False
        self._m_index = self._create_file_stream(self._m_index_file_name, read_only, self._index_stream_buf_size)
        self._m_data = self._create_file_stream(self._m_data_file_name, read_only, self._data_stream_buf_size)
        if (index_in_memory_max_length > 0 and (self._m_index.length < index_in_memory_max_length)): 
            self._m_index_buf = Utils.newArrayOfBytes(self._m_index.length, 0)
            self._m_index.position = 0
            self._m_index.read(self._m_index_buf, 0, len(self._m_index_buf))
        return True
    
    def __calc_data_optimized_length(self) -> int:
        res = 0
        if (self._m_index is not None): 
            buf = Utils.newArrayOfBytes(10000 * KeyBaseTable.__index_record_size, 0)
            self._m_index.position = 0
            while True:
                i = self._m_index.read(buf, 0, len(buf))
                if (i < KeyBaseTable.__index_record_size): 
                    break
                j = 0
                while j < i: 
                    lo = int.from_bytes(buf[j:j+8], byteorder="little")
                    if (lo > (0)): 
                        le = int.from_bytes(buf[j + 8:j + 8+4], byteorder="little")
                        if (le > 0): 
                            res += (le)
                    j += KeyBaseTable.__index_record_size
        elif (self._m_index_buf is not None): 
            i = 0
            while (i + KeyBaseTable.__index_record_size) <= len(self._m_index_buf): 
                lo = int.from_bytes(self._m_index_buf[i:i+8], byteorder="little")
                if (lo > (0)): 
                    le = int.from_bytes(self._m_index_buf[i + 8:i + 8+4], byteorder="little")
                    if (le > 0): 
                        res += (le)
                i += KeyBaseTable.__index_record_size
        return res
    
    def _shift_index(self, delta_key : int) -> None:
        if (self._m_index.length <= KeyBaseTable.__index_record_size): 
            return
        self._m_index_buf = (None)
        len0_ = (self._m_index.length - (KeyBaseTable.__index_record_size))
        buf = Utils.newArrayOfBytes(len0_, 0)
        self._m_index.position = KeyBaseTable.__index_record_size
        self._m_index.read(buf, 0, len(buf))
        empty = Utils.newArrayOfBytes(delta_key * KeyBaseTable.__index_record_size, 0)
        i = 0
        while i < len(empty): 
            empty[i] = (0)
            i += 1
        self._m_index.position = KeyBaseTable.__index_record_size
        self._m_index.write(empty, 0, len(empty))
        self._m_index.write(buf, 0, len(buf))
    
    def _read_index0(self) -> bytearray:
        res = Utils.newArrayOfBytes(KeyBaseTable.__index_record_size, 0)
        self._m_index.position = 0
        if (self._m_index.read(res, 0, len(res)) != len(res)): 
            return None
        return res
    
    def _write_index0(self, info : bytearray) -> None:
        len0_ = len(info)
        if (len0_ > KeyBaseTable.__index_record_size): 
            len0_ = KeyBaseTable.__index_record_size
        self._m_index.position = 0
        self._m_index.write(info, 0, len0_)
    
    def __read_index_info(self, key : int, disp : int, len0_ : int) -> bool:
        disp.value = (0)
        len0_.value = 0
        p = key
        p *= (KeyBaseTable.__index_record_size)
        if (self._m_index_buf is not None): 
            if ((p + (KeyBaseTable.__index_record_size)) > len(self._m_index_buf)): 
                return False
            disp.value = int.from_bytes(self._m_index_buf[p:p+8], byteorder="little")
            len0_.value = int.from_bytes(self._m_index_buf[(p + (8)):(p + (8))+4], byteorder="little")
        elif (self._m_index is not None): 
            if ((p + (KeyBaseTable.__index_record_size)) > self._m_index.length): 
                return False
            self._m_index.position = p
            buf = Utils.newArrayOfBytes(KeyBaseTable.__index_record_size, 0)
            if (self._m_index.read(buf, 0, KeyBaseTable.__index_record_size) != KeyBaseTable.__index_record_size): 
                return False
            disp.value = int.from_bytes(buf[0:0+8], byteorder="little")
            len0_.value = int.from_bytes(buf[8:8+4], byteorder="little")
        else: 
            return False
        if (len0_.value < 0): 
            return False
        return True
    
    def __write_index_info(self, key : int, disp : int, len0_ : int) -> None:
        dbuf = (disp).to_bytes(8, byteorder="little")
        lbuf = (len0_).to_bytes(4, byteorder="little")
        p = key
        p *= (KeyBaseTable.__index_record_size)
        if (self._m_index_buf is not None and (p + (KeyBaseTable.__index_record_size)) <= len(self._m_index_buf)): 
            for i in range(8):
                self._m_index_buf[p + (i)] = dbuf[i]
            for i in range(4):
                self._m_index_buf[p + (8) + (i)] = lbuf[i]
        if (p > self._m_index.length): 
            buf = Utils.newArrayOfBytes(p - self._m_index.length, 0)
            i = 0
            while i < len(buf): 
                buf[i] = (0)
                i += 1
            self._m_index.position = self._m_index.length
            self._m_index.write(buf, 0, len(buf))
        self._m_index.position = p
        self._m_index.write(dbuf, 0, 8)
        self._m_index.write(lbuf, 0, 4)
    
    def read_key_data_len(self, key : int) -> int:
        if (self._m_data is None): 
            if (not self.open0_(True, 0)): 
                return -1
        disp = 0
        len0_ = 0
        wrapdisp2682 = RefOutArgWrapper(0)
        wraplen2683 = RefOutArgWrapper(0)
        inoutres2684 = self.__read_index_info(key, wrapdisp2682, wraplen2683)
        disp = wrapdisp2682.value
        len0_ = wraplen2683.value
        if (not inoutres2684): 
            return -1
        else: 
            return len0_
    
    def read_key_data(self, key : int, max_len : int=0) -> bytearray:
        log0_ = False
        if (self._m_data is None): 
            if (log0_): 
                ConsoleHelper.write0_(" m_Data = null ")
            if (not self.open0_(True, 0)): 
                if (log0_): 
                    ConsoleHelper.write0_(" Can't open ")
                return None
        disp = 0
        len0_ = 0
        wrapdisp2685 = RefOutArgWrapper(0)
        wraplen2686 = RefOutArgWrapper(0)
        inoutres2687 = self.__read_index_info(key, wrapdisp2685, wraplen2686)
        disp = wrapdisp2685.value
        len0_ = wraplen2686.value
        if (not inoutres2687): 
            if (log0_): 
                ConsoleHelper.write0_(" Can't read IndexInfo ")
            return None
        if (log0_): 
            ConsoleHelper.write0_(" Disp={0}; Len = {1} ".format(disp, len0_))
        if (len0_ < 1): 
            return None
        if (disp >= self._m_data.length): 
            if (log0_): 
                ConsoleHelper.write0_(" disp ({0}) >= length ({1}) ".format(disp, self._m_data.length))
            return None
        if (max_len > 0 and len0_ > max_len): 
            len0_ = max_len
        res = Utils.newArrayOfBytes(len0_, 0)
        self._m_data.position = disp
        self._m_data.read(res, 0, len(res))
        if (self.auto_zip_data): 
            return KeyBaseTable.decompress_deflate(res)
        return res
    
    def read_keys_data(self, key_min : int, max_count : int, max_data_size : int=10000000) -> typing.List[tuple]:
        if (self.__m_read_ind_buf is None or len(self.__m_read_ind_buf) != (max_count * KeyBaseTable.__index_record_size)): 
            self.__m_read_ind_buf = Utils.newArrayOfBytes(max_count * KeyBaseTable.__index_record_size, 0)
        p = key_min
        p *= (KeyBaseTable.__index_record_size)
        self._m_index.position = p
        dlen = self._m_index.read(self.__m_read_ind_buf, 0, len(self.__m_read_ind_buf))
        if (dlen < KeyBaseTable.__index_record_size): 
            return None
        disp0 = 0
        len0 = 0
        ind = 0
        while (ind + KeyBaseTable.__index_record_size) <= len(self.__m_read_ind_buf): 
            disp0 = int.from_bytes(self.__m_read_ind_buf[ind:ind+8], byteorder="little")
            len0 = int.from_bytes(self.__m_read_ind_buf[ind + 8:ind + 8+4], byteorder="little")
            if (len0 > 0): 
                break
            key_min += 1
            ind += KeyBaseTable.__index_record_size
        if (len0 == 0): 
            return None
        ind0 = ind
        dpos_max = disp0 + (len0)
        ind += KeyBaseTable.__index_record_size
        first_pass3075 = True
        while True:
            if first_pass3075: first_pass3075 = False
            else: ind += KeyBaseTable.__index_record_size
            if (not ((ind + KeyBaseTable.__index_record_size) <= dlen)): break
            disp = int.from_bytes(self.__m_read_ind_buf[ind:ind+8], byteorder="little")
            len0_ = int.from_bytes(self.__m_read_ind_buf[ind + 8:ind + 8+4], byteorder="little")
            if (len0_ == 0): 
                continue
            if (disp > (dpos_max + (100)) or (disp < disp0)): 
                break
            if ((disp + (len0_)) > dpos_max): 
                if (((disp + (len0_)) - disp0) > max_data_size): 
                    break
                dpos_max = (disp + (len0_))
            else: 
                pass
        ind1 = ind
        dats = Utils.newArrayOfBytes(dpos_max - disp0, 0)
        self._m_data.position = disp0
        self._m_data.read(dats, 0, len(dats))
        res = dict()
        id0_ = key_min
        ind = ind0
        first_pass3076 = True
        while True:
            if first_pass3076: first_pass3076 = False
            else: ind += KeyBaseTable.__index_record_size; id0_ += 1
            if (not (ind < ind1)): break
            disp = int.from_bytes(self.__m_read_ind_buf[ind:ind+8], byteorder="little")
            len0_ = int.from_bytes(self.__m_read_ind_buf[ind + 8:ind + 8+4], byteorder="little")
            if (len0_ == 0): 
                continue
            dat = Utils.newArrayOfBytes(len0_, 0)
            i = 0
            while i < len0_: 
                dat[i] = dats[(disp - disp0) + (i)]
                i += 1
            if (self.auto_zip_data): 
                dat = KeyBaseTable.decompress_deflate(dat)
            res[id0_] = dat
        return res
    
    def remove_key_data(self, key : int) -> None:
        if (not self.open0_(False, 0)): 
            return
        disp = 0
        len0_ = 0
        wrapdisp2688 = RefOutArgWrapper(0)
        wraplen2689 = RefOutArgWrapper(0)
        inoutres2690 = self.__read_index_info(key, wrapdisp2688, wraplen2689)
        disp = wrapdisp2688.value
        len0_ = wraplen2689.value
        if (not inoutres2690): 
            return
        if (disp == (0)): 
            return
        self.__write_index_info(key, 0, 0)
        self.__m_unique_key_position = key
    
    def begin_fetch(self) -> None:
        if (self._m_index is None): 
            self.open0_(True, 0)
        self.__m_fetch_pos = 0
    
    def fetch_dic(self, res : typing.List[tuple], max_count : int) -> None:
        if (self._m_index is None): 
            return
        while self.__m_fetch_pos < self._m_index.length:
            id0_ = math.floor(self.__m_fetch_pos / KeyBaseTable.__index_record_size)
            data = self.read_key_data(id0_, 0)
            self.__m_fetch_pos += 12
            if (data is not None): 
                res[id0_] = data
            if (len(res) >= max_count): 
                break
    
    def fetch_percent(self) -> int:
        if (self._m_index.length > (100000)): 
            return math.floor(self.__m_fetch_pos / ((math.floor(self._m_index.length / (100)))))
        elif ((self._m_index.length) == 0): 
            return 0
        else: 
            return math.floor((self.__m_fetch_pos * 100) / (self._m_index.length))
    
    def fetch(self, max_count : int) -> typing.List[tuple]:
        if (self._m_index is None): 
            return None
        res = dict()
        while self.__m_fetch_pos < self._m_index.length:
            id0_ = math.floor(self.__m_fetch_pos / KeyBaseTable.__index_record_size)
            data = self.read_key_data(id0_, 0)
            self.__m_fetch_pos += 12
            if (data is not None): 
                res[id0_] = data
            if (len(res) >= max_count): 
                break
        return res
    
    def _end_fetch(self) -> None:
        self._close()
    
    def write_key_data(self, key : int, data : bytearray) -> None:
        if (self.auto_zip_data): 
            data = KeyBaseTable.compress_deflate(data)
        self.__add_data(key, data, self._m_data)
    
    def update_part_of_data(self, key : int, data : bytearray, pos : int) -> None:
        disp = 0
        len0_ = 0
        wrapdisp2691 = RefOutArgWrapper(0)
        wraplen2692 = RefOutArgWrapper(0)
        inoutres2693 = self.__read_index_info(key, wrapdisp2691, wraplen2692)
        disp = wrapdisp2691.value
        len0_ = wraplen2692.value
        if (not inoutres2693): 
            return
        self._m_data.position = disp + (pos)
        self._m_data.write(data, 0, len(data))
    
    def update_start_of_data(self, key : int, data : bytearray) -> None:
        disp = 0
        len0_ = 0
        wrapdisp2694 = RefOutArgWrapper(0)
        wraplen2695 = RefOutArgWrapper(0)
        inoutres2696 = self.__read_index_info(key, wrapdisp2694, wraplen2695)
        disp = wrapdisp2694.value
        len0_ = wraplen2695.value
        if (not inoutres2696): 
            return
        self._m_data.position = disp
        self._m_data.write(data, 0, len(data))
    
    def __add_data(self, key : int, data : bytearray, dst : Stream) -> None:
        if (data is None or self._m_index is None or dst is None): 
            return
        if (dst == self._m_data): 
            disp = 0
            len0_ = 0
            wrapdisp2697 = RefOutArgWrapper(0)
            wraplen2698 = RefOutArgWrapper(0)
            inoutres2699 = self.__read_index_info(key, wrapdisp2697, wraplen2698)
            disp = wrapdisp2697.value
            len0_ = wraplen2698.value
            if (inoutres2699): 
                if (len0_ >= len(data) and (disp + (len0_)) <= dst.length): 
                    dst.position = disp
                    dst.write(data, 0, len(data))
                    self.__write_index_info(key, disp, len(data))
                    return
        if (dst.length == (0)): 
            dst.writebyte(0xFF)
            dst.writebyte(0xFF)
        pos = dst.length
        if (len(data) > 0): 
            for i in range(2):
                try: 
                    dst.position = dst.length
                    dst.write(data, 0, len(data))
                    break
                except Exception as ex: 
                    if (i == 0): 
                        pass
                    if (i == 1): 
                        raise ex
        self.__write_index_info(key, pos, (0 if data is None else len(data)))
    
    def need_optimize(self, min_percent : int=10, analyze_disk_space : bool=True) -> bool:
        if (self._m_data is None): 
            return False
        le0 = self.__calc_data_optimized_length()
        if (le0 == (0)): 
            return False
        ration = 100 + min_percent
        ration /= (100)
        d = self._m_data.length
        d /= (le0)
        if (d > ration): 
            return True
        if (d < 1.05): 
            return False
        return False
    
    def optimize(self, min_percent : int=10) -> bool:
        is_opened = self._m_data is not None and self._m_data.writable
        if (is_opened): 
            self.flush()
        elif (not self.open0_(False, 10000000)): 
            return False
        if (min_percent > 0): 
            if (not self.need_optimize(min_percent, True)): 
                if (not is_opened): 
                    self._close()
                return False
        dir0_ = pathlib.PurePath(self._m_index_file_name).parent.absolute()
        temp_dat_file = pathlib.PurePath(dir0_).joinpath("temp.dat")
        if (pathlib.Path(temp_dat_file).is_file()): 
            pathlib.Path(temp_dat_file).unlink()
        temp_ind_file = pathlib.PurePath(dir0_).joinpath("temp.ind")
        if (pathlib.Path(temp_ind_file).is_file()): 
            pathlib.Path(temp_ind_file).unlink()
        tmp_table = KeyBaseTable(self.index, "temp", dir0_)
        tmp_table.open0_(False, 0)
        sw = Stopwatch()
        max0_ = self.get_max_key()
        id0_ = 1
        sw.start()
        p0 = 0
        auto_zip = self.auto_zip_data
        self.auto_zip_data = False
        while id0_ <= max0_:
            if (max0_ > 10000): 
                p = math.floor(id0_ / ((math.floor(max0_ / 100))))
                if (p != p0): 
                    p0 = p
                    print(" {0}%".format(p0), end="", flush=True)
            datas = self.read_keys_data(id0_, 1000, 10000000)
            if (datas is not None): 
                for kp in datas.items(): 
                    tmp_table.write_key_data(kp[0], kp[1])
                    if (kp[0] > id0_): 
                        id0_ = kp[0]
            id0_ += 1
        sw.stop()
        self._close()
        tmp_table.close()
        self.auto_zip_data = auto_zip
        pathlib.Path(self._m_data_file_name).unlink()
        shutil.move(temp_dat_file, self._m_data_file_name)
        pathlib.Path(self._m_index_file_name).unlink()
        shutil.move(temp_ind_file, self._m_index_file_name)
        if (is_opened): 
            self.open0_(False, 0)
        return True
    
    def upload_data_from_other_dir(self, dir_name : str, remove_after_copy : bool) -> bool:
        src_index_file_name = pathlib.PurePath(dir_name).joinpath(pathlib.PurePath(self._m_index_file_name).name)
        src_data_file_name = pathlib.PurePath(dir_name).joinpath(pathlib.PurePath(self._m_data_file_name).name)
        if (not pathlib.Path(src_index_file_name).is_file() or not pathlib.Path(src_data_file_name).is_file()): 
            return False
        is_opened = self._m_data is not None and self._m_data.writable
        self._close()
        if (remove_after_copy): 
            if (pathlib.Path(self._m_data_file_name).is_file()): 
                pathlib.Path(self._m_data_file_name).unlink()
            shutil.move(src_data_file_name, self._m_data_file_name)
            if (pathlib.Path(self._m_index_file_name).is_file()): 
                pathlib.Path(self._m_index_file_name).unlink()
            shutil.move(src_index_file_name, self._m_index_file_name)
        else: 
            shutil.copy(src_data_file_name, self._m_data_file_name)
            shutil.copy(src_index_file_name, self._m_index_file_name)
        if (is_opened): 
            self.open0_(False, 0)
        return True
    
    @staticmethod
    def compress_deflate(dat : bytearray) -> bytearray:
        if (dat is None): 
            return None
        zip0_ = None
        zip0_ = zlib.compress(dat, -15)
        return zip0_
    
    @staticmethod
    def decompress_deflate(zip0_ : bytearray) -> bytearray:
        if (zip0_ is None or (len(zip0_) < 1)): 
            return None
        try: 
            return zlib.decompress(zip0_, -15)
        except Exception as ex: 
            return None