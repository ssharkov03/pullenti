# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import pathlib
import uuid
import datetime
import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.unisharp.Streams import MemoryStream
from pullenti.unisharp.Streams import Stream

from pullenti.address.internal.gar.HouseObject import HouseObject
from pullenti.address.internal.FiasHelper import FiasHelper
from pullenti.address.internal.gar.AddressObject import AddressObject
from pullenti.address.internal.gar.ParamType import ParamType
from pullenti.address.internal.gar.HTreeRoot import HTreeRoot
from pullenti.ner.address.StreetKind import StreetKind
from pullenti.ner.Referent import Referent
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.address.StreetReferent import StreetReferent
from pullenti.util.repository.KeyBaseTable import KeyBaseTable
from pullenti.util.repository.IRepository import IRepository
from pullenti.address.internal.gar.AddrTyp import AddrTyp
from pullenti.address.internal.gar.FiasHouseTable import FiasHouseTable
from pullenti.address.internal.gar.FiasAddrTable import FiasAddrTable
from pullenti.address.internal.gar.PTreeRoot import PTreeRoot
from pullenti.address.internal.gar.ParamsTable import ParamsTable
from pullenti.address.internal.gar.ATreeRoot import ATreeRoot
from pullenti.address.internal.gar.FiasRoomTable import FiasRoomTable

