# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.address.GarLevel import GarLevel
from pullenti.address.HouseType import HouseType
from pullenti.address.RoomType import RoomType
from pullenti.address.StroenType import StroenType
from pullenti.address.BaseAttributes import BaseAttributes
from pullenti.address.RoomAttributes import RoomAttributes
from pullenti.ner.fias.FiasAnalyzer import FiasAnalyzer
from pullenti.address.AreaAttributes import AreaAttributes
from pullenti.address.HouseAttributes import HouseAttributes
from pullenti.address.internal.gar.AddressObject import AddressObject

class GarHelper:
    
    REGIONS = None
    
    __m_lock = None
    
    @staticmethod
    def init() -> None:
        GarHelper.REGIONS = list()
        if (FiasAnalyzer.FIAS_DB is None): 
            return
        robj = FiasAnalyzer.FIAS_DB.getao(1)
        if (robj is None): 
            return
        ga = list()
        for id0_ in robj.children_ids: 
            ao = FiasAnalyzer.FIAS_DB.getao(id0_)
            if (ao is None): 
                continue
            if (ao.level != (1)): 
                continue
            g = GarHelper.create_gar_area(ao)
            if ((isinstance(g.attrs, AreaAttributes)) and g.attrs.level == GarLevel.REGION): 
                ga.append(g)
        i = 0
        while i < (len(ga) - 1): 
            j = 0
            while j < (len(ga) - 1): 
                if (ga[j].compareTo(ga[j + 1]) < 0): 
                    h = ga[j]
                    ga[j] = ga[j + 1]
                    ga[j + 1] = h
                j += 1
            i += 1
        for g in ga: 
            GarHelper.REGIONS.append(g)
    
    @staticmethod
    def get_object_actual(sid : str) -> int:
        if (FiasAnalyzer.FIAS_DB is None or Utils.isNullOrEmpty(sid)): 
            return -1
        return FiasAnalyzer.FIAS_DB.get_actual(sid)
    
    @staticmethod
    def get_object_guid(sid : str) -> str:
        go = GarHelper.get_object(sid)
        if (go is None): 
            return None
        return go.guid
    
    @staticmethod
    def get_object_parent_id(sid : str) -> str:
        if (FiasAnalyzer.FIAS_DB is None or Utils.isNullOrEmpty(sid)): 
            return None
        id0_ = FiasAnalyzer.FIAS_DB.get_parent_id(sid)
        if (id0_ == 0): 
            return None
        if (sid[0] == 'r'): 
            if (((id0_ & 0x80000000)) != 0): 
                id0_ &= 0x7FFFFFFF
            return "h{0}".format(id0_)
        return "a{0}".format(id0_)
    
    @staticmethod
    def get_object_level(sid : str) -> 'GarLevel':
        if (sid is None): 
            return GarLevel.UNDEFINED
        iid = 0
        wrapiid110 = RefOutArgWrapper(0)
        inoutres111 = Utils.tryParseInt(sid[1:], wrapiid110)
        iid = wrapiid110.value
        if (not inoutres111): 
            return GarLevel.UNDEFINED
        if (sid[0] == 'a'): 
            ao = FiasAnalyzer.FIAS_DB.getao(iid)
            if (ao is None): 
                return GarLevel.UNDEFINED
            return Utils.valToEnum(ao.level, GarLevel)
        if (sid[0] == 'h'): 
            ho = FiasAnalyzer.FIAS_DB.get_house(iid)
            if (ho is None): 
                return GarLevel.UNDEFINED
            return (GarLevel.PLOT if ho.house_typ == (5) else GarLevel.BUILDING)
        if (sid[0] == 'r'): 
            return GarLevel.ROOM
        return GarLevel.UNDEFINED
    
    @staticmethod
    def get_object(sid : str) -> 'GarObject':
        if (sid is None or FiasAnalyzer.FIAS_DB is None): 
            return None
        iid = 0
        wrapiid112 = RefOutArgWrapper(0)
        inoutres113 = Utils.tryParseInt(sid[1:], wrapiid112)
        iid = wrapiid112.value
        if (not inoutres113): 
            return None
        if (sid[0] == 'a'): 
            ao = FiasAnalyzer.FIAS_DB.getao(iid)
            if (ao is None): 
                return None
            return GarHelper.create_gar_area(ao)
        if (sid[0] == 'h'): 
            ho = FiasAnalyzer.FIAS_DB.get_house(iid)
            if (ho is None): 
                return None
            return GarHelper.create_gar_house(ho)
        if (sid[0] == 'r'): 
            ho = FiasAnalyzer.FIAS_DB.get_room(iid)
            if (ho is None): 
                return None
            return GarHelper.create_gar_room(ho)
        return None
    
    @staticmethod
    def get_object_params(sid : str) -> typing.List[tuple]:
        if (FiasAnalyzer.FIAS_DB is None): 
            return None
        iid = 0
        wrapiid114 = RefOutArgWrapper(0)
        inoutres115 = Utils.tryParseInt(sid[1:], wrapiid114)
        iid = wrapiid114.value
        if (not inoutres115): 
            return None
        if (sid[0] == 'a'): 
            return FiasAnalyzer.FIAS_DB.getaoparams(iid)
        if (sid[0] == 'h'): 
            return FiasAnalyzer.FIAS_DB.get_house_params(iid)
        if (sid[0] == 'r'): 
            return FiasAnalyzer.FIAS_DB.get_room_params(iid)
        return None
    
    @staticmethod
    def get_children_objects(id0_ : str, ignore_houses : bool=False) -> typing.List['GarObject']:
        if (Utils.isNullOrEmpty(id0_)): 
            return GarHelper.REGIONS
        res = GarHelper.get_children_objects_by_id(id0_, ignore_houses)
        if (res is not None): 
            for r in res: 
                r.parent_id = id0_
                if (r.alt_parent_id is not None and r.alt_parent_id == id0_): 
                    r.alt_parent_id = (None)
        return res
    
    @staticmethod
    def get_children_objects_by_id(sid : str, ignore_houses : bool=False) -> typing.List['GarObject']:
        if (FiasAnalyzer.FIAS_DB is None or Utils.isNullOrEmpty(sid)): 
            return None
        res = list()
        iid = 0
        wrapiid116 = RefOutArgWrapper(0)
        inoutres117 = Utils.tryParseInt(sid[1:], wrapiid116)
        iid = wrapiid116.value
        if (not inoutres117): 
            return None
        if (sid[0] == 'a'): 
            ao = FiasAnalyzer.FIAS_DB.getao(iid)
            if (ao is None): 
                return None
            if (ao.children_ids is not None): 
                areas = list()
                houses = list()
                rooms = list()
                for id0_ in ao.children_ids: 
                    mm = (id0_) & (AddressObject.ROOMMASK)
                    if (mm == AddressObject.ROOMMASK): 
                        if (ignore_houses): 
                            continue
                        ro = FiasAnalyzer.FIAS_DB.get_room(((id0_) ^ (AddressObject.ROOMMASK)))
                        if (ro is not None): 
                            rooms.append(ro)
                    elif (mm == AddressObject.HOUSEMASK): 
                        if (ignore_houses): 
                            continue
                        ho = FiasAnalyzer.FIAS_DB.get_house(((id0_) ^ (AddressObject.HOUSEMASK)))
                        if (ho is not None): 
                            houses.append(ho)
                    else: 
                        ch = GarHelper.create_gar_aby_id(id0_)
                        if (ch is not None): 
                            areas.append(ch)
                i = 0
                while i < (len(areas) - 1): 
                    j = 0
                    while j < (len(areas) - 1): 
                        if (areas[j].compareTo(areas[j + 1]) < 0): 
                            h = areas[j]
                            areas[j] = areas[j + 1]
                            areas[j + 1] = h
                        j += 1
                    i += 1
                i = 0
                while i < (len(houses) - 1): 
                    j = 0
                    while j < (len(houses) - 1): 
                        if (houses[j].compareTo(houses[j + 1]) < 0): 
                            h = houses[j]
                            houses[j] = houses[j + 1]
                            houses[j + 1] = h
                        j += 1
                    i += 1
                for a in areas: 
                    res.append(a)
                for h in houses: 
                    gh = GarHelper.create_gar_house(h)
                    if (gh is not None): 
                        res.append(gh)
                for r in rooms: 
                    rh = GarHelper.create_gar_room(r)
                    if (rh is not None): 
                        res.append(rh)
            return res
        if (sid[0] == 'h'): 
            ho = FiasAnalyzer.FIAS_DB.get_house(iid)
            if (ho is None or ho.room_ids is None): 
                return None
            rooms = list()
            for id0_ in ho.room_ids: 
                ro = FiasAnalyzer.FIAS_DB.get_room(id0_)
                if (ro is not None): 
                    rooms.append(ro)
            i = 0
            while i < (len(rooms) - 1): 
                j = 0
                while j < (len(rooms) - 1): 
                    if (rooms[j].compareTo(rooms[j + 1]) > 0): 
                        r = rooms[j]
                        rooms[j] = rooms[j + 1]
                        rooms[j + 1] = r
                    j += 1
                i += 1
            for r in rooms: 
                gr = GarHelper.create_gar_room(r)
                if (gr is not None): 
                    res.append(gr)
        if (sid[0] == 'r'): 
            ho = FiasAnalyzer.FIAS_DB.get_room(iid)
            if (ho is None or ho.children_ids is None): 
                return None
            rooms = list()
            for id0_ in ho.children_ids: 
                ro = FiasAnalyzer.FIAS_DB.get_room(id0_)
                if (ro is not None): 
                    rooms.append(ro)
            i = 0
            while i < (len(rooms) - 1): 
                j = 0
                while j < (len(rooms) - 1): 
                    if (rooms[j].compareTo(rooms[j + 1]) > 0): 
                        r = rooms[j]
                        rooms[j] = rooms[j + 1]
                        rooms[j + 1] = r
                    j += 1
                i += 1
            for r in rooms: 
                gr = GarHelper.create_gar_room(r)
                if (gr is not None): 
                    res.append(gr)
        return res
    
    @staticmethod
    def create_gar_aby_id(id0_ : int) -> 'GarObject':
        aa = FiasAnalyzer.FIAS_DB.getao(id0_)
        if (aa is None): 
            return None
        return GarHelper.create_gar_area(aa)
    
    @staticmethod
    def create_gar_area(a : 'AddressObject') -> 'GarObject':
        from pullenti.address.GarObject import GarObject
        aa = AreaAttributes()
        ga = GarObject(aa)
        ga.id0_ = "a{0}".format(a.id0_)
        aa.names.extend(a.names)
        if (a.typ is not None): 
            aa.types.append(a.typ.name)
        if (a.old_typ is not None): 
            aa.types.append(a.old_typ.name)
        aa.level = (Utils.valToEnum(a.level, GarLevel))
        ga.expired = not a.actual
        ga.guid = a.guid
        if (a.children_ids is not None): 
            ga.children_count = len(a.children_ids)
        if (a.parents_id is not None and len(a.parents_id) > 0): 
            ga.parent_id = "a{0}".format(a.parents_id[0])
            if (a.alt_parent_id != 0 and a.parents_id[0] != a.alt_parent_id): 
                ga.alt_parent_id = "a".format(a.alt_parent_id)
        return ga
    
    @staticmethod
    def create_gar_house(a : 'HouseObject') -> 'GarObject':
        from pullenti.address.GarObject import GarObject
        if (a is None): 
            return None
        sid = "h" + str(a.id0_)
        ha = HouseAttributes()
        ga = GarObject(ha)
        ga.id0_ = sid
        ha.number = a.house_number
        ha.typ = (Utils.valToEnum(a.house_typ, HouseType))
        ha.build_number = a.build_number
        ha.stroen_number = a.struc_number
        ha.stroen_typ = (Utils.valToEnum(a.struc_typ, StroenType))
        ha.level = (GarLevel.PLOT if ha.typ == HouseType.PLOT else GarLevel.BUILDING)
        ga.expired = not a.actual
        ga.guid = a.guid
        if (a.parent_id > 0): 
            ga.parent_id = ("a" + str(a.parent_id))
        ga.children_count = (0 if a.room_ids is None else len(a.room_ids))
        return ga
    
    @staticmethod
    def create_gar_room(a : 'RoomObject') -> 'GarObject':
        from pullenti.address.GarObject import GarObject
        sid = "r" + str(a.id0_)
        ra = RoomAttributes()
        ga = GarObject(ra)
        ga.id0_ = sid
        if (a.room_number is not None): 
            ra.number = a.room_number
            ra.typ = (Utils.valToEnum(a.room_typ, RoomType))
        elif (a.flat_number is not None): 
            ra.number = a.flat_number
            ra.typ = (Utils.valToEnum(a.flat_typ, RoomType))
        ra.level = GarLevel.ROOM
        ga.expired = not a.actual
        ga.guid = a.guid
        if (a.children_ids is not None): 
            ga.children_count = len(a.children_ids)
        if (a.house_id != (0) and (((a.house_id) & 0x80000000)) == 0): 
            ga.parent_id = ("h" + str(a.house_id))
        elif (a.house_id != (0) and (((a.house_id) & 0x80000000)) != 0): 
            id0_ = (a.house_id) & 0x7FFFFFFF
            ga.parent_id = ("h" + str(id0_))
        return ga
    
    @staticmethod
    def can_be_parent(ch : 'GarLevel', par : 'GarLevel', par_is_city : bool) -> bool:
        if (ch == GarLevel.COUNTRY): 
            return False
        if (ch == GarLevel.REGION): 
            return par == GarLevel.COUNTRY
        if (ch == GarLevel.ADMINAREA): 
            return par == GarLevel.COUNTRY or par == GarLevel.REGION
        if (ch == GarLevel.MUNICIPALAREA): 
            return par == GarLevel.COUNTRY or par == GarLevel.REGION
        if (ch == GarLevel.SETTLEMENT): 
            return par == GarLevel.MUNICIPALAREA or par == GarLevel.REGION
        if (ch == GarLevel.CITY): 
            return (par == GarLevel.COUNTRY or par == GarLevel.REGION or par == GarLevel.MUNICIPALAREA) or par == GarLevel.ADMINAREA or par == GarLevel.SETTLEMENT
        if (ch == GarLevel.LOCALITY): 
            if ((par == GarLevel.ADMINAREA or par == GarLevel.MUNICIPALAREA or par == GarLevel.SETTLEMENT) or par == GarLevel.CITY): 
                return True
            if (par == GarLevel.REGION and par_is_city): 
                return True
            if (par == GarLevel.LOCALITY): 
                return True
            return False
        if (ch == GarLevel.AREA): 
            if (par == GarLevel.REGION): 
                return par_is_city
            if ((par == GarLevel.LOCALITY or par == GarLevel.CITY or par == GarLevel.ADMINAREA) or par == GarLevel.MUNICIPALAREA or par == GarLevel.SETTLEMENT): 
                return True
            if (par == GarLevel.AREA): 
                return True
            return False
        if (ch == GarLevel.STREET): 
            if (par == GarLevel.REGION): 
                return par_is_city
            if (par == GarLevel.LOCALITY or par == GarLevel.CITY or par == GarLevel.AREA): 
                return True
            if (par == GarLevel.ADMINAREA): 
                return True
            return False
        if (ch == GarLevel.BUILDING or ch == GarLevel.PLOT): 
            if (par == GarLevel.LOCALITY or par == GarLevel.AREA or par == GarLevel.STREET): 
                return True
            return False
        if (ch == GarLevel.ROOM): 
            if (par == GarLevel.BUILDING): 
                return True
            return False
        if (ch == GarLevel.CARPLACE): 
            pass
        if (ch == GarLevel.SPECIAL): 
            if ((par == GarLevel.STREET or par == GarLevel.AREA or par == GarLevel.LOCALITY) or par == GarLevel.CITY): 
                return True
            if (par == GarLevel.PLOT or par == GarLevel.BUILDING): 
                return True
            return False
        return False
    
    # static constructor for class GarHelper
    @staticmethod
    def _static_ctor():
        GarHelper.REGIONS = list()
        GarHelper.__m_lock = object()

GarHelper._static_ctor()