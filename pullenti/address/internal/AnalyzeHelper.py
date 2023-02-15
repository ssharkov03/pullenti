# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
import math
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.address.GarLevel import GarLevel
from pullenti.ner.address.AddressDetailType import AddressDetailType
from pullenti.address.SpecialType import SpecialType
from pullenti.ner.address.StreetKind import StreetKind
from pullenti.address.BaseAttributes import BaseAttributes
from pullenti.ner.Referent import Referent
from pullenti.address.internal.gar.HouseObject import HouseObject
from pullenti.address.internal.gar.AddressObject import AddressObject
from pullenti.address.SpecialAttributes import SpecialAttributes
from pullenti.ner.fias.FiasReferent import FiasReferent
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.address.RoomType import RoomType
from pullenti.ner.NumberToken import NumberToken
from pullenti.address.HouseType import HouseType
from pullenti.address.StroenType import StroenType
from pullenti.ner.fias.FiasAnalyzer import FiasAnalyzer
from pullenti.address.HouseAttributes import HouseAttributes
from pullenti.ner.Token import Token
from pullenti.ner.address.StreetReferent import StreetReferent
from pullenti.ner.TextToken import TextToken
from pullenti.ner.address.AddressReferent import AddressReferent
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.address.internal.gar.RoomObject import RoomObject
from pullenti.address.GarObject import GarObject
from pullenti.address.internal.CorrectionHelper import CorrectionHelper
from pullenti.address.RoomAttributes import RoomAttributes
from pullenti.address.AreaAttributes import AreaAttributes
from pullenti.address.TextAddress import TextAddress
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.address.TextObject import TextObject
from pullenti.address.internal.GarHelper import GarHelper
from pullenti.ner.SourceOfAnalysis import SourceOfAnalysis

class AnalyzeHelper:
    
    __m_proc0 = None
    
    __m_proc1 = None
    
    @staticmethod
    def set_default_geo(geo : str) -> None:
        for a in AnalyzeHelper.__m_proc1.analyzers: 
            if (isinstance(a, FiasAnalyzer)): 
                a.default_address_object = geo
    
    @staticmethod
    def init() -> None:
        AnalyzeHelper.__m_proc0 = ProcessorService.create_empty_processor()
        AnalyzeHelper.__m_proc1 = ProcessorService.create_specific_processor(FiasAnalyzer.ANALYZER_NAME)
        for a in AnalyzeHelper.__m_proc1.analyzers: 
            if (a.name == "GEO" or a.name == "ADDRESS" or a.name == FiasAnalyzer.ANALYZER_NAME): 
                pass
            else: 
                a.ignore_this_analyzer = True
    
    @staticmethod
    def analyze(txt : str, corr : typing.List[tuple], one_addr : bool, corr_text : str) -> typing.List['TextAddress']:
        corr_text.value = (None)
        if (Utils.isNullOrEmpty(txt)): 
            return None
        co = None
        if (corr is not None and "" in corr): 
            co = corr[""]
        if (one_addr): 
            txt = CorrectionHelper.correct(txt)
            corr_text.value = txt
        res = AnalyzeHelper.__analyze(txt, co, one_addr)
        if (res is None or len(res) != 1 or res[0].last_item is None): 
            return res
        if (len(res[0].last_item.gars) > 0): 
            return res
        txt0 = Utils.trimEndString(txt)
        if (len(txt0) > 0 and str.isdigit(txt0[len(txt0) - 1])): 
            txt0 += "-й"
            res1 = AnalyzeHelper.__analyze(txt0, co, one_addr)
            if ((res1 is not None and len(res1) == 1 and res1[0].last_item is not None) and len(res1[0].last_item.gars) > 0): 
                if (res1[0].end_char >= len(txt)): 
                    res1[0].end_char = (len(txt) - 1)
                return res1
        return res
    
    @staticmethod
    def __get_all_referents(t : 'Token', res : typing.List[tuple]) -> None:
        rt = Utils.asObjectOrNull(t, ReferentToken)
        if (rt is None): 
            return
        if ((isinstance(rt.referent, AddressReferent)) or (isinstance(rt.referent, StreetReferent)) or (isinstance(rt.referent, GeoReferent))): 
            li = [ ]
            wrapli91 = RefOutArgWrapper(None)
            inoutres92 = Utils.tryGetValue(res, rt.referent, wrapli91)
            li = wrapli91.value
            if (not inoutres92): 
                li = list()
                res[rt.referent] = li
            li.append(rt)
        tt = rt.begin_token
        while tt is not None and tt.end_char <= rt.end_char: 
            AnalyzeHelper.__get_all_referents(tt, res)
            tt = tt.next0_
    
    @staticmethod
    def __analyze(txt : str, co : typing.List[tuple], one_addr : bool) -> typing.List['TextAddress']:
        res = list()
        if (AnalyzeHelper.__m_proc1 is None): 
            return res
        ar = AnalyzeHelper.__m_proc1.process(SourceOfAnalysis._new93(txt, co, False, ("ADDRESS" if one_addr else None)), None, None)
        if (ar is None or ar.first_token is None): 
            return res
        refs = dict()
        t = ar.first_token
        while t is not None: 
            AnalyzeHelper.__get_all_referents(t, refs)
            t = t.next0_
        if (ar.first_token.kit.corrected_tokens is not None): 
            for kp in ar.first_token.kit.corrected_tokens.items(): 
                if (isinstance(kp[0], TextToken)): 
                    pass
        for e0_ in ar.entities: 
            if (e0_.get_slot_value(GeoReferent.ATTR_FIAS) is not None): 
                AnalyzeHelper.__create_gars(e0_)
        res0 = list()
        t = ar.first_token
        first_pass2718 = True
        while True:
            if first_pass2718: first_pass2718 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (isinstance(t, ReferentToken)): 
                obj = AnalyzeHelper.__create_obj(Utils.asObjectOrNull(t, ReferentToken), refs, 0)
                if (obj is None): 
                    continue
                if (not (isinstance(obj.tag, Token))): 
                    obj.tag = (t)
                o = obj
                while o is not None: 
                    if ((isinstance(o._tag2, TextObject)) and len(o.gars) > 0 and len(o._tag2.gars) > 1): 
                        go = o.gars[0]
                        par = Utils.asObjectOrNull(o._tag2, TextObject)
                        if (par._find_gar_by_id(go.parent_id) is not None): 
                            par.gars.clear()
                            for gg in o.gars: 
                                if (gg.parent_id is not None and par._find_gar_by_id(gg.parent_id) is None): 
                                    par.gars.append(GarHelper.get_object(gg.parent_id))
                    o = (Utils.asObjectOrNull(o._tag2, TextObject))
                if (len(obj.gars) > 1): 
                    if (obj.gars[0].expired and not obj.gars[1].expired): 
                        dd = obj.gars[1]
                        del obj.gars[1]
                        obj.gars.insert(0, dd)
                if (len(res0) > 0 and (isinstance(res0[len(res0) - 1].attrs, AreaAttributes)) and (isinstance(obj.attrs, AreaAttributes))): 
                    last = res0[len(res0) - 1]
                    if ((((last.attrs.level == GarLevel.STREET or last.attrs.level == GarLevel.AREA)) and ((obj.attrs.level == GarLevel.STREET or obj.attrs.level == GarLevel.AREA)) and len(obj.gars) > 0) and len(last.gars) > 0): 
                        go = obj.gars[0]
                        if (last._find_gar_by_id(go.parent_id) is not None): 
                            obj._tag2 = (last)
                            obj.tag = (t)
                            res0[len(res0) - 1] = obj
                            continue
                    if ((obj._tag2 is None and ((last.attrs.level == GarLevel.CITY or last.attrs.level == GarLevel.REGION)) and obj.attrs.level == GarLevel.CITY) and len(last.gars) > 0 and len(obj.gars) > 0): 
                        for par in obj.gars: 
                            parpar = GarHelper.get_object(par.parent_id)
                            if (last._find_gar_by_id(par.id0_) is not None or ((parpar is not None and last._find_gar_by_id(parpar.id0_) is not None))): 
                                obj._tag2 = (last)
                                del res0[len(res0) - 1]
                                obj.gars.clear()
                                obj.gars.append(par)
                                break
                spec = AnalyzeHelper.__create_specobj(Utils.asObjectOrNull(t, ReferentToken))
                if (spec is not None): 
                    spec._tag2 = (obj)
                    obj = spec
                res0.append(obj)
                obj.tag = (t)
        if (len(res0) > 1 and one_addr): 
            i = 1
            while i < len(res0): 
                a0 = res0[0]
                a1 = res0[i]
                a = Utils.asObjectOrNull(a1._tag2, TextObject)
                while a is not None: 
                    if (str(a) == str(a0)): 
                        a0._tag2 = a._tag2
                        del res0[0]
                        i -= 1
                        break
                    a = (Utils.asObjectOrNull(a._tag2, TextObject))
                i += 1
        if (one_addr and len(res0) > 1): 
            a0 = res0[0]
            a1 = res0[1]
            a = a1
            while a is not None: 
                if (a._tag2 is None): 
                    if ((a.attrs.level) >= (a0.attrs.level)): 
                        a._tag2 = (a0)
                        del res0[0]
                        break
                a = (Utils.asObjectOrNull(a._tag2, TextObject))
        for r in res0: 
            res.append(AnalyzeHelper.__create_text_address(r, one_addr, txt))
        if (len(res) > 1 and one_addr): 
            res[0].coef = math.floor(res[0].coef / len(res))
            res[0].coef_without_house = math.floor(res[0].coef_without_house / len(res))
            res[0].coef_pure_text = math.floor(res[0].coef_pure_text / len(res))
        return res
    
    @staticmethod
    def __create_text_address(tobj : 'TextObject', one : bool, txt : str) -> 'TextAddress':
        res = TextAddress()
        if (isinstance(tobj.tag, Token)): 
            res.begin_char = tobj.tag.begin_char
            res.end_char = tobj.tag.end_char
        if (one): 
            res.text = txt
        elif (res.end_char > 0 and (res.end_char < len(txt))): 
            res.text = txt[res.begin_char:res.begin_char+(res.end_char + 1) - res.begin_char]
        dcoef = 100
        dcoef1 = 100
        dcoef0 = 100
        to_with_gar = None
        to = tobj
        while to is not None: 
            par = Utils.asObjectOrNull(to._tag2, TextObject)
            if (isinstance(to.attrs, RoomAttributes)): 
                if (((par is None or par.attrs.level != GarLevel.BUILDING)) and len(to.gars) != 1): 
                    dcoef /= (2)
                    dcoef1 /= (2)
            if (isinstance(to.attrs, HouseAttributes)): 
                if (par is None or ((par.attrs.level != GarLevel.STREET and par.attrs.level != GarLevel.AREA and par.attrs.level != GarLevel.SETTLEMENT))): 
                    if (len(to.gars) != 1): 
                        dcoef /= (2)
                        dcoef1 /= (2)
            if (len(to.gars) == 0): 
                if (isinstance(to.attrs, SpecialAttributes)): 
                    pass
                elif (isinstance(to.attrs, RoomAttributes)): 
                    pass
                elif (par is not None and len(par.gars) > 0 and par.gars[0].expired): 
                    pass
                elif (((to.attrs.level == GarLevel.MUNICIPALAREA or to.attrs.level == GarLevel.ADMINAREA)) and to_with_gar == tobj): 
                    pass
                elif ((to.attrs.level) >= (GarLevel.BUILDING)): 
                    dcoef *= 0.9
                elif ((to.attrs.level) >= (GarLevel.AREA)): 
                    dcoef *= 0.8
                    dcoef1 *= 0.8
                elif (((to.attrs.level == GarLevel.LOCALITY or to.attrs.level == GarLevel.SETTLEMENT)) and par is not None and len(par.gars) == 1): 
                    dcoef *= 0.9
                    dcoef1 *= 0.9
                else: 
                    dcoef *= 0.6
                    dcoef1 *= 0.6
                res.items.append(to)
            else: 
                if (to_with_gar is None): 
                    to_with_gar = to
                res.items.append(to)
                if (len(to.gars) > 1 and not to.gars[1].expired): 
                    pars = list()
                    for g in to.gars: 
                        id0_ = g.parent_id
                        if (id0_ is not None and not id0_ in pars): 
                            pars.append(id0_)
                    co = 1 / (len(pars))
                    if (len(pars) > 1): 
                        nams = list()
                        pars2 = list()
                        for p in pars: 
                            oo = GarHelper.get_object(p)
                            if (oo is None): 
                                continue
                            if (not str(oo) in nams): 
                                nams.append(str(oo))
                            if (not Utils.ifNotNull(oo.parent_id, "") in pars2): 
                                pars2.append(Utils.ifNotNull(oo.parent_id, ""))
                        if (len(nams) == 1 and len(pars2) == 1): 
                            co = (1)
                    dcoef *= co
                    if ((to.attrs.level) <= (GarLevel.STREET)): 
                        dcoef1 *= co
            to = (Utils.asObjectOrNull(to._tag2, TextObject))
        total_char = 0
        not_char = 0
        max0_ = len(txt)
        i = 0
        if (one): 
            i = txt.find("дом,корпус,кв.")
            if (((i)) > 0): 
                max0_ = i
            i = txt.find("ТП-")
            if (((i)) > 0 and (i < max0_)): 
                max0_ = i
            i = txt.find("РП-")
            if (((i)) > 0 and (i < max0_)): 
                max0_ = i
            i = txt.find("ВЛ-")
            if (((i)) > 0 and (i < max0_)): 
                max0_ = i
            i = txt.find("КЛ-")
            if (((i)) > 0 and (i < max0_)): 
                max0_ = i
            i = txt.find("КТПН-")
            if (((i)) > 0 and (i < max0_)): 
                max0_ = i
            for i in range(max0_ - 1, 0, -1):
                if ((Utils.isWhitespace(txt[i]) or txt[i] == ',' or txt[i] == '-') or txt[i] == '.'): 
                    max0_ = i
                else: 
                    break
            else: i = 0
            i = 0
            first_pass2719 = True
            while True:
                if first_pass2719: first_pass2719 = False
                else: i += 1
                if (not (i < max0_)): break
                if (AnalyzeHelper.__starts_with(txt, i, "РФ")): 
                    i += 2
                    continue
                if (AnalyzeHelper.__starts_with(txt, i, "РОССИЯ")): 
                    i += 6
                    continue
                if (str.isalpha(txt[i])): 
                    break
            if (i < res.begin_char): 
                res.begin_char = i
            while i < max0_: 
                if (str.isalnum(txt[i])): 
                    total_char += 1
                    if ((i < res.begin_char) or i > res.end_char): 
                        not_char += 1
                i += 1
            if (total_char > 0 and not_char > 0): 
                dcoef *= (((total_char - not_char)) / (total_char))
                dcoef1 *= (((total_char - not_char)) / (total_char))
                dcoef0 *= (((total_char - not_char)) / (total_char))
            if (((res.end_char + 1) < max0_) and res.error_message is None): 
                res.error_message = "Непонятный фрагмент: '{0}'".format(txt[res.end_char + 1:res.end_char + 1+max0_ - res.end_char - 1].strip())
        res.coef = (math.floor(dcoef))
        res.coef_without_house = (math.floor(dcoef1))
        res.coef_pure_text = (math.floor(dcoef0))
        if (to_with_gar is not None): 
            g = to_with_gar.gars[0]
            while g is not None: 
                if (res.find_item(g.attrs.level) is None and (isinstance(g.attrs, AreaAttributes))): 
                    it = TextObject(g.attrs)
                    it.gars.append(g)
                    res.items.append(it)
                g = GarHelper.get_object(g.parent_id)
        k = 0
        while k < len(res.items): 
            i = 0
            while i < (len(res.items) - 1): 
                if ((res.items[i].attrs.level) > (res.items[i + 1].attrs.level)): 
                    it = res.items[i]
                    res.items[i] = res.items[i + 1]
                    res.items[i + 1] = it
                i += 1
            k += 1
        return res
    
    @staticmethod
    def __starts_with(txt : str, i : int, sub : str) -> bool:
        j = 0
        while j < len(sub): 
            if ((i + j) >= len(txt)): 
                return False
            if (str.upper(txt[i + j]) != str.upper(sub[j])): 
                return False
            j += 1
        return True
    
    @staticmethod
    def __create_specobj(t : 'ReferentToken') -> 'TextObject':
        addr = Utils.asObjectOrNull(t.referent, AddressReferent)
        if (addr is None): 
            return None
        dt = addr.detail
        ty = SpecialType.UNDEFINED
        if (dt == AddressDetailType.NEAR): 
            ty = SpecialType.NEAR
        elif (dt == AddressDetailType.EAST): 
            ty = SpecialType.EAST
        elif (dt == AddressDetailType.NORTH): 
            ty = SpecialType.NORTH
        elif (dt == AddressDetailType.NORTHEAST): 
            ty = SpecialType.NORTHEAST
        elif (dt == AddressDetailType.NORTHWEST): 
            ty = SpecialType.NORTHWEST
        elif (dt == AddressDetailType.SOUTH): 
            ty = SpecialType.SOUTH
        elif (dt == AddressDetailType.SOUTHEAST): 
            ty = SpecialType.SOUTHEAST
        elif (dt == AddressDetailType.SOUTHWEST): 
            ty = SpecialType.SOUTHWEST
        elif (dt == AddressDetailType.WEST): 
            ty = SpecialType.WEST
        if (ty == SpecialType.UNDEFINED): 
            return None
        sa = SpecialAttributes()
        sa.typ = ty
        sa.param = addr.get_string_value(AddressReferent.ATTR_DETAILPARAM)
        return TextObject(sa)
    
    @staticmethod
    def __create_obj(t : 'ReferentToken', refs : typing.List[tuple], lev : int) -> 'TextObject':
        if (lev > 10): 
            return None
        res = None
        own = None
        house_is_empty = True
        sown = None
        if (isinstance(t.referent, GeoReferent)): 
            geo = Utils.asObjectOrNull(t.referent, GeoReferent)
            if (geo.is_state and geo.alpha2 == "RU"): 
                return None
            aa = AreaAttributes()
            res = TextObject(aa)
            typs = t.referent.get_string_values(GeoReferent.ATTR_TYPE)
            if (len(typs) > 0): 
                aa.types.extend(typs)
            AnalyzeHelper.__set_name(aa, t.referent, GeoReferent.ATTR_NAME)
            res.tag = (t.referent)
            own = geo.higher
            if (geo.is_state): 
                aa.level = GarLevel.COUNTRY
            elif (geo.is_city): 
                aa.level = GarLevel.LOCALITY
                for ty in typs: 
                    if (ty == "город"): 
                        aa.level = GarLevel.CITY
                        break
                    elif (ty == "городское поселение" or ty == "сельское поселение"): 
                        aa.level = GarLevel.SETTLEMENT
                        break
            elif (geo.is_region): 
                for ty in typs: 
                    if ((ty == "городской округ" or ty == "муниципальный район" or ty == "муниципальный округ") or ty == "федеральная территория"): 
                        aa.level = GarLevel.MUNICIPALAREA
                        break
                    elif (ty == "район" or ty == "автономный округ"): 
                        aa.level = GarLevel.ADMINAREA
                        break
                    elif (ty == "область" or ty == "край"): 
                        aa.level = GarLevel.REGION
                        break
                    elif (ty == "сельский округ"): 
                        aa.level = GarLevel.SETTLEMENT
                        break
        elif (isinstance(t.referent, StreetReferent)): 
            aa = AreaAttributes()
            res = TextObject(aa)
            aa.types.extend(t.referent.typs)
            AnalyzeHelper.__set_name(aa, t.referent, StreetReferent.ATTR_NAME)
            aa.number = t.referent.get_string_value(StreetReferent.ATTR_NUMBER)
            if (aa.number is not None): 
                str0_ = t.referent.get_string_value(StreetReferent.ATTR_SECNUMBER)
                if (str0_ is not None): 
                    n1 = 0
                    n2 = 0
                    wrapn194 = RefOutArgWrapper(0)
                    inoutres95 = Utils.tryParseInt(aa.number, wrapn194)
                    wrapn296 = RefOutArgWrapper(0)
                    inoutres97 = Utils.tryParseInt(str0_, wrapn296)
                    n1 = wrapn194.value
                    n2 = wrapn296.value
                    if (inoutres95 and inoutres97): 
                        if (n1 > n2): 
                            aa.number = "{0} {1}".format(n2, n1)
                        else: 
                            aa.number = "{0} {1}".format(n1, n2)
                    elif (Utils.compareStrings(aa.number, str0_, False) > 0): 
                        aa.number = "{0} {1}".format(str0_, aa.number)
                    else: 
                        aa.number = "{0} {1}".format(aa.number, str0_)
            res.tag = (t.referent)
            own = (Utils.asObjectOrNull(t.referent.get_slot_value(StreetReferent.ATTR_GEO), GeoReferent))
            sown = t.referent.higher
            aa.level = GarLevel.STREET
            ki = t.referent.kind
            if (ki == StreetKind.AREA or ki == StreetKind.ORG): 
                aa.level = GarLevel.AREA
        elif (isinstance(t.referent, AddressReferent)): 
            ar = Utils.asObjectOrNull(t.referent, AddressReferent)
            ha = HouseAttributes()
            ha.level = GarLevel.BUILDING
            res = TextObject(ha)
            if (ar.house is not None and ar.house != "0"): 
                ha.number = ar.house
                house_is_empty = False
                ha.typ = (Utils.valToEnum(ar.house_type, HouseType))
            if (ar.house_or_plot is not None and ar.house_or_plot != "0"): 
                ha.number = ar.house_or_plot
                house_is_empty = False
                ha.typ = HouseType.UNDEFINED
            if (ar.building is not None and ar.building != "0"): 
                ha.stroen_number = ar.building
                house_is_empty = False
                ha.stroen_typ = (Utils.valToEnum(ar.building_type, StroenType))
            if (ar.corpus is not None and ar.corpus != "0"): 
                ha.build_number = ar.corpus
                house_is_empty = False
            if (ar.plot is not None and ar.plot != "0"): 
                ha.number = ar.plot
                ha.typ = HouseType.PLOT
                house_is_empty = False
                ha.level = GarLevel.PLOT
        if (res is None): 
            return None
        gobjs = Utils.asObjectOrNull(t.referent.tag, list)
        if (gobjs is not None and len(gobjs) > 0): 
            res.gars.extend(gobjs)
            if (gobjs[0].attrs.level == GarLevel.REGION or res.attrs.level == GarLevel.UNDEFINED): 
                res.attrs.level = gobjs[0].attrs.level
            if (((isinstance(res.attrs, HouseAttributes)) and res.attrs.typ == HouseType.UNDEFINED and len(res.gars) == 1) and (isinstance(gobjs[0].attrs, HouseAttributes))): 
                res.attrs.typ = gobjs[0].attrs.typ
            aa = Utils.asObjectOrNull(res.attrs, AreaAttributes)
            if ((aa is not None and len(aa.types) > 0 and aa.types[0] == "населенный пункт") and (isinstance(gobjs[0].attrs, AreaAttributes))): 
                aa.types[0] = gobjs[0].attrs.types[0]
        pars = None
        has_own = False
        tt = t.begin_token
        first_pass2720 = True
        while True:
            if first_pass2720: first_pass2720 = False
            else: tt = tt.next0_
            if (not (tt is not None and tt.end_char <= t.end_char)): break
            if (isinstance(tt, ReferentToken)): 
                if (tt.get_referent() == t.referent): 
                    continue
                hi = AnalyzeHelper.__create_obj(Utils.asObjectOrNull(tt, ReferentToken), refs, lev + 1)
                if (hi is not None): 
                    if (pars is None): 
                        pars = list()
                    pars.append(hi)
                    if (hi.tag == own or hi.tag == sown): 
                        has_own = True
        for k in range(2):
            if (has_own): 
                break
            rr = own
            if (k > 0): 
                rr = (sown)
            if (rr is None): 
                continue
            li = [ ]
            wrapli98 = RefOutArgWrapper(None)
            inoutres99 = Utils.tryGetValue(refs, rr, wrapli98)
            li = wrapli98.value
            if (not inoutres99): 
                continue
            rt = None
            for oc in li: 
                if (oc.begin_char >= t.begin_char and oc.end_char <= t.end_char): 
                    rt = oc
                    break
            if (rt is None): 
                for oc in li: 
                    if (oc.end_char <= t.end_char): 
                        rt = oc
                        break
            if (rt is None): 
                rt = li[0]
            hi = AnalyzeHelper.__create_obj(rt, refs, lev + 1)
            if (hi is not None): 
                if (pars is None): 
                    pars = list()
                pars.insert(0, hi)
                has_own = True
            break
        if (pars is not None): 
            while len(pars) > 1:
                ch = False
                i = 0
                first_pass2721 = True
                while True:
                    if first_pass2721: first_pass2721 = False
                    else: i += 1
                    if (not (i < (len(pars) - 1))): break
                    r1 = Utils.asObjectOrNull(pars[i].tag, Referent)
                    r2 = Utils.asObjectOrNull(pars[i + 1].tag, Referent)
                    if (r1 is None or r2 is None): 
                        continue
                    ok = False
                    if ((isinstance(r2, GeoReferent)) and r2.higher == r1 and pars[i + 1]._tag2 is None): 
                        ok = True
                    elif ((isinstance(r2, StreetReferent)) and r2.find_slot(StreetReferent.ATTR_GEO, r1, True) is not None): 
                        ok = True
                    if (ok): 
                        pars[i + 1]._tag2 = (pars[i])
                        del pars[i]
                        ch = True
                        break
                    if ((isinstance(r1, GeoReferent)) and r1.higher == r2 and pars[i]._tag2 is None): 
                        ok = True
                    elif ((isinstance(r1, StreetReferent)) and r1.find_slot(StreetReferent.ATTR_GEO, r2, True) is not None): 
                        ok = True
                    if (ok): 
                        pars[i]._tag2 = (pars[i + 1])
                        del pars[i + 1]
                        ch = True
                        break
                    top_par2 = None
                    top_par2 = pars[i + 1]
                    while isinstance(top_par2._tag2, TextObject): 
                        pass
                        top_par2 = (Utils.asObjectOrNull(top_par2._tag2, TextObject))
                    if (len(top_par2.gars) > 0): 
                        for gg in top_par2.gars: 
                            pp = gg
                            while pp is not None: 
                                if (pars[i]._find_gar_by_id(pp.id0_) is not None): 
                                    ok = True
                                    if (len(top_par2.gars) > 1): 
                                        top_par2.gars.clear()
                                        top_par2.gars.append(gg)
                                    break
                                pp = GarHelper.get_object(pp.parent_id)
                            if (ok): 
                                break
                    if (ok): 
                        if (top_par2.gars[0].id0_ == pars[i].gars[0].id0_): 
                            pass
                        else: 
                            top_par2._tag2 = (pars[i])
                        del pars[i]
                        ch = True
                        break
                if (not ch): 
                    break
            if (len(pars) >= 1): 
                res._tag2 = (pars[0])
        if (((isinstance(t.referent, StreetReferent)) and (isinstance(res.attrs, AreaAttributes)) and gobjs is not None) and len(gobjs) > 0 and t.referent.number is not None): 
            ok = True
            if (t.referent.number in gobjs[0].attrs.names[0]): 
                ok = False
            else: 
                ar = ProcessorService.get_empty_processor().process(SourceOfAnalysis(gobjs[0].attrs.names[0]), None, None)
                tt = ar.first_token
                while tt is not None: 
                    if (isinstance(tt, NumberToken)): 
                        ok = False
                    tt = tt.next0_
            if (ok): 
                a1 = AddressReferent()
                a1.house_or_plot = t.referent.number
                aid = 0
                wrapaid100 = RefOutArgWrapper(0)
                inoutres101 = Utils.tryParseInt(res.gars[0].id0_[1:], wrapaid100)
                aid = wrapaid100.value
                if (inoutres101): 
                    hos = FiasAnalyzer.FIAS_DB.find_houses(aid, a1)
                    if (hos is not None and len(hos) == 1): 
                        hgar = GarHelper.create_gar_house(hos[0])
                        res.attrs.number = (None)
                        ha = HouseAttributes()
                        ha.level = GarLevel.BUILDING
                        thou = TextObject(ha)
                        ha.number = a1.house_or_plot
                        ha.typ = hgar.attrs.typ
                        thou._tag2 = (res)
                        thou.gars.append(hgar)
                        res = thou
                        house_is_empty = False
        if (isinstance(t.referent, AddressReferent)): 
            ar = Utils.asObjectOrNull(t.referent, AddressReferent)
            if ((ar.flat is not None or ar.office is not None or ar.box is not None) or ar.pavilion is not None or ar.corpus_or_flat is not None): 
                ra = RoomAttributes()
                ra.level = GarLevel.ROOM
                robj = TextObject(ra)
                if (ar.flat is not None): 
                    ra.number = ar.flat
                    ra.typ = RoomType.FLAT
                elif (ar.office is not None): 
                    ra.number = ar.office
                    ra.typ = RoomType.OFFICE
                elif (ar.box is not None): 
                    ra.number = ar.box
                    ra.typ = RoomType.SPACE
                elif (ar.pavilion is not None): 
                    ra.number = ar.pavilion
                    ra.typ = RoomType.PAVILION
                elif (ar.corpus_or_flat is not None): 
                    ra.number = ar.corpus_or_flat
                    ra.typ = RoomType.FLAT
                robj._tag2 = (res)
                if (len(res.gars) > 0): 
                    ii = 0
                    while ii < len(res.gars): 
                        if (res.gars[ii].attrs.level == GarLevel.ROOM): 
                            gg = res.gars[ii]
                            robj.gars.append(gg)
                            del res.gars[ii]
                            par = GarHelper.get_object(gg.parent_id)
                            if (par is not None and res._find_gar_by_id(par.id0_) is None): 
                                res.gars.append(par)
                            ii -= 1
                        ii += 1
                res = robj
                house_is_empty = False
            elif ((len(res.gars) == 0 and (isinstance(res.attrs, HouseAttributes)) and (Utils.ifNotNull(res.attrs.number, "")).find('/') > 0) and (isinstance(res._tag2, TextObject)) and ((len(res._tag2.gars) == 1 and (isinstance(res._tag2.gars[0].attrs, AreaAttributes)) and res.attrs.typ == HouseType.UNDEFINED))): 
                num = res.attrs.number
                ii = num.find('/')
                a1 = AddressReferent()
                a1.house = num[0:0+ii]
                a1.flat = num[ii + 1:]
                aid = 0
                wrapaid102 = RefOutArgWrapper(0)
                inoutres103 = Utils.tryParseInt(res._tag2.gars[0].id0_[1:], wrapaid102)
                aid = wrapaid102.value
                if (inoutres103): 
                    hos = FiasAnalyzer.FIAS_DB.find_houses(aid, a1)
                    if (hos is not None and len(hos) == 1): 
                        hgar = GarHelper.create_gar_house(hos[0])
                        res.gars.append(hgar)
                        res.attrs.number = a1.house
                        ra = RoomAttributes()
                        ra.level = GarLevel.ROOM
                        ra.number = a1.flat
                        ra.typ = RoomType.ROOM
                        troom = TextObject(ra)
                        troom._tag2 = (res)
                        res = troom
                        ro = FiasAnalyzer.FIAS_DB.find_room(hos[0].id0_, a1)
                        if (ro is not None): 
                            rgar = GarHelper.create_gar_room(ro)
                            res.gars.append(rgar)
        if (res is None): 
            return None
        if ((isinstance(res.attrs, AreaAttributes)) and res.attrs.level == GarLevel.UNDEFINED and res._tag2 is not None): 
            res.attrs.level = GarLevel.ADMINAREA
        if (((isinstance(res.attrs, AreaAttributes)) and res.attrs.level == GarLevel.STREET and res._tag2 is not None) and res._tag2.attrs.level == GarLevel.ADMINAREA and "район" in res._tag2.attrs.types): 
            res._tag2.attrs.level = GarLevel.AREA
        if ((isinstance(res.attrs, HouseAttributes)) and house_is_empty): 
            return Utils.asObjectOrNull(res._tag2, TextObject)
        return res
    
    @staticmethod
    def __set_name(a : 'AreaAttributes', r : 'Referent', typ : str) -> None:
        names = r.get_string_values(typ)
        if (names is None or len(names) == 0): 
            return
        long_name = None
        i = 0
        while i < len(names): 
            nam = names[i]
            names[i] = MiscHelper.convert_first_char_upper_and_other_lower(nam)
            if (long_name is None): 
                long_name = names[i]
            elif (len(long_name) > len(names[i])): 
                long_name = names[i]
            i += 1
        if (len(names) > 1 and names[0] != long_name): 
            names.remove(long_name)
            names.insert(0, long_name)
        a.names = names
    
    @staticmethod
    def __create_gars(r : 'Referent') -> None:
        fias = list()
        gg = list()
        for s in r.slots: 
            if (s.type_name == GeoReferent.ATTR_FIAS): 
                fias.append(Utils.asObjectOrNull(s.value, FiasReferent))
        for f in fias: 
            if (not (isinstance(f.tag, GarObject))): 
                if (isinstance(f.fias_obj, AddressObject)): 
                    f.tag = (GarHelper.create_gar_area(Utils.asObjectOrNull(f.fias_obj, AddressObject)))
                elif (isinstance(f.fias_obj, HouseObject)): 
                    f.tag = (GarHelper.create_gar_house(Utils.asObjectOrNull(f.fias_obj, HouseObject)))
                elif (isinstance(f.fias_obj, RoomObject)): 
                    f.tag = (GarHelper.create_gar_room(Utils.asObjectOrNull(f.fias_obj, RoomObject)))
            if (isinstance(f.tag, GarObject)): 
                gg.append(Utils.asObjectOrNull(f.tag, GarObject))
        if (len(gg) > 0): 
            r.tag = (gg)
            if (len(gg) > 1): 
                if (gg[0].expired and not gg[1].expired): 
                    dd = gg[1]
                    del gg[1]
                    gg.insert(0, dd)