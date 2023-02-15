# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
import pathlib
import threading
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.Analyzer import Analyzer
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.Referent import Referent
from pullenti.ner.TextToken import TextToken
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.address.internal.gar.HouseObject import HouseObject
from pullenti.ner.SourceOfAnalysis import SourceOfAnalysis
from pullenti.ner.fias.FiasReferent import FiasReferent
from pullenti.ner.address.StreetReferent import StreetReferent
from pullenti.ner.fias.internal.MetaFias import MetaFias
from pullenti.ner.core.internal.PullentiNerCoreInternalResourceHelper import PullentiNerCoreInternalResourceHelper
from pullenti.address.internal.gar.FiasDatabase import FiasDatabase
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.address.internal.gar.AddrTyp import AddrTyp
from pullenti.ner.address.AddressReferent import AddressReferent
from pullenti.address.internal.gar.AddressObject import AddressObject
from pullenti.ner.core.AnalyzerData import AnalyzerData

class FiasAnalyzer(Analyzer):
    """ Привязка географических объектов к классификатору ГАР ФИАС """
    
    class FiasAnalyzerData(AnalyzerData):
        
        def __init__(self) -> None:
            super().__init__()
            self.__m_hash = dict()
            self.__m_hash2 = dict()
            self.__m_hash_bti = dict()
            self.__m_hash2bti = dict()
        
        def register_referent(self, referent : 'Referent') -> 'Referent':
            from pullenti.address.internal.gar.AddressObject import AddressObject
            from pullenti.ner.fias.FiasReferent import FiasReferent
            fr = Utils.asObjectOrNull(referent, FiasReferent)
            if (fr is None): 
                return None
            if (fr.unom > 0): 
                rr = None
                wraprr1036 = RefOutArgWrapper(None)
                inoutres1037 = Utils.tryGetValue(self.__m_hash_bti, fr.unom, wraprr1036)
                rr = wraprr1036.value
                if (inoutres1037): 
                    rr.merge_slots(referent, True)
                    return rr
                referent = super().register_referent(referent)
                self.__m_hash_bti[fr.unom] = referent
                if (isinstance(referent.tag, AddressObject)): 
                    id0_ = referent.tag.id0_
                    if (not id0_ in self.__m_hash2bti): 
                        self.__m_hash2bti[id0_] = fr
                    referent.add_slot("@INT_ID", str(id0_), True, 0)
                return referent
            else: 
                referent = super().register_referent(referent)
                if (isinstance(referent.tag, AddressObject)): 
                    id0_ = referent.tag.id0_
                    if (not id0_ in self.__m_hash2): 
                        self.__m_hash2[id0_] = fr
                    referent.add_slot("@INT_ID", str(id0_), True, 0)
                return referent
        
        def remove_referent(self, r : 'Referent') -> None:
            from pullenti.ner.fias.FiasReferent import FiasReferent
            fr = Utils.asObjectOrNull(r, FiasReferent)
            if (fr is None): 
                return
            if (fr.unom > 0): 
                if (fr.unom in self.__m_hash_bti): 
                    del self.__m_hash_bti[fr.unom]
            else: 
                pass
            super().remove_referent(r)
        
        def find_by_id(self, id0_ : int, bti : bool) -> 'FiasReferent':
            r = None
            if (bti): 
                wrapr1038 = RefOutArgWrapper(None)
                inoutres1039 = Utils.tryGetValue(self.__m_hash2bti, id0_, wrapr1038)
                r = wrapr1038.value
                if (inoutres1039): 
                    return r
                else: 
                    return None
            else: 
                wrapr1040 = RefOutArgWrapper(None)
                inoutres1041 = Utils.tryGetValue(self.__m_hash2, id0_, wrapr1040)
                r = wrapr1040.value
                if (inoutres1041): 
                    return r
                else: 
                    return None
    
    def __init__(self) -> None:
        super().__init__()
        self.__m_default_address_object = None;
        self.__m_def_path = None
    
    ANALYZER_NAME = "FIAS"
    
    @property
    def name(self) -> str:
        return FiasAnalyzer.ANALYZER_NAME
    
    @property
    def caption(self) -> str:
        return "Привязка к ГАР ФИАС"
    
    @property
    def description(self) -> str:
        return "Привязка к адресным объектам ГАР ФИАС"
    
    def clone(self) -> 'Analyzer':
        return FiasAnalyzer()
    
    @property
    def progress_weight(self) -> int:
        return 1
    
    @property
    def is_specific(self) -> bool:
        return True
    
    @property
    def type_system(self) -> typing.List['ReferentClass']:
        return [MetaFias._global_meta]
    
    @property
    def images(self) -> typing.List[tuple]:
        res = dict()
        res[MetaFias.OBJ_IMAGE_ID] = PullentiNerCoreInternalResourceHelper.get_bytes("fiasobj.png")
        res[MetaFias.HOUSE_IMAGE_ID] = PullentiNerCoreInternalResourceHelper.get_bytes("fiashouse.png")
        res[MetaFias.STREET_IMAGE_ID] = PullentiNerCoreInternalResourceHelper.get_bytes("fiasstreet.png")
        res[MetaFias.ROOM_IMAGE_ID] = PullentiNerCoreInternalResourceHelper.get_bytes("fiasroom.png")
        return res
    
    def create_referent(self, type0_ : str) -> 'Referent':
        if (type0_ == FiasReferent.OBJ_TYPENAME): 
            return FiasReferent()
        return None
    
    def create_analyzer_data(self) -> 'AnalyzerData':
        return FiasAnalyzer.FiasAnalyzerData()
    
    @property
    def default_address_object(self) -> str:
        """ Объект по умолчанию (когда задана, например, только улица) """
        return self.__m_default_address_object
    @default_address_object.setter
    def default_address_object(self, value) -> str:
        self.__m_default_address_object = value
        self.__m_def_path = (None)
        if (Utils.isNullOrEmpty(value)): 
            return value
        if (FiasAnalyzer.FIAS_DB is None): 
            return value
        with ProcessorService.create_specific_processor(FiasAnalyzer.ANALYZER_NAME) as proc: 
            ar = proc.process(SourceOfAnalysis(value), None, None)
            if (ar is not None): 
                if (isinstance(ar.first_token, ReferentToken)): 
                    fo = Utils.asObjectOrNull(ar.first_token.get_referent().get_slot_value(GeoReferent.ATTR_FIAS), FiasReferent)
                    if (fo is not None): 
                        while fo is not None: 
                            id0_ = 0
                            wrapid1042 = RefOutArgWrapper(0)
                            inoutres1043 = Utils.tryParseInt(Utils.ifNotNull(fo.get_string_value("@INT_ID"), ""), wrapid1042)
                            id0_ = wrapid1042.value
                            if (inoutres1043): 
                                ao = FiasAnalyzer.FIAS_DB.getao(id0_)
                                if (ao is not None): 
                                    if (self.__m_def_path is None): 
                                        self.__m_def_path = list()
                                    self.__m_def_path.append(ao)
                            fo = (Utils.asObjectOrNull(fo.parent_referent, FiasReferent))
        return value
    
    def process(self, kit : 'AnalysisKit') -> None:
        if (FiasAnalyzer.FIAS_DB is None and FiasAnalyzer.BTI_DB is None): 
            return
        ad = Utils.asObjectOrNull(kit.get_analyzer_data(self), FiasAnalyzer.FiasAnalyzerData)
        for k in range(2):
            a = kit.processor.find_analyzer(("GEO" if k == 0 else "ADDRESS"))
            if (a is None): 
                continue
            ad0 = kit.get_analyzer_data(a)
            if (ad0 is None): 
                continue
            for r in ad0.referents: 
                if (FiasAnalyzer.FIAS_DB is not None): 
                    self.__process(r, ad, FiasAnalyzer.FIAS_DB, AddressReferent.ATTR_FIAS, 0)
                    if ((isinstance(r, StreetReferent)) and r.find_slot(AddressReferent.ATTR_FIAS, None, True) is None and r.number is not None): 
                        str0_ = Utils.asObjectOrNull(r, StreetReferent)
                        num = str0_.number
                        str0_.number = None
                        self.__process(r, ad, FiasAnalyzer.FIAS_DB, AddressReferent.ATTR_FIAS, 0)
                        str0_.number = num
                if (FiasAnalyzer.BTI_DB is not None): 
                    self.__process(r, ad, FiasAnalyzer.BTI_DB, AddressReferent.ATTR_BTI, 0)
    
    M_FIAS_LOCK = None
    
    def __process_address(self, r : 'AddressReferent', ad : 'FiasAnalyzerData', fdb : 'FiasDatabase', attr_name : str, region : int) -> None:
        r.tag = (r)
        for kk in range(2):
            has_fias = False
            has_street = r.find_slot(AddressReferent.ATTR_STREET, None, True) is not None
            iii = 0
            first_pass2871 = True
            while True:
                if first_pass2871: first_pass2871 = False
                else: iii += 1
                if (not (iii < len(r.slots))): break
                s = r.slots[iii]
                if (not (isinstance(s.value, Referent))): 
                    continue
                if (isinstance(s.value, FiasReferent)): 
                    continue
                if (has_street and not (isinstance(s.value, StreetReferent))): 
                    continue
                rr = Utils.asObjectOrNull(s.value, Referent)
                if (rr.type_name == "ORGANIZATION"): 
                    if (kk == 0): 
                        continue
                elif (kk > 0): 
                    continue
                self.__process(rr, ad, fdb, attr_name, region)
                fli0 = list()
                fli1 = list()
                attr_name1 = attr_name + "1"
                for ss in s.value.slots: 
                    if (ss.type_name == attr_name and (isinstance(ss.value, FiasReferent))): 
                        fobj = Utils.asObjectOrNull(ss.value, FiasReferent)
                        fli0.append(fobj)
                        fobj._can_be_wrong = False
                    elif (has_street): 
                        pass
                    elif ((isinstance(ss.value, Referent)) and ss.value.find_slot(attr_name, None, True) is not None): 
                        fobj = Utils.asObjectOrNull(ss.value.get_slot_value(attr_name), FiasReferent)
                        if (fobj is not None): 
                            fli0.append(fobj)
                            fobj._can_be_wrong = True
                    elif (ss.type_name == attr_name1 and (isinstance(ss.value, FiasReferent))): 
                        fobj = Utils.asObjectOrNull(ss.value, FiasReferent)
                        fli1.append(fobj)
                        fobj._can_be_wrong = False
                    elif ((isinstance(ss.value, Referent)) and ss.value.find_slot(attr_name1, None, True) is not None): 
                        fobj = Utils.asObjectOrNull(ss.value.get_slot_value(attr_name1), FiasReferent)
                        if (fobj is not None): 
                            fli1.append(fobj)
                            fobj._can_be_wrong = True
                okcou = 0
                res_li = list()
                remove_attrs1 = False
                for k in range(2):
                    fli = (fli0 if k == 0 else fli1)
                    j0 = len(fli)
                    if (not has_street): 
                        for j in range(len(fli) - 1, -1, -1):
                            if ((isinstance(fli[j].parent_referent, FiasReferent)) and not Utils.asObjectOrNull(fli[j].parent_referent, FiasReferent) in fli): 
                                fli.append(Utils.asObjectOrNull(fli[j].parent_referent, FiasReferent))
                                fli[j].parent_referent._can_be_wrong = True
                    j = 0
                    first_pass2872 = True
                    while True:
                        if first_pass2872: first_pass2872 = False
                        else: j += 1
                        if (not (j < len(fli))): break
                        if (okcou > 0 and j >= j0): 
                            break
                        fobj = fli[j]
                        ao = Utils.asObjectOrNull(fobj.tag, AddressObject)
                        if (ao is None): 
                            continue
                        hos = fdb.find_houses(ao.id0_, Utils.asObjectOrNull(r, AddressReferent))
                        if (hos is None): 
                            continue
                        for ho in hos: 
                            fias_ = FiasReferent()
                            fias_._set_by_house_object(ho)
                            fias_.tag = (ho)
                            fias_.add_slot(FiasReferent.ATTR_OWNER, fobj, True, 0)
                            res_li.append(fias_)
                            if (fobj._can_be_wrong or ho.tag is not None): 
                                fias_._can_be_wrong = True
                        okcou += 1
                    okcou = 0
                    for fias_ in res_li: 
                        if (not fias_._can_be_wrong): 
                            okcou += 1
                    if (okcou > 0): 
                        for ii in range(len(res_li) - 1, -1, -1):
                            if (res_li[ii]._can_be_wrong): 
                                del res_li[ii]
                    if (len(res_li) > 1): 
                        max0_ = -100
                        c = 0
                        for aa in res_li: 
                            c = aa._calc_equal_coef(Utils.asObjectOrNull(r, AddressReferent))
                            if (((c)) > max0_): 
                                max0_ = c
                        for ii in range(len(res_li) - 1, -1, -1):
                            if (res_li[ii]._calc_equal_coef(Utils.asObjectOrNull(r, AddressReferent)) < max0_): 
                                del res_li[ii]
                    if (len(res_li) == 2 and res_li[0].get_string_value("HOUSETYP") != res_li[1].get_string_value("HOUSETYP")): 
                        pass
                    if (len(res_li) > 0): 
                        if (k == 0): 
                            remove_attrs1 = True
                        break
                for fi in res_li: 
                    fias_ = Utils.asObjectOrNull(ad.register_referent(fi), FiasReferent)
                    ro = fdb.find_room(fias_.tag.id0_, Utils.asObjectOrNull(r, AddressReferent))
                    if (ro is not None): 
                        fias1 = FiasReferent()
                        fias1._set_by_room_object(ro)
                        fias1.add_slot(FiasReferent.ATTR_OWNER, fias_, True, 0)
                        fias_ = (Utils.asObjectOrNull(ad.register_referent(fias1), FiasReferent))
                    r.add_slot(attr_name, fias_, False, 0)
                    has_fias = True
                if (remove_attrs1 and len(fli1) > 0): 
                    s.value.add_slot(attr_name1, None, True, 0)
            if (has_fias): 
                break
        fi_list = None
        for s in r.slots: 
            if (s.type_name == attr_name and (isinstance(s.value, FiasReferent))): 
                if (fi_list is None): 
                    fi_list = list()
                fi_list.append(s)
        if (fi_list is None or (len(fi_list) < 2)): 
            return
        nam = str(r)
        if ("Мичур" in nam): 
            for f in fi_list: 
                if (f.value.parent_referent is not None): 
                    nam2 = "{0}{1}".format(f.value, f.value.parent_referent)
                    if ("Мичур" in nam2): 
                        if ("Олимп" in nam and not "Олимп" in nam2): 
                            r.slots.remove(f)
                        elif (not "Олимп" in nam and "Олимп" in nam2): 
                            r.slots.remove(f)
    
    def __get_region(self, r : 'Referent', attr_name : str) -> int:
        if (r is None): 
            return 0
        obj = Utils.asObjectOrNull(r.get_slot_value(attr_name), FiasReferent)
        if (obj is not None and (isinstance(obj.tag, AddressObject))): 
            return obj.tag.region
        if (self.__m_def_path is not None and len(self.__m_def_path) > 0): 
            return self.__m_def_path[0].region
        return 0
    
    def __process(self, r : 'Referent', ad : 'FiasAnalyzerData', fdb : 'FiasDatabase', attr_name : str, region : int) -> None:
        if (r is None): 
            return
        if (r.get_string_value(attr_name) is not None): 
            return
        r.tag = (r)
        if (isinstance(r, GeoReferent)): 
            if (r.is_state): 
                return
            hi = r.higher
            if (hi is not None): 
                self.__process(hi, ad, fdb, attr_name, region)
                if (region == (0)): 
                    region = self.__get_region(hi, attr_name)
        if ((isinstance(r, StreetReferent)) and r.higher is not None): 
            self.__process(r.higher, ad, fdb, attr_name, region)
            if (region == (0)): 
                region = self.__get_region(r.higher, attr_name)
            if (r.higher.find_slot(GeoReferent.ATTR_FIAS, None, True) is None and r.find_slot(StreetReferent.ATTR_GEO, None, True) is None): 
                geo1 = Utils.asObjectOrNull(r.higher.get_slot_value(StreetReferent.ATTR_GEO), GeoReferent)
                if (geo1 is None): 
                    return
                if (geo1.find_slot(GeoReferent.ATTR_FIAS, None, True) is None): 
                    return
                r.add_slot(StreetReferent.ATTR_GEO, geo1, False, 0)
        if ((isinstance(r, StreetReferent)) and r.find_slot(StreetReferent.ATTR_GEO, None, True) is not None): 
            geo1 = Utils.asObjectOrNull(r.get_slot_value(StreetReferent.ATTR_GEO), GeoReferent)
            if (geo1 is not None): 
                self.__process(geo1, ad, fdb, attr_name, region)
                if (region == (0)): 
                    region = self.__get_region(geo1, attr_name)
                if (geo1.find_slot(GeoReferent.ATTR_FIAS, None, True) is None): 
                    if (geo1.is_city): 
                        return
                    if (geo1.higher is None): 
                        return
                    if (geo1.higher.find_slot(GeoReferent.ATTR_FIAS, None, True) is None): 
                        return
        if ((isinstance(r, StreetReferent)) and r.find_slot(StreetReferent.ATTR_GEO, None, True) is None and r.higher is None): 
            if (self.__m_def_path is None or len(self.__m_def_path) == 0): 
                return
        if (isinstance(r, AddressReferent)): 
            self.__process_address(Utils.asObjectOrNull(r, AddressReferent), ad, fdb, attr_name, region)
            return
        r.tag = (r)
        parent = r.parent_referent
        if (parent is None and r.type_name == "ORGANIZATION"): 
            for s in r.slots: 
                if (s.type_name == "GEO" and (isinstance(s.value, GeoReferent))): 
                    parent = (Utils.asObjectOrNull(s.value, GeoReferent))
                    if (region == (0)): 
                        region = self.__get_region(parent, attr_name)
                    break
        prob = fdb._get_string_entries(r, region)
        if (prob is None or len(prob) == 0): 
            return
        if (region == (0)): 
            if (len(prob) > 20): 
                return
            if (len(prob) > 5): 
                geo2 = Utils.asObjectOrNull(r, GeoReferent)
                if (geo2 is not None): 
                    if (geo2.is_city and not geo2.is_big_city): 
                        return
        par_objs = None
        par_objs2 = None
        geo = r
        for i in range(7):
            ge = None
            if (isinstance(geo, StreetReferent)): 
                ge = geo.parent_referent
            elif (isinstance(geo, GeoReferent)): 
                ge = (Utils.asObjectOrNull(geo.get_slot_value(GeoReferent.ATTR_HIGHER), GeoReferent))
            if (ge is None): 
                break
            firef = Utils.asObjectOrNull(ge.get_slot_value(attr_name), FiasReferent)
            if (firef is not None): 
                if ((isinstance(r, StreetReferent)) and i > 0): 
                    if ((isinstance(ge, GeoReferent)) and not ge.is_city): 
                        return
                par_objs = list()
                for ss in ge.slots: 
                    if ((isinstance(ss.value, FiasReferent)) and (isinstance(ss.value.tag, AddressObject))): 
                        ao = Utils.asObjectOrNull(ss.value.tag, AddressObject)
                        par_objs.append(ao)
                        if (len(ao.parents_id) > 0): 
                            if (isinstance(r, StreetReferent)): 
                                ao2 = fdb.getao(ao.parents_id[0])
                                if (ao2 is not None and not ao2 in par_objs): 
                                    is_in_pars = False
                                    for ppp in par_objs: 
                                        if (ppp.id0_ == ao2.id0_): 
                                            is_in_pars = True
                                    if (not is_in_pars): 
                                        if (par_objs2 is None): 
                                            par_objs2 = list()
                                        par_objs2.append(ao2)
                break
            geo = ge
            if ((isinstance(ge, GeoReferent)) and ge.is_state): 
                if (ge.alpha2 == "RU"): 
                    pass
                else: 
                    return
        if (par_objs is None and parent is None and (isinstance(r, StreetReferent))): 
            if (self.__m_def_path is not None and len(self.__m_def_path) > 0 and fdb == FiasAnalyzer.FIAS_DB): 
                par_objs = list()
                par_objs.append(self.__m_def_path[0])
        prob2 = (None if par_objs2 is None else list(prob))
        if (par_objs is not None): 
            vars0_ = list()
            eqpar_var = None
            eq_coef = 0
            for i in range(len(prob) - 1, -1, -1):
                has = False
                for p in par_objs: 
                    if (p.id0_ in prob[i].parents_id): 
                        if (prob[i].parents_id[0] == p.id0_): 
                            if (eqpar_var is None): 
                                eqpar_var = list()
                            elif (eq_coef == 0): 
                                eqpar_var.clear()
                            eqpar_var.append(prob[i])
                            eq_coef = 1
                        has = True
                    if (prob[i].alt_parent_id == p.id0_): 
                        if (eqpar_var is None): 
                            eqpar_var = list()
                        elif (eq_coef == 0): 
                            eqpar_var.clear()
                        if (not prob[i] in eqpar_var): 
                            eqpar_var.append(prob[i])
                        has = True
                        eq_coef = 1
                if (has or eq_coef > 0): 
                    continue
                for p in par_objs: 
                    if (len(p.parents_id) > 0 and p.parents_id[0] in prob[i].parents_id): 
                        typ = fdb.get_addr_type(prob[i].typ_id)
                        if (typ.check_type(r) > 0): 
                            if (eqpar_var is None): 
                                eqpar_var = list()
                            eqpar_var.append(prob[i])
                        else: 
                            vars0_.append(prob[i])
                        break
                del prob[i]
            if (eqpar_var is not None): 
                prob = eqpar_var
            if (len(prob) == 0 and (len(vars0_) < 3)): 
                prob.extend(vars0_)
        if (par_objs2 is not None and prob2 is not None and len(prob2) > 0): 
            vars0_ = list()
            eqpar_var = None
            for i in range(len(prob2) - 1, -1, -1):
                has = False
                for p in par_objs2: 
                    if (p.id0_ in prob2[i].parents_id): 
                        if (prob2[i].parents_id[0] == p.id0_): 
                            if (eqpar_var is None): 
                                eqpar_var = list()
                            eqpar_var.append(prob2[i])
                        has = True
                    elif (prob2[i].alt_parent_id == p.id0_): 
                        if (eqpar_var is None): 
                            eqpar_var = list()
                        eqpar_var.append(prob2[i])
                        has = True
                if (has): 
                    continue
                for p in par_objs2: 
                    if (len(p.parents_id) > 0 and p.parents_id[0] in prob2[i].parents_id): 
                        vars0_.append(prob2[i])
                        break
                del prob2[i]
            if (eqpar_var is not None): 
                prob2 = eqpar_var
            if (len(prob2) == 0 and (len(vars0_) < 3)): 
                prob2.extend(vars0_)
            if (len(prob) == 0): 
                prob = prob2
                prob2 = (None)
        if (len(prob) == 0): 
            return
        if (par_objs is None and (isinstance(r, StreetReferent)) and fdb == FiasAnalyzer.FIAS_DB): 
            return
        i = 0
        while i < (len(prob) - 1): 
            j = 0
            while j < (len(prob) - 1): 
                if (prob[j].compareTo(prob[j + 1]) > 0): 
                    pp = prob[j]
                    prob[j] = prob[j + 1]
                    prob[j + 1] = pp
                j += 1
            i += 1
        res = list()
        res2 = list()
        for p in prob: 
            ao = fdb.getao(p.id0_)
            if (ao is None): 
                continue
            if (ao.typ is not None): 
                if (ao.typ.typ != AddrTyp.Typs.STREET): 
                    pass
                co = ao.typ.check_type(r)
                if (co > 0): 
                    pass
                elif (ao.unom == 1209 and fdb == FiasAnalyzer.BTI_DB): 
                    pass
                elif (co == 0): 
                    res2.append(ao)
                    continue
                elif (ao.old_typ is not None and ao.old_typ.check_type(r) > 0): 
                    pass
                else: 
                    continue
            res.append(ao)
        if (len(res) == 0 and len(res2) > 0): 
            res = res2
        if (len(res) == 0): 
            return
        if (len(res) > 1): 
            exp0_ = 0
            for re in res: 
                if (re.typ.typ != AddrTyp.Typs.ORG and r.find_slot(GeoReferent.ATTR_TYPE, re.typ.name, True) is not None): 
                    exp0_ += 1
            if (exp0_ > 0 and (exp0_ < len(res))): 
                for i in range(len(res) - 1, -1, -1):
                    if (res[i].typ is not None and res[i].typ.typ != AddrTyp.Typs.ORG and r.find_slot(GeoReferent.ATTR_TYPE, res[i].typ.name, True) is None): 
                        del res[i]
        if (len(res) > 1): 
            if (not res[0].actual): 
                i = 1
                while i < len(res): 
                    if (res[i].actual): 
                        a = res[i]
                        del res[i]
                        res.insert(0, a)
                        break
                    i += 1
        if (len(res) > 1): 
            if (par_objs is None and parent is None): 
                if (self.__m_def_path is not None and len(self.__m_def_path) > 0): 
                    ii = -1
                    for i in range(len(res) - 1, -1, -1):
                        if (self.__m_def_path[0].id0_ in res[i].parents_id): 
                            ii = i
                            break
                    if (ii >= 0): 
                        for i in range(len(res) - 1, -1, -1):
                            if (not self.__m_def_path[0].id0_ in res[i].parents_id): 
                                del res[i]
        if (isinstance(r, StreetReferent)): 
            if (len(res) > 1): 
                for i in range(len(res) - 1, -1, -1):
                    if (par_objs is not None and len(par_objs) == 1 and len(par_objs[0].parents_id) == 0): 
                        del0_ = False
                        j = 0
                        first_pass2873 = True
                        while True:
                            if first_pass2873: first_pass2873 = False
                            else: j += 1
                            if (not (j < len(res[i].parents_id))): break
                            if (res[i].parents_id[j] == par_objs[0].id0_): 
                                break
                            else: 
                                ao = fdb.getao(res[i].parents_id[j])
                                if (ao is not None and ao.typ is not None and ao.typ.typ == AddrTyp.Typs.REGION): 
                                    continue
                                del0_ = True
                                break
                        if (del0_): 
                            del res[i]
                            continue
            if (len(res) > 1 and res[0].typ.typ != AddrTyp.Typs.ORG): 
                words = list()
                for s in r.slots: 
                    if (s.type_name == StreetReferent.ATTR_NAME): 
                        ww = FiasAnalyzer.__get_norm_words(Utils.asObjectOrNull(s.value, str))
                        if (ww is not None): 
                            for w in ww: 
                                if (not w in words): 
                                    words.append(w)
                res1 = list()
                max0_ = 0
                for ao in res: 
                    if (len(ao.names) > 0): 
                        ww = FiasAnalyzer.__get_norm_words(ao.names[0])
                        if (ww is None): 
                            continue
                        m = 0
                        for w in ww: 
                            if (w in words): 
                                m += 1
                        if (m > max0_): 
                            res1.clear()
                            res1.append(ao)
                            max0_ = m
                        elif (m == max0_): 
                            res1.append(ao)
                res = res1
        alt_addr = None
        if (prob2 is not None and len(prob2) == 1): 
            jj = 0
            jj = 0
            while jj < len(prob): 
                if (prob[jj].id0_ == prob2[0].id0_): 
                    break
                jj += 1
            if (jj >= len(prob)): 
                ao = fdb.getao(prob2[0].id0_)
                if (ao is not None and ao.typ is not None): 
                    co = ao.typ.check_type(r)
                    if (co > 0): 
                        res.append(ao)
                        alt_addr = ao
        paths = list()
        min_coef = 100
        for re in res: 
            li = list()
            fias_ = FiasReferent()
            fias_._set_by_address_object(re)
            li.insert(0, fias_)
            co = 0
            for id0_ in re.parents_id: 
                exi = ad.find_by_id(id0_, fdb == FiasAnalyzer.BTI_DB)
                if (exi is None): 
                    aoo = fdb.getao(id0_)
                    if (aoo is None): 
                        break
                    exi = FiasReferent()
                    exi._set_by_address_object(aoo)
                if (fdb == FiasAnalyzer.BTI_DB): 
                    ao = Utils.asObjectOrNull(exi.tag, AddressObject)
                    if (ao is not None and ao.typ is not None): 
                        if (ao.typ.typ != AddrTyp.Typs.REGION): 
                            is_in_pars = False
                            for ppp in res: 
                                if (ppp.id0_ == ao.id0_): 
                                    is_in_pars = True
                            if (not is_in_pars): 
                                co += 1
                li.insert(0, exi)
            if (re == alt_addr): 
                pass
            elif (co < min_coef): 
                if (co == (min_coef - 1) and (len(paths) == 1 & alt_addr is None)): 
                    alt_addr = (Utils.asObjectOrNull(li[len(li) - 1].tag, AddressObject))
                else: 
                    paths.clear()
                min_coef = co
            elif (co > min_coef): 
                if (fdb == FiasAnalyzer.BTI_DB and r.find_slot(GeoReferent.ATTR_NAME, "ЗЕЛЕНОГРАД", True) is not None): 
                    pass
                elif (fdb == FiasAnalyzer.BTI_DB and r.find_slot(GeoReferent.ATTR_NAME, "ТРОИЦК", True) is not None): 
                    pass
                elif (co == (min_coef + 1) and (len(paths) == 1 & alt_addr is None)): 
                    alt_addr = (Utils.asObjectOrNull(li[len(li) - 1].tag, AddressObject))
                else: 
                    continue
            paths.append(li)
        if (len(paths) < 100): 
            for li in paths: 
                i = 0
                while i < len(li): 
                    li[i] = (Utils.asObjectOrNull(ad.register_referent(li[i]), FiasReferent))
                    if ((i + 1) < len(li)): 
                        li[i + 1].add_slot(FiasReferent.ATTR_OWNER, li[i], True, 0)
                    i += 1
                nam = attr_name
                ao = Utils.asObjectOrNull(li[len(li) - 1].tag, AddressObject)
                if (ao is not None and alt_addr is not None and alt_addr.id0_ == ao.id0_): 
                    nam += "1"
                r.add_slot(nam, li[len(li) - 1], False, 0)
    
    M_PROC0 = None
    
    @staticmethod
    def __get_norm_words(str0_ : str) -> typing.List[str]:
        if (FiasAnalyzer.M_PROC0 is None): 
            FiasAnalyzer.M_PROC0 = ProcessorService.create_empty_processor()
        ar = FiasAnalyzer.M_PROC0.process(SourceOfAnalysis(str0_), None, None)
        res = list()
        if (ar.first_token is not None): 
            t = ar.first_token
            while t is not None: 
                if ((isinstance(t, TextToken)) and t.chars.is_letter): 
                    res.append(t.term)
                t = t.next0_
        return res
    
    FIAS_PATH = None
    """ По умолчанию, это папка Fias в текущей директории запуска """
    
    BTI_PATH = None
    """ Этот папка для классификатора БТИ """
    
    @staticmethod
    def init_fias(fias_path : str) -> bool:
        if (FiasAnalyzer.FIAS_PATH == fias_path and FiasAnalyzer.FIAS_DB is not None): 
            return True
        FiasAnalyzer.deinit_fias()
        with FiasAnalyzer.M_FIAS_LOCK: 
            FiasAnalyzer.FIAS_PATH = fias_path
            FiasAnalyzer.M_FIAS_INITIALIZED = False
            FiasAnalyzer.FIAS_DB = (None)
            if (Utils.isNullOrEmpty(FiasAnalyzer.FIAS_PATH)): 
                return True
            if (pathlib.Path(Utils.ifNotNull(FiasAnalyzer.FIAS_PATH, "")).is_dir()): 
                FiasAnalyzer.FIAS_DB = FiasDatabase()
                FiasAnalyzer.FIAS_DB.initialize(FiasAnalyzer.FIAS_PATH)
                FiasAnalyzer.M_FIAS_INITIALIZED = True
                return True
            return False
    
    @staticmethod
    def deinit_fias() -> None:
        with FiasAnalyzer.M_FIAS_LOCK: 
            if (FiasAnalyzer.M_FIAS_INITIALIZED): 
                FiasAnalyzer.M_FIAS_INITIALIZED = False
                if (FiasAnalyzer.FIAS_DB is not None): 
                    FiasAnalyzer.FIAS_DB.close()
                FiasAnalyzer.FIAS_DB = (None)
    
    @staticmethod
    def init_bti(bti_path : str) -> bool:
        FiasAnalyzer.BTI_PATH = bti_path
        FiasAnalyzer.M_BTI_INITIALIZED = False
        FiasAnalyzer.BTI_DB = (None)
        if (pathlib.Path(Utils.ifNotNull(FiasAnalyzer.BTI_PATH, "")).is_dir()): 
            FiasAnalyzer.BTI_DB = FiasDatabase()
            FiasAnalyzer.BTI_DB.initialize(FiasAnalyzer.BTI_PATH)
            FiasAnalyzer.M_BTI_INITIALIZED = True
            return True
        return False
    
    FIAS_DB = None
    
    BTI_DB = None
    
    M_FIAS_INITIALIZED = False
    
    M_BTI_INITIALIZED = False
    
    def dispose(self) -> None:
        if (FiasAnalyzer.M_FIAS_INITIALIZED): 
            FiasAnalyzer.M_FIAS_INITIALIZED = False
            if (FiasAnalyzer.FIAS_DB is not None): 
                FiasAnalyzer.FIAS_DB.close()
            FiasAnalyzer.FIAS_DB = (None)
        if (FiasAnalyzer.M_BTI_INITIALIZED): 
            FiasAnalyzer.M_BTI_INITIALIZED = False
            if (FiasAnalyzer.BTI_DB is not None): 
                FiasAnalyzer.BTI_DB.close()
            FiasAnalyzer.BTI_DB = (None)
    
    M_INITED = None
    
    @staticmethod
    def initialize() -> None:
        if (FiasAnalyzer.M_INITED): 
            return
        FiasAnalyzer.M_INITED = True
        MetaFias.initialize()
        ProcessorService.register_analyzer(FiasAnalyzer())
    
    # static constructor for class FiasAnalyzer
    @staticmethod
    def _static_ctor():
        FiasAnalyzer.M_FIAS_LOCK = threading.Lock()

FiasAnalyzer._static_ctor()