# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import datetime
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.util.repository.FixRecordBaseTable import FixRecordBaseTable
from pullenti.util.repository.BaseTable import BaseTable

class DateIndexTable(FixRecordBaseTable):
    
    def __init__(self, index_ : 'IRepository', name_ : str) -> None:
        super().__init__(index_, name_)
    
    __s_min_date = None
    
    def _calc_key(self, dt : datetime.datetime, read_only : bool) -> int:
        if (DateIndexTable.__s_min_date is None): 
            dat = self._read_index0()
            if (dat is not None): 
                i = 0
                wrapi2677 = RefOutArgWrapper(i)
                DateIndexTable.__s_min_date = BaseTable._to_date(dat, wrapi2677)
                i = wrapi2677.value
                if (DateIndexTable.__s_min_date is None): 
                    DateIndexTable.__s_min_date = ((datetime.datetime(2010, 1, 1, 0, 0, 0)) + datetime.timedelta(days=-1))
        if (DateIndexTable.__s_min_date is None): 
            if (read_only): 
                return -1
            DateIndexTable.__s_min_date = Utils.getDate(dt)
            tmp = bytearray()
            BaseTable._get_bytes_for_date(tmp, DateIndexTable.__s_min_date)
            self._write_index0(bytearray(tmp))
        elif (DateIndexTable.__s_min_date > Utils.getDate(dt)): 
            if (read_only): 
                return -1
            self.flush()
            ts0 = DateIndexTable.__s_min_date - Utils.getDate(dt)
            self._shift_index(ts0.days)
            DateIndexTable.__s_min_date = Utils.getDate(dt)
            tmp = bytearray()
            BaseTable._get_bytes_for_date(tmp, DateIndexTable.__s_min_date)
            self._write_index0(bytearray(tmp))
        ts = Utils.getDate(dt) - DateIndexTable.__s_min_date
        return (ts.days) + 1
    
    def get_date_by_id(self, id0_ : int) -> datetime.datetime:
        if (DateIndexTable.__s_min_date is None): 
            self._calc_key(datetime.datetime.now(), True)
        if (DateIndexTable.__s_min_date is None): 
            return None
        return (DateIndexTable.__s_min_date + datetime.timedelta(days=id0_ - 1))