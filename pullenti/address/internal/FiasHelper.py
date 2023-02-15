# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.unisharp.Streams import Stream

from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.address.StreetReferent import StreetReferent
from pullenti.ner.address.internal.AddressItemToken import AddressItemToken

class FiasHelper:
    
    @staticmethod
    def correct_fias_name(name : str) -> str:
        if (name is None): 
            return None
        ii = name.find(", находящ")
        if (ii < 0): 
            ii = name.find(",находящ")
        if (ii > 0): 
            name = name[0:0+ii].strip()
        return name
    
    @staticmethod
    def corr_name(str0_ : str) -> str:
        res = io.StringIO()
        FiasHelper.__corr_name(res, str0_.upper())
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def __corr_name(res : io.StringIO, str0_ : str) -> int:
        corr = 0
        i = 0
        first_pass2723 = True
        while True:
            if first_pass2723: first_pass2723 = False
            else: i += 1
            if (not (i < len(str0_))): break
            ch = str0_[i]
            if (ch == 'Ь' or ch == 'Ъ'): 
                corr += 1
                continue
            if (str.isalnum(ch) or ch == ' ' or ch == '-'): 
                if (ch == '-'): 
                    ch = ' '
                    corr += 1
                if (i > 0 and res.tell() > 0 and Utils.getCharAtStringIO(res, res.tell() - 1) == ch): 
                    corr += 1
                    continue
                print(ch, end="", file=res)
        return corr
    
    @staticmethod
    def __add_name_variants(res : typing.List[str], name : str, num : str=None) -> None:
        if (name is None): 
            return
        items = list()
        sps = 0
        hiphs = 0
        i = 0
        while i < len(name): 
            ch = name[i]
            j = 0
            if (str.isalpha(ch)): 
                j = i
                while j < len(name): 
                    if (not str.isalpha(name[j])): 
                        break
                    j += 1
                if (i == 0 and j == len(name)): 
                    items.append(name)
                else: 
                    items.append(name[i:i+j - i])
                i = (j - 1)
            elif (ch == ' ' or ch == '.'): 
                sps += 1
            elif (ch == '-'): 
                hiphs += 1
            elif (str.isdigit(ch) and num is None): 
                j = i
                while j < len(name): 
                    if (not str.isdigit(name[j])): 
                        break
                    j += 1
                num = name[i:i+j - i]
                i = (j - 1)
            i += 1
        std_adj = None
        i = 0
        while i < len(items): 
            it = items[i]
            for k in range(2):
                adjs = (FiasHelper.__m_std_arjso if k == 0 else FiasHelper.__m_std_arjse)
                for a in adjs: 
                    if (it.startswith(a)): 
                        if (len(it) == (len(a) + 2)): 
                            std_adj = a
                            del items[i]
                            break
                        if (len(it) == (len(a) + 1)): 
                            if (k == 0 and it[len(a)] == 'О'): 
                                pass
                            elif (k == 1 and it[len(a)] == 'Е'): 
                                pass
                            else: 
                                continue
                            std_adj = a
                            del items[i]
                            break
                        if (len(it) > (len(a) + 3)): 
                            if (k == 0 and it[len(a)] == 'О'): 
                                pass
                            elif (k == 1 and it[len(a)] == 'Е'): 
                                pass
                            else: 
                                continue
                            std_adj = a
                            items[i] = it[len(a) + 1:]
                            break
                if (std_adj is not None): 
                    break
            if (std_adj is not None): 
                break
            i += 1
        for kk in range(2):
            tmp = io.StringIO()
            corr = False
            i = 0
            while i < len(items): 
                if (FiasHelper.__corr_name(tmp, items[i]) > 0): 
                    corr = True
                i += 1
            if (std_adj is not None): 
                print("_{0}".format(std_adj[0]), end="", file=tmp, flush=True)
            if (num is not None): 
                print(num, end="", file=tmp)
            r = Utils.toStringStringIO(tmp)
            if (not r in res): 
                res.append(r)
            if (corr): 
                Utils.setLengthStringIO(tmp, 0)
                i = 0
                while i < len(items): 
                    print(items[i], end="", file=tmp)
                    i += 1
                if (std_adj is not None): 
                    print("_{0}".format(std_adj[0]), end="", file=tmp, flush=True)
                if (num is not None): 
                    print(num, end="", file=tmp)
                r = Utils.toStringStringIO(tmp)
                if (not r in res): 
                    res.append(r)
            if (len(items) <= 1): 
                break
            items.reverse()
    
    __m_std_arjso = None
    
    __m_std_arjse = None
    
    @staticmethod
    def _get_strings(r : 'Referent') -> typing.List[str]:
        if (r is None): 
            return None
        res = list()
        if (isinstance(r, GeoReferent)): 
            for s in r.slots: 
                if (s.type_name == GeoReferent.ATTR_NAME): 
                    FiasHelper.__add_name_variants(res, Utils.asObjectOrNull(s.value, str), None)
        elif (r.type_name == "ORGANIZATION"): 
            num = r.get_string_value("NUMBER")
            for s in r.slots: 
                if (s.type_name == "NAME"): 
                    FiasHelper.__add_name_variants(res, Utils.asObjectOrNull(s.value, str), num)
                elif (s.type_name == "EPONYM"): 
                    FiasHelper.__add_name_variants(res, s.value.upper(), num)
            if (len(res) == 0 and num is not None): 
                res.append(num)
        elif (isinstance(r, StreetReferent)): 
            str0_ = Utils.asObjectOrNull(r, StreetReferent)
            num = str0_.number
            sec_num = str0_.sec_number
            if (sec_num is not None and num is not None): 
                n1 = 0
                n2 = 0
                wrapn1104 = RefOutArgWrapper(0)
                inoutres105 = Utils.tryParseInt(num, wrapn1104)
                wrapn2106 = RefOutArgWrapper(0)
                inoutres107 = Utils.tryParseInt(sec_num, wrapn2106)
                n1 = wrapn1104.value
                n2 = wrapn2106.value
                if (inoutres105 and inoutres107): 
                    if (n1 > n2): 
                        num = "{0} {1}".format(sec_num, num)
                    else: 
                        num = "{0} {1}".format(num, sec_num)
                elif (Utils.compareStrings(num, sec_num, False) < 0): 
                    num = "{0} {1}".format(num, sec_num)
                else: 
                    num = "{0} {1}".format(sec_num, num)
            for s in r.slots: 
                if (s.type_name == StreetReferent.ATTR_NAME): 
                    FiasHelper.__add_name_variants(res, Utils.asObjectOrNull(s.value, str), num)
            if (len(res) == 0 and num is not None): 
                res.append(num)
            if (len(res) == 0): 
                ty = r.get_string_value(StreetReferent.ATTR_TYPE)
                if (ty is not None): 
                    res.append(FiasHelper.corr_name(ty.upper()))
        return res
    
    @staticmethod
    def get_house_string(ho : 'HouseObject') -> str:
        if (ho.struc_number is None and ho.build_number is None): 
            re = FiasHelper.__corr_number(ho.house_number)
            if (Utils.isNullOrEmpty(re)): 
                return "0"
            return re
        res = io.StringIO()
        str0_ = FiasHelper.__corr_number(ho.house_number)
        if (str0_ is not None): 
            print(str0_, end="", file=res)
        str0_ = FiasHelper.__corr_number(ho.build_number)
        if ((str0_) is not None): 
            print("b{0}".format(str0_), end="", file=res, flush=True)
        str0_ = FiasHelper.__corr_number(ho.struc_number)
        if ((str0_) is not None): 
            print("s{0}".format(str0_), end="", file=res, flush=True)
        if (res.tell() == 0): 
            return "0"
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def __corr_number(str0_ : str) -> str:
        if (Utils.isNullOrEmpty(str0_)): 
            return None
        if (str0_ == "0"): 
            return None
        if ("Б/Н" in str0_): 
            str0_ = str0_.replace("Б/Н", "")
            if (Utils.isNullOrEmpty(str0_)): 
                return None
        if ("НЕТ" in str0_): 
            str0_ = str0_.replace("НЕТ", "")
            if (Utils.isNullOrEmpty(str0_)): 
                return None
        if (str0_.startswith("БН") or str0_.endswith("БН")): 
            str0_ = str0_.replace("БН", "")
            if (Utils.isNullOrEmpty(str0_)): 
                return None
        while len(str0_) > 1 and str0_[0] == '0':
            str0_ = str0_[1:]
        digs = 0
        lets = 0
        for s in str0_: 
            if (str.isdigit(s)): 
                digs += 1
            elif (str.isalpha(s)): 
                lets += 1
        if (digs == len(str0_)): 
            return str0_
        if (digs == 0 and lets == 0): 
            return str0_
        res = io.StringIO()
        i = 0
        while i < len(str0_): 
            ch = str0_[i]
            if (str.isdigit(ch)): 
                if (res.tell() > 0 and str.isdigit(Utils.getCharAtStringIO(res, res.tell() - 1)) and not str.isdigit(str0_[i - 1])): 
                    print(' ', end="", file=res)
                print(ch, end="", file=res)
            elif (str.isalpha(ch)): 
                corr = (AddressItemToken.correct_char(str.upper(ch)) if lets == 1 else ch)
                if ((ord(corr)) == 0): 
                    corr = ch
                print(corr, end="", file=res)
            i += 1
        while res.tell() > 0 and Utils.getCharAtStringIO(res, res.tell() - 1) == ' ':
            Utils.setLengthStringIO(res, res.tell() - 1)
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def get_house_strings(a : 'AddressReferent') -> typing.List[str]:
        s = None
        str0_ = None
        s = a.plot
        if ((s) is not None): 
            str0_ = FiasHelper.__corr_number(a.plot)
            res0 = list()
            res0.append(str0_)
            return res0
        s = a.house_or_plot
        if ((s) is not None): 
            str0_ = FiasHelper.__corr_number(a.house_or_plot)
        else: 
            s = a.house
            if ((s) is not None): 
                str0_ = FiasHelper.__corr_number(s)
        str2 = None
        str22 = None
        s = a.corpus
        if ((s) is not None): 
            str2 = FiasHelper.__corr_number(s)
        s = a.corpus_or_flat
        if ((s) is not None): 
            str22 = FiasHelper.__corr_number(s)
            if (str22 is not None and not str.isdigit(str22[0]) and str2 is None): 
                str2 = str22
                str22 = (None)
        str3 = None
        s = a.building
        if ((s) is not None): 
            str3 = FiasHelper.__corr_number(s)
        else: 
            s = a.block
            if ((s) is not None): 
                str3 = FiasHelper.__corr_number(s)
        if (str0_ is None and str2 is None and str3 is None): 
            if (a.house is not None or a.corpus is not None): 
                res0 = list()
                res0.append("0")
                return res0
            return None
        res = list()
        if (not Utils.isNullOrEmpty(str0_)): 
            if (str2 is None): 
                if (str3 is None): 
                    res.append(str0_)
                    ii = str0_.find(' ')
                    if (ii > 0): 
                        fi = str0_[0:0+ii]
                        se = str0_[ii + 1:]
                        res.append("{0} {1}".format(se, fi))
                        res.append("{0}b{1}".format(fi, se))
                        res.append("{0}s{1}".format(fi, se))
                    elif (len(str0_) > 1 and str.isalpha(str0_[len(str0_) - 1]) and str.isdigit(str0_[len(str0_) - 2])): 
                        num1 = str0_[0:0+len(str0_) - 1]
                        ch = str0_[len(str0_) - 1]
                        res.append("{0}s{1}".format(num1, ch))
                else: 
                    res.append("{0}s{1}".format(str0_, str3))
                res.append("b" + res[0])
                if (str22 is not None and str3 is None): 
                    res.append("{0}b{1}".format(str0_, str22))
                if (str3 == "1"): 
                    res.append(str0_)
                elif (str3 is None): 
                    res.append(str0_ + "b1")
                    res.append(str0_ + "s1")
                    res.append(str0_ + "sА")
                    res.append(str0_ + "bА")
            elif (str3 is None): 
                res.append("{0}b{1}".format(str0_, str2))
                res.append("{0}s{1}".format(str0_, str2))
                if (not str.isdigit(str2[0])): 
                    sss = FiasHelper.__corr_number(str0_ + str2)
                    res.append(sss)
                    res.append("b" + sss)
                elif (len(str2) > 1 and str.isdigit(str2[0]) and not str.isdigit(str2[len(str2) - 1])): 
                    res.append("{0}b{1}s{2}".format(str0_, str2[0:0+len(str2) - 1], str2[len(str2) - 1]))
                if (str2 == "1"): 
                    res.append(str0_)
            else: 
                res.append("{0}b{1}s{2}".format(str0_, str2, str3))
                if (not str.isdigit(str2[0])): 
                    sss = FiasHelper.__corr_number(str0_ + str2)
                    res.append("{0}s{1}".format(sss, str3))
                    res.append("b{0}s{1}".format(sss, str3))
                if (str2 == "1"): 
                    res.append("{0}s{1}".format(str0_, str3))
        elif (str2 is None): 
            res.append("s" + str3)
            res.append("b" + str3)
        elif (str3 is None): 
            res.append("b" + str2)
            res.append(str2)
            res.append("s" + str2)
        else: 
            res.append("b{0}s{1}".format(str2, str3))
            res.append("{0}s{1}".format(str2, str3))
            res.append("s{0}b{1}".format(str2, str3))
        return res
    
    @staticmethod
    def get_room_string(ho : 'RoomObject') -> str:
        if (ho.room_number is None): 
            return FiasHelper.__corr_number(ho.flat_number)
        res = io.StringIO()
        str0_ = FiasHelper.__corr_number(ho.flat_number)
        str0_ = FiasHelper.__corr_number(ho.room_number)
        if ((str0_) is not None): 
            print("r{0}".format(str0_), end="", file=res, flush=True)
        if (res.tell() == 0): 
            return "0"
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def get_room_stringr(a : 'AddressReferent') -> str:
        res = Utils.ifNotNull(Utils.ifNotNull(a.flat, Utils.ifNotNull(a.pavilion, a.box)), a.corpus_or_flat)
        if (res is not None): 
            room = Utils.ifNotNull(a.office, a.room)
            if (room is not None): 
                res = "{0}r{1}".format(res, room)
        else: 
            res = (Utils.ifNotNull(a.office, a.room))
        return res
    
    @staticmethod
    def parse_code(cod : str, aa : int) -> typing.List[int]:
        cods = list()
        aa.value = 0
        if (cod is None or (len(cod) < 11)): 
            return cods
        i = 0
        cods.append(int(cod[0:0+2]))
        cods.append(int(cod[2:2+3]))
        cods.append(int(cod[5:5+3]))
        cods.append(int(cod[8:8+3]))
        i = len(cod)
        if (i == 13): 
            aa.value = int(cod[11:])
        elif (i >= 15): 
            cods.append(int(cod[11:11+4]))
            if (i == 17): 
                aa.value = int(cod[15:])
            elif (i >= 19): 
                cods.append(int(cod[15:15+4]))
                if (i == 23): 
                    cods.append(int(cod[19:19+4]))
        return cods
    
    @staticmethod
    def serialize_byte(res : Stream, val : int) -> None:
        res.writebyte(val)
    
    @staticmethod
    def serialize_short(res : Stream, val : int) -> None:
        res.writebyte(val)
        res.writebyte((val >> 8))
    
    @staticmethod
    def serialize_int(res : Stream, val : int) -> None:
        res.writebyte(val)
        res.writebyte((val >> 8))
        res.writebyte((val >> 16))
        res.writebyte((val >> 24))
    
    @staticmethod
    def deserialize_byte(str0_ : Stream) -> int:
        return str0_.readbyte()
    
    @staticmethod
    def deserialize_short(str0_ : Stream) -> int:
        b0 = str0_.readbyte()
        b1 = str0_.readbyte()
        res = b1
        res <<= 8
        return (res | b0)
    
    @staticmethod
    def deserialize_int(str0_ : Stream) -> int:
        b0 = str0_.readbyte()
        b1 = str0_.readbyte()
        b2 = str0_.readbyte()
        b3 = str0_.readbyte()
        res = b3
        res <<= 8
        res |= b2
        res <<= 8
        res |= b1
        res <<= 8
        return (res | b0)
    
    @staticmethod
    def serialize_string(res : Stream, s : str, utf8 : bool=False) -> None:
        if (s is None): 
            res.writebyte(0xFF)
        elif (len(s) == 0): 
            res.writebyte(0)
        else: 
            data = (s.encode("UTF-8", 'ignore') if utf8 else FiasHelper.encode_string1251(s))
            res.writebyte(len(data))
            res.write(data, 0, len(data))
    
    @staticmethod
    def deserialize_string_from_bytes(dat : bytearray, ind : int, utf8 : bool=False) -> str:
        len0_ = dat[ind.value]
        ind.value += 1
        if (len0_ == (0xFF)): 
            return None
        if (len0_ == (0)): 
            return ""
        res = (dat[ind.value:ind.value+len0_].decode("UTF-8", 'ignore') if utf8 else FiasHelper.decode_string1251(dat, ind.value, len0_))
        ind.value += (len0_)
        return res
    
    @staticmethod
    def deserialize_string(str0_ : Stream) -> str:
        len0_ = str0_.readbyte()
        if (len0_ == (0xFF)): 
            return None
        if (len0_ == (0)): 
            return ""
        buf = Utils.newArrayOfBytes(len0_, 0)
        str0_.read(buf, 0, len0_)
        return FiasHelper.decode_string1251(buf, 0, -1)
    
    __m_1251_utf = None
    
    __m_utf_1251 = None
    
    @staticmethod
    def encode_string1251(str0_ : str) -> bytearray:
        if (str0_ is None): 
            return Utils.newArrayOfBytes(0, 0)
        res = Utils.newArrayOfBytes(len(str0_), 0)
        j = 0
        while j < len(str0_): 
            i = ord(str0_[j])
            if (i < 0x80): 
                res[j] = (i)
            else: 
                b = 0
                wrapb108 = RefOutArgWrapper(0)
                inoutres109 = Utils.tryGetValue(FiasHelper.__m_utf_1251, i, wrapb108)
                b = wrapb108.value
                if (inoutres109): 
                    res[j] = b
                else: 
                    res[j] = (ord('?'))
            j += 1
        return res
    
    @staticmethod
    def decode_string1251(dat : bytearray, pos : int=0, len0_ : int=-1) -> str:
        if (dat is None): 
            return None
        if (len(dat) == 0): 
            return ""
        if (len0_ < 0): 
            len0_ = (len(dat) - pos)
        tmp = io.StringIO()
        j = pos
        while (j < (pos + len0_)) and (j < len(dat)): 
            i = dat[j]
            if (i < 0x80): 
                print(chr(i), end="", file=tmp)
            elif (FiasHelper.__m_1251_utf[i] == 0): 
                print('?', end="", file=tmp)
            else: 
                print(chr(FiasHelper.__m_1251_utf[i]), end="", file=tmp)
            j += 1
        return Utils.toStringStringIO(tmp)
    
    # static constructor for class FiasHelper
    @staticmethod
    def _static_ctor():
        FiasHelper.__m_std_arjso = ["СТАР", "НОВ", "МАЛ", "СЕВЕР", "ЮГ", "ЮЖН", "ЗАПАДН", "ВОСТОЧН", "КРАСН", "ГЛАВН", "ВЕЛИК"]
        FiasHelper.__m_std_arjse = ["ВЕРХН", "НИЖН", "СРЕДН", "БОЛЬШ"]
        FiasHelper.__m_1251_utf = Utils.newArray(256, 0)
        FiasHelper.__m_utf_1251 = dict()
        for i in range(0x80):
            FiasHelper.__m_1251_utf[i] = i
        m_1251_80_bf = [0x0402, 0x0403, 0x201A, 0x0453, 0x201E, 0x2026, 0x2020, 0x2021, 0x20AC, 0x2030, 0x0409, 0x2039, 0x040A, 0x040C, 0x040B, 0x040F, 0x0452, 0x2018, 0x2019, 0x201C, 0x201D, 0x2022, 0x2013, 0x2014, 0x0000, 0x2122, 0x0459, 0x203A, 0x045A, 0x045C, 0x045B, 0x045F, 0x00A0, 0x040E, 0x045E, 0x0408, 0x00A4, 0x0490, 0x00A6, 0x00A7, 0x0401, 0x00A9, 0x0404, 0x00AB, 0x00AC, 0x00AD, 0x00AE, 0x0407, 0x00B0, 0x00B1, 0x0406, 0x0456, 0x0491, 0x00B5, 0x00B6, 0x00B7, 0x0451, 0x2116, 0x0454, 0x00BB, 0x0458, 0x0405, 0x0455, 0x0457]
        for i in range(0x40):
            FiasHelper.__m_1251_utf[i + 0x80] = m_1251_80_bf[i]
            FiasHelper.__m_utf_1251[m_1251_80_bf[i]] = (i + 0x80)
        for i in range(0x20):
            FiasHelper.__m_1251_utf[i + 0xC0] = ((ord('А')) + i)
            FiasHelper.__m_utf_1251[(ord('А')) + i] = (i + 0xC0)
        for i in range(0x20):
            FiasHelper.__m_1251_utf[i + 0xE0] = ((ord('а')) + i)
            FiasHelper.__m_utf_1251[(ord('а')) + i] = (i + 0xE0)

FiasHelper._static_ctor()