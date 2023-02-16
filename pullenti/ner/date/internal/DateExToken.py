# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import datetime
import typing
import math
import operator
from enum import IntEnum
from pullenti.unisharp.Utils import Utils

from pullenti.morph.MorphNumber import MorphNumber
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.date.DateRangeReferent import DateRangeReferent
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.date.DatePointerType import DatePointerType
from pullenti.ner.date.internal.DateItemToken import DateItemToken
from pullenti.ner.date.DateReferent import DateReferent
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper

class DateExToken(MetaToken):
    # ВСЁ, этот класс теперь используется внутренним робразом, а DateReferent поддерживает относительные даты-время
    # Используется для нахождения в тексте абсолютных и относительных дат и диапазонов,
    # например, "в прошлом году", "за первый квартал этого года", "два дня назад и т.п."
    
    class DateExItemTokenType(IntEnum):
        UNDEFINED = 0
        CENTURY = 1
        DECADE = 2
        YEAR = 3
        HALFYEAR = 4
        QUARTAL = 5
        SEASON = 6
        MONTH = 7
        WEEK = 8
        DAY = 9
        DAYOFWEEK = 10
        HOUR = 11
        MINUTE = 12
        WEEKEND = 13
        
        @classmethod
        def has_value(cls, value):
            return any(value == item.value for item in cls)
    
    class DateValues:
        
        def __init__(self) -> None:
            self.day1 = 0
            self.day2 = 0
            self.month1 = 0
            self.month2 = 0
            self.year1 = 0
            self.year2 = 0
        
        def __str__(self) -> str:
            tmp = io.StringIO()
            if (self.year1 > 0): 
                print("Year:{0}".format(self.year1), end="", file=tmp, flush=True)
                if (self.year2 > self.year1): 
                    print("..{0}".format(self.year2), end="", file=tmp, flush=True)
            if (self.month1 > 0): 
                print(" Month:{0}".format(self.month1), end="", file=tmp, flush=True)
                if (self.month2 > self.month1): 
                    print("..{0}".format(self.month2), end="", file=tmp, flush=True)
            if (self.day1 > 0): 
                print(" Day:{0}".format(self.day1), end="", file=tmp, flush=True)
                if (self.day2 > self.day1): 
                    print("..{0}".format(self.day2), end="", file=tmp, flush=True)
            return Utils.toStringStringIO(tmp).strip()
        
        def generate_date(self, today : datetime.datetime, end_of_diap : bool) -> datetime.datetime:
            year = self.year1
            if (year == 0): 
                year = today.year
            if (end_of_diap and self.year2 > self.year1): 
                year = self.year2
            if (year < 0): 
                return datetime.datetime.min
            mon = self.month1
            if (mon == 0): 
                mon = (12 if end_of_diap else 1)
            elif (end_of_diap and self.month2 > 0): 
                mon = self.month2
            day = self.day1
            if (day == 0): 
                day = (31 if end_of_diap else 1)
                if (day > Utils.lastDayOfMonth(year, mon)): 
                    day = Utils.lastDayOfMonth(year, mon)
            elif (self.day2 > 0 and end_of_diap): 
                day = self.day2
            if (day > Utils.lastDayOfMonth(year, mon)): 
                return datetime.datetime.min
            return datetime.datetime(year, mon, day, 0, 0, 0)
        
        @staticmethod
        def try_create(list0_ : typing.List['DateExItemToken'], today : datetime.datetime, tense : int) -> 'DateValues':
            oo = False
            if (list0_ is not None): 
                for v in list0_: 
                    if (v.typ != DateExToken.DateExItemTokenType.HOUR and v.typ != DateExToken.DateExItemTokenType.MINUTE): 
                        oo = True
            if (not oo): 
                return DateExToken.DateValues._new802(today.year, today.month, today.day)
            if (list0_ is None or len(list0_) == 0): 
                return None
            j = 0
            while j < len(list0_): 
                if (list0_[j].typ == DateExToken.DateExItemTokenType.DAYOFWEEK): 
                    if (j > 0 and list0_[j - 1].typ == DateExToken.DateExItemTokenType.WEEK): 
                        break
                    we = DateExToken.DateExItemToken._new803(list0_[j].begin_token, list0_[j].end_token, DateExToken.DateExItemTokenType.WEEK, True)
                    if (list0_[j].is_value_relate): 
                        list0_[j].is_value_relate = False
                        if (list0_[j].value < 0): 
                            we.value = -1
                            list0_[j].value = (- list0_[j].value)
                    list0_.insert(j, we)
                    break
                j += 1
            res = DateExToken.DateValues()
            it = None
            i = 0
            has_rel = False
            if ((i < len(list0_)) and list0_[i].typ == DateExToken.DateExItemTokenType.CENTURY): 
                it = list0_[i]
                if (not it.is_value_relate): 
                    res.year1 = ((((math.floor(today.year / 1000))) * 1000) + (it.value * 100))
                else: 
                    res.year1 = ((((math.floor(today.year / 100))) * 100) + (it.value * 100))
                res.year2 = (res.year1 + 99)
                i += 1
            if ((i < len(list0_)) and list0_[i].typ == DateExToken.DateExItemTokenType.DECADE): 
                it = list0_[i]
                if ((i > 0 and list0_[i - 1].typ == DateExToken.DateExItemTokenType.CENTURY and not it.is_value_relate) and (res.year1 + 99) == res.year2): 
                    res.year1 += (((it.value - 1)) * 10)
                    res.year2 = (res.year1 + 9)
                elif (not it.is_value_relate): 
                    res.year1 = ((((math.floor(today.year / 100))) * 100) + (it.value * 10))
                else: 
                    res.year1 = ((((math.floor(today.year / 10))) * 10) + (it.value * 10))
                res.year2 = (res.year1 + 9)
                return res
            if ((i < len(list0_)) and list0_[i].typ == DateExToken.DateExItemTokenType.YEAR): 
                it = list0_[i]
                if (not it.is_value_relate): 
                    res.year1 = it.value
                else: 
                    if (res.year1 > 0 and res.year2 > res.year1 and it.value >= 0): 
                        res.year1 += it.value
                        res.year2 = res.year1
                    else: 
                        res.year1 = (today.year + it.value)
                    has_rel = True
                i += 1
            if ((i < len(list0_)) and list0_[i].typ == DateExToken.DateExItemTokenType.HALFYEAR): 
                it = list0_[i]
                if (not it.is_value_relate): 
                    if (it.is_last or it.value == 2): 
                        res.month1 = 7
                        res.month2 = 12
                    else: 
                        res.month1 = 1
                        res.month2 = 6
                else: 
                    v = (2 if today.month > 6 else 1)
                    v += it.value
                    while v > 2:
                        res.year1 += 1
                        v -= 2
                    while v < 1:
                        res.year1 -= 1
                        v += 2
                    if (v == 1): 
                        res.month1 = 1
                        res.month2 = 6
                    else: 
                        res.month1 = 7
                        res.month2 = 12
                    has_rel = True
                i += 1
            if ((i < len(list0_)) and list0_[i].typ == DateExToken.DateExItemTokenType.QUARTAL): 
                it = list0_[i]
                v = 0
                if (not it.is_value_relate): 
                    if (res.year1 == 0): 
                        v0 = 1 + ((math.floor(((today.month - 1)) / 3)))
                        if (it.value > v0 and (tense < 0)): 
                            res.year1 = (today.year - 1)
                        elif ((it.value < v0) and tense > 0): 
                            res.year1 = (today.year + 1)
                        else: 
                            res.year1 = today.year
                    v = it.value
                else: 
                    if (res.year1 == 0): 
                        res.year1 = today.year
                    v = (1 + ((math.floor(((today.month - 1)) / 3))) + it.value)
                while v > 3:
                    v -= 3
                    res.year1 += 1
                while v <= 0:
                    v += 3
                    res.year1 -= 1
                res.month1 = ((((v - 1)) * 3) + 1)
                res.month2 = (res.month1 + 2)
                return res
            if ((i < len(list0_)) and list0_[i].typ == DateExToken.DateExItemTokenType.SEASON): 
                it = list0_[i]
                v = 0
                if (not it.is_value_relate): 
                    if (res.year1 == 0): 
                        v0 = 1 + ((math.floor(((today.month - 1)) / 3)))
                        if (it.value > v0 and (tense < 0)): 
                            res.year1 = (today.year - 1)
                        elif ((it.value < v0) and tense > 0): 
                            res.year1 = (today.year + 1)
                        else: 
                            res.year1 = today.year
                    v = it.value
                else: 
                    if (res.year1 == 0): 
                        res.year1 = today.year
                    v = it.value
                if (v == 1): 
                    res.month1 = 12
                    res.year2 = res.year1
                    res.year1 -= 1
                    res.month2 = 2
                elif (v == 2): 
                    res.month1 = 3
                    res.month2 = 5
                elif (v == 3): 
                    res.month1 = 6
                    res.month2 = 8
                elif (v == 4): 
                    res.month1 = 9
                    res.month2 = 11
                else: 
                    return None
                return res
            if ((i < len(list0_)) and list0_[i].typ == DateExToken.DateExItemTokenType.MONTH): 
                it = list0_[i]
                if (not it.is_value_relate): 
                    if (res.year1 == 0): 
                        if (it.value > today.month and (tense < 0)): 
                            res.year1 = (today.year - 1)
                        elif ((it.value < today.month) and tense > 0): 
                            res.year1 = (today.year + 1)
                        else: 
                            res.year1 = today.year
                    res.month1 = it.value
                else: 
                    has_rel = True
                    if (res.year1 == 0): 
                        res.year1 = today.year
                    v = today.month + it.value
                    while v > 12:
                        v -= 12
                        res.year1 += 1
                    while v <= 0:
                        v += 12
                        res.year1 -= 1
                    res.month1 = v
                i += 1
            if ((i < len(list0_)) and list0_[i].typ == DateExToken.DateExItemTokenType.WEEKEND and i == 0): 
                it = list0_[i]
                has_rel = True
                if (res.year1 == 0): 
                    res.year1 = today.year
                if (res.month1 == 0): 
                    res.month1 = today.month
                if (res.day1 == 0): 
                    res.day1 = today.day
                dt0 = datetime.datetime(res.year1, res.month1, res.day1, 0, 0, 0)
                dow = dt0.weekday()
                if (dow == 0): 
                    dt0 = (dt0 + datetime.timedelta(days=5))
                elif (dow == 1): 
                    dt0 = (dt0 + datetime.timedelta(days=4))
                elif (dow == 2): 
                    dt0 = (dt0 + datetime.timedelta(days=3))
                elif (dow == 3): 
                    dt0 = (dt0 + datetime.timedelta(days=2))
                elif (dow == 4): 
                    dt0 = (dt0 + datetime.timedelta(days=1))
                elif (dow == 5): 
                    dt0 = (dt0 + datetime.timedelta(days=-1))
                elif (dow == 6): 
                    pass
                if (it.value != 0): 
                    dt0 = (dt0 + datetime.timedelta(days=it.value * 7))
                res.year1 = dt0.year
                res.month1 = dt0.month
                res.day1 = dt0.day
                dt0 = (dt0 + datetime.timedelta(days=1))
                res.year1 = dt0.year
                res.month2 = dt0.month
                res.day2 = dt0.day
                i += 1
            if (((i < len(list0_)) and list0_[i].typ == DateExToken.DateExItemTokenType.WEEK and i == 0) and list0_[i].is_value_relate): 
                it = list0_[i]
                has_rel = True
                if (res.year1 == 0): 
                    res.year1 = today.year
                if (res.month1 == 0): 
                    res.month1 = today.month
                if (res.day1 == 0): 
                    res.day1 = today.day
                dt0 = datetime.datetime(res.year1, res.month1, res.day1, 0, 0, 0)
                dow = dt0.weekday()
                if (dow == 1): 
                    dt0 = (dt0 + datetime.timedelta(days=-1))
                elif (dow == 2): 
                    dt0 = (dt0 + datetime.timedelta(days=-2))
                elif (dow == 3): 
                    dt0 = (dt0 + datetime.timedelta(days=-3))
                elif (dow == 4): 
                    dt0 = (dt0 + datetime.timedelta(days=-4))
                elif (dow == 5): 
                    dt0 = (dt0 + datetime.timedelta(days=-5))
                elif (dow == 6): 
                    dt0 = (dt0 + datetime.timedelta(days=-6))
                if (it.value != 0): 
                    dt0 = (dt0 + datetime.timedelta(days=it.value * 7))
                res.year1 = dt0.year
                res.month1 = dt0.month
                res.day1 = dt0.day
                dt0 = (dt0 + datetime.timedelta(days=6))
                res.year1 = dt0.year
                res.month2 = dt0.month
                res.day2 = dt0.day
                i += 1
            if ((i < len(list0_)) and list0_[i].typ == DateExToken.DateExItemTokenType.DAY): 
                it = list0_[i]
                if (not it.is_value_relate): 
                    res.day1 = it.value
                    if (res.month1 == 0): 
                        if (res.year1 == 0): 
                            res.year1 = today.year
                        if (it.value > today.day and (tense < 0)): 
                            res.month1 = (today.month - 1)
                            if (res.month1 <= 0): 
                                res.month1 = 12
                                res.year1 -= 1
                        elif ((it.value < today.day) and tense > 0): 
                            res.month1 = (today.month + 1)
                            if (res.month1 > 12): 
                                res.month1 = 1
                                res.year1 += 1
                        else: 
                            res.month1 = today.month
                else: 
                    has_rel = True
                    if (res.year1 == 0): 
                        res.year1 = today.year
                    if (res.month1 == 0): 
                        res.month1 = today.month
                    v = today.day + it.value
                    while v > Utils.lastDayOfMonth(res.year1, res.month1):
                        v -= Utils.lastDayOfMonth(res.year1, res.month1)
                        res.month1 += 1
                        if (res.month1 > 12): 
                            res.month1 = 1
                            res.year1 += 1
                    while v <= 0:
                        res.month1 -= 1
                        if (res.month1 <= 0): 
                            res.month1 = 12
                            res.year1 -= 1
                        v += Utils.lastDayOfMonth(res.year1, res.month1)
                    res.day1 = v
                i += 1
            if ((i < len(list0_)) and list0_[i].typ == DateExToken.DateExItemTokenType.DAYOFWEEK): 
                it = list0_[i]
                if ((i > 0 and list0_[i - 1].typ == DateExToken.DateExItemTokenType.WEEK and it.value >= 1) and it.value <= 7): 
                    res.day1 = ((res.day1 + it.value) - 1)
                    while res.day1 > Utils.lastDayOfMonth(res.year1, res.month1):
                        res.day1 -= Utils.lastDayOfMonth(res.year1, res.month1)
                        res.month1 += 1
                        if (res.month1 > 12): 
                            res.month1 = 1
                            res.year1 += 1
                    res.day2 = res.day1
                    res.month2 = res.month1
                    i += 1
            return res
        
        @staticmethod
        def _new802(_arg1 : int, _arg2 : int, _arg3 : int) -> 'DateValues':
            res = DateExToken.DateValues()
            res.year1 = _arg1
            res.month1 = _arg2
            res.day1 = _arg3
            return res
    
    class DateExItemToken(MetaToken):
        
        def __init__(self, begin : 'Token', end : 'Token') -> None:
            super().__init__(begin, end, None)
            self.typ = DateExToken.DateExItemTokenType.UNDEFINED
            self.value = 0
            self.is_value_relate = False
            self.is_last = False
            self.is_value_notstrict = False
            self.src = None;
        
        def __str__(self) -> str:
            tmp = io.StringIO()
            print("{0} ".format(Utils.enumToString(self.typ)), end="", file=tmp, flush=True)
            if (self.is_value_notstrict): 
                print("~", end="", file=tmp)
            if (self.is_value_relate): 
                print("{0}{1}{2}".format(("" if self.value < 0 else "+"), self.value, (" (last)" if self.is_last else "")), end="", file=tmp, flush=True)
            else: 
                print(self.value, end="", file=tmp)
            return Utils.toStringStringIO(tmp)
        
        @staticmethod
        def try_parse(t : 'Token', prev : typing.List['DateExItemToken'], level : int=0, no_corr_after : bool=False) -> 'DateExItemToken':
            from pullenti.morph.MorphNumber import MorphNumber
            from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
            from pullenti.ner.TextToken import TextToken
            from pullenti.ner.core.MiscHelper import MiscHelper
            from pullenti.ner.date.DateReferent import DateReferent
            from pullenti.ner.NumberToken import NumberToken
            from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
            from pullenti.ner.date.internal.DateItemToken import DateItemToken
            if (t is None or level > 10): 
                return None
            if (t.is_value("СЕГОДНЯ", "СЬОГОДНІ")): 
                return DateExToken.DateExItemToken._new809(t, t, DateExToken.DateExItemTokenType.DAY, 0, True)
            if (t.is_value("ЗАВТРА", None)): 
                return DateExToken.DateExItemToken._new809(t, t, DateExToken.DateExItemTokenType.DAY, 1, True)
            if (t.is_value("ЗАВТРАШНИЙ", "ЗАВТРАШНІЙ") and t.next0_ is not None and t.next0_.is_value("ДЕНЬ", None)): 
                return DateExToken.DateExItemToken._new809(t, t.next0_, DateExToken.DateExItemTokenType.DAY, 1, True)
            if (t.is_value("ПОСЛЕЗАВТРА", "ПІСЛЯЗАВТРА")): 
                return DateExToken.DateExItemToken._new809(t, t, DateExToken.DateExItemTokenType.DAY, 2, True)
            if (t.is_value("ПОСЛЕЗАВТРАШНИЙ", "ПІСЛЯЗАВТРАШНІЙ") and t.next0_ is not None and t.next0_.is_value("ДЕНЬ", None)): 
                return DateExToken.DateExItemToken._new809(t, t.next0_, DateExToken.DateExItemTokenType.DAY, 2, True)
            if (t.is_value("ВЧЕРА", "ВЧОРА")): 
                return DateExToken.DateExItemToken._new809(t, t, DateExToken.DateExItemTokenType.DAY, -1, True)
            if (t.is_value("ВЧЕРАШНИЙ", "ВЧОРАШНІЙ") and t.next0_ is not None and t.next0_.is_value("ДЕНЬ", None)): 
                return DateExToken.DateExItemToken._new809(t, t.next0_, DateExToken.DateExItemTokenType.DAY, -1, True)
            if (t.is_value("ПОЗАВЧЕРА", "ПОЗАВЧОРА")): 
                return DateExToken.DateExItemToken._new809(t, t, DateExToken.DateExItemTokenType.DAY, -2, True)
            if (t.is_value("ПОЗАВЧЕРАШНИЙ", "ПОЗАВЧОРАШНІЙ") and t.next0_ is not None and t.next0_.is_value("ДЕНЬ", None)): 
                return DateExToken.DateExItemToken._new809(t, t.next0_, DateExToken.DateExItemTokenType.DAY, -2, True)
            if (t.is_value("ПОЛЧАСА", "ПІВГОДИНИ")): 
                return DateExToken.DateExItemToken._new809(t, t, DateExToken.DateExItemTokenType.MINUTE, 30, True)
            if (t.is_value("ЗИМА", None)): 
                return DateExToken.DateExItemToken._new828(t, t, DateExToken.DateExItemTokenType.SEASON, 1)
            if (t.is_value("ВЕСНА", None)): 
                return DateExToken.DateExItemToken._new828(t, t, DateExToken.DateExItemTokenType.SEASON, 2)
            if (t.is_value("ЛЕТО", "ЛІТО") and not t.is_value("ЛЕТ", None)): 
                return DateExToken.DateExItemToken._new828(t, t, DateExToken.DateExItemTokenType.SEASON, 3)
            if (t.is_value("ОСЕНЬ", "ОСЕНІ")): 
                return DateExToken.DateExItemToken._new828(t, t, DateExToken.DateExItemTokenType.SEASON, 4)
            if (prev is not None and len(prev) > 0): 
                if (((t.is_value("Т", None) and t.next0_ is not None and t.next0_.is_char('.')) and t.next0_.next0_ is not None and t.next0_.next0_.is_value("Г", None)) and t.next0_.next0_.next0_ is not None and t.next0_.next0_.next0_.is_char('.')): 
                    return DateExToken.DateExItemToken._new803(t, t.next0_.next0_.next0_, DateExToken.DateExItemTokenType.YEAR, True)
            npt = NounPhraseHelper.try_parse(t, Utils.valToEnum((NounPhraseParseAttr.PARSENUMERICASADJECTIVE) | (NounPhraseParseAttr.PARSEPREPOSITION), NounPhraseParseAttr), 0, None)
            if (npt is not None and npt.begin_token == npt.end_token): 
                if (npt.end_token.is_value("ПРОШЛЫЙ", "МИНУЛИЙ") or npt.end_token.is_value("БУДУЩИЙ", "МАЙБУТНІЙ")): 
                    npt = (None)
            if (npt is None): 
                if ((isinstance(t, NumberToken)) and t.int_value is not None): 
                    res0 = DateExToken.DateExItemToken.try_parse(t.next0_, prev, level + 1, True)
                    if (res0 is not None and ((res0.value == 1 or res0.value == 0))): 
                        res0.begin_token = t
                        res0.value = t.int_value
                        if (t.previous is not None and ((t.previous.is_value("ЧЕРЕЗ", None) or t.previous.is_value("СПУСТЯ", None)))): 
                            res0.is_value_relate = True
                        elif (res0.end_token.next0_ is not None): 
                            if (res0.end_token.next0_.is_value("СПУСТЯ", None)): 
                                res0.is_value_relate = True
                                res0.end_token = res0.end_token.next0_
                            elif (res0.end_token.next0_.is_value("НАЗАД", None)): 
                                res0.is_value_relate = True
                                res0.value = (- res0.value)
                                res0.end_token = res0.end_token.next0_
                            elif (res0.end_token.next0_.is_value("ТОМУ", None) and res0.end_token.next0_.next0_ is not None and res0.end_token.next0_.next0_.is_value("НАЗАД", None)): 
                                res0.is_value_relate = True
                                res0.value = (- res0.value)
                                res0.end_token = res0.end_token.next0_.next0_
                        return res0
                    dtt = DateItemToken.try_parse(t, None, False)
                    if (dtt is not None and dtt.typ == DateItemToken.DateItemType.YEAR): 
                        return DateExToken.DateExItemToken._new828(t, dtt.end_token, DateExToken.DateExItemTokenType.YEAR, dtt.int_value)
                    if (t.next0_ is not None and t.next0_.is_value("ЧИСЛО", None)): 
                        ne = DateExToken.DateExItemToken.try_parse(t.next0_.next0_, prev, level + 1, False)
                        if (ne is not None and ne.typ == DateExToken.DateExItemTokenType.MONTH): 
                            return DateExToken.DateExItemToken._new828(t, t.next0_, DateExToken.DateExItemTokenType.DAY, t.int_value)
                delt = 0
                ok = True
                last = False
                t1 = t
                if (t.is_value("СЛЕДУЮЩИЙ", "НАСТУПНИЙ") or t.is_value("БУДУЩИЙ", "МАЙБУТНІЙ") or t.is_value("БЛИЖАЙШИЙ", "НАЙБЛИЖЧИЙ")): 
                    delt = 1
                elif (t.is_value("ПРЕДЫДУЩИЙ", "ПОПЕРЕДНІЙ") or t.is_value("ПРОШЛЫЙ", "МИНУЛИЙ") or t.is_value("ПРОШЕДШИЙ", None)): 
                    delt = -1
                elif (t.is_value("ПОЗАПРОШЛЫЙ", "ПОЗАМИНУЛИЙ")): 
                    delt = -2
                elif (t.is_value("ЭТОТ", "ЦЕЙ") or t.is_value("ТЕКУЩИЙ", "ПОТОЧНИЙ")): 
                    if ((isinstance(t, TextToken)) and ((t.term == "ЭТО" or t.term == "ЦЕ"))): 
                        ok = False
                elif (t.is_value("ПОСЛЕДНИЙ", "ОСТАННІЙ")): 
                    last = True
                    if (isinstance(t.next0_, NumberToken)): 
                        delt = t.next0_.int_value
                        t1 = t.next0_
                        next0__ = DateExToken.DateExItemToken.try_parse(t1.next0_, None, 0, False)
                        if (next0__ is not None and next0__.value == 0): 
                            next0__.begin_token = t
                            next0__.is_last = True
                            next0__.value = (- delt)
                            next0__.is_value_relate = True
                            return next0__
                    else: 
                        next0__ = DateExToken.DateExItemToken.try_parse(t.next0_, None, 0, False)
                        if (next0__ is not None and next0__.value == 0): 
                            next0__.begin_token = t
                            next0__.is_last = True
                            next0__.is_value_relate = True
                            if (next0__.typ == DateExToken.DateExItemTokenType.HALFYEAR): 
                                next0__.value = 2
                                next0__.is_value_relate = False
                            return next0__
                else: 
                    ok = False
                if (ok): 
                    tt = t.previous
                    while tt is not None: 
                        if (tt.is_newline_after): 
                            break
                        dr = Utils.asObjectOrNull(tt.get_referent(), DateReferent)
                        if (dr is not None and dr.is_relative): 
                            ty0 = DateExToken.DateExItemTokenType.UNDEFINED
                            for s in dr.slots: 
                                if (s.type_name == DateReferent.ATTR_MONTH): 
                                    ty0 = DateExToken.DateExItemTokenType.MONTH
                                elif (s.type_name == DateReferent.ATTR_YEAR): 
                                    ty0 = DateExToken.DateExItemTokenType.YEAR
                                elif (s.type_name == DateReferent.ATTR_DAY): 
                                    ty0 = DateExToken.DateExItemTokenType.DAY
                                elif (s.type_name == DateReferent.ATTR_WEEK): 
                                    ty0 = DateExToken.DateExItemTokenType.WEEK
                                elif (s.type_name == DateReferent.ATTR_CENTURY): 
                                    ty0 = DateExToken.DateExItemTokenType.CENTURY
                                elif (s.type_name == DateReferent.ATTR_QUARTAL): 
                                    ty0 = DateExToken.DateExItemTokenType.QUARTAL
                                elif (s.type_name == DateReferent.ATTR_HALFYEAR): 
                                    ty0 = DateExToken.DateExItemTokenType.HALFYEAR
                                elif (s.type_name == DateReferent.ATTR_DECADE): 
                                    ty0 = DateExToken.DateExItemTokenType.DECADE
                            if (ty0 != DateExToken.DateExItemTokenType.UNDEFINED): 
                                return DateExToken.DateExItemToken._new809(t, t, ty0, delt, True)
                        if (MiscHelper.can_be_start_of_sentence(tt)): 
                            break
                        tt = tt.previous
                return None
            ty = DateExToken.DateExItemTokenType.HOUR
            val = 0
            if (npt.noun.is_value("ГОД", "РІК") or npt.noun.is_value("ГОДИК", None) or npt.noun.is_value("ЛЕТ", None)): 
                ty = DateExToken.DateExItemTokenType.YEAR
            elif (npt.noun.is_value("ПОЛГОДА", "ПІВРОКУ") or npt.noun.is_value("ПОЛУГОДИЕ", "ПІВРІЧЧЯ")): 
                ty = DateExToken.DateExItemTokenType.HALFYEAR
            elif (npt.noun.is_value("ВЕК", None) or npt.noun.is_value("СТОЛЕТИЕ", "СТОЛІТТЯ")): 
                ty = DateExToken.DateExItemTokenType.CENTURY
            elif (npt.noun.is_value("КВАРТАЛ", None)): 
                ty = DateExToken.DateExItemTokenType.QUARTAL
            elif (npt.noun.is_value("ДЕСЯТИЛЕТИЕ", "ДЕСЯТИЛІТТЯ") or npt.noun.is_value("ДЕКАДА", None)): 
                ty = DateExToken.DateExItemTokenType.DECADE
            elif (npt.noun.is_value("МЕСЯЦ", "МІСЯЦЬ")): 
                ty = DateExToken.DateExItemTokenType.MONTH
            elif (npt.noun.is_value("ДЕНЬ", None) or npt.noun.is_value("ДЕНЕК", None)): 
                if (npt.end_token.next0_ is not None and npt.end_token.next0_.is_value("НЕДЕЛЯ", "ТИЖДЕНЬ")): 
                    return None
                ty = DateExToken.DateExItemTokenType.DAY
            elif (npt.noun.is_value("ЧИСЛО", None) and len(npt.adjectives) > 0 and (isinstance(npt.adjectives[0].begin_token, NumberToken))): 
                ty = DateExToken.DateExItemTokenType.DAY
            elif (npt.noun.is_value("НЕДЕЛЯ", "ТИЖДЕНЬ") or npt.noun.is_value("НЕДЕЛЬКА", None)): 
                if (t.previous is not None and t.previous.is_value("ДЕНЬ", None)): 
                    return None
                if (t.previous is not None and ((t.previous.is_value("ЗА", None) or t.previous.is_value("НА", None)))): 
                    ty = DateExToken.DateExItemTokenType.WEEK
                elif (t.is_value("ЗА", None) or t.is_value("НА", None)): 
                    ty = DateExToken.DateExItemTokenType.WEEK
                else: 
                    ty = DateExToken.DateExItemTokenType.WEEK
            elif (npt.noun.is_value("ВЫХОДНОЙ", "ВИХІДНИЙ")): 
                ty = DateExToken.DateExItemTokenType.WEEKEND
            elif (npt.noun.is_value("ЧАС", "ГОДИНА") or npt.noun.is_value("ЧАСИК", None) or npt.noun.is_value("ЧАСОК", None)): 
                ty = DateExToken.DateExItemTokenType.HOUR
            elif (npt.noun.is_value("МИНУТА", "ХВИЛИНА") or npt.noun.is_value("МИНУТКА", None)): 
                ty = DateExToken.DateExItemTokenType.MINUTE
            elif (npt.noun.is_value("ПОНЕДЕЛЬНИК", "ПОНЕДІЛОК")): 
                ty = DateExToken.DateExItemTokenType.DAYOFWEEK
                val = 1
            elif (npt.noun.is_value("ВТОРНИК", "ВІВТОРОК")): 
                ty = DateExToken.DateExItemTokenType.DAYOFWEEK
                val = 2
            elif (npt.noun.is_value("СРЕДА", "СЕРЕДА")): 
                ty = DateExToken.DateExItemTokenType.DAYOFWEEK
                val = 3
            elif (npt.noun.is_value("ЧЕТВЕРГ", "ЧЕТВЕР")): 
                ty = DateExToken.DateExItemTokenType.DAYOFWEEK
                val = 4
            elif (npt.noun.is_value("ПЯТНИЦЯ", None)): 
                ty = DateExToken.DateExItemTokenType.DAYOFWEEK
                val = 5
            elif (npt.noun.is_value("СУББОТА", "СУБОТА")): 
                ty = DateExToken.DateExItemTokenType.DAYOFWEEK
                val = 6
            elif (npt.noun.is_value("ВОСКРЕСЕНЬЕ", "НЕДІЛЯ") or npt.noun.is_value("ВОСКРЕСЕНИЕ", None)): 
                ty = DateExToken.DateExItemTokenType.DAYOFWEEK
                val = 7
            else: 
                dti = DateItemToken.try_parse(npt.end_token, None, False)
                if (dti is not None and dti.typ == DateItemToken.DateItemType.MONTH): 
                    ty = DateExToken.DateExItemTokenType.MONTH
                    val = dti.int_value
                else: 
                    return None
            res = DateExToken.DateExItemToken._new828(t, npt.end_token, ty, val)
            heg = False
            i = 0
            while i < len(npt.adjectives): 
                a = npt.adjectives[i]
                if (a.is_value("СЛЕДУЮЩИЙ", "НАСТУПНИЙ") or a.is_value("БУДУЩИЙ", "МАЙБУТНІЙ") or a.is_value("БЛИЖАЙШИЙ", "НАЙБЛИЖЧИЙ")): 
                    if (res.value == 0 and ty != DateExToken.DateExItemTokenType.WEEKEND): 
                        res.value = 1
                    res.is_value_relate = True
                elif (a.is_value("ПРЕДЫДУЩИЙ", "ПОПЕРЕДНІЙ") or a.is_value("ПРОШЛЫЙ", "МИНУЛИЙ") or a.is_value("ПРОШЕДШИЙ", None)): 
                    if (res.value == 0): 
                        res.value = 1
                    res.is_value_relate = True
                    heg = True
                elif (a.is_value("ПОЗАПРОШЛЫЙ", "ПОЗАМИНУЛИЙ")): 
                    if (res.value == 0): 
                        res.value = 2
                    res.is_value_relate = True
                    heg = True
                elif (a.begin_token == a.end_token and (isinstance(a.begin_token, NumberToken)) and a.begin_token.int_value is not None): 
                    if (res.typ != DateExToken.DateExItemTokenType.DAYOFWEEK): 
                        res.value = a.begin_token.int_value
                elif (a.is_value("ЭТОТ", "ЦЕЙ") or a.is_value("ТЕКУЩИЙ", "ПОТОЧНИЙ")): 
                    res.is_value_relate = True
                elif (a.is_value("ПЕРВЫЙ", "ПЕРШИЙ")): 
                    res.value = 1
                elif (a.is_value("ПОСЛЕДНИЙ", "ОСТАННІЙ")): 
                    res.is_value_relate = True
                    res.is_last = True
                    if (((i + 1) < len(npt.adjectives)) and (isinstance(npt.adjectives[i + 1].begin_token, NumberToken)) and npt.adjectives[i + 1].begin_token.int_value is not None): 
                        i += 1
                        res.value = (- npt.adjectives[i].begin_token.int_value)
                        res.is_last = True
                    elif (i > 0 and (isinstance(npt.adjectives[i - 1].begin_token, NumberToken)) and npt.adjectives[i - 1].begin_token.int_value is not None): 
                        res.value = (- npt.adjectives[i - 1].begin_token.int_value)
                        res.is_last = True
                elif (a.is_value("ПРЕДПОСЛЕДНИЙ", "ПЕРЕДОСТАННІЙ")): 
                    res.is_value_relate = True
                    res.is_last = True
                    res.value = -1
                elif (a.is_value("БЛИЖАЙШИЙ", "НАЙБЛИЖЧИЙ") and res.typ == DateExToken.DateExItemTokenType.DAYOFWEEK): 
                    pass
                else: 
                    return None
                i += 1
            if (npt.anafor is not None): 
                if (npt.anafor.is_value("ЭТОТ", "ЦЕЙ")): 
                    if (npt.morph.number != MorphNumber.SINGULAR): 
                        return None
                    if (res.value == 0): 
                        res.is_value_relate = True
                    if (prev is None or len(prev) == 0): 
                        if (t.previous is not None and t.previous.get_morph_class_in_dictionary().is_preposition): 
                            pass
                        elif (t.get_morph_class_in_dictionary().is_preposition): 
                            pass
                        elif (ty == DateExToken.DateExItemTokenType.YEAR or ty == DateExToken.DateExItemTokenType.MONTH or ty == DateExToken.DateExItemTokenType.WEEK): 
                            pass
                        else: 
                            return None
                else: 
                    return None
            ch = False
            if (not no_corr_after and res.end_token.next0_ is not None): 
                tt = res.end_token.next0_
                tt0 = res.begin_token
                if (tt.is_value("СПУСТЯ", None) or tt0.is_value("СПУСТЯ", None) or tt0.is_value("ЧЕРЕЗ", None)): 
                    ch = True
                    res.is_value_relate = True
                    if (res.value == 0): 
                        res.value = 1
                    res.end_token = tt
                elif (tt.is_value("НАЗАД", None)): 
                    ch = True
                    res.is_value_relate = True
                    if (res.value == 0): 
                        res.value = -1
                    else: 
                        res.value = (- res.value)
                    res.end_token = tt
                elif (tt.is_value("ТОМУ", None) and tt.next0_ is not None and tt.next0_.is_value("НАЗАД", None)): 
                    ch = True
                    res.is_value_relate = True
                    if (res.value == 0): 
                        res.value = -1
                    else: 
                        res.value = (- res.value)
                    res.end_token = tt.next0_
            if (heg): 
                res.value = (- res.value)
            if (t.previous is not None): 
                if (t.previous.is_value("ЧЕРЕЗ", None) or t.previous.is_value("СПУСТЯ", None)): 
                    res.is_value_relate = True
                    if (res.value == 0): 
                        res.value = 1
                    res.begin_token = t.previous
                    ch = True
                elif (t.previous.is_value("ЗА", None) and res.value == 0): 
                    if (not npt.morph.case_.is_accusative): 
                        return None
                    if (npt.end_token.next0_ is not None and npt.end_token.next0_.is_value("ДО", None)): 
                        return None
                    if (npt.begin_token == npt.end_token): 
                        return None
                    if (not res.is_last): 
                        res.is_value_relate = True
                        ch = True
            if (res.begin_token == res.end_token): 
                if (t.previous is not None and t.previous.is_value("ПО", None)): 
                    return None
            if (ch and res.typ != DateExToken.DateExItemTokenType.DAY): 
                if (res.typ == DateExToken.DateExItemTokenType.WEEK): 
                    res.value *= 7
                    res.typ = DateExToken.DateExItemTokenType.DAY
                elif (res.typ == DateExToken.DateExItemTokenType.MONTH): 
                    res.value *= 30
                    res.typ = DateExToken.DateExItemTokenType.DAY
                elif (res.typ == DateExToken.DateExItemTokenType.QUARTAL): 
                    res.value *= 91
                    res.typ = DateExToken.DateExItemTokenType.DAY
                elif (res.typ == DateExToken.DateExItemTokenType.YEAR): 
                    res.value *= 365
                    res.typ = DateExToken.DateExItemTokenType.DAY
            return res
        
        def compareTo(self, other : 'DateExItemToken') -> int:
            if ((self.typ) < (other.typ)): 
                return -1
            if ((self.typ) > (other.typ)): 
                return 1
            return 0
        
        @staticmethod
        def _new803(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'DateExItemTokenType', _arg4 : bool) -> 'DateExItemToken':
            res = DateExToken.DateExItemToken(_arg1, _arg2)
            res.typ = _arg3
            res.is_value_relate = _arg4
            return res
        
        @staticmethod
        def _new806(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'DateExItemTokenType', _arg4 : int, _arg5 : 'DateReferent') -> 'DateExItemToken':
            res = DateExToken.DateExItemToken(_arg1, _arg2)
            res.typ = _arg3
            res.value = _arg4
            res.src = _arg5
            return res
        
        @staticmethod
        def _new809(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'DateExItemTokenType', _arg4 : int, _arg5 : bool) -> 'DateExItemToken':
            res = DateExToken.DateExItemToken(_arg1, _arg2)
            res.typ = _arg3
            res.value = _arg4
            res.is_value_relate = _arg5
            return res
        
        @staticmethod
        def _new828(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'DateExItemTokenType', _arg4 : int) -> 'DateExItemToken':
            res = DateExToken.DateExItemToken(_arg1, _arg2)
            res.typ = _arg3
            res.value = _arg4
            return res
        
        @staticmethod
        def _new890(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'DateExItemTokenType') -> 'DateExItemToken':
            res = DateExToken.DateExItemToken(_arg1, _arg2)
            res.typ = _arg3
            return res
    
    def __init__(self, begin : 'Token', end : 'Token') -> None:
        super().__init__(begin, end, None)
        self.is_diap = False
        self.items_from = list()
        self.items_to = list()
    
    def __str__(self) -> str:
        tmp = io.StringIO()
        for it in self.items_from: 
            print("{0}{1}; ".format(("(fr)" if self.is_diap else ""), str(it)), end="", file=tmp, flush=True)
        for it in self.items_to: 
            print("(to){0}; ".format(str(it)), end="", file=tmp, flush=True)
        return Utils.toStringStringIO(tmp)
    
    def get_date(self, now : datetime.datetime, tense : int=0) -> datetime.datetime:
        dvl = DateExToken.DateValues.try_create((self.items_from if len(self.items_from) > 0 else self.items_to), now, tense)
        try: 
            dt = dvl.generate_date(now, False)
            if (dt == datetime.datetime.min): 
                return None
            dt = self.__correct_hours(dt, (self.items_from if len(self.items_from) > 0 else self.items_to), now)
            return dt
        except Exception as ex: 
            return None
    
    def get_dates(self, now : datetime.datetime, from0_ : datetime.datetime, to : datetime.datetime, tense : int=0) -> bool:
        from0_.value = datetime.datetime.min
        to.value = datetime.datetime.min
        has_hours = False
        for it in self.items_from: 
            if (it.typ == DateExToken.DateExItemTokenType.HOUR or it.typ == DateExToken.DateExItemTokenType.MINUTE): 
                has_hours = True
        for it in self.items_to: 
            if (it.typ == DateExToken.DateExItemTokenType.HOUR or it.typ == DateExToken.DateExItemTokenType.MINUTE): 
                has_hours = True
        li = list()
        if (has_hours): 
            for it in self.items_from: 
                if (it.typ != DateExToken.DateExItemTokenType.HOUR and it.typ != DateExToken.DateExItemTokenType.MINUTE): 
                    li.append(it)
            for it in self.items_to: 
                if (it.typ != DateExToken.DateExItemTokenType.HOUR and it.typ != DateExToken.DateExItemTokenType.MINUTE): 
                    exi = False
                    for itt in li: 
                        if (itt.typ == it.typ): 
                            exi = True
                            break
                    if (not exi): 
                        li.append(it)
            # PYTHON: sort(key=attrgetter('typ'))
            li.sort(key=operator.attrgetter('typ'))
            dvl = DateExToken.DateValues.try_create(li, now, tense)
            if (dvl is None): 
                return False
            try: 
                from0_.value = dvl.generate_date(now, False)
                if (from0_.value == datetime.datetime.min): 
                    return False
            except Exception as ex: 
                return False
            to.value = from0_.value
            from0_.value = self.__correct_hours(from0_.value, self.items_from, now)
            to.value = self.__correct_hours(to.value, (self.items_from if len(self.items_to) == 0 else self.items_to), now)
            return True
        gr_year = False
        for f in self.items_from: 
            if (f.typ == DateExToken.DateExItemTokenType.CENTURY or f.typ == DateExToken.DateExItemTokenType.DECADE): 
                gr_year = True
        if (len(self.items_to) == 0 and not gr_year): 
            dvl = DateExToken.DateValues.try_create(self.items_from, now, tense)
            if (dvl is None): 
                return False
            try: 
                from0_.value = dvl.generate_date(now, False)
                if (from0_.value == datetime.datetime.min): 
                    return False
            except Exception as ex: 
                return False
            try: 
                to.value = dvl.generate_date(now, True)
                if (to.value == datetime.datetime.min): 
                    to.value = from0_.value
            except Exception as ex: 
                to.value = from0_.value
            return True
        li.clear()
        for it in self.items_from: 
            li.append(it)
        for it in self.items_to: 
            exi = False
            for itt in li: 
                if (itt.typ == it.typ): 
                    exi = True
                    break
            if (not exi): 
                li.append(it)
        # PYTHON: sort(key=attrgetter('typ'))
        li.sort(key=operator.attrgetter('typ'))
        dvl1 = DateExToken.DateValues.try_create(li, now, tense)
        li.clear()
        for it in self.items_to: 
            li.append(it)
        for it in self.items_from: 
            exi = False
            for itt in li: 
                if (itt.typ == it.typ): 
                    exi = True
                    break
            if (not exi): 
                li.append(it)
        # PYTHON: sort(key=attrgetter('typ'))
        li.sort(key=operator.attrgetter('typ'))
        dvl2 = DateExToken.DateValues.try_create(li, now, tense)
        try: 
            from0_.value = dvl1.generate_date(now, False)
            if (from0_.value == datetime.datetime.min): 
                return False
        except Exception as ex: 
            return False
        try: 
            to.value = dvl2.generate_date(now, True)
            if (to.value == datetime.datetime.min): 
                return False
        except Exception as ex: 
            return False
        return True
    
    def __correct_hours(self, dt : datetime.datetime, li : typing.List['DateExItemToken'], now : datetime.datetime) -> datetime.datetime:
        has_hour = False
        for it in li: 
            if (it.typ == DateExToken.DateExItemTokenType.HOUR): 
                has_hour = True
                if (it.is_value_relate): 
                    dt = datetime.datetime(dt.year, dt.month, dt.day, now.hour, now.minute, 0)
                    dt = (dt + datetime.timedelta(hours=it.value))
                elif (it.value > 0 and (it.value < 24)): 
                    dt = datetime.datetime(dt.year, dt.month, dt.day, it.value, 0, 0)
            elif (it.typ == DateExToken.DateExItemTokenType.MINUTE): 
                if (not has_hour): 
                    dt = datetime.datetime(dt.year, dt.month, dt.day, now.hour, 0, 0)
                if (it.is_value_relate): 
                    dt = datetime.datetime(dt.year, dt.month, dt.day, dt.hour, 0, 0)
                    dt = (dt + datetime.timedelta(minutes=it.value))
                    if (not has_hour): 
                        dt = (dt + datetime.timedelta(minutes=now.minute))
                elif (it.value > 0 and (it.value < 60)): 
                    dt = datetime.datetime(dt.year, dt.month, dt.day, dt.hour, it.value, 0)
        return dt
    
    @staticmethod
    def try_parse(t : 'Token') -> 'DateExToken':
        if (t is None): 
            return None
        if (t.is_value("ЗА", None) and t.next0_ is not None and t.next0_.is_value("ПЕРИОД", None)): 
            ne = DateExToken.try_parse(t.next0_.next0_)
            if (ne is not None and ne.is_diap): 
                ne.begin_token = t
                return ne
        res = None
        to_regime = False
        from_regime = False
        t0 = None
        tt = t
        first_pass2837 = True
        while True:
            if first_pass2837: first_pass2837 = False
            else: tt = tt.next0_
            if (not (tt is not None)): break
            drr = Utils.asObjectOrNull(tt.get_referent(), DateRangeReferent)
            if (drr is not None): 
                res = DateExToken._new804(t, tt, True)
                fr = drr.date_from
                if (fr is not None): 
                    if (fr.pointer == DatePointerType.TODAY): 
                        return None
                    DateExToken.__add_items(fr, res.items_from, tt)
                to = drr.date_to
                if (to is not None): 
                    if (to.pointer == DatePointerType.TODAY): 
                        return None
                    DateExToken.__add_items(to, res.items_to, tt)
                has_year = False
                if (len(res.items_from) > 0 and res.items_from[0].typ == DateExToken.DateExItemTokenType.YEAR): 
                    has_year = True
                elif (len(res.items_to) > 0 and res.items_to[0].typ == DateExToken.DateExItemTokenType.YEAR): 
                    has_year = True
                if (not has_year and (tt.whitespaces_after_count < 3)): 
                    dit = DateExToken.DateExItemToken.try_parse(tt.next0_, (res.items_to if len(res.items_to) > 0 else res.items_from), 0, False)
                    if (dit is not None and dit.typ == DateExToken.DateExItemTokenType.YEAR): 
                        if (len(res.items_from) > 0): 
                            res.items_from.insert(0, dit)
                        if (len(res.items_to) > 0): 
                            res.items_to.insert(0, dit)
                        res.end_token = dit.end_token
                return res
            dr = Utils.asObjectOrNull(tt.get_referent(), DateReferent)
            if (dr is not None): 
                if (dr.pointer == DatePointerType.TODAY): 
                    return None
                if (res is None): 
                    res = DateExToken(t, tt)
                li = list()
                DateExToken.__add_items(dr, li, tt)
                if (len(li) == 0): 
                    continue
                if (to_regime): 
                    ok = True
                    for v in li: 
                        for vv in res.items_to: 
                            if (vv.typ == v.typ): 
                                ok = False
                    if (not ok): 
                        break
                    res.items_to.extend(li)
                    res.end_token = tt
                else: 
                    ok = True
                    for v in li: 
                        for vv in res.items_from: 
                            if (vv.typ == v.typ): 
                                ok = False
                    if (not ok): 
                        break
                    res.items_from.extend(li)
                    res.end_token = tt
                has_year = False
                if (len(res.items_from) > 0 and res.items_from[0].typ == DateExToken.DateExItemTokenType.YEAR): 
                    has_year = True
                elif (len(res.items_to) > 0 and res.items_to[0].typ == DateExToken.DateExItemTokenType.YEAR): 
                    has_year = True
                if (not has_year and (tt.whitespaces_after_count < 3)): 
                    dit = DateExToken.DateExItemToken.try_parse(tt.next0_, None, 0, False)
                    if (dit is not None and dit.typ == DateExToken.DateExItemTokenType.YEAR): 
                        if (len(res.items_from) > 0): 
                            res.items_from.insert(0, dit)
                        if (len(res.items_to) > 0): 
                            res.items_to.insert(0, dit)
                        res.end_token = dit.end_token
                        tt = res.end_token
                continue
            if (tt.morph.class0_.is_preposition): 
                if (tt.is_value("ПО", None) or tt.is_value("ДО", None)): 
                    to_regime = True
                    if (t0 is None): 
                        t0 = tt
                elif (tt.is_value("С", None) or tt.is_value("ОТ", None)): 
                    from_regime = True
                    if (t0 is None): 
                        t0 = tt
                continue
            it = DateExToken.DateExItemToken.try_parse(tt, (None if res is None else ((res.items_to if to_regime else res.items_from))), 0, False)
            if (it is None): 
                break
            if (tt.is_value("ДЕНЬ", None) and tt.next0_ is not None and tt.next0_.is_value("НЕДЕЛЯ", None)): 
                break
            if (it.end_token == tt and ((it.typ == DateExToken.DateExItemTokenType.HOUR or it.typ == DateExToken.DateExItemTokenType.MINUTE))): 
                if (tt.previous is None or not tt.previous.morph.class0_.is_preposition): 
                    break
            if (res is None): 
                if ((it.typ == DateExToken.DateExItemTokenType.DAY or it.typ == DateExToken.DateExItemTokenType.MONTH or it.typ == DateExToken.DateExItemTokenType.WEEK) or it.typ == DateExToken.DateExItemTokenType.QUARTAL or it.typ == DateExToken.DateExItemTokenType.YEAR): 
                    if (it.begin_token == it.end_token and not it.is_value_relate and it.value == 0): 
                        return None
                res = DateExToken(t, tt)
            if (to_regime): 
                res.items_to.append(it)
            else: 
                res.items_from.append(it)
                if (it.is_last and it.value != 0 and it.value != -1): 
                    res.items_to.append(DateExToken.DateExItemToken._new803(it.begin_token, it.end_token, it.typ, True))
                    from_regime = True
            tt = it.end_token
            res.end_token = tt
        if (res is not None): 
            if (t0 is not None and res.begin_token.previous == t0): 
                res.begin_token = t0
            res.is_diap = (from_regime or to_regime)
            # PYTHON: sort(key=attrgetter('typ'))
            res.items_from.sort(key=operator.attrgetter('typ'))
            # PYTHON: sort(key=attrgetter('typ'))
            res.items_to.sort(key=operator.attrgetter('typ'))
            if ((len(res.items_from) == 1 and len(res.items_to) == 0 and res.items_from[0].is_last) and res.items_from[0].value == 0): 
                return None
        return res
    
    @staticmethod
    def __add_items(fr : 'DateReferent', res : typing.List['DateExItemToken'], tt : 'Token') -> None:
        if (fr.century > 0): 
            res.append(DateExToken.DateExItemToken._new806(tt, tt, DateExToken.DateExItemTokenType.CENTURY, fr.century, fr))
        if (fr.decade > 0): 
            res.append(DateExToken.DateExItemToken._new806(tt, tt, DateExToken.DateExItemTokenType.DECADE, fr.decade, fr))
        if (fr.year > 0): 
            res.append(DateExToken.DateExItemToken._new806(tt, tt, DateExToken.DateExItemTokenType.YEAR, fr.year, fr))
        elif (fr.pointer == DatePointerType.TODAY): 
            res.append(DateExToken.DateExItemToken._new809(tt, tt, DateExToken.DateExItemTokenType.YEAR, 0, True))
        if (fr.month > 0): 
            res.append(DateExToken.DateExItemToken._new806(tt, tt, DateExToken.DateExItemTokenType.MONTH, fr.month, fr))
        elif (fr.pointer == DatePointerType.TODAY): 
            res.append(DateExToken.DateExItemToken._new809(tt, tt, DateExToken.DateExItemTokenType.MONTH, 0, True))
        if (fr.day > 0): 
            res.append(DateExToken.DateExItemToken._new806(tt, tt, DateExToken.DateExItemTokenType.DAY, fr.day, fr))
        elif (fr.pointer == DatePointerType.TODAY): 
            res.append(DateExToken.DateExItemToken._new809(tt, tt, DateExToken.DateExItemTokenType.DAY, 0, True))
        if (fr.find_slot(DateReferent.ATTR_HOUR, None, True) is not None): 
            res.append(DateExToken.DateExItemToken._new806(tt, tt, DateExToken.DateExItemTokenType.HOUR, fr.hour, fr))
        elif (fr.pointer == DatePointerType.TODAY): 
            res.append(DateExToken.DateExItemToken._new809(tt, tt, DateExToken.DateExItemTokenType.HOUR, 0, True))
        if (fr.find_slot(DateReferent.ATTR_MINUTE, None, True) is not None): 
            res.append(DateExToken.DateExItemToken._new806(tt, tt, DateExToken.DateExItemTokenType.MINUTE, fr.minute, fr))
        elif (fr.pointer == DatePointerType.TODAY): 
            res.append(DateExToken.DateExItemToken._new809(tt, tt, DateExToken.DateExItemTokenType.MINUTE, 0, True))
    
    @staticmethod
    def _new804(_arg1 : 'Token', _arg2 : 'Token', _arg3 : bool) -> 'DateExToken':
        res = DateExToken(_arg1, _arg2)
        res.is_diap = _arg3
        return res