# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.address.internal.FiasHelper import FiasHelper
from pullenti.address.internal.SearchLevel import SearchLevel
from pullenti.address.internal.gar.AddrTyp import AddrTyp
from pullenti.address.internal.gar.AddressObject import AddressObject
from pullenti.address.internal.GarHelper import GarHelper
from pullenti.address.GarParam import GarParam
from pullenti.address.SearchResult import SearchResult
from pullenti.address.internal.gar.ParamType import ParamType
from pullenti.address.internal.SearchAddressItem import SearchAddressItem
from pullenti.ner.fias.FiasAnalyzer import FiasAnalyzer
from pullenti.address.internal.AddrSearchFormal import AddrSearchFormal

class AddressSearchHelper:
    
    @staticmethod
    def search(sp : 'SearchParams') -> 'SearchResult':
        res = SearchResult._new77(sp)
        if (sp.param_typ != GarParam.UNDEFINED and not Utils.isNullOrEmpty(sp.param_value)): 
            if (FiasAnalyzer.FIAS_DB is None): 
                return None
            ids = FiasAnalyzer.FIAS_DB.find_by_param(Utils.valToEnum(sp.param_typ, ParamType), sp.param_value)
            if (ids is None): 
                return res
            res.total_count = len(ids)
            i = 0
            first_pass2716 = True
            while True:
                if first_pass2716: first_pass2716 = False
                else: i += 1
                if (not (i < len(ids))): break
                if (len(res.objects) >= sp.max_count): 
                    break
                id0_ = ids[i]
                if ((((id0_) & 0x80000000)) == 0): 
                    aa = GarHelper.create_gar_aby_id(id0_)
                    if (aa is not None): 
                        res.objects.append(aa)
                    continue
                if ((((id0_) & 0x40000000)) == 0): 
                    ho = FiasAnalyzer.FIAS_DB.get_house(((id0_) & 0x3FFFFFFF))
                    gh = GarHelper.create_gar_house(ho)
                    if (gh is not None): 
                        res.objects.append(gh)
                else: 
                    ro = FiasAnalyzer.FIAS_DB.get_room(((id0_) & 0x3FFFFFFF))
                    rh = GarHelper.create_gar_room(ro)
                    if (rh is not None): 
                        res.objects.append(rh)
            return res
        ain = list()
        if (sp.region > 0): 
            ain.append(SearchAddressItem._new78(SearchLevel.REGION, str(sp.region)))
        if (not Utils.isNullOrEmpty(sp.area)): 
            ain.append(SearchAddressItem._new79(SearchLevel.AREA, FiasHelper.corr_name(sp.area)))
        if (not Utils.isNullOrEmpty(sp.city)): 
            ain.append(SearchAddressItem._new79(SearchLevel.CITY, FiasHelper.corr_name(sp.city)))
        if (not Utils.isNullOrEmpty(sp.street)): 
            ain.append(SearchAddressItem._new79(SearchLevel.STREET, FiasHelper.corr_name(sp.street)))
        if (len(ain) > 0): 
            ain[len(ain) - 1].search = True
        total = 0
        wraptotal82 = RefOutArgWrapper(0)
        sain = AddressSearchHelper.process(ain, sp.max_count, wraptotal82)
        total = wraptotal82.value
        res.total_count = total
        if (sain is not None): 
            for a in sain: 
                if (isinstance(a.tag, AddressObject)): 
                    ga = GarHelper.create_gar_area(Utils.asObjectOrNull(a.tag, AddressObject))
                    if (ga is not None): 
                        res.objects.append(ga)
        return res
    
    M_ONTO_REGS = None
    
    @staticmethod
    def process(ain : typing.List['SearchAddressItem'], max_count : int, total : int) -> typing.List['SearchAddressItem']:
        total.value = 0
        mai = None
        reg_id = None
        for a in ain: 
            if (a.search): 
                mai = AddrSearchFormal(a)
                nn = 0
                wrapnn83 = RefOutArgWrapper(0)
                inoutres84 = Utils.tryParseInt(Utils.ifNotNull(reg_id, ""), wrapnn83)
                nn = wrapnn83.value
                if (inoutres84): 
                    mai.reg_id = nn
                break
            elif (a.level == SearchLevel.REGION): 
                reg_id = a.id0_
        if (mai is None): 
            return None
        if (FiasAnalyzer.FIAS_DB is None): 
            return None
        if (Utils.isNullOrEmpty(mai.src.text) and mai.src.level != SearchLevel.REGION and len(ain) > 1): 
            ain0 = list()
            ai_max = None
            for a in ain: 
                if (((a.level) < (mai.src.level)) and not Utils.isNullOrEmpty(a.text)): 
                    aa = SearchAddressItem._new79(a.level, a.text)
                    ain0.append(aa)
                    if (ai_max is None): 
                        ai_max = aa
                    elif ((aa.level) > (ai_max.level)): 
                        ai_max = aa
            if (ai_max is None): 
                return None
            ai_max.search = True
            res0 = AddressSearchHelper.process(ain0, max_count, total)
            if (res0 is None or len(res0) != 1 or res0[0].level == SearchLevel.REGION): 
                return None
            total.value = 0
            ao = Utils.asObjectOrNull(res0[0].tag, AddressObject)
            if (ao is None): 
                return None
            all0 = FiasAnalyzer.FIAS_DB.get_all_children(ao.id0_)
            res00 = list()
            ggg0 = dict()
            for ai in all0: 
                if (len(res00) >= max_count): 
                    total.value = len(all0)
                    break
                ao0 = FiasAnalyzer.FIAS_DB.getao(ai.id0_)
                if (ao0 is None): 
                    continue
                if (ao0.id0_ in ggg0): 
                    continue
                ai0 = SearchAddressItem._new86(str(ao0.id0_), ao0, mai.src.level, res0[0], "{0} {1}".format(ao0.names[0], ao0.typ.name))
                res00.append(ai0)
                total.value = len(res0)
                ggg0[ao0.id0_] = True
            return res00
        res = list()
        all0_ = mai.search()
        if (len(all0_) == 0): 
            return res
        for a in ain: 
            if (not a.search and ((a.level) < (mai.src.level))): 
                par = AddrSearchFormal(a)
                pars = par.search()
                if (len(pars) == 0): 
                    continue
                for i in range(len(all0_) - 1, -1, -1):
                    has_par = False
                    for p in pars: 
                        if (all0_[i].parents_id is not None and p.id0_ in all0_[i].parents_id): 
                            has_par = True
                            break
                    if (not has_par): 
                        del all0_[i]
        ggg = dict()
        for k in range(2):
            for a in all0_: 
                if (len(res) >= max_count): 
                    total.value = len(all0_)
                    break
                ao = FiasAnalyzer.FIAS_DB.getao(a.id0_)
                if (ao is None): 
                    continue
                if (ao.id0_ in ggg): 
                    continue
                if (not mai.check(ao, k > 0)): 
                    continue
                ai = SearchAddressItem._new87(str(ao.id0_), ao, mai.src.level, "{0} {1}".format(ao.names[0], ao.typ.name))
                res.append(ai)
                total.value = len(res)
                ggg[ao.id0_] = True
                for pid in a.parents_id: 
                    pao = FiasAnalyzer.FIAS_DB.getao(pid)
                    if (pao is None): 
                        continue
                    lev = (ai.level) - 1
                    if (pid == a.parents_id[len(a.parents_id) - 1]): 
                        if (pao.typ.typ == AddrTyp.Typs.CITY and str(pao.id0_) in AddressSearchHelper.M_ONTO_REGS): 
                            pass
                        else: 
                            lev = 1
                    if (ai.level == SearchLevel.STREET): 
                        if (pao.typ.typ != AddrTyp.Typs.VILLAGE and pao.typ.typ != AddrTyp.Typs.CITY and pao.typ.typ != AddrTyp.Typs.ORG): 
                            continue
                    elif (ai.level == SearchLevel.CITY): 
                        if (pao.typ.typ != AddrTyp.Typs.REGION and pao.typ.typ != AddrTyp.Typs.CITY and lev != 1): 
                            continue
                    elif (ai.level == SearchLevel.AREA): 
                        if (pid != a.parents_id[len(a.parents_id) - 1]): 
                            continue
                    pai = SearchAddressItem._new87(str(pao.id0_), pao, Utils.valToEnum(lev, SearchLevel), "{0} {1}".format(pao.names[0], pao.typ.name))
                    ai.parent = pai
                    ai = pai
                if (ai.id0_ in AddressSearchHelper.M_ONTO_REGS): 
                    reg = AddressSearchHelper.M_ONTO_REGS[ai.id0_]
                    if (ai.level != SearchLevel.REGION): 
                        pai = SearchAddressItem._new89(Utils.ifNotNull(reg.id0_, reg.text), SearchLevel.REGION, reg.text)
                        ai.parent = pai
                    else: 
                        ai.text = reg.text
                        ai.id0_ = (Utils.ifNotNull(reg.id0_, reg.text))
            if (len(res) > 0): 
                break
        for r in res: 
            if ((r.level == SearchLevel.STREET and r.parent is not None and r.parent.level == SearchLevel.REGION) and r.parent.parent is None and r.parent.tag.typ.typ == AddrTyp.Typs.CITY): 
                r.parent.level = SearchLevel.CITY
        i = 0
        while i < (len(res) - 1): 
            j = 0
            while j < (len(res) - 1): 
                if (res[j].compareTo(res[j + 1]) > 0): 
                    r = res[j]
                    res[j] = res[j + 1]
                    res[j + 1] = r
                j += 1
            i += 1
        return res
    
    # static constructor for class AddressSearchHelper
    @staticmethod
    def _static_ctor():
        AddressSearchHelper.M_ONTO_REGS = dict()

AddressSearchHelper._static_ctor()