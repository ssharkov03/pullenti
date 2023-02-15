# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
import datetime
import math
import threading
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.TextAnnotation import TextAnnotation
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.Referent import Referent
from pullenti.ner.Token import Token
from pullenti.ner.core.AnalyzerData import AnalyzerData
from pullenti.morph.MorphLang import MorphLang
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.core.internal.PullentiNerCoreInternalResourceHelper import PullentiNerCoreInternalResourceHelper
from pullenti.ner.date.internal.MetaDateRange import MetaDateRange
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.date.internal.MetaDate import MetaDate
from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.Termin import Termin
from pullenti.ner.Analyzer import Analyzer
from pullenti.ner.core.NumberHelper import NumberHelper
from pullenti.ner.date.DatePointerType import DatePointerType
from pullenti.ner.date.internal.DateAnalyzerData import DateAnalyzerData
from pullenti.ner.date.DateReferent import DateReferent
from pullenti.ner.date.DateRangeReferent import DateRangeReferent

class DateAnalyzer(Analyzer):
    """ Анализатор для дат и их диапазонов """
    
    ANALYZER_NAME = "DATE"
    """ Имя анализатора ("DATE") """
    
    @property
    def name(self) -> str:
        return DateAnalyzer.ANALYZER_NAME
    
    @property
    def caption(self) -> str:
        return "Даты"
    
    @property
    def description(self) -> str:
        return "Даты и диапазоны дат"
    
    def clone(self) -> 'Analyzer':
        return DateAnalyzer()
    
    @property
    def type_system(self) -> typing.List['ReferentClass']:
        return [MetaDate.GLOBAL_META, MetaDateRange.GLOBAL_META]
    
    @property
    def used_extern_object_types(self) -> typing.List[str]:
        return ["PHONE"]
    
    @property
    def images(self) -> typing.List[tuple]:
        res = dict()
        res[MetaDate.DATE_FULL_IMAGE_ID] = PullentiNerCoreInternalResourceHelper.get_bytes("datefull.png")
        res[MetaDate.DATE_IMAGE_ID] = PullentiNerCoreInternalResourceHelper.get_bytes("date.png")
        res[MetaDate.DATE_REL_IMAGE_ID] = PullentiNerCoreInternalResourceHelper.get_bytes("daterel.png")
        res[MetaDateRange.DATE_RANGE_IMAGE_ID] = PullentiNerCoreInternalResourceHelper.get_bytes("daterange.png")
        res[MetaDateRange.DATE_RANGE_REL_IMAGE_ID] = PullentiNerCoreInternalResourceHelper.get_bytes("daterangerel.png")
        return res
    
    def create_referent(self, type0_ : str) -> 'Referent':
        if (type0_ == DateReferent.OBJ_TYPENAME): 
            return DateReferent()
        if (type0_ == DateRangeReferent.OBJ_TYPENAME): 
            return DateRangeReferent()
        return None
    
    @property
    def progress_weight(self) -> int:
        return 10
    
    def create_analyzer_data(self) -> 'AnalyzerData':
        return DateAnalyzerData()
    
    @staticmethod
    def _get_data(t : 'Token') -> 'DateAnalyzerData':
        if (t is None): 
            return None
        return Utils.asObjectOrNull(t.kit.get_analyzer_data_by_analyzer_name(DateAnalyzer.ANALYZER_NAME), DateAnalyzerData)
    
    def process(self, kit : 'AnalysisKit') -> None:
        from pullenti.ner.date.internal.DateItemToken import DateItemToken
        from pullenti.ner.date.internal.DateExToken import DateExToken
        from pullenti.ner.date.internal.DateRelHelper import DateRelHelper
        ad = Utils.asObjectOrNull(kit.get_analyzer_data(self), DateAnalyzerData)
        DateItemToken.SPEED_REGIME = False
        DateItemToken._prepare_all_data(kit.first_token)
        ad.dregime = True
        t = kit.first_token
        first_pass2843 = True
        while True:
            if first_pass2843: first_pass2843 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.is_ignored): 
                continue
            rts = None
            about = None
            t1 = None
            pli = DateItemToken.try_parse_list(t, 20)
            if (pli is None or len(pli) == 0): 
                pass
            else: 
                high = False
                tt = t.previous
                first_pass2844 = True
                while True:
                    if first_pass2844: first_pass2844 = False
                    else: tt = tt.previous
                    if (not (tt is not None)): break
                    if (tt.is_value("ДАТА", None) or tt.is_value("DATE", None) or tt.is_value("ВЫДАТЬ", None)): 
                        high = True
                        break
                    if (tt.is_char(':') or tt.is_hiphen): 
                        continue
                    if (isinstance(tt.get_referent(), DateReferent)): 
                        high = True
                        break
                    if (not (isinstance(tt, TextToken))): 
                        break
                    if (not ((tt.morph.case_.is_genitive))): 
                        break
                if (len(pli) > 1 and pli[0].ptr == DatePointerType.ABOUT): 
                    about = pli[0]
                    del pli[0]
                rts = DateAnalyzer.__try_attach(pli, high)
                if ((rts is None and len(pli) > 2 and pli[2].typ == DateItemToken.DateItemType.DELIM) and pli[2].begin_token.is_comma): 
                    del pli[2:2+len(pli) - 2]
                    rts = DateAnalyzer.__try_attach(pli, high)
                t1 = pli[len(pli) - 1].end_token
            if (rts is None): 
                if (rts is None): 
                    if (t1 is not None): 
                        t = t1
                    continue
            dat = None
            hi = None
            i = 0
            while i < len(rts): 
                rt = rts[i]
                if (isinstance(rt.referent, DateRangeReferent)): 
                    dr = Utils.asObjectOrNull(rt.referent, DateRangeReferent)
                    if (dr.date_from is not None): 
                        dr.date_from = Utils.asObjectOrNull(ad.register_referent(dr.date_from), DateReferent)
                    if (dr.date_to is not None): 
                        dr.date_to = Utils.asObjectOrNull(ad.register_referent(dr.date_to), DateReferent)
                    rt.referent = ad.register_referent(rt.referent)
                    if (rt.begin_token.previous is not None and rt.begin_token.previous.is_value("ПЕРИОД", None)): 
                        rt.begin_token = rt.begin_token.previous
                    kit.embed_token(rt)
                    t = (rt)
                    break
                dt = Utils.asObjectOrNull(rt.referent, DateReferent)
                if (dt.higher is not None): 
                    dt.higher = Utils.asObjectOrNull(ad.register_referent(dt.higher), DateReferent)
                rt.referent = ad.register_referent(dt)
                hi = (Utils.asObjectOrNull(rt.referent, DateReferent))
                if ((i < (len(rts) - 1)) and rt.tag is None): 
                    rt.referent.add_occurence(TextAnnotation._new934(kit.sofa, rt.begin_char, rt.end_char, rt.referent))
                else: 
                    dat = (Utils.asObjectOrNull(rt.referent, DateReferent))
                    if (about is not None): 
                        if (rt.begin_char > about.begin_char): 
                            rt.begin_token = about.begin_token
                        dat.pointer = DatePointerType.ABOUT
                    kit.embed_token(rt)
                    t = (rt)
                    j = i + 1
                    while j < len(rts): 
                        if (rts[j].begin_char == t.begin_char): 
                            rts[j].begin_token = t
                        if (rts[j].end_char == t.end_char): 
                            rts[j].end_token = t
                        j += 1
                i += 1
            if ((dat is not None and t.previous is not None and t.previous.is_hiphen) and t.previous.previous is not None and (isinstance(t.previous.previous.get_referent(), DateReferent))): 
                dat0 = Utils.asObjectOrNull(t.previous.previous.get_referent(), DateReferent)
                dr = Utils.asObjectOrNull(ad.register_referent(DateRangeReferent._new935(dat0, dat)), DateRangeReferent)
                diap = ReferentToken(dr, t.previous.previous, t)
                kit.embed_token(diap)
                t = (diap)
                continue
            if ((dat is not None and t.previous is not None and ((t.previous.is_hiphen or t.previous.is_value("ПО", None) or t.previous.is_value("И", None)))) and (isinstance(t.previous.previous, NumberToken)) and t.previous.previous.int_value is not None): 
                t0 = t.previous.previous
                dat0 = None
                num = t0.int_value
                if (dat.day > 0 and (num < dat.day) and num > 0): 
                    if (dat.higher is not None): 
                        dat0 = DateReferent._new936(dat.higher, num)
                    elif (dat.month > 0): 
                        dat0 = DateReferent._new937(dat.month, num)
                elif (dat.year > 0 and (num < dat.year) and ((num > 1000 or ((t.previous.previous.previous is not None and t.previous.previous.previous.is_value("С", None)))))): 
                    dat0 = DateReferent._new938(num)
                elif ((dat.year < 0) and num > (- dat.year)): 
                    dat0 = DateReferent._new938(- num)
                if (dat0 is not None): 
                    rt0 = ReferentToken(ad.register_referent(dat0), t0, t0)
                    kit.embed_token(rt0)
                    if (not t.previous.is_hiphen): 
                        continue
                    dat0 = (Utils.asObjectOrNull(rt0.referent, DateReferent))
                    dr = Utils.asObjectOrNull(ad.register_referent(DateRangeReferent._new935(dat0, dat)), DateRangeReferent)
                    diap = ReferentToken(dr, rt0, t)
                    if (diap.begin_token.previous is not None and diap.begin_token.previous.is_value("С", None)): 
                        diap.begin_token = diap.begin_token.previous
                    kit.embed_token(diap)
                    t = (diap)
                    continue
        DateAnalyzer.__apply_date_range0(kit, ad)
        t = kit.first_token
        first_pass2845 = True
        while True:
            if first_pass2845: first_pass2845 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.is_ignored): 
                continue
            det = DateExToken.try_parse(t)
            if (det is None): 
                continue
            rel = False
            for it in det.items_from: 
                if (it.is_value_relate): 
                    rel = True
            for it in det.items_to: 
                if (it.is_value_relate): 
                    rel = True
            if (not rel): 
                t = det.end_token
                continue
            rts = DateRelHelper.create_referents(det)
            if (rts is None or len(rts) == 0): 
                continue
            root = Utils.asObjectOrNull(rts[0].tag, Referent)
            i = 0
            while i < len(rts): 
                rt = rts[i]
                old = rt.referent
                rt.referent = ad.register_referent(rt.referent)
                if (old == root): 
                    root = rt.referent
                if (old != rt.referent): 
                    j = i + 1
                    while j < len(rts): 
                        for s in rts[j].referent.slots: 
                            if (s.value == old): 
                                s.value = rt.referent
                        j += 1
                if (root is not None): 
                    for s in root.slots: 
                        if (s.value == old): 
                            s.value = rt.referent
                if (rt.referent == root): 
                    if (rt.begin_char > t.begin_char): 
                        rt.begin_token = t
                    if (rt.end_char < det.end_char): 
                        rt.end_token = det.end_token
                    root = (None)
                kit.embed_token(rt)
                t = (rt)
                j = i + 1
                while j < len(rts): 
                    if (rts[j].begin_char == t.begin_char): 
                        rts[j].begin_token = t
                    if (rts[j].end_char == t.end_char): 
                        rts[j].end_token = t
                    j += 1
                i += 1
            if (root is not None): 
                if (t.begin_char > det.begin_char or (t.end_char < det.end_char)): 
                    rt = ReferentToken(root, (det.begin_token if t.begin_char > det.begin_char else t), (det.end_token if t.end_char < det.end_char else t))
                    kit.embed_token(rt)
                    t = (rt)
        ad.dregime = False
    
    def process_referent(self, begin : 'Token', param : str) -> 'ReferentToken':
        return DateAnalyzer.process_referent_stat(begin, param)
    
    @staticmethod
    def process_referent_stat(begin : 'Token', param : str=None) -> 'ReferentToken':
        from pullenti.ner.date.internal.DateItemToken import DateItemToken
        if (begin is None): 
            return None
        ad = DateAnalyzer._get_data(begin)
        if (ad is None): 
            return None
        if (ad.level > 2): 
            return None
        if (begin.is_value("ДО", None) and (isinstance(begin.next0_, ReferentToken)) and (isinstance(begin.next0_.get_referent(), DateReferent))): 
            drr = DateRangeReferent._new941(Utils.asObjectOrNull(begin.next0_.get_referent(), DateReferent))
            res1 = ReferentToken(drr, begin, begin.next0_)
            if (res1.end_token.next0_ is not None and res1.end_token.next0_.is_value("ВКЛЮЧИТЕЛЬНО", None)): 
                res1.end_token = res1.end_token.next0_
            else: 
                drr.add_slot("@EXCLUDE", "true", True, 0)
            res1.data = (ad)
            return res1
        if (begin.is_value("ПОСЛЕ", None) and (isinstance(begin.next0_, ReferentToken)) and (isinstance(begin.next0_.get_referent(), DateReferent))): 
            drr = DateRangeReferent._new942(Utils.asObjectOrNull(begin.next0_.get_referent(), DateReferent))
            res1 = ReferentToken(drr, begin, begin.next0_)
            if (res1.end_token.next0_ is not None and res1.end_token.next0_.is_value("ВКЛЮЧИТЕЛЬНО", None)): 
                res1.end_token = res1.end_token.next0_
            else: 
                drr.add_slot("@EXCLUDE", "true", True, 0)
            res1.data = (ad)
            return res1
        ad.level += 1
        pli = DateItemToken.try_parse_list(begin, 10)
        ad.level -= 1
        if (pli is None or len(pli) == 0): 
            return None
        ad.level += 1
        rts = DateAnalyzer.__try_attach(pli, True)
        ad.level -= 1
        if (rts is None or len(rts) == 0): 
            return None
        res = rts[len(rts) - 1]
        i = 0
        while i < (len(rts) - 1): 
            if ((isinstance(res.referent, DateReferent)) and (isinstance(rts[i].referent, DateReferent))): 
                res.referent.merge_slots(rts[i].referent, True)
            else: 
                rts[i].data = (ad)
            i += 1
        res.referent.add_slot(DateReferent.ATTR_HIGHER, None, True, 0)
        res.data = (ad)
        return res
    
    @staticmethod
    def __try_attach(dts : typing.List['DateItemToken'], high : bool) -> typing.List['ReferentToken']:
        from pullenti.ner.date.internal.DateItemToken import DateItemToken
        if (dts is None or len(dts) == 0): 
            return None
        if ((dts[0].can_be_hour and len(dts) > 2 and dts[1].typ == DateItemToken.DateItemType.DELIM) and dts[2].int_value >= 0 and (dts[2].int_value < 60)): 
            if (dts[0].typ == DateItemToken.DateItemType.HOUR or ((dts[0].typ == DateItemToken.DateItemType.NUMBER and ((dts[2].typ == DateItemToken.DateItemType.HOUR or dts[2].typ == DateItemToken.DateItemType.NUMBER))))): 
                if (len(dts) > 3 and dts[3].typ == DateItemToken.DateItemType.DELIM and dts[3].string_value == dts[1].string_value): 
                    pass
                else: 
                    dts1 = list(dts)
                    del dts1[0:0+3]
                    res1 = DateAnalyzer.__try_attach(dts1, False)
                    if (res1 is not None and (isinstance(res1[len(res1) - 1].referent, DateReferent)) and res1[len(res1) - 1].referent.day > 0): 
                        time = DateReferent._new943(dts[0].int_value, dts[2].int_value)
                        time.higher = Utils.asObjectOrNull(res1[len(res1) - 1].referent, DateReferent)
                        res1.append(ReferentToken(time, dts[0].begin_token, res1[len(res1) - 1].end_token))
                        return res1
        if (dts[0].typ == DateItemToken.DateItemType.HOUR and len(dts) > 2 and dts[1].typ == DateItemToken.DateItemType.MINUTE): 
            ii = 2
            if ((ii < len(dts)) and dts[ii].typ == DateItemToken.DateItemType.SECOND): 
                ii += 1
            dts1 = list(dts)
            del dts1[0:0+ii]
            res1 = DateAnalyzer.__try_attach(dts1, False)
            if (res1 is not None and (isinstance(res1[len(res1) - 1].referent, DateReferent)) and res1[len(res1) - 1].referent.day > 0): 
                time = DateReferent._new943(dts[0].int_value, dts[1].int_value)
                if (ii > 2): 
                    time.second = dts[2].int_value
                time.higher = Utils.asObjectOrNull(res1[len(res1) - 1].referent, DateReferent)
                res1.append(ReferentToken(time, dts[0].begin_token, res1[len(res1) - 1].end_token))
                return res1
        if ((dts[0].can_be_day and len(dts) > 4 and dts[1].typ == DateItemToken.DateItemType.DELIM) and dts[1].begin_token.is_comma_and and dts[2].can_be_day): 
            has_month = False
            has_year = False
            for kk in range(2):
                ii = 3
                while ii < len(dts): 
                    if (dts[ii].can_be_day or ((dts[ii].typ == DateItemToken.DateItemType.DELIM and dts[ii].begin_token.is_comma_and))): 
                        pass
                    elif (dts[ii].typ == DateItemToken.DateItemType.MONTH): 
                        has_month = True
                    elif (dts[ii].typ == DateItemToken.DateItemType.YEAR): 
                        has_year = True
                        break
                    else: 
                        break
                    ii += 1
                if (has_year): 
                    break
                if (not has_month or kk > 0): 
                    break
                if (len(dts) < 17): 
                    break
                dts1 = DateItemToken.try_parse_list(dts[0].begin_token, 100)
                if (dts1 is not None and len(dts1) > len(dts)): 
                    dts = dts1
                else: 
                    break
            if (has_year and has_month): 
                dts2 = list(dts)
                del dts2[0:0+2]
                res2 = DateAnalyzer.__try_attach(dts2, high)
                if (res2 is not None and (isinstance(res2[len(res2) - 1].referent, DateReferent))): 
                    dd = DateReferent()
                    dd.day = dts[0].int_value
                    dd.higher = res2[len(res2) - 1].referent.higher
                    res2.append(ReferentToken(dd, dts[0].begin_token, dts[0].end_token))
                    return res2
        if (((dts[0].can_be_day and len(dts) > 5 and dts[1].typ == DateItemToken.DateItemType.MONTH) and dts[2].typ == DateItemToken.DateItemType.DELIM and dts[2].begin_token.is_comma_and) and dts[3].can_be_day): 
            has_month = False
            has_year = False
            for kk in range(2):
                ii = 3
                while ii < len(dts): 
                    if (dts[ii].can_be_day or ((dts[ii].typ == DateItemToken.DateItemType.DELIM and dts[ii].begin_token.is_comma_and))): 
                        pass
                    elif (dts[ii].typ == DateItemToken.DateItemType.MONTH): 
                        has_month = True
                    elif (dts[ii].typ == DateItemToken.DateItemType.YEAR): 
                        has_year = True
                        break
                    else: 
                        break
                    ii += 1
                if (has_year): 
                    break
                if (not has_month or kk > 0): 
                    break
                if (len(dts) < 17): 
                    break
                dts1 = DateItemToken.try_parse_list(dts[0].begin_token, 100)
                if (dts1 is not None and len(dts1) > len(dts)): 
                    dts = dts1
                else: 
                    break
            if (has_year and has_month): 
                dts2 = list(dts)
                del dts2[0:0+3]
                res2 = DateAnalyzer.__try_attach(dts2, high)
                if (res2 is not None and (isinstance(res2[len(res2) - 1].referent, DateReferent))): 
                    yy = res2[len(res2) - 1].referent.higher
                    if (yy is not None): 
                        yy = yy.higher
                    if (yy is not None and yy.year > 0): 
                        mm = DateReferent()
                        mm.month = dts[1].int_value
                        mm.higher = yy
                        res2.append(ReferentToken(mm, dts[1].begin_token, dts[1].end_token))
                        dd = DateReferent()
                        dd.day = dts[0].int_value
                        dd.higher = mm
                        res2.append(ReferentToken(dd, dts[0].begin_token, dts[1].end_token))
                        return res2
        year = None
        mon = None
        day = None
        cent = None
        tenyears = None
        point = None
        year_is_dif = False
        b = False
        wrapyear997 = RefOutArgWrapper(None)
        wrapmon998 = RefOutArgWrapper(None)
        wrapday999 = RefOutArgWrapper(None)
        b = DateAnalyzer.__apply_rule_formal(dts, high, wrapyear997, wrapmon998, wrapday999)
        year = wrapyear997.value
        mon = wrapmon998.value
        day = wrapday999.value
        if (b): 
            tt = dts[0].begin_token.previous
            if (tt is not None): 
                if (tt.is_value("№", None) or tt.is_value("N", None)): 
                    b = False
        if (dts[0].typ == DateItemToken.DateItemType.CENTURY): 
            if (len(dts) == 1): 
                if (isinstance(dts[0].begin_token, NumberToken)): 
                    return None
                if (NumberHelper.try_parse_roman(dts[0].begin_token) is None): 
                    return None
            cent = dts[0]
            b = True
        elif (dts[0].typ == DateItemToken.DateItemType.TENYEARS): 
            tenyears = dts[0]
            b = True
        if (len(dts) == 1 and dts[0].ptr == DatePointerType.TODAY): 
            res0 = list()
            res0.append(ReferentToken(DateReferent._new945(DatePointerType.TODAY), dts[0].begin_token, dts[0].end_token))
            return res0
        if (len(dts) == 1 and dts[0].typ == DateItemToken.DateItemType.YEAR and dts[0].year <= 0): 
            res0 = list()
            res0.append(ReferentToken(DateReferent._new945(DatePointerType.UNDEFINED), dts[0].begin_token, dts[0].end_token))
            return res0
        if (not b and dts[0].typ == DateItemToken.DateItemType.POINTER and len(dts) > 1): 
            if (dts[1].typ == DateItemToken.DateItemType.YEAR): 
                year = dts[1]
                point = dts[0]
                b = True
            elif (dts[1].typ == DateItemToken.DateItemType.CENTURY): 
                cent = dts[1]
                point = dts[0]
                b = True
            elif (dts[1].typ == DateItemToken.DateItemType.TENYEARS): 
                tenyears = dts[1]
                point = dts[0]
                b = True
            elif (dts[1].typ == DateItemToken.DateItemType.MONTH): 
                mon = dts[1]
                point = dts[0]
                if (len(dts) > 2 and ((dts[2].typ == DateItemToken.DateItemType.YEAR or dts[2].can_be_year))): 
                    year = dts[2]
                b = True
        if (not b): 
            wrapyear947 = RefOutArgWrapper(None)
            wrapmon948 = RefOutArgWrapper(None)
            wrapday949 = RefOutArgWrapper(None)
            wrapyear_is_dif950 = RefOutArgWrapper(False)
            b = DateAnalyzer.__apply_rule_with_month(dts, high, wrapyear947, wrapmon948, wrapday949, wrapyear_is_dif950)
            year = wrapyear947.value
            mon = wrapmon948.value
            day = wrapday949.value
            year_is_dif = wrapyear_is_dif950.value
        if (not b): 
            wrapyear951 = RefOutArgWrapper(None)
            wrapmon952 = RefOutArgWrapper(None)
            wrapday953 = RefOutArgWrapper(None)
            b = DateAnalyzer.__apply_rule_year_only(dts, wrapyear951, wrapmon952, wrapday953)
            year = wrapyear951.value
            mon = wrapmon952.value
            day = wrapday953.value
        if (not b): 
            if (len(dts) == 2 and dts[0].typ == DateItemToken.DateItemType.HOUR and dts[1].typ == DateItemToken.DateItemType.MINUTE): 
                t00 = dts[0].begin_token.previous
                if (t00 is not None and (((t00.is_value("ТЕЧЕНИЕ", None) or t00.is_value("ПРОТЯГОМ", None) or t00.is_value("ЧЕРЕЗ", None)) or t00.is_value("ТЕЧІЮ", None)))): 
                    pass
                else: 
                    res0 = list()
                    time = DateReferent._new943(dts[0].int_value, dts[1].int_value)
                    res0.append(ReferentToken(time, dts[0].begin_token, dts[1].end_token))
                    cou = 0
                    tt = dts[0].begin_token.previous
                    while tt is not None and (cou < 1000): 
                        if (isinstance(tt.get_referent(), DateReferent)): 
                            dr = Utils.asObjectOrNull(tt.get_referent(), DateReferent)
                            if (dr.find_slot(DateReferent.ATTR_DAY, None, True) is None and dr.higher is not None): 
                                dr = dr.higher
                            if (dr.find_slot(DateReferent.ATTR_DAY, None, True) is not None): 
                                time.higher = dr
                                break
                        tt = tt.previous; cou += 1
                    return res0
            if ((len(dts) == 4 and dts[0].typ == DateItemToken.DateItemType.MONTH and dts[1].typ == DateItemToken.DateItemType.DELIM) and dts[2].typ == DateItemToken.DateItemType.MONTH and dts[3].can_be_year): 
                res0 = list()
                yea = DateReferent._new938(dts[3].int_value)
                res0.append(ReferentToken._new956(yea, dts[3].begin_token, dts[3].end_token, dts[3].morph))
                mon1 = DateReferent._new957(dts[0].int_value, yea)
                res0.append(ReferentToken._new958(mon1, dts[0].begin_token, dts[0].end_token, mon1))
                mon2 = DateReferent._new957(dts[2].int_value, yea)
                res0.append(ReferentToken(mon2, dts[2].begin_token, dts[3].end_token))
                return res0
            if (((len(dts) >= 4 and dts[0].typ == DateItemToken.DateItemType.NUMBER and dts[0].can_be_day) and dts[1].typ == DateItemToken.DateItemType.DELIM and dts[2].typ == DateItemToken.DateItemType.NUMBER) and dts[2].can_be_day and dts[3].typ == DateItemToken.DateItemType.MONTH): 
                if (len(dts) == 4 or ((len(dts) == 5 and dts[4].can_be_year))): 
                    res0 = list()
                    yea = None
                    if (len(dts) == 5): 
                        yea = DateReferent._new938(dts[4].year)
                        res0.append(ReferentToken(yea, dts[4].begin_token, dts[4].end_token))
                    mo = DateReferent._new957(dts[3].int_value, yea)
                    res0.append(ReferentToken(mo, dts[3].begin_token, dts[len(dts) - 1].end_token))
                    da1 = DateReferent._new962(dts[0].int_value, mo)
                    res0.append(ReferentToken(da1, dts[0].begin_token, dts[0].end_token))
                    da2 = DateReferent._new962(dts[2].int_value, mo)
                    res0.append(ReferentToken(da2, dts[2].begin_token, dts[len(dts) - 1].end_token))
                    dr = DateRangeReferent()
                    dr.date_from = da1
                    dr.date_to = da2
                    res0.append(ReferentToken(dr, dts[0].begin_token, dts[len(dts) - 1].end_token))
                    return res0
            if ((len(dts) >= 3 and dts[0].can_by_month and dts[1].typ == DateItemToken.DateItemType.DELIM) and dts[2].can_be_year and dts[1].string_value == "."): 
                if (((len(dts) >= 7 and dts[3].begin_token.is_hiphen and dts[4].can_by_month) and dts[5].string_value == "." and dts[6].can_be_year) and dts[2].int_value <= dts[6].int_value): 
                    res0 = list()
                    yea1 = DateReferent._new938(dts[2].year)
                    res0.append(ReferentToken(yea1, dts[2].begin_token, dts[2].end_token))
                    mon1 = DateReferent._new957(dts[0].int_value, yea1)
                    res0.append(ReferentToken(mon1, dts[0].begin_token, dts[2].end_token))
                    yea2 = DateReferent._new938(dts[6].year)
                    res0.append(ReferentToken(yea2, dts[6].begin_token, dts[6].end_token))
                    mon2 = DateReferent._new957(dts[4].int_value, yea2)
                    res0.append(ReferentToken(mon2, dts[4].begin_token, dts[6].end_token))
                    dr = DateRangeReferent()
                    dr.date_from = mon1
                    dr.date_to = mon2
                    res0.append(ReferentToken(dr, dts[0].begin_token, dts[6].end_token))
                    return res0
                ok2 = False
                if (len(dts) == 5 and dts[3].begin_token.is_hiphen and dts[4].typ == DateItemToken.DateItemType.POINTER): 
                    ok2 = True
                if ((len(dts) == 3 and dts[2].end_token.next0_ is not None and dts[2].end_token.next0_.is_hiphen) and dts[2].end_token.next0_.next0_ is not None and dts[2].end_token.next0_.next0_.is_value("ПО", None)): 
                    ok2 = True
                if (ok2): 
                    res0 = list()
                    yea1 = DateReferent._new938(dts[2].year)
                    res0.append(ReferentToken(yea1, dts[2].begin_token, dts[2].end_token))
                    mon1 = DateReferent._new957(dts[0].int_value, yea1)
                    res0.append(ReferentToken(mon1, dts[0].begin_token, dts[2].end_token))
                    tt2 = dts[2].end_token.next0_.next0_
                    if (tt2.is_value("ПО", None)): 
                        tt2 = tt2.next0_
                    dts2 = DateItemToken.try_parse_list(tt2, 20)
                    if (dts2 is not None and len(dts2) == 1 and dts2[0].typ == DateItemToken.DateItemType.POINTER): 
                        nows = DateAnalyzer.__try_attach(dts2, False)
                        if (nows is not None and len(nows) == 1 and (isinstance(nows[0].referent, DateReferent))): 
                            dr = DateRangeReferent()
                            dr.date_from = mon1
                            dr.date_to = Utils.asObjectOrNull(nows[0].referent, DateReferent)
                            res0.append(nows[0])
                            res0.append(ReferentToken(dr, dts[0].begin_token, nows[0].end_token))
                    return res0
            if ((dts[0].typ == DateItemToken.DateItemType.MONTH and len(dts) == 1 and dts[0].end_token.next0_ is not None) and ((dts[0].end_token.next0_.is_hiphen or dts[0].end_token.next0_.is_value("ПО", None) or dts[0].end_token.next0_.is_value("НА", None)))): 
                rt = DateAnalyzer.process_referent_stat(dts[0].end_token.next0_.next0_, None)
                if (rt is not None): 
                    dr0 = Utils.asObjectOrNull(rt.referent, DateReferent)
                    if ((dr0 is not None and dr0.year > 0 and dr0.month > 0) and dr0.day == 0 and dr0.month > dts[0].int_value): 
                        dr_year0 = DateReferent._new938(dr0.year)
                        res0 = list()
                        res0.append(ReferentToken(dr_year0, dts[0].end_token, dts[0].end_token))
                        dr_mon0 = DateReferent._new957(dts[0].int_value, dr_year0)
                        res0.append(ReferentToken(dr_mon0, dts[0].begin_token, dts[0].end_token))
                        return res0
            if (((len(dts) == 3 and dts[1].typ == DateItemToken.DateItemType.DELIM and dts[1].begin_token.is_hiphen) and dts[0].can_be_year and dts[2].can_be_year) and (dts[0].int_value < dts[2].int_value)): 
                ok = False
                if (dts[2].typ == DateItemToken.DateItemType.YEAR): 
                    ok = True
                elif (dts[0].length_char == 4 and dts[2].length_char == 4 and dts[0].begin_token.previous is not None): 
                    tt0 = dts[0].begin_token.previous
                    if (tt0.is_char('(') and dts[2].end_token.next0_ is not None and dts[2].end_token.next0_.is_char(')')): 
                        ok = True
                    elif (tt0.is_value("IN", None) or tt0.is_value("SINCE", None) or tt0.is_value("В", "У")): 
                        ok = True
                if (ok): 
                    res0 = list()
                    res0.append(ReferentToken(DateReferent._new938(dts[0].year), dts[0].begin_token, dts[0].end_token))
                    res0.append(ReferentToken(DateReferent._new938(dts[2].year), dts[2].begin_token, dts[2].end_token))
                    return res0
            if (len(dts) > 1 and dts[0].typ == DateItemToken.DateItemType.YEAR): 
                res0 = list()
                res0.append(ReferentToken(DateReferent._new938(dts[0].year), dts[0].begin_token, dts[0].end_token))
                return res0
            if (dts[0].ltyp != DateItemToken.FirstLastTyp.NO and len(dts) > 1): 
                high = True
            if (high): 
                if (len(dts) == 1 and dts[0].can_be_year and dts[0].typ == DateItemToken.DateItemType.NUMBER): 
                    res0 = list()
                    res0.append(ReferentToken(DateReferent._new938(dts[0].year), dts[0].begin_token, dts[0].end_token))
                    return res0
                if ((((len(dts) == 3 and dts[0].can_be_year and dts[0].typ == DateItemToken.DateItemType.NUMBER) and dts[2].can_be_year and dts[2].typ == DateItemToken.DateItemType.NUMBER) and (dts[0].year < dts[2].year) and dts[1].typ == DateItemToken.DateItemType.DELIM) and dts[1].begin_token.is_hiphen): 
                    res0 = list()
                    y1 = DateReferent._new938(dts[0].year)
                    res0.append(ReferentToken(y1, dts[0].begin_token, dts[0].end_token))
                    y2 = DateReferent._new938(dts[2].year)
                    res0.append(ReferentToken(y1, dts[2].begin_token, dts[2].end_token))
                    ra = DateRangeReferent._new935(y1, y2)
                    res0.append(ReferentToken(ra, dts[0].begin_token, dts[2].end_token))
                    return res0
            if (dts[0].typ == DateItemToken.DateItemType.QUARTAL or dts[0].typ == DateItemToken.DateItemType.HALFYEAR or ((dts[0].typ == DateItemToken.DateItemType.MONTH and dts[0].ltyp != DateItemToken.FirstLastTyp.NO))): 
                if (len(dts) == 1 or dts[1].typ == DateItemToken.DateItemType.YEAR): 
                    res0 = list()
                    ii = 0
                    yea = None
                    if (len(dts) > 1): 
                        ii = 1
                        yea = DateReferent._new938(dts[1].int_value)
                        res0.append(ReferentToken._new956(yea, dts[1].begin_token, dts[1].end_token, dts[1].morph))
                    else: 
                        cou = 0
                        tt = dts[0].begin_token
                        while tt is not None: 
                            cou += 1
                            if (cou > 200): 
                                break
                            if (isinstance(tt, ReferentToken)): 
                                yea = DateAnalyzer.__find_year_(tt.get_referent())
                                if ((yea) is not None): 
                                    break
                            if (tt.is_newline_before): 
                                break
                            tt = tt.previous
                    if (yea is None): 
                        return None
                    m1 = 0
                    m2 = 0
                    if (dts[0].typ == DateItemToken.DateItemType.HALFYEAR): 
                        if (dts[0].int_value == 2 or dts[0].ltyp == DateItemToken.FirstLastTyp.LAST): 
                            m1 = 7
                            m2 = 12
                        elif (dts[0].int_value == 1): 
                            m1 = 1
                            m2 = 6
                        else: 
                            return None
                    elif (dts[0].typ == DateItemToken.DateItemType.QUARTAL): 
                        if (dts[0].ltyp == DateItemToken.FirstLastTyp.FIRST): 
                            m1 = 1
                            m2 = (dts[0].int_value * 3)
                        elif (dts[0].ltyp == DateItemToken.FirstLastTyp.LAST): 
                            m1 = (13 - (dts[0].int_value * 3))
                            m2 = 12
                        elif (dts[0].int_value == 1): 
                            m1 = 1
                            m2 = 3
                        elif (dts[0].int_value == 2): 
                            m1 = 4
                            m2 = 6
                        elif (dts[0].int_value == 3): 
                            m1 = 7
                            m2 = 9
                        elif (dts[0].int_value == 4 or dts[0].ltyp == DateItemToken.FirstLastTyp.LAST): 
                            m1 = 10
                            m2 = 12
                        else: 
                            return None
                    elif (dts[0].typ == DateItemToken.DateItemType.MONTH and dts[0].ltyp != DateItemToken.FirstLastTyp.NO): 
                        if (dts[0].ltyp == DateItemToken.FirstLastTyp.FIRST): 
                            m1 = 1
                            m2 = dts[0].int_value
                        else: 
                            m1 = (13 - dts[0].int_value)
                            m2 = 12
                    else: 
                        return None
                    mon1 = DateReferent._new957(m1, yea)
                    res0.append(ReferentToken(mon1, dts[0].begin_token, dts[0].begin_token))
                    mon2 = DateReferent._new957(m2, yea)
                    res0.append(ReferentToken(mon2, dts[0].end_token, dts[0].end_token))
                    dr = DateRangeReferent()
                    dr.date_from = mon1
                    dr.date_to = mon2
                    res0.append(ReferentToken(dr, dts[0].begin_token, dts[ii].end_token))
                    return res0
            if ((len(dts) == 3 and dts[1].typ == DateItemToken.DateItemType.DELIM and ((dts[1].string_value == "." or dts[1].string_value == ":"))) and dts[0].can_be_hour and dts[2].can_be_minute): 
                ok = False
                if (dts[0].begin_token.previous is not None and ((dts[0].begin_token.previous.is_value("В", None) or dts[0].begin_token.previous.is_value("ОКОЛО", None)))): 
                    ok = True
                if (ok): 
                    time = DateReferent._new943(dts[0].int_value, dts[2].int_value)
                    cou = 0
                    tt = dts[0].begin_token.previous
                    while tt is not None and (cou < 1000): 
                        if (isinstance(tt.get_referent(), DateReferent)): 
                            dr = Utils.asObjectOrNull(tt.get_referent(), DateReferent)
                            if (dr.find_slot(DateReferent.ATTR_DAY, None, True) is None and dr.higher is not None): 
                                dr = dr.higher
                            if (dr.find_slot(DateReferent.ATTR_DAY, None, True) is not None): 
                                time.higher = dr
                                break
                        tt = tt.previous; cou += 1
                    tt1 = dts[2].end_token
                    if (tt1.next0_ is not None and tt1.next0_.is_value("ЧАС", None)): 
                        tt1 = tt1.next0_
                        dtsli = DateItemToken.try_parse_list(tt1.next0_, 20)
                        if (dtsli is not None): 
                            res1 = DateAnalyzer.__try_attach(dtsli, True)
                            if (res1 is not None and res1[len(res1) - 1].referent.day > 0): 
                                time.higher = Utils.asObjectOrNull(res1[len(res1) - 1].referent, DateReferent)
                                res1.append(ReferentToken(time, dts[0].begin_token, tt1))
                                return res1
                    tt2 = DateAnalyzer.__corr_time(tt1.next0_, time)
                    if (tt2 is not None): 
                        tt1 = tt2
                    res0 = list()
                    res0.append(ReferentToken(time, dts[0].begin_token, tt1))
                    return res0
            if ((len(dts) == 1 and dts[0].typ == DateItemToken.DateItemType.MONTH and dts[0].begin_token.previous is not None) and dts[0].begin_token.previous.morph.class0_.is_preposition): 
                if (dts[0].chars.is_latin_letter and dts[0].chars.is_all_lower): 
                    pass
                else: 
                    res0 = list()
                    res0.append(ReferentToken(DateReferent._new984(dts[0].int_value), dts[0].begin_token, dts[0].end_token))
                    return res0
            return None
        res = list()
        dr_year = None
        dr_mon = None
        dr_day = None
        t0 = None
        t1 = None
        if (cent is not None): 
            ce = DateReferent._new985((- cent.int_value if cent.new_age < 0 else cent.int_value), cent.relate)
            t1 = cent.end_token
            rt = ReferentToken(ce, cent.begin_token, t1)
            res.append(rt)
        if (tenyears is not None): 
            ce = DateReferent._new986(tenyears.int_value, tenyears.relate)
            if (cent is not None): 
                ce.higher = Utils.asObjectOrNull(res[len(res) - 1].referent, DateReferent)
            t1 = tenyears.end_token
            rt = ReferentToken(ce, tenyears.begin_token, t1)
            res.append(rt)
        if (year is not None and year.year > 0): 
            dr_year = DateReferent._new938((- year.year if year.new_age < 0 else year.year))
            if (not year_is_dif): 
                t1 = year.end_token
                if (t1.next0_ is not None and t1.next0_.is_value("ГОРОД", None)): 
                    tt2 = t1.next0_.next0_
                    if (tt2 is None): 
                        t1 = t1.next0_
                        year.end_token = t1
                    elif ((tt2.whitespaces_before_count < 3) and ((tt2.morph.class0_.is_preposition or tt2.chars.is_all_lower))): 
                        t1 = t1.next0_
                        year.end_token = t1
            t0 = year.begin_token
            res.append(ReferentToken._new956(dr_year, t0, year.end_token, year.morph))
            if (((len(dts) == 3 and year == dts[2] and mon is None) and day is None and dts[0].year > 0) and dts[1].typ == DateItemToken.DateItemType.DELIM and dts[1].end_token.is_hiphen): 
                dr_year0 = DateReferent._new938((- dts[0].year if year.new_age < 0 else dts[0].year))
                t0 = dts[0].begin_token
                res.append(ReferentToken(dr_year0, t0, dts[0].end_token))
        if (mon is not None): 
            dr_mon = DateReferent._new984(mon.int_value)
            if (dr_year is not None): 
                dr_mon.higher = dr_year
            if (t0 is None or (mon.begin_char < t0.begin_char)): 
                t0 = mon.begin_token
            if (t1 is None or mon.end_char > t1.end_char): 
                t1 = mon.end_token
            if (dr_year is None and t1.next0_ is not None and ((t1.next0_.is_value("ПО", None) or t1.next0_.is_value("НА", None)))): 
                rt = DateAnalyzer.process_referent_stat(t1.next0_.next0_, None)
                if (rt is not None): 
                    dr0 = Utils.asObjectOrNull(rt.referent, DateReferent)
                    if (dr0 is not None and dr0.year > 0 and dr0.month > 0): 
                        dr_year = DateReferent._new938(dr0.year)
                        t0 = t1
                        res.append(ReferentToken(dr_year, t0, t1))
                        dr_mon.higher = dr_year
            res.append(ReferentToken._new956(dr_mon, t0, t1, mon.morph))
            if (day is not None): 
                dr_day = DateReferent._new993(day.int_value)
                dr_day.higher = dr_mon
                if (day.begin_char < t0.begin_char): 
                    t0 = day.begin_token
                if (day.end_char > t1.end_char): 
                    t1 = day.end_token
                tt = None
                tt = t0.previous
                while tt is not None: 
                    if (not tt.is_char_of(",.")): 
                        break
                    tt = tt.previous
                dow = DateItemToken.DAYS_OF_WEEK.try_parse(tt, TerminParseAttr.NO)
                if (dow is not None): 
                    t0 = tt
                    dr_day.day_of_week = dow.termin.tag
                res.append(ReferentToken._new956(dr_day, t0, t1, day.morph))
                if (dts[0].typ == DateItemToken.DateItemType.HOUR): 
                    hou = DateReferent._new995(dr_day)
                    hou.hour = dts[0].int_value
                    hou.minute = 0
                    if (dts[1].typ == DateItemToken.DateItemType.MINUTE): 
                        hou.minute = dts[1].int_value
                        if (dts[2].typ == DateItemToken.DateItemType.SECOND): 
                            hou.second = dts[2].int_value
                    res.append(ReferentToken(hou, dts[0].begin_token, t1))
                    return res
        if (point is not None and len(res) > 0): 
            poi = DateReferent()
            poi.pointer = point.ptr
            poi.higher = Utils.asObjectOrNull(res[len(res) - 1].referent, DateReferent)
            res.append(ReferentToken(poi, point.begin_token, t1))
            return res
        if (dr_day is not None and not year_is_dif): 
            rt = DateAnalyzer.__try_attach_time(t1.next0_, True)
            if (rt is not None): 
                rt.referent.higher = dr_day
                rt.begin_token = t0
                res.append(rt)
            else: 
                i = 1
                while i < len(dts): 
                    if (t0.begin_char == dts[i].begin_char): 
                        if (i > 2): 
                            del dts[i:i+len(dts) - i]
                            rt = DateAnalyzer.__try_attach_time_li(dts, True)
                            if (rt is not None): 
                                rt.referent.higher = dr_day
                                rt.end_token = t1
                                res.append(rt)
                            break
                    i += 1
        if (len(res) == 1): 
            dt0 = Utils.asObjectOrNull(res[0].referent, DateReferent)
            if (dt0.month == 0): 
                tt = res[0].begin_token.previous
                if (tt is not None and tt.is_char('_') and not tt.is_newline_after): 
                    while tt is not None: 
                        if (not tt.is_char('_')): 
                            break
                        else: 
                            res[0].begin_token = tt
                        tt = tt.previous
                    if (BracketHelper.can_be_end_of_sequence(tt, True, None, False)): 
                        tt = tt.previous
                        while tt is not None: 
                            if (tt.is_newline_after): 
                                break
                            elif (tt.is_char('_')): 
                                pass
                            else: 
                                if (BracketHelper.can_be_start_of_sequence(tt, True, False)): 
                                    res[0].begin_token = tt
                                break
                            tt = tt.previous
                tt = res[0].end_token.next0_
                if (tt is not None and tt.is_char_of("(,")): 
                    dit = DateItemToken.try_parse(tt.next0_, None, False)
                    if (dit is not None and dit.typ == DateItemToken.DateItemType.MONTH): 
                        dr_mon = DateReferent._new996(dt0, dit.int_value)
                        pr_mon = ReferentToken(dr_mon, res[0].begin_token, dit.end_token)
                        if (tt.is_char('(') and pr_mon.end_token.next0_ is not None and pr_mon.end_token.next0_.is_char(')')): 
                            pr_mon.end_token = pr_mon.end_token.next0_
                        res.append(pr_mon)
        if (len(res) > 0 and dr_day is not None): 
            la = res[len(res) - 1]
            tt = la.end_token.next0_
            if (tt is not None and tt.is_char(',')): 
                tt = tt.next0_
            tok = DateItemToken.DAYS_OF_WEEK.try_parse(tt, TerminParseAttr.NO)
            if (tok is not None): 
                la.end_token = tok.end_token
                dr_day.day_of_week = tok.termin.tag
        return res
    
    @staticmethod
    def __find_year_(r : 'Referent') -> 'DateReferent':
        dr = Utils.asObjectOrNull(r, DateReferent)
        if (dr is not None): 
            while dr is not None: 
                if (dr.higher is None and dr.year > 0): 
                    return dr
                dr = dr.higher
            return None
        drr = Utils.asObjectOrNull(r, DateRangeReferent)
        if (drr is not None): 
            dr = DateAnalyzer.__find_year_(drr.date_from)
            if ((dr) is not None): 
                return dr
            dr = DateAnalyzer.__find_year_(drr.date_to)
            if ((dr) is not None): 
                return dr
        return None
    
    @staticmethod
    def __try_attach_time(t : 'Token', after_date : bool) -> 'ReferentToken':
        from pullenti.ner.date.internal.DateItemToken import DateItemToken
        if (t is None): 
            return None
        if (t.is_value("ГОРОД", None) and t.next0_ is not None): 
            t = t.next0_
        while t is not None and ((t.morph.class0_.is_preposition or t.morph.class0_.is_adverb or t.is_comma)):
            if (t.morph.language.is_ru): 
                if (not t.is_value("ПО", None) and not t.is_value("НА", None)): 
                    t = t.next0_
                else: 
                    break
            else: 
                t = t.next0_
        if (t is None): 
            return None
        dts = DateItemToken.try_parse_list(t, 10)
        return DateAnalyzer.__try_attach_time_li(dts, after_date)
    
    @staticmethod
    def __corr_time(t0 : 'Token', time : 'DateReferent') -> 'Token':
        from pullenti.ner.date.internal.DateItemToken import DateItemToken
        t1 = None
        t = t0
        first_pass2846 = True
        while True:
            if first_pass2846: first_pass2846 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (not (isinstance(t, TextToken))): 
                break
            term = t.term
            if (term == "МСК"): 
                t1 = t
                continue
            npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.PARSEPREPOSITION, 0, None)
            if (npt is not None and npt.end_token.is_value("ВРЕМЯ", None)): 
                t1 = npt.end_token
                t = t1
                continue
            if ((t.is_char_of("(") and t.next0_ is not None and t.next0_.is_value("МСК", None)) and t.next0_.next0_ is not None and t.next0_.next0_.is_char(')')): 
                t = t.next0_.next0_
                t1 = t
                continue
            if ((term == "PM" or term == "РМ" or t.is_value("ВЕЧЕР", "ВЕЧІР")) or t.is_value("ДЕНЬ", None)): 
                if (time.hour < 12): 
                    time.hour = time.hour + 12
                t1 = t
                continue
            if ((term == "AM" or term == "АМ" or term == "Ч") or t.is_value("ЧАС", None)): 
                t1 = t
                continue
            if (t.is_char('+')): 
                ddd = DateItemToken.try_parse_list(t.next0_, 20)
                if ((ddd is not None and len(ddd) == 3 and ddd[0].typ == DateItemToken.DateItemType.NUMBER) and ddd[1].typ == DateItemToken.DateItemType.DELIM and ddd[2].typ == DateItemToken.DateItemType.NUMBER): 
                    t1 = ddd[2].end_token
                    continue
            if (t.is_char_of(",.")): 
                continue
            break
        return t1
    
    @staticmethod
    def __try_attach_time_li(dts : typing.List['DateItemToken'], after_date : bool) -> 'ReferentToken':
        from pullenti.ner.date.internal.DateItemToken import DateItemToken
        if (dts is None or (len(dts) < 1)): 
            return None
        t0 = dts[0].begin_token
        t1 = None
        time = None
        if (len(dts) == 1): 
            if (dts[0].typ == DateItemToken.DateItemType.HOUR and after_date): 
                time = DateReferent._new943(dts[0].int_value, 0)
                t1 = dts[0].end_token
            else: 
                return None
        elif (dts[0].typ == DateItemToken.DateItemType.HOUR and dts[1].typ == DateItemToken.DateItemType.MINUTE): 
            time = DateReferent._new943(dts[0].int_value, dts[1].int_value)
            t1 = dts[1].end_token
            if (len(dts) > 2 and dts[2].typ == DateItemToken.DateItemType.SECOND): 
                t1 = dts[2].end_token
                time.second = dts[2].int_value
        elif ((((len(dts) > 2 and dts[0].typ == DateItemToken.DateItemType.NUMBER and dts[1].typ == DateItemToken.DateItemType.DELIM) and ((dts[1].string_value == ":" or dts[1].string_value == "." or dts[1].string_value == "-")) and dts[2].typ == DateItemToken.DateItemType.NUMBER) and (dts[0].int_value < 24) and (dts[2].int_value < 60)) and dts[2].length_char == 2 and after_date): 
            time = DateReferent._new943(dts[0].int_value, dts[2].int_value)
            t1 = dts[2].end_token
            if ((len(dts) > 4 and dts[3].string_value == dts[1].string_value and dts[4].typ == DateItemToken.DateItemType.NUMBER) and (dts[4].int_value < 60)): 
                time.second = dts[4].int_value
                t1 = dts[4].end_token
        if (time is None): 
            return None
        tt = DateAnalyzer.__corr_time(t1.next0_, time)
        if (tt is not None): 
            t1 = tt
        cou = 0
        tt = t0.previous
        while tt is not None and (cou < 1000): 
            if (isinstance(tt.get_referent(), DateReferent)): 
                dr = Utils.asObjectOrNull(tt.get_referent(), DateReferent)
                if (dr.find_slot(DateReferent.ATTR_DAY, None, True) is None and dr.higher is not None): 
                    dr = dr.higher
                if (dr.find_slot(DateReferent.ATTR_DAY, None, True) is not None): 
                    time.higher = dr
                    break
            tt = tt.previous; cou += 1
        if (t1.next0_ is not None): 
            if (t1.next0_.is_value("ЧАС", None)): 
                t1 = t1.next0_
        return ReferentToken(time, t0, t1)
    
    @staticmethod
    def __apply_rule_formal(its : typing.List['DateItemToken'], high : bool, year : 'DateItemToken', mon : 'DateItemToken', day : 'DateItemToken') -> bool:
        from pullenti.ner.date.internal.DateItemToken import DateItemToken
        year.value = (None)
        mon.value = (None)
        day.value = (None)
        i = 0
        j = 0
        i = 0
        first_pass2847 = True
        while True:
            if first_pass2847: first_pass2847 = False
            else: i += 1
            if (not (i < (len(its) - 4))): break
            if (its[i].begin_token.previous is not None and its[i].begin_token.previous.is_char(')') and (its[i].whitespaces_before_count < 2)): 
                return False
            if (not its[i].can_be_day and not its[i].can_be_year and not its[i].can_by_month): 
                continue
            if (not its[i].is_whitespace_before): 
                if (its[i].begin_token.previous is not None and ((its[i].begin_token.previous.is_char_of("(;,") or its[i].begin_token.previous.morph.class0_.is_preposition or its[i].begin_token.previous.is_table_control_char))): 
                    pass
                elif (i > 0): 
                    continue
            j = i
            first_pass2848 = True
            while True:
                if first_pass2848: first_pass2848 = False
                else: j += 1
                if (not (j < (i + 4))): break
                if (its[j].is_whitespace_after): 
                    if (high and not its[j].is_newline_after): 
                        continue
                    if (i == 0 and len(its) == 5 and ((j == 1 or j == 3))): 
                        if (its[j].whitespaces_after_count < 2): 
                            continue
                    break
            if (j < (i + 4)): 
                continue
            if (its[i + 1].typ != DateItemToken.DateItemType.DELIM or its[i + 3].typ != DateItemToken.DateItemType.DELIM or its[i + 1].string_value != its[i + 3].string_value): 
                continue
            j = (i + 5)
            if ((j < len(its)) and not its[j].is_whitespace_before): 
                if (its[j].typ == DateItemToken.DateItemType.DELIM and its[j].is_whitespace_after): 
                    pass
                else: 
                    continue
            mon.value = (its[i + 2] if its[i + 2].can_by_month else None)
            if (not its[i].can_be_day): 
                if (not its[i].can_be_year): 
                    continue
                year.value = its[i]
                if (mon.value is not None and its[i + 4].can_be_day): 
                    day.value = its[i + 4]
                elif (its[i + 2].can_be_day and its[i + 4].can_by_month): 
                    day.value = its[i + 2]
                    mon.value = its[i + 4]
                else: 
                    continue
            elif (not its[i].can_be_year): 
                if (not its[i + 4].can_be_year): 
                    if (not high): 
                        continue
                year.value = its[i + 4]
                if (mon.value is not None and its[i].can_be_day): 
                    day.value = its[i]
                elif (its[i].can_by_month and its[i + 2].can_be_day): 
                    mon.value = its[i]
                    day.value = its[i + 2]
                else: 
                    continue
            else: 
                continue
            if ((mon.value.int_value < 10) and not mon.value.is_zero_headed): 
                if (year.value.int_value < 1980): 
                    continue
            delim = its[i + 1].string_value[0]
            if ((delim != '/' and delim != '\\' and delim != '.') and delim != '-'): 
                continue
            if (delim == '.' or delim == '-'): 
                if (year.value == its[i] and (year.value.int_value < 1900)): 
                    continue
            if ((i + 5) < len(its)): 
                del its[i + 5:i + 5+len(its) - i - 5]
            if (i > 0): 
                del its[0:0+i]
            return True
        if (len(its) >= 5 and its[0].is_whitespace_before and its[4].is_whitespace_after): 
            if (its[1].typ == DateItemToken.DateItemType.DELIM and its[2].typ == DateItemToken.DateItemType.DELIM): 
                if (its[0].length_char == 2 and its[2].length_char == 2 and ((its[4].length_char == 2 or its[4].length_char == 4))): 
                    if (its[0].can_be_day and its[2].can_by_month and its[4].typ == DateItemToken.DateItemType.NUMBER): 
                        if ((not its[0].is_whitespace_after and not its[1].is_whitespace_after and not its[2].is_whitespace_after) and not its[3].is_whitespace_after): 
                            iyear = 0
                            y = its[4].int_value
                            if (y > 80 and (y < 100)): 
                                iyear = (1900 + y)
                            elif (y <= (Utils.getDate(datetime.datetime.today()).year - 2000)): 
                                iyear = (y + 2000)
                            else: 
                                return False
                            its[4].year = iyear
                            year.value = its[4]
                            mon.value = its[2]
                            day.value = its[0]
                            return True
        if (high and its[0].can_be_year and len(its) == 1): 
            year.value = its[0]
            return True
        if (its[0].begin_token.previous is not None and its[0].begin_token.previous.is_value("ОТ", None) and len(its) == 4): 
            if (its[0].can_be_day and its[3].can_be_year): 
                if (its[1].typ == DateItemToken.DateItemType.DELIM and its[2].can_by_month): 
                    year.value = its[3]
                    mon.value = its[2]
                    day.value = its[0]
                    return True
                if (its[2].typ == DateItemToken.DateItemType.DELIM and its[1].can_by_month): 
                    year.value = its[3]
                    mon.value = its[1]
                    day.value = its[0]
                    return True
        if ((len(its) == 3 and its[0].typ == DateItemToken.DateItemType.NUMBER and its[0].can_be_day) and its[1].can_by_month): 
            if (its[2].typ == DateItemToken.DateItemType.YEAR or ((its[2].can_be_year and its[0].begin_token.previous is not None and its[0].begin_token.previous.is_value("ОТ", None)))): 
                if (((BracketHelper.is_bracket(its[0].begin_token, False) and BracketHelper.is_bracket(its[0].end_token, False))) or ((its[0].begin_token.previous is not None and its[0].begin_token.previous.get_morph_class_in_dictionary().is_preposition))): 
                    year.value = its[2]
                    mon.value = its[1]
                    day.value = its[0]
                    return True
        return False
    
    @staticmethod
    def __apply_rule_with_month(its : typing.List['DateItemToken'], high : bool, year : 'DateItemToken', mon : 'DateItemToken', day : 'DateItemToken', year_is_diff : bool) -> bool:
        from pullenti.ner.date.internal.DateItemToken import DateItemToken
        year.value = (None)
        mon.value = (None)
        day.value = (None)
        year_is_diff.value = False
        i = 0
        if (len(its) == 2): 
            if (its[0].typ == DateItemToken.DateItemType.MONTH and its[0].ltyp == DateItemToken.FirstLastTyp.NO and its[1].typ == DateItemToken.DateItemType.YEAR): 
                year.value = its[1]
                mon.value = its[0]
                return True
            if (its[0].can_be_day and its[1].typ == DateItemToken.DateItemType.MONTH): 
                mon.value = its[1]
                day.value = its[0]
                return True
        i = 0
        while i < len(its): 
            if (its[i].typ == DateItemToken.DateItemType.MONTH and its[i].ltyp == DateItemToken.FirstLastTyp.NO): 
                break
            i += 1
        if (i >= len(its)): 
            return False
        lang = its[i].lang
        year.value = (None)
        day.value = (None)
        mon.value = its[i]
        i0 = i
        i1 = i
        year_val = 0
        if ((lang.is_ru or lang.is_it or lang.is_by) or lang.is_ua): 
            if (((i + 1) < len(its)) and its[i + 1].typ == DateItemToken.DateItemType.YEAR): 
                year.value = its[i + 1]
                i1 = (i + 1)
                if (i > 0 and its[i - 1].can_be_day): 
                    day.value = its[i - 1]
                    i0 = (i - 1)
            elif (i > 0 and its[i - 1].typ == DateItemToken.DateItemType.YEAR): 
                year.value = its[i - 1]
                i0 = (i - 1)
                if (((i + 1) < len(its)) and its[i + 1].can_be_day): 
                    day.value = its[i + 1]
                    i1 = (i + 1)
            elif (((i + 1) < len(its)) and its[i + 1].can_be_year): 
                if (its[i + 1].typ == DateItemToken.DateItemType.NUMBER): 
                    t00 = its[0].begin_token
                    if (t00.previous is not None and t00.previous.is_char_of(".,")): 
                        t00 = t00.previous.previous
                    if (t00 is not None and (t00.whitespaces_after_count < 3)): 
                        if (((t00.is_value("УЛИЦА", None) or t00.is_value("УЛ", None) or t00.is_value("ПРОСПЕКТ", None)) or t00.is_value("ПРОСП", None) or t00.is_value("ПР", None)) or t00.is_value("ПЕРЕУЛОК", None) or t00.is_value("ПЕР", None)): 
                            return False
                year.value = its[i + 1]
                i1 = (i + 1)
                if (i > 0 and its[i - 1].can_be_day): 
                    day.value = its[i - 1]
                    i0 = (i - 1)
            elif ((i == 0 and its[0].typ == DateItemToken.DateItemType.MONTH and len(its) == 3) and its[i + 1].typ == DateItemToken.DateItemType.DELIM and its[i + 2].can_be_year): 
                year.value = its[i + 2]
                i1 = (i + 2)
            elif (i > 1 and its[i - 2].can_be_year and its[i - 1].can_be_day): 
                year.value = its[i - 2]
                day.value = its[i - 1]
                i0 = (i - 2)
            elif (i > 0 and its[i - 1].can_be_year): 
                year.value = its[i - 1]
                i0 = (i - 1)
                if (((i + 1) < len(its)) and its[i + 1].can_be_day): 
                    day.value = its[i + 1]
                    i1 = (i + 1)
            if (year.value is None and i == 1 and its[i - 1].can_be_day): 
                j = i + 1
                first_pass2849 = True
                while True:
                    if first_pass2849: first_pass2849 = False
                    else: j += 1
                    if (not (j < len(its))): break
                    if (its[j].typ == DateItemToken.DateItemType.DELIM): 
                        continue
                    if (its[j].typ == DateItemToken.DateItemType.YEAR): 
                        year.value = its[j]
                        day.value = its[i - 1]
                        i0 = (i - 1)
                        i1 = i
                        year_is_diff.value = True
                        break
                    if (not its[j].can_be_day): 
                        break
                    j += 1
                    if (j >= len(its)): 
                        break
                    if (its[j].typ == DateItemToken.DateItemType.MONTH): 
                        continue
                    if (its[j].typ == DateItemToken.DateItemType.DELIM and ((j + 1) < len(its)) and its[j + 1].can_be_day): 
                        continue
                    break
        elif (lang.is_en): 
            if (i == 1 and its[0].can_be_day): 
                i1 = 2
                day.value = its[0]
                i0 = 0
                if ((i1 < len(its)) and its[i1].typ == DateItemToken.DateItemType.DELIM): 
                    i1 += 1
                if ((i1 < len(its)) and its[i1].can_be_year): 
                    year.value = its[i1]
                if (year.value is None): 
                    i1 = 1
                    year_val = DateAnalyzer.__find_year(its[0].begin_token)
            elif (i == 0): 
                if (len(its) > 1 and its[1].can_be_year and not its[1].can_be_day): 
                    i1 = 2
                    year.value = its[1]
                elif (len(its) > 1 and its[1].can_be_day): 
                    day.value = its[1]
                    i1 = 2
                    if ((i1 < len(its)) and its[i1].typ == DateItemToken.DateItemType.DELIM): 
                        i1 += 1
                    if ((i1 < len(its)) and its[i1].can_be_year): 
                        year.value = its[i1]
                    if (year.value is None): 
                        i1 = 1
                        year_val = DateAnalyzer.__find_year(its[0].begin_token)
        if (year.value is None and year_val == 0 and len(its) == 3): 
            if (its[0].typ == DateItemToken.DateItemType.YEAR and its[1].can_be_day and its[2].typ == DateItemToken.DateItemType.MONTH): 
                i1 = 2
                year.value = its[0]
                day.value = its[1]
        if (year.value is not None or year_val > 0): 
            return True
        if (day.value is not None and len(its) == 2): 
            return True
        return False
    
    @staticmethod
    def __find_year(t : 'Token') -> int:
        year = 0
        prevdist = 0
        tt = t
        while tt is not None: 
            if (tt.is_newline_before): 
                prevdist += 10
            prevdist += 1
            if (isinstance(tt, ReferentToken)): 
                if (isinstance(tt.referent, DateReferent)): 
                    year = tt.referent.year
                    break
            tt = tt.previous
        dist = 0
        tt = t
        while tt is not None: 
            if (tt.is_newline_after): 
                dist += 10
            dist += 1
            if (isinstance(tt, ReferentToken)): 
                if (isinstance(tt.referent, DateReferent)): 
                    if (year > 0 and (prevdist < dist)): 
                        return year
                    else: 
                        return tt.referent.year
            tt = tt.next0_
        return year
    
    @staticmethod
    def __apply_rule_year_only(its : typing.List['DateItemToken'], year : 'DateItemToken', mon : 'DateItemToken', day : 'DateItemToken') -> bool:
        from pullenti.ner.date.internal.DateItemToken import DateItemToken
        year.value = (None)
        mon.value = (None)
        day.value = (None)
        i = 0
        doubt = False
        i = 0
        while i < len(its): 
            if (its[i].typ == DateItemToken.DateItemType.YEAR): 
                break
            elif (its[i].typ == DateItemToken.DateItemType.NUMBER): 
                doubt = True
            elif (its[i].typ != DateItemToken.DateItemType.DELIM): 
                return False
            i += 1
        if (i >= len(its)): 
            if (((len(its) == 1 and its[0].can_be_year and its[0].int_value > 1900) and its[0].can_be_year and (its[0].int_value < 2100)) and its[0].begin_token.previous is not None): 
                if (((its[0].begin_token.previous.is_value("В", None) or its[0].begin_token.previous.is_value("У", None) or its[0].begin_token.previous.is_value("З", None)) or its[0].begin_token.previous.is_value("IN", None) or its[0].begin_token.previous.is_value("SINCE", None))): 
                    if (its[0].length_char == 4 or its[0].begin_token.morph.class0_.is_adjective): 
                        year.value = its[0]
                        return True
            return False
        if ((i + 1) == len(its)): 
            if (its[i].int_value > 1900 or its[i].new_age != 0): 
                year.value = its[i]
                return True
            if (doubt): 
                return False
            if (its[i].int_value > 10 and (its[i].int_value < 100)): 
                if (its[i].begin_token.previous is not None): 
                    if (its[i].begin_token.previous.is_value("В", None) or its[i].begin_token.previous.is_value("IN", None) or its[i].begin_token.previous.is_value("У", None)): 
                        year.value = its[i]
                        return True
                if (its[i].begin_token.is_value("В", None) or its[i].begin_token.is_value("У", None) or its[i].begin_token.is_value("IN", None)): 
                    year.value = its[i]
                    return True
            if (its[i].int_value >= 100): 
                year.value = its[i]
                return True
            return False
        if (len(its) == 1 and its[0].typ == DateItemToken.DateItemType.YEAR and its[0].year <= 0): 
            year.value = its[0]
            return True
        if (((len(its) > 2 and its[0].can_be_year and its[1].typ == DateItemToken.DateItemType.DELIM) and its[1].begin_token.is_hiphen and its[2].typ == DateItemToken.DateItemType.YEAR) and (its[0].year0 < its[2].year0)): 
            year.value = its[0]
            return True
        if (its[0].typ == DateItemToken.DateItemType.YEAR): 
            if ((its[0].begin_token.previous is not None and its[0].begin_token.previous.is_hiphen and (isinstance(its[0].begin_token.previous.previous, ReferentToken))) and (isinstance(its[0].begin_token.previous.previous.get_referent(), DateReferent))): 
                year.value = its[0]
                return True
        return False
    
    @staticmethod
    def __apply_date_range(ad : 'AnalyzerData', its : typing.List['DateItemToken'], lang : 'MorphLang') -> 'DateRangeReferent':
        from pullenti.ner.date.internal.DateItemToken import DateItemToken
        lang.value = MorphLang()
        if (its is None or (len(its) < 3)): 
            return None
        if ((its[0].can_be_year and its[1].string_value == "-" and its[2].typ == DateItemToken.DateItemType.YEAR) and (its[0].year < its[2].year)): 
            res = DateRangeReferent()
            res.date_from = Utils.asObjectOrNull(ad.register_referent(DateReferent._new938(its[0].year)), DateReferent)
            rt1 = ReferentToken(res.date_from, its[0].begin_token, its[0].end_token)
            res.date_to = Utils.asObjectOrNull(ad.register_referent(DateReferent._new938(its[2].year)), DateReferent)
            rt2 = ReferentToken(res.date_to, its[2].begin_token, its[2].end_token)
            lang.value = its[2].lang
            return res
        return None
    
    @staticmethod
    def __apply_date_range0(kit : 'AnalysisKit', ad : 'AnalyzerData') -> None:
        from pullenti.ner.date.internal.DateItemToken import DateItemToken
        t = kit.first_token
        first_pass2850 = True
        while True:
            if first_pass2850: first_pass2850 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.is_ignored): 
                continue
            if (not (isinstance(t, TextToken))): 
                continue
            year_val1 = 0
            year_val2 = 0
            date1 = None
            date2 = None
            lang = MorphLang()
            t0 = t.next0_
            str0_ = t.term
            if (str0_ == "ON" and (isinstance(t0, TextToken))): 
                tok = DateItemToken.DAYS_OF_WEEK.try_parse(t0, TerminParseAttr.NO)
                if (tok is not None): 
                    dow = DateReferent._new1005(tok.termin.tag)
                    rtd = ReferentToken(ad.register_referent(dow), t, tok.end_token)
                    kit.embed_token(rtd)
                    t = (rtd)
                    continue
            is_betwen = False
            if (str0_ == "С" or str0_ == "C"): 
                lang = MorphLang.RU
            elif (str0_ == "МЕЖДУ"): 
                lang = MorphLang.RU
                is_betwen = True
            elif (str0_ == "З"): 
                lang = MorphLang.UA
            elif (str0_ == "ПОМІЖ" or str0_ == "МІЖ"): 
                lang = MorphLang.UA
                is_betwen = True
            elif (str0_ == "BETWEEN"): 
                lang = MorphLang.EN
                is_betwen = True
            elif (str0_ == "IN"): 
                lang = MorphLang.EN
                if ((t0 is not None and t0.is_value("THE", None) and t0.next0_ is not None) and t0.next0_.is_value("PERIOD", None)): 
                    t0 = t0.next0_.next0_
            elif (str0_ == "ПО" or str0_ == "ДО" or str0_ == "BEFORE"): 
                if ((isinstance(t.next0_, ReferentToken)) and (isinstance(t.next0_.get_referent(), DateReferent))): 
                    dr = DateRangeReferent._new941(Utils.asObjectOrNull(t.next0_.get_referent(), DateReferent))
                    rt0 = ReferentToken(ad.register_referent(dr), t, t.next0_)
                    if (rt0.end_token.next0_ is not None and rt0.end_token.next0_.is_value("ВКЛЮЧИТЕЛЬНО", None)): 
                        rt0.end_token = rt0.end_token.next0_
                    else: 
                        dr.add_slot("@EXCLUDE", "true", True, 0)
                    kit.embed_token(rt0)
                    t = (rt0)
                    continue
            elif (((str0_ == "ПОСЛЕ" or str0_ == "AFTER")) and (isinstance(t.next0_, ReferentToken)) and (isinstance(t.next0_.get_referent(), DateReferent))): 
                dr = DateRangeReferent._new942(Utils.asObjectOrNull(t.next0_.get_referent(), DateReferent))
                rt0 = ReferentToken(ad.register_referent(dr), t, t.next0_)
                if (rt0.end_token.next0_ is not None and rt0.end_token.next0_.is_value("ВКЛЮЧИТЕЛЬНО", None)): 
                    rt0.end_token = rt0.end_token.next0_
                else: 
                    dr.add_slot("@EXCLUDE", "true", True, 0)
                kit.embed_token(rt0)
                t = (rt0)
                continue
            else: 
                continue
            if (t0 is None): 
                continue
            if (isinstance(t0, ReferentToken)): 
                date1 = (Utils.asObjectOrNull(t0.referent, DateReferent))
            if (date1 is None): 
                if ((isinstance(t0, NumberToken)) and t0.int_value is not None): 
                    v = t0.int_value
                    if ((v < 1000) or v >= 2100): 
                        continue
                    year_val1 = v
                else: 
                    continue
            else: 
                year_val1 = date1.year
            t1 = t0.next0_
            if (t1 is None): 
                continue
            if (t1.is_value("ПО", "ДО") or t1.is_value("ДО", None)): 
                lang = t1.morph.language
            elif (t1.is_value("AND", None)): 
                lang = MorphLang.EN
            elif (t1.is_hiphen and lang.equals(MorphLang.EN)): 
                pass
            elif (lang.is_ua and t1.is_value("І", None)): 
                pass
            elif (t1.is_and and is_betwen): 
                pass
            else: 
                continue
            t1 = t1.next0_
            if (t1 is None): 
                continue
            if (isinstance(t1, ReferentToken)): 
                date2 = (Utils.asObjectOrNull(t1.referent, DateReferent))
            if (date2 is None): 
                if ((isinstance(t1, NumberToken)) and t1.int_value is not None): 
                    nt1 = NumberHelper.try_parse_number_with_postfix(t1)
                    if (nt1 is not None): 
                        continue
                    v = t1.int_value
                    if (v > 0 and (v < year_val1)): 
                        yy = year_val1 % 100
                        if (yy < v): 
                            v += (((math.floor(year_val1 / 100))) * 100)
                    if ((v < 1000) or v >= 2100): 
                        continue
                    year_val2 = v
                else: 
                    continue
            else: 
                year_val2 = date2.year
            if (year_val1 > year_val2 and year_val2 > 0): 
                continue
            if (year_val1 == year_val2): 
                if (date1 is None or date2 is None): 
                    continue
                if (DateReferent.compare(date1, date2) >= 0): 
                    continue
            if (date1 is None): 
                date1 = (Utils.asObjectOrNull(ad.register_referent(DateReferent._new938(year_val1)), DateReferent))
                rt0 = ReferentToken(date1, t0, t0)
                kit.embed_token(rt0)
                if (t0 == t): 
                    t = (rt0)
            if (date2 is None): 
                date2 = (Utils.asObjectOrNull(ad.register_referent(DateReferent._new938(year_val2)), DateReferent))
                rt1 = ReferentToken(date2, t1, t1)
                kit.embed_token(rt1)
                t1 = (rt1)
            rt = ReferentToken(ad.register_referent(DateRangeReferent._new935(date1, date2)), t, t1)
            if (t.previous is not None): 
                if (t.previous.is_value("ПРОМЕЖУТОК", "ПРОМІЖОК") or t.previous.is_value("ДИАПАЗОН", "ДІАПАЗОН") or t.previous.is_value("ПЕРИОД", "ПЕРІОД")): 
                    rt.begin_token = t.previous
            kit.embed_token(rt)
            t = (rt)
    
    __m_lock = None
    
    __m_inited = None
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.date.internal.DateItemToken import DateItemToken
        from pullenti.ner.measure.MeasureAnalyzer import MeasureAnalyzer
        with DateAnalyzer.__m_lock: 
            if (DateAnalyzer.__m_inited): 
                return
            DateAnalyzer.__m_inited = True
            MeasureAnalyzer.initialize()
            MetaDate.initialize()
            MetaDateRange.initialize()
            try: 
                Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = True
                DateItemToken.initialize()
                Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = False
            except Exception as ex: 
                raise Utils.newException(ex.__str__(), ex)
            ProcessorService.register_analyzer(DateAnalyzer())
        MeasureAnalyzer.initialize()
    
    # static constructor for class DateAnalyzer
    @staticmethod
    def _static_ctor():
        DateAnalyzer.__m_lock = threading.Lock()

DateAnalyzer._static_ctor()