class FiasDatabase(IRepository):
    # База данных ФИАС (ГАР)
    
    def __init__(self) -> None:
        self.__basedir = None;
        self.id0_ = None;
        self.create_date = None;
        self.read_only = True
        self.__big_city_ids = list()
        self.__big_city_names = list()
        self.__m_types = dict()
        self.__m_addr_table = None;
        self.__m_house_table = None;
        self.__m_room_table = None;
        self.__m_house_map_table = None;
        self.__m_addr_string_tree = None;
        self.__m_addr_params = None;
        self.__m_house_params = None;
        self.__m_room_params = None;
        self.__m_params_maps = dict()
        self.__outlog = False
    
    @property
    def base_dir(self) -> str:
        return self.__basedir
    @base_dir.setter
    def base_dir(self, value) -> str:
        self.__basedir = value
        return self.__basedir
    
    def initialize(self, dir_name : str) -> None:
        self.base_dir = dir_name
        if (not pathlib.Path(dir_name).is_dir()): 
            pathlib.Path(dir_name).mkdir(exist_ok=True)
        self.__m_addr_table = FiasAddrTable(self)
        self.__m_addr_table.open0_(self.read_only, 0)
        self.__m_house_table = FiasHouseTable(self)
        self.__m_house_table.open0_(self.read_only, 0)
        self.__m_room_table = FiasRoomTable(self)
        self.__m_room_table.open0_(self.read_only, 0)
        self.__m_house_map_table = KeyBaseTable(self, "housemaps")
        self.__m_house_map_table.open0_(self.read_only, 0)
        self.__m_addr_params = ParamsTable._new29(self, "addressparams", True)
        self.__m_addr_params.open0_(self.read_only, 0)
        self.__m_house_params = ParamsTable._new29(self, "houseparams", True)
        self.__m_house_params.open0_(self.read_only, 0)
        self.__m_room_params = ParamsTable._new29(self, "roomparams", True)
        self.__m_room_params.open0_(self.read_only, 0)
        fname = pathlib.PurePath(self.base_dir).joinpath("types.xml")
        if (not pathlib.Path(fname).is_file()): 
            fname = pathlib.PurePath(self.base_dir).joinpath("types.dat")
        if (pathlib.Path(fname).is_file()): 
            id0__ = None
            dt = None
            wrapid32 = RefOutArgWrapper(id0__)
            wrapdt33 = RefOutArgWrapper(dt)
            typs = AddrTyp._load(fname, wrapid32, wrapdt33)
            id0__ = wrapid32.value
            dt = wrapdt33.value
            if (typs is not None): 
                self.__m_types = typs
            self.id0_ = id0__
            self.create_date = dt
        else: 
            self.id0_ = str(uuid.uuid4())
            self.create_date = "{0}.{1}.{2}".format(datetime.datetime.now().year, "{:02d}".format(datetime.datetime.now().month), "{:02d}".format(datetime.datetime.now().day))
        self.__m_addr_string_tree = ATreeRoot()
        fname = pathlib.PurePath(self.base_dir).joinpath("addressmap.dat")
        if (pathlib.Path(fname).is_file()): 
            self.__m_addr_string_tree.load(fname)
        for ty in FiasDatabase.__m_param_types: 
            fname = pathlib.PurePath(self.base_dir).joinpath("paramap{0}.dat".format(ty))
            tn = PTreeRoot()
            if (ty == ParamType.KLADRCODE or ty == ParamType.KADASTERNUMBER or ty == ParamType.REESTERNUMBER): 
                tn.max_length = 8
            elif (ty == ParamType.GUID): 
                tn.max_length = 5
            try: 
                if (pathlib.Path(fname).is_file()): 
                    tn.load(fname)
            except Exception as ex: 
                pass
            self.__m_params_maps[ty] = tn
        roots = self.getao(1)
        if (roots is not None and roots.children_ids is not None): 
            for id0__ in roots.children_ids: 
                if ((((id0__) & (AddressObject.ROOMMASK))) != 0): 
                    continue
                uid = id0__
                ao = self.getao(uid)
                if (ao is None or ao.typ is None): 
                    continue
                if (ao.typ.name == "город"): 
                    self.__big_city_ids.append(uid)
                    self.__big_city_names.append(ao.names[0].upper())
                if (ao.children_ids is not None): 
                    for id2 in ao.children_ids: 
                        if ((((id2) & (AddressObject.ROOMMASK))) != 0): 
                            continue
                        uid = (id2)
                        ao2 = self.getao(uid)
                        if (ao2 is None or ao2.typ is None): 
                            continue
                        if (ao2.typ.name == "город"): 
                            self.__big_city_ids.append(uid)
                            self.__big_city_names.append(ao2.names[0].upper())
    
    def add_addr_type(self, typ : str) -> 'AddrTyp':
        ty = None
        for kp in self.__m_types.items(): 
            if (kp[1].name == typ): 
                ty = kp[1]
                break
        if (ty is None): 
            ty = AddrTyp._new34(len(self.__m_types) + 1, typ)
            self.__m_types[ty.id0_] = ty
        return ty
    
    def get_addr_types(self) -> typing.List['AddrTyp']:
        return list(self.__m_types.values())
    
    def find_addr_type(self, name : str) -> 'AddrTyp':
        for kp in self.__m_types.items(): 
            if (kp[1].can_be_equal(name)): 
                return kp[1]
        return None
    
    def get_addr_type(self, id0__ : int) -> 'AddrTyp':
        res = None
        wrapres35 = RefOutArgWrapper(None)
        inoutres36 = Utils.tryGetValue(self.__m_types, id0__, wrapres35)
        res = wrapres35.value
        if (not inoutres36): 
            return None
        else: 
            return res
    
    @property
    def objects_count(self) -> int:
        if (self.__m_addr_table is None): 
            return 0
        return self.__m_addr_table.get_max_key()
    
    @property
    def houses_count(self) -> int:
        if (self.__m_house_table is None): 
            return 0
        return self.__m_house_table.get_max_key()
    
    @property
    def rooms_count(self) -> int:
        if (self.__m_room_table is None): 
            return 0
        return self.__m_room_table.get_max_key()
    
    __m_param_types = None
    
    def _close(self) -> None:
        if (self.__m_addr_table is not None): 
            self.__m_addr_table._close()
            self.__m_addr_table = (None)
        if (self.__m_addr_string_tree is not None): 
            self.__m_addr_string_tree.close0_()
            self.__m_addr_string_tree = (None)
        if (self.__m_house_table is not None): 
            self.__m_house_table._close()
            self.__m_house_table = (None)
        if (self.__m_room_table is not None): 
            self.__m_room_table._close()
            self.__m_room_table = (None)
        if (self.__m_house_map_table is not None): 
            self.__m_house_map_table._close()
            self.__m_house_map_table = (None)
        if (self.__m_addr_params is not None): 
            self.__m_addr_params._close()
            self.__m_addr_params = (None)
        if (self.__m_house_params is not None): 
            self.__m_house_params._close()
            self.__m_house_params = (None)
        if (self.__m_room_params is not None): 
            self.__m_room_params._close()
            self.__m_room_params = (None)
        for kp in self.__m_params_maps.items(): 
            kp[1].close0_()
        self.__m_params_maps.clear()
    
    def collect(self) -> None:
        if (self.__m_addr_string_tree is not None): 
            self.__m_addr_string_tree.collect()
        for kp in self.__m_params_maps.items(): 
            kp[1].collect()
    
    def clear(self) -> None:
        pass
    
    @property
    def out_log(self) -> bool:
        return self.__outlog
    @out_log.setter
    def out_log(self, value) -> bool:
        self.__outlog = value
        return self.__outlog
    
    def close(self) -> None:
        self._close()
    
    def find_by_param(self, ty : 'ParamType', value : str) -> typing.List[int]:
        p = None
        wrapp39 = RefOutArgWrapper(None)
        inoutres40 = Utils.tryGetValue(self.__m_params_maps, ty, wrapp39)
        p = wrapp39.value
        if (not inoutres40): 
            return None
        tn = p.find(value)
        if (tn is None): 
            return None
        res = list()
        for ui in tn.ids: 
            pars = None
            if ((((ui) & 0x80000000)) == 0): 
                pars = self.getaoparams(ui)
            elif ((((ui) & 0x40000000)) == 0): 
                pars = self.get_house_params(((ui) & 0x3FFFFFFF))
            else: 
                pars = self.get_room_params(((ui) & 0x3FFFFFFF))
            if (pars is None): 
                continue
            val = None
            wrapval37 = RefOutArgWrapper(None)
            inoutres38 = Utils.tryGetValue(pars, ty, wrapval37)
            val = wrapval37.value
            if (not inoutres38): 
                continue
            if (val == value): 
                res.append(ui)
        return res
    
    def get_parent_id(self, sid : str) -> int:
        iid = 0
        wrapiid41 = RefOutArgWrapper(0)
        inoutres42 = Utils.tryParseInt(sid[1:], wrapiid41)
        iid = wrapiid41.value
        if (not inoutres42): 
            return 0
        if (iid < 0): 
            return 0
        if (sid[0] == 'a'): 
            with self.__m_addr_table.m_lock: 
                return self.__m_addr_table.get_parent_id(iid)
        if (sid[0] == 'h'): 
            with self.__m_house_table.m_lock: 
                return self.__m_house_table.get_parent_id(iid)
        if (sid[0] == 'r'): 
            with self.__m_room_table.m_lock: 
                return self.__m_room_table.get_parent_id(iid)
        return 0
    
    def get_actual(self, sid : str) -> int:
        iid = 0
        wrapiid43 = RefOutArgWrapper(0)
        inoutres44 = Utils.tryParseInt(sid[1:], wrapiid43)
        iid = wrapiid43.value
        if (not inoutres44): 
            return -1
        if (iid < 0): 
            return -1
        if (sid[0] == 'a'): 
            with self.__m_addr_table.m_lock: 
                return self.__m_addr_table.get_actual(iid)
        if (sid[0] == 'h'): 
            with self.__m_house_table.m_lock: 
                return self.__m_house_table.get_actual(iid)
        if (sid[0] == 'r'): 
            with self.__m_room_table.m_lock: 
                return self.__m_room_table.get_actual(iid)
        return 0
    
    def getao(self, id0__ : int) -> 'AddressObject':
        if (self.__m_addr_table is None): 
            return None
        with self.__m_addr_table.m_lock: 
            ao = AddressObject._new45(id0__)
            if (self.__m_addr_table.get(id0__, ao, self.__m_types)): 
                return ao
            else: 
                return None
    
    def getaoparams(self, id0__ : int) -> typing.List[tuple]:
        if (self.__m_addr_params is None): 
            return None
        with self.__m_addr_params.m_lock: 
            return self.__m_addr_params.get_params(id0__)
    
    def putaoparams(self, id0__ : int, pars : typing.List[tuple]) -> None:
        if (self.__m_addr_params is None): 
            return
        self.__m_addr_params.put_params(id0__, pars, False)
    
    def putao(self, ao : 'AddressObject', only_attrs : bool=False) -> bool:
        if (self.__m_addr_table is None): 
            return False
        if (ao.id0_ == 0): 
            ao.id0_ = (self.__m_addr_table.get_max_key() + 1)
        self.__m_addr_table.add(ao.id0_, ao, only_attrs)
        return True
    
    def get_house(self, id0__ : int) -> 'HouseObject':
        if (self.__m_house_table is None): 
            return None
        with self.__m_house_table.m_lock: 
            ao = HouseObject._new46(id0__)
            if (self.__m_house_table.get(id0__, ao)): 
                return ao
            else: 
                return None
    
    def put_house(self, ao : 'HouseObject') -> bool:
        if (self.__m_house_table is None): 
            return False
        if (ao.parent_id == 0): 
            return False
        if (ao.id0_ == 0): 
            ao.id0_ = (self.__m_house_table.get_max_key() + 1)
        self.__m_house_table.add(ao.id0_, ao)
        str0_ = FiasHelper.get_house_string(ao)
        if (str0_ is None): 
            return True
        dat = self.__m_house_map_table.read_key_data(ao.parent_id, 0)
        htree = HTreeRoot()
        if (dat is not None): 
            htree.load(dat)
        htree.add(str0_, ao.id0_, ao.actual)
        with MemoryStream() as mem: 
            htree.save(mem)
            dat = mem.toarray()
            self.__m_house_map_table.write_key_data(ao.parent_id, dat)
            return True
    
    def find_houses(self, addr_id : int, a : 'AddressReferent') -> typing.List['HouseObject']:
        strs = FiasHelper.get_house_strings(a)
        if (strs is None): 
            return None
        is_plot = a.plot is not None
        is_undef = a.house_or_plot is not None
        dat = None
        with self.__m_house_map_table.m_lock: 
            dat = self.__m_house_map_table.read_key_data(addr_id, 0)
        if (dat is None): 
            return None
        tree = HTreeRoot()
        try: 
            tree.load(dat)
        except Exception as ex: 
            return None
        res = None
        for s in strs: 
            tn = tree.find(s)
            if (tn is not None and tn.id0_ > 0): 
                house = self.get_house(tn.id0_)
                if (house is not None): 
                    if (is_undef or ((is_plot and house.house_typ == (5))) or ((not is_plot and house.house_typ != (5)))): 
                        if (s != strs[0]): 
                            house.tag = (res)
                        res = list()
                        res.append(house)
                if (tn.other_ids is not None): 
                    for id0__ in tn.other_ids: 
                        house = self.get_house(id0__)
                        if (house is not None): 
                            if (is_undef or ((is_plot and house.house_typ == (5))) or ((not is_plot and house.house_typ != (5)))): 
                                if (s != strs[0]): 
                                    house.tag = (res)
                                if (res is None): 
                                    res = list()
                                res.append(house)
                if (res is not None): 
                    return res
        return None
    
    def get_house_params(self, id0__ : int) -> typing.List[tuple]:
        if (self.__m_house_params is None): 
            return None
        with self.__m_house_params.m_lock: 
            return self.__m_house_params.get_params(id0__)
    
    def put_house_params(self, id0__ : int, pars : typing.List[tuple]) -> None:
        if (self.__m_house_params is None): 
            return
        self.__m_house_params.put_params(id0__, pars, False)
    
    def _put_string_entry(self, ao : 'AddressObject', str0_ : str) -> None:
        if (ao.id0_ > 0 and ao.typ is not None): 
            self.__m_addr_string_tree.add(str0_, ao.id0_, ao.typ.id0_, ao.parents_id, ao.alt_parent_id, ao.region)
    
    def _clear_string_entries(self) -> None:
        self.__m_addr_string_tree.children = dict()
    
    def get_all_string_entries_by_start(self, start : str, reg_id : int) -> typing.List['AddrInfo']:
        res = list()
        root = None
        with self.__m_addr_string_tree.m_lock: 
            root = self.__m_addr_string_tree.find(start, False, True)
            if (root is None): 
                root = self.__m_addr_string_tree.find(start, True, False)
            if (root is not None): 
                self.__add_addr_info_res(root, reg_id, res)
        return res
    
    def __add_addr_info_res(self, n : 'ATreeNode', reg_id : int, res : typing.List['AddrInfo']) -> None:
        if (n.lazy_pos > 0): 
            self.__m_addr_string_tree.load_node(n)
        if (n.objs is not None): 
            for o in n.objs: 
                if (reg_id != 0): 
                    if ((o.region) != reg_id): 
                        continue
                exi = False
                for r in res: 
                    if (r.id0_ == o.id0_): 
                        exi = True
                    break
                if (not exi): 
                    res.append(o)
        if (n.children is not None): 
            for kp in n.children.items(): 
                self.__add_addr_info_res(kp[1], reg_id, res)
    
    def get_all_children(self, id0__ : int) -> typing.List['AddrInfo']:
        res = list()
        with self.__m_addr_string_tree.m_lock: 
            for ch in self.__m_addr_string_tree.children.items(): 
                self.__add_children(id0__, ch[1], res)
        return res
    
    def __add_children(self, id0__ : int, n : 'ATreeNode', res : typing.List['AddrInfo']) -> None:
        if (n.objs is not None): 
            for o in n.objs: 
                if (o.parents_id is not None and len(o.parents_id) > 0 and o.parents_id[0] == id0__): 
                    res.append(o)
        if (n.children is not None): 
            for ch in n.children.items(): 
                self.__add_children(id0__, ch[1], res)
    
    def _get_string_entries(self, r : 'Referent', region : int) -> typing.List['AddrInfo']:
        if (self.__m_addr_string_tree is None): 
            return None
        strs = FiasHelper._get_strings(r)
        if (strs is None or len(strs) == 0): 
            return None
        res = None
        with self.__m_addr_string_tree.m_lock: 
            for k in range(2):
                for s in strs: 
                    li = None
                    li = self.__m_addr_string_tree.find(s, k > 0, False)
                    if (li is None or li.objs is None): 
                        continue
                    if (len(li.objs) > 1000 and region == (0)): 
                        return None
                    if (res is None): 
                        res = list()
                        for o in li.objs: 
                            if (region != (0) and o.region != region and o.region != (0)): 
                                pass
                            else: 
                                res.append(o)
                    else: 
                        for o in li.objs: 
                            if (region != (0) and o.region != region and o.region != (0)): 
                                continue
                            ex = False
                            for ll in res: 
                                if (ll.id0_ == o.id0_): 
                                    ex = True
                                    break
                            if (not ex): 
                                res.append(o)
                    if (res is not None and len(res) > 100): 
                        break
                if (res is not None): 
                    break
        if ((isinstance(r, GeoReferent)) and r.is_region): 
            if (res is not None and r is not None): 
                for i in range(len(res) - 1, -1, -1):
                    ty = self.get_addr_type(res[i].typ_id)
                    if (ty is not None): 
                        if (ty.check_type(r) < 0): 
                            del res[i]
        if ((region == (0) and res is not None and len(res) > 1) and (isinstance(r, GeoReferent)) and r.is_big_city): 
            for s in r.slots: 
                if (s.type_name == "NAME" and Utils.asObjectOrNull(s.value, str) in self.__big_city_names): 
                    for i in range(len(res) - 1, -1, -1):
                        if (res[i].id0_ in self.__big_city_ids): 
                            it = res[i]
                            res.clear()
                            res.append(it)
                            return res
        if (res is not None and r is not None): 
            for i in range(len(res) - 1, -1, -1):
                ty = self.get_addr_type(res[i].typ_id)
                if (ty is not None): 
                    co = ty.check_type(r)
                    if (co >= 0): 
                        continue
                ty = self.get_addr_type(res[i].alt_typ_id)
                if (ty is not None): 
                    co = ty.check_type(r)
                    if (co >= 0): 
                        continue
                del res[i]
        if (res is not None and len(res) > 0): 
            return res
        sr = Utils.asObjectOrNull(r, StreetReferent)
        if (sr is not None and sr.kind == StreetKind.ROAD and sr.number is not None): 
            num = sr.number
            sr.number = None
            res1 = self._get_string_entries(sr, region)
            sr.number = num
            if (res1 is None): 
                return None
            with self.__m_addr_string_tree.m_lock: 
                li = self.__m_addr_string_tree.find(num, False, False)
                if (li is None or li.objs is None): 
                    return None
                res = list()
                for km in li.objs: 
                    ty = self.get_addr_type(km.typ_id)
                    if (ty is None or ty.name != "километр"): 
                        continue
                    for aa in res1: 
                        if (km.parents_id[0] == aa.id0_): 
                            res.append(km)
                            break
                if (len(res) > 0): 
                    return res
        return None
    
    def put_room(self, ro : 'RoomObject') -> bool:
        if (ro.house_id == (0)): 
            return False
        self.__m_room_table.add(ro.id0_, ro)
        return True
    
    def get_room(self, id0__ : int) -> 'RoomObject':
        with self.__m_room_table.m_lock: 
            return self.__m_room_table.get(id0__)
    
    def get_room_params(self, id0__ : int) -> typing.List[tuple]:
        if (self.__m_room_params is None): 
            return None
        with self.__m_room_params.m_lock: 
            return self.__m_room_params.get_params(id0__)
    
    def put_room_params(self, id0__ : int, pars : typing.List[tuple]) -> None:
        if (self.__m_room_params is None): 
            return
        self.__m_room_params.put_params(id0__, pars, False)
    
    def find_room(self, house_id : int, a : 'AddressReferent') -> 'RoomObject':
        if (house_id == 0): 
            return None
        key = FiasHelper.get_room_stringr(a)
        if (key is None): 
            return None
        ho = self.get_house(house_id)
        if (ho is None or ho.room_ids is None): 
            return None
        with self.__m_room_table.m_lock: 
            for id0__ in ho.room_ids: 
                ro = self.__m_room_table.get(id0__)
                if (ro is None): 
                    continue
                if (FiasHelper.get_room_string(ro) == key): 
                    return ro
        return None
    
    # static constructor for class FiasDatabase
    @staticmethod
    def _static_ctor():
        FiasDatabase.__m_param_types = [ParamType.KADASTERNUMBER, ParamType.KLADRCODE, ParamType.OKATO, ParamType.OKTMO, ParamType.POSTINDEX, ParamType.REESTERNUMBER, ParamType.GUID]

FiasDatabase._static_ctor()