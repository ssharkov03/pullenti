# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import typing
from pullenti.unisharp.Utils import Utils

from pullenti.address.HouseType import HouseType
from pullenti.address.SpecialAttributes import SpecialAttributes
from pullenti.address.RoomType import RoomType
from pullenti.address.GarLevel import GarLevel
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.address.AreaAttributes import AreaAttributes
from pullenti.address.HouseAttributes import HouseAttributes
from pullenti.address.RoomAttributes import RoomAttributes
from pullenti.address.internal.GarHelper import GarHelper

class RepaddrSearchObj:
    
    __error = 1000
    
    def __init__(self, a : 'TextObject', typs : 'RepTypTable') -> None:
        self.search_strs = list()
        self.type_ids = list()
        self.lev = GarLevel.UNDEFINED
        self.src = None;
        self.src = a
        aa = Utils.asObjectOrNull(a.attrs, AreaAttributes)
        if (aa is None): 
            return
        self.lev = aa.level
        for ty in aa.types: 
            self.type_ids.append(typs.get_id(ty))
        if (len(a.gars) > 0): 
            for g in a.gars: 
                if (g is not None): 
                    self.search_strs.append(g.guid.replace("-", ""))
        i0 = len(self.search_strs)
        if (aa.names is not None): 
            for v in aa.names: 
                self.search_strs.append(self.__corr_string(v.upper()))
        if (aa.number is not None): 
            if (i0 == len(self.search_strs)): 
                self.search_strs.append(aa.number)
            else: 
                i = i0
                while i < len(self.search_strs): 
                    self.search_strs[i] = "{0} {1}".format(self.search_strs[i], aa.number)
                    i += 1
    
    def __corr_string(self, str0_ : str) -> str:
        need_corr = False
        for ch in str0_: 
            if (ch == 'Ь' or ch == 'Ъ'): 
                need_corr = True
        i = 0
        while i < (len(str0_) - 1): 
            if (str0_[i] == str0_[i + 1]): 
                need_corr = True
            i += 1
        if (not need_corr): 
            return str0_
        res = io.StringIO()
        i = 0
        first_pass2725 = True
        while True:
            if first_pass2725: first_pass2725 = False
            else: i += 1
            if (not (i < len(str0_))): break
            ch = str0_[i]
            if (ch == 'Ь' or ch == 'Ъ'): 
                continue
            if (res.tell() > 0 and Utils.getCharAtStringIO(res, res.tell() - 1) == ch): 
                continue
            print(ch, end="", file=res)
        return Utils.toStringStringIO(res)
    
    def calc_coef(self, o : 'RepAddrTreeNodeObj', parent : 'RepaddrObject', parent2 : 'RepaddrObject') -> int:
        if (o.lev != self.lev): 
            return RepaddrSearchObj.__error
        ret = 0
        eq_typs = False
        for id0_ in self.type_ids: 
            if (id0_ in o.typ_ids): 
                eq_typs = True
                break
        if (not eq_typs): 
            if (self.lev == GarLevel.AREA or self.lev == GarLevel.LOCALITY): 
                if (len(self.src.attrs.names) == 0): 
                    return RepaddrSearchObj.__error
                ret += 10
            else: 
                return RepaddrSearchObj.__error
        if (parent is None): 
            if (o.parents is None or len(o.parents) == 0): 
                pass
            else: 
                return RepaddrSearchObj.__error
        else: 
            if (o.parents is None or len(o.parents) == 0): 
                return RepaddrSearchObj.__error
            i = Utils.indexOfList(o.parents, parent.id0_, 0)
            if (i < 0): 
                if (parent2 is not None and GarHelper.can_be_parent(self.lev, parent2.level, "город" in parent2.types)): 
                    i = Utils.indexOfList(o.parents, parent2.id0_, 0)
                    if (i >= 0): 
                        ret += 10
                    else: 
                        return RepaddrSearchObj.__error
                else: 
                    return RepaddrSearchObj.__error
        return ret
    
    @staticmethod
    def get_search_strings(o : 'TextObject') -> typing.List[str]:
        res = list()
        tmp = io.StringIO()
        h = Utils.asObjectOrNull(o.attrs, HouseAttributes)
        r = Utils.asObjectOrNull(o.attrs, RoomAttributes)
        s = Utils.asObjectOrNull(o.attrs, SpecialAttributes)
        if (h is not None): 
            if (h.number is not None or h.typ != HouseType.UNDEFINED): 
                if (h.typ == HouseType.PLOT): 
                    print('p', end="", file=tmp)
                elif (h.typ == HouseType.GARAGE): 
                    print('g', end="", file=tmp)
                print(("0" if Utils.isNullOrEmpty(h.number) else h.number), end="", file=tmp)
            if (h.build_number is not None): 
                print("b{0}".format(h.build_number), end="", file=tmp, flush=True)
            if (h.stroen_number is not None): 
                print("s{0}".format(h.stroen_number), end="", file=tmp, flush=True)
        elif (r is not None): 
            if (r.number is not None or r.typ != RoomType.UNDEFINED): 
                if (r.typ == RoomType.FLAT): 
                    print('f', end="", file=tmp)
                elif (r.typ == RoomType.CARPLACE): 
                    print('c', end="", file=tmp)
                print(("0" if Utils.isNullOrEmpty(r.number) else r.number), end="", file=tmp)
        if (tmp.tell() == 0): 
            print(str(o), end="", file=tmp)
        res.append(Utils.toStringStringIO(tmp))
        if (s is None): 
            i = 0
            while i < tmp.tell(): 
                if (str.isalpha(Utils.getCharAtStringIO(tmp, i)) and str.isupper(Utils.getCharAtStringIO(tmp, i))): 
                    ch = Utils.getCharAtStringIO(tmp, i)
                    ch1 = LanguageHelper.get_cyr_for_lat(ch)
                    if ((ord(ch1)) != 0): 
                        Utils.setCharAtStringIO(tmp, i, ch1)
                        res.append(Utils.toStringStringIO(tmp))
                        Utils.setCharAtStringIO(tmp, i, ch)
                    if (h is not None): 
                        if ((h.stroen_number is None and h.build_number is None and i > 0) and str.isdigit(Utils.getCharAtStringIO(tmp, i - 1))): 
                            Utils.insertStringIO(tmp, i, "s")
                            res.append(Utils.toStringStringIO(tmp))
                            Utils.removeStringIO(tmp, i, 1)
                i += 1
        for g in o.gars: 
            res.append(g.guid.replace("-", ""))
        return res