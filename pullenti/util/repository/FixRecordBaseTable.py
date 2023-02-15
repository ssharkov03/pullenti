# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import typing
import struct
import math
import operator
import pathlib
from pullenti.unisharp.Utils import Utils

from pullenti.util.repository.KeyBaseTable import KeyBaseTable

class FixRecordBaseTable(KeyBaseTable):
    
    class FieldDefinition:
        """ Описание поля фиксированной записи """
        
        def __init__(self) -> None:
            self.is_key = False
            self.is_float = False
            self.merge_add = False
            self.name = None;
        
        def __str__(self) -> str:
            res = io.StringIO()
            if (self.name is not None): 
                print("{0} ".format(self.name), end="", file=res, flush=True)
            if (self.is_key): 
                print("Key ", end="", file=res)
            print(("Float" if self.is_float else "Int"), end="", file=res)
            if (self.merge_add): 
                print(" MergeAdd", end="", file=res)
            return Utils.toStringStringIO(res)
    
    class FixRecordsBuffer:
        
        def __init__(self, base_key_ : int, fields_ : typing.List['FieldDefinition']) -> None:
            self.base_key = 0
            self._record_size = 0
            self._key_count = 0
            self.fields = None;
            self.__m_ints = None;
            self.__m_floats = None;
            self.base_key = base_key_
            self._key_count = 0
            self._record_size = 0
            self.fields = fields_
            for f in fields_: 
                if (f.is_float): 
                    if (self.__m_floats is None): 
                        self.__m_floats = list()
                    self.__m_floats.append(list())
                else: 
                    if (self.__m_ints is None): 
                        self.__m_ints = list()
                    self.__m_ints.append(list())
                    if (f.is_key): 
                        self._key_count += 1
                self._record_size += 4
        
        @property
        def count(self) -> int:
            return (0 if self.__m_ints is None else len(self.__m_ints[0]))
        
        def find(self, i1 : int) -> int:
            return (-1 if self.__m_ints is None else Utils.indexOfList(self.__m_ints[0], i1, 0))
        
        def get_float(self, ind : int, i : int) -> float:
            if (self.__m_floats is None or (ind < 0) or ind >= len(self.__m_floats)): 
                return 0
            if ((i < 0) or i >= len(self.__m_floats[ind])): 
                return 0
            else: 
                return self.__m_floats[ind][i]
        
        def get_int(self, ind : int, i : int) -> int:
            if (self.__m_ints is None or (ind < 0) or ind >= len(self.__m_ints)): 
                return 0
            if ((i < 0) or i >= len(self.__m_ints[ind])): 
                return 0
            else: 
                return self.__m_ints[ind][i]
        
        def set_float(self, ind : int, i : int, val : float) -> None:
            if ((self.__m_floats is None or (ind < 0) or ind >= len(self.__m_floats)) or (i < 0)): 
                return
            if (i == len(self.__m_floats[ind])): 
                self.__m_floats[ind].append(val)
            else: 
                self.__m_floats[ind][i] = val
        
        def set_int(self, ind : int, i : int, val : int) -> None:
            if ((self.__m_ints is None or (ind < 0) or ind >= len(self.__m_ints)) or (i < 0)): 
                return
            if (i == len(self.__m_ints[ind])): 
                self.__m_ints[ind].append(val)
            else: 
                self.__m_ints[ind][i] = val
        
        def get_bytes_array(self) -> bytearray:
            res = bytearray()
            i = 0
            while i < self.count: 
                self.get_bytes(i, res)
                i += 1
            return bytearray(res)
        
        def get_bytes(self, i : int, res : bytearray) -> None:
            if (self.__m_ints is not None): 
                j = 0
                while j < len(self.__m_ints): 
                    res.extend((self.__m_ints[j][i]).to_bytes(4, byteorder="little"))
                    j += 1
            if (self.__m_floats is not None): 
                j = 0
                while j < len(self.__m_floats): 
                    res.extend(bytearray(struct.pack("f", self.__m_floats[j][i])))
                    j += 1
        
        def _add(self, i1 : int, i2 : int, i3 : int, f1 : float, f2 : float, f3 : float, i4 : int) -> bool:
            if (self.count > 0): 
                if (self._compare_with(self.count - 1, i1, i2) >= 0): 
                    return False
            if (self.__m_ints is not None): 
                self.__m_ints[0].append(i1)
                if (len(self.__m_ints) > 1): 
                    self.__m_ints[1].append(i2)
                if (len(self.__m_ints) > 2): 
                    self.__m_ints[2].append(i3)
                if (len(self.__m_ints) > 3): 
                    self.__m_ints[3].append(i4)
            if (self.__m_floats is not None): 
                self.__m_floats[0].append(f1)
                if (len(self.__m_floats) > 1): 
                    self.__m_floats[1].append(f2)
                if (len(self.__m_floats) > 2): 
                    self.__m_floats[2].append(f3)
            return True
        
        def _remove(self, ind : int) -> None:
            if (self.__m_ints is not None): 
                for li in self.__m_ints: 
                    del li[ind]
            if (self.__m_floats is not None): 
                for li in self.__m_floats: 
                    del li[ind]
        
        def _restore(self, data : bytearray) -> None:
            cou = math.floor(len(data) / self._record_size)
            self.__clear(cou)
            ind = 0
            i = 0
            while i < cou: 
                if (self.__m_ints is not None): 
                    j = 0
                    while j < len(self.__m_ints): 
                        self.__m_ints[j].append(int.from_bytes(data[ind:ind+4], byteorder="little"))
                        ind += 4
                        j += 1
                if (self.__m_floats is not None): 
                    j = 0
                    while j < len(self.__m_floats): 
                        self.__m_floats[j].append(struct.unpack('f', data[ind:ind+4])[0])
                        ind += 4
                        j += 1
                i += 1
        
        def cut(self, max_count_ : int, float_ind : int) -> bool:
            if (self.count <= max_count_): 
                return False
            if ((float_ind < 0) or float_ind >= len(self.__m_floats)): 
                return False
            li = list()
            i = 0
            while i < len(self.__m_floats[float_ind]): 
                li.append(FixRecordBaseTable.Temp._new2678(i, self.__m_floats[float_ind][i]))
                i += 1
            # PYTHON: sort(key=attrgetter('val'))
            li.sort(key=operator.attrgetter('val'))
            inds = list()
            for i in range(len(li) - 1, max_count_ - 1, -1):
                inds.append(li[i].ind)
            inds.sort()
            for i in range(len(inds) - 1, -1, -1):
                self._remove(inds[i])
            return True
        
        def __clear(self, capacity : int) -> None:
            if (self.__m_ints is not None): 
                for li in self.__m_ints: 
                    li.clear()
            if (self.__m_floats is not None): 
                for li in self.__m_floats: 
                    li.clear()
        
        def _compare_with_buf(self, ind : int, rd : 'FixRecordsBuffer', rb_ind : int) -> int:
            if (self.__m_ints is None): 
                return 0
            if (self.__m_ints[0][ind] < rd.__m_ints[0][rb_ind]): 
                return -1
            if (self.__m_ints[0][ind] > rd.__m_ints[0][rb_ind]): 
                return 1
            if ((self._key_count < 2) or (len(self.__m_ints) < 2)): 
                return 0
            if (self.__m_ints[1][ind] < rd.__m_ints[1][rb_ind]): 
                return -1
            if (self.__m_ints[1][ind] > rd.__m_ints[1][rb_ind]): 
                return 1
            return 0
        
        def _compare_with(self, ind : int, i1 : int, i2 : int) -> int:
            if (self.__m_ints is None): 
                return 0
            if (self.__m_ints[0][ind] < i1): 
                return -1
            if (self.__m_ints[0][ind] > i1): 
                return 1
            if ((self._key_count < 2) or (len(self.__m_ints) < 2)): 
                return 0
            if (self.__m_ints[1][ind] < i2): 
                return -1
            if (self.__m_ints[1][ind] > i2): 
                return 1
            return 0
        
        def check(self) -> bool:
            i = 0
            while i < (self.count - 1): 
                cmp = self._compare_with_buf(i, self, i + 1)
                if (cmp >= 0): 
                    return False
                i += 1
            return True
        
        @staticmethod
        def merge(buf1 : 'FixRecordsBuffer', buf2 : 'FixRecordsBuffer') -> 'FixRecordsBuffer':
            buf = buf1._merge_with(buf2)
            res = FixRecordBaseTable.FixRecordsBuffer(buf1.base_key, buf1.fields)
            res._restore(bytearray(buf))
            return res
        
        def _merge_with(self, buf : 'FixRecordsBuffer') -> bytearray:
            cou = self.count + ((math.floor(buf.count / 2)))
            i = ((math.floor(self.count / 2))) + buf.count
            if (cou < i): 
                cou = i
            res = bytearray()
            i = 0
            j = 0
            while (i < self.count) or (j < buf.count):
                if (i >= self.count): 
                    buf.get_bytes(j, res)
                    j += 1
                    continue
                if (j >= buf.count): 
                    self.get_bytes(i, res)
                    i += 1
                    continue
                cmp = self._compare_with_buf(i, buf, j)
                if (cmp < 0): 
                    self.get_bytes(i, res)
                    i += 1
                    continue
                if (cmp > 0): 
                    buf.get_bytes(j, res)
                    j += 1
                    continue
                ii = 0
                fi = 0
                ff = 0
                while ff < len(self.fields): 
                    if (self.fields[ff].is_float): 
                        f = buf.get_float(fi, j)
                        if (self.fields[ff].merge_add): 
                            self.set_float(fi, i, self.get_float(fi, i) + f)
                        elif (f > 0): 
                            self.set_float(fi, i, f)
                        fi += 1
                    else: 
                        if (self.fields[ff].merge_add): 
                            self.set_int(ii, i, self.get_int(ii, i) + buf.get_int(ii, j))
                        ii += 1
                    ff += 1
                self.get_bytes(i, res)
                i += 1
                j += 1
            return res
    
    class Temp(object):
        
        def __init__(self) -> None:
            self.ind = 0
            self.val = 0
        
        def compareTo(self, obj : object) -> int:
            f = obj.val
            if (self.val > f): 
                return -1
            if (self.val < f): 
                return 1
            return 0
        
        @staticmethod
        def _new2678(_arg1 : int, _arg2 : float) -> 'Temp':
            res = FixRecordBaseTable.Temp()
            res.ind = _arg1
            res.val = _arg2
            return res
    
    def __init__(self, index_ : 'IRepository', name_ : str) -> None:
        super().__init__(index_, name_, None)
        self.max_count = 0
        self.max_count_float_index = 0
        self._m_fix_record_fields = list()
        self.__m_add_buffer = None;
        self.__m_last_readed_fix_records = None;
        self.__m_fetch_last_id = 0
    
    @property
    def record_size(self) -> int:
        return len(self._m_fix_record_fields) * 4
    
    @property
    def records_count(self) -> int:
        if (self._m_data is not None): 
            return math.floor(self._m_data.length / (self.record_size))
        fi = pathlib.Path(self._m_data_file_name)
        if (fi.is_file()): 
            return math.floor(fi.stat().st_size / (self.record_size))
        return 0
    
    def _close(self) -> None:
        self.__m_last_readed_fix_records = (None)
        try: 
            self.__save_buffer()
        except Exception as ex: 
            pass
        super()._close()
    
    def flush(self) -> None:
        try: 
            self.__save_buffer()
        except Exception as ex: 
            pass
        super().flush()
    
    def _add_fix_record(self, key : int, i1 : int, i2 : int, i3 : int, f1 : float, f2 : float, f3 : float, i4 : int=0) -> None:
        if (self.__m_last_readed_fix_records is not None and self.__m_last_readed_fix_records.base_key == key): 
            self.__m_last_readed_fix_records = (None)
        if (self.__m_add_buffer is not None and self.__m_add_buffer.base_key != key): 
            self.__save_buffer()
        if (self.__m_add_buffer is None): 
            self.__m_add_buffer = FixRecordBaseTable.FixRecordsBuffer(key, self._m_fix_record_fields)
        if (not self.__m_add_buffer._add(i1, i2, i3, f1, f2, f3, i4)): 
            self.__save_buffer()
            self.__m_add_buffer = FixRecordBaseTable.FixRecordsBuffer(key, self._m_fix_record_fields)
            self.__m_add_buffer._add(i1, i2, i3, f1, f2, f3, i4)
    
    def get_fix_records(self, key : int) -> 'FixRecordsBuffer':
        if (self.__m_add_buffer is not None): 
            if (key == self.__m_add_buffer.base_key): 
                self.__save_buffer()
        if (self.__m_last_readed_fix_records is not None and self.__m_last_readed_fix_records.base_key == key): 
            return self.__m_last_readed_fix_records
        res = FixRecordBaseTable.FixRecordsBuffer(key, self._m_fix_record_fields)
        data = self.read_key_data(key, 0)
        if (data is not None): 
            res._restore(data)
        self.__m_last_readed_fix_records = res
        return res
    
    def save_fix_records(self, buf : 'FixRecordsBuffer') -> None:
        self.__m_last_readed_fix_records = (None)
        self.write_key_data(buf.base_key, buf.get_bytes_array())
    
    def __save_buffer(self) -> None:
        if (self.__m_add_buffer is None): 
            return
        ex_data = self.read_key_data(self.__m_add_buffer.base_key, 0)
        if (ex_data is None or len(ex_data) == 0): 
            if (self.max_count > 0 and (self.max_count < self.__m_add_buffer.count)): 
                self.__m_add_buffer.cut(self.max_count, self.max_count_float_index)
            self.write_key_data(self.__m_add_buffer.base_key, self.__m_add_buffer.get_bytes_array())
            self.__m_add_buffer = (None)
            return
        ex_recs = FixRecordBaseTable.FixRecordsBuffer(self.__m_add_buffer.base_key, self._m_fix_record_fields)
        ex_recs._restore(ex_data)
        res = ex_recs._merge_with(self.__m_add_buffer)
        bytes0_ = None
        if (self.max_count > 0): 
            cou = math.floor(len(res) / ex_recs._record_size)
            if (cou > self.max_count): 
                tmp = FixRecordBaseTable.FixRecordsBuffer(self.__m_add_buffer.base_key, self._m_fix_record_fields)
                tmp._restore(bytearray(res))
                tmp.cut(self.max_count, self.max_count_float_index)
                bytes0_ = tmp.get_bytes_array()
        if (bytes0_ is None): 
            bytes0_ = (bytearray(res))
        self.write_key_data(self.__m_add_buffer.base_key, bytes0_)
        self.__m_add_buffer = (None)
    
    def begin_fetch_all_fix_records_buffer(self, first_id : int=1) -> None:
        self.__m_fetch_last_id = (first_id - 1)
    
    def fetch_fix_records_buffer(self, max_count_ : int=1000) -> typing.List['FixRecordsBuffer']:
        self.__m_fetch_last_id += 1
        if (self.__m_fetch_last_id > self.get_max_key()): 
            return None
        dats = self.read_keys_data(self.__m_fetch_last_id, max_count_, 10000000)
        res = list()
        if (dats is None): 
            self.__m_fetch_last_id += max_count_
            return res
        for kp in dats.items(): 
            if (kp[1] is not None): 
                buf = FixRecordBaseTable.FixRecordsBuffer(kp[0], self._m_fix_record_fields)
                buf._restore(kp[1])
                res.append(buf)
                self.__m_fetch_last_id = kp[0]
        return res