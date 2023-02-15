# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import pathlib
import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.unisharp.Streams import MemoryStream
from pullenti.unisharp.Streams import FileStream
from pullenti.unisharp.Streams import Stream

from pullenti.util.repository.KeyBaseTable import KeyBaseTable
from pullenti.address.GarLevel import GarLevel
from pullenti.address.HouseType import HouseType
from pullenti.address.internal.RepChildrenTable import RepChildrenTable
from pullenti.address.RoomAttributes import RoomAttributes
from pullenti.address.internal.RepObjTable import RepObjTable
from pullenti.address.internal.RepObjTree import RepObjTree
from pullenti.address.AreaAttributes import AreaAttributes
from pullenti.address.HouseAttributes import HouseAttributes
from pullenti.address.internal.RepAddrTree import RepAddrTree
from pullenti.address.internal.RepTypTable import RepTypTable
from pullenti.address.SpecialAttributes import SpecialAttributes
from pullenti.address.internal.RepaddrSearchObj import RepaddrSearchObj
from pullenti.address.RepaddrObject import RepaddrObject
from pullenti.address.internal.RepAddrTreeNodeObj import RepAddrTreeNodeObj
from pullenti.address.internal.GarHelper import GarHelper

class AddressRepository(object):
    """ Репозиторий адресов (Адрессарий)
    
    """
    
    def __init__(self) -> None:
        self.__m_base_dir = None;
        self.__m_typs = None;
        self.__m_objs = None;
        self.__m_chis = None;
        self.__m_atree = None;
        self.__m_cobjs = None;
        self.__m_otrees = dict()
        self.__m_otree_ids = list()
        self.__m_modified = False
        self.__m_root = None;
    
    def __search(self, addr : 'TextAddress', add_ : bool) -> int:
        path = list()
        house = None
        room = None
        spec = None
        ret = 0
        for a in addr.items: 
            if (isinstance(a.attrs, SpecialAttributes)): 
                spec = a
            elif (isinstance(a.attrs, RoomAttributes)): 
                room = a
            elif (isinstance(a.attrs, HouseAttributes)): 
                house = a
            elif (isinstance(a.attrs, AreaAttributes)): 
                path.append(a)
        if (len(path) == 0): 
            return ret
        if (path[0].attrs.level == GarLevel.COUNTRY or path[0].attrs.level == GarLevel.REGION or path[0].attrs.level == GarLevel.CITY): 
            pass
        else: 
            return -1
        opath = list()
        modif = False
        i = 0
        first_pass2727 = True
        while True:
            if first_pass2727: first_pass2727 = False
            else: i += 1
            if (not (i < len(path))): break
            cur = path[i]
            so = RepaddrSearchObj(cur, self.__m_typs)
            coef = 100
            best = None
            for str0_ in so.search_strs: 
                objs = self.__m_atree.find(str0_)
                if (objs is None or len(objs) == 0): 
                    continue
                for o in objs: 
                    co = so.calc_coef(o, (opath[0] if len(opath) > 0 else None), (opath[1] if len(opath) > 1 else None))
                    if (co < coef): 
                        coef = co
                        best = o
                if (coef == 0): 
                    break
            if (best is None): 
                if (not add_): 
                    return ret
                new_obj = RepaddrObject()
                new_obj.spelling = str(cur)
                new_obj.level = cur.attrs.level
                new_obj.types.extend(cur.attrs.types)
                if (len(opath) > 0): 
                    if (not GarHelper.can_be_parent(new_obj.level, opath[0].level, "город" in opath[0].types)): 
                        continue
                    new_obj.parents = list()
                    new_obj.parents.append(opath[0].id0_)
                new_obj.id0_ = (self.__m_objs.get_max_key() + 1)
                if (len(cur.gars) > 0): 
                    new_obj.gar_guids = list()
                    for g in cur.gars: 
                        new_obj.gar_guids.append(g.guid)
                self.__m_objs.add(new_obj.id0_, new_obj)
                cur.rep_object = new_obj
                best = RepAddrTreeNodeObj()
                best.id0_ = new_obj.id0_
                best.lev = so.lev
                best.typ_ids.extend(so.type_ids)
                best.parents = new_obj.parents
                for str0_ in so.search_strs: 
                    self.__m_atree.add(str0_, best)
                modif = True
                ret += 1
            else: 
                cur.rep_object = self.get_object(best.id0_)
                if (cur.rep_object is None): 
                    continue
                if (add_): 
                    if (best.correct(cur.rep_object, self.__m_typs, (opath[0] if len(opath) > 0 else None))): 
                        self.__m_objs.add(best.id0_, cur.rep_object)
                        modif = True
                    for str0_ in so.search_strs: 
                        if (self.__m_atree.add(str0_, best)): 
                            modif = True
            if (cur.rep_object is not None): 
                opath.insert(0, cur.rep_object)
        if (len(opath) == 0): 
            return ret
        for kk in range(3):
            pid = opath[0].id0_
            tobj = None
            if (kk == 0 and house is not None): 
                tobj = house
            elif (kk == 1 and room is not None): 
                tobj = room
            elif (kk == 2 and spec is not None): 
                tobj = spec
            if (tobj is None): 
                continue
            strs = RepaddrSearchObj.get_search_strings(tobj)
            tree = self.__get_tree(pid)
            if (tree is None): 
                break
            id0_ = 0
            for s in strs: 
                id0_ = tree.find(s)
                if (id0_ > 0): 
                    break
            if (id0_ == 0): 
                if (not add_): 
                    return ret
                new_obj = RepaddrObject()
                new_obj.spelling = str(tobj)
                new_obj.level = (((GarLevel.PLOT if house.attrs.typ == HouseType.PLOT else GarLevel.BUILDING)) if kk == 0 else (GarLevel.ROOM if kk == 1 else GarLevel.SPECIAL))
                if (not GarHelper.can_be_parent(new_obj.level, opath[0].level, "город" in opath[0].types)): 
                    continue
                new_obj.parents = list()
                new_obj.parents.append(pid)
                id0_ = (self.__m_objs.get_max_key() + 1)
                new_obj.id0_ = id0_
                if (len(tobj.gars) > 0): 
                    new_obj.gar_guids = list()
                    for g in tobj.gars: 
                        new_obj.gar_guids.append(g.guid)
                self.__m_objs.add(new_obj.id0_, new_obj)
                tobj.rep_object = new_obj
                ret += 1
                modif = True
            else: 
                tobj.rep_object = self.get_object(id0_)
                if (tobj.rep_object is None): 
                    break
            if (add_): 
                for s in strs: 
                    if (tree.add(s, id0_)): 
                        modif = True
            opath.insert(0, tobj.rep_object)
        if (modif): 
            self.__m_modified = True
            self.__m_objs.flush()
            corr_chi = False
            if (self.__m_root.children is None): 
                self.__m_root.children = list()
            if (not opath[len(opath) - 1].id0_ in self.__m_root.children): 
                self.__m_root.children.append(opath[len(opath) - 1].id0_)
                self.__m_chis.add(1, self.__m_root.children)
                corr_chi = True
            i = 0
            first_pass2728 = True
            while True:
                if first_pass2728: first_pass2728 = False
                else: i += 1
                if (not (i < (len(opath) - 1))): break
                if (opath[i + 1].children is None): 
                    opath[i + 1].children = list()
                if (not GarHelper.can_be_parent(opath[i].level, opath[i + 1].level, "город" in opath[i + 1].types)): 
                    continue
                if (not opath[i].id0_ in opath[i + 1].children): 
                    opath[i + 1].children.append(opath[i].id0_)
                    self.__m_chis.add(opath[i + 1].id0_, opath[i + 1].children)
                    corr_chi = True
            if (corr_chi): 
                self.__m_chis.flush()
        return ret
    
    def open0_(self, path_name : str) -> None:
        """ Открыть репозиторий
        
        Args:
            path_name(str): папка, если папки не существует или пуста, то репозиторий будет в ней создан
        """
        self.__m_base_dir = pathlib.PurePath(path_name).absolute()
        if (not pathlib.Path(self.__m_base_dir).is_dir()): 
            pathlib.Path(self.__m_base_dir).mkdir(exist_ok=True)
        self.__m_typs = RepTypTable(path_name)
        self.__m_typs.open0_(False, 0)
        self.__m_objs = RepObjTable(self.__m_typs, path_name)
        self.__m_objs.open0_(False, 0)
        self.__m_chis = RepChildrenTable(path_name)
        self.__m_chis.open0_(False, 0)
        self.__m_root = self.__m_objs.get(1)
        if (self.__m_root is None): 
            self.__m_root = RepaddrObject()
            self.__m_root.spelling = "Root"
            self.__m_objs.add(1, self.__m_root)
            self.__m_objs.flush()
        else: 
            self.__m_root.children = self.__m_chis.get(1)
        self.__m_atree = RepAddrTree()
        nam = pathlib.PurePath(self.__m_base_dir).joinpath("atree.dat")
        if (pathlib.Path(nam).is_file()): 
            self.__m_atree.open0_(pathlib.Path(nam).read_bytes())
        self.__m_cobjs = KeyBaseTable(None, "cobjs", self.base_dir)
        self.__m_cobjs.open0_(False, 0)
        self.__m_modified = False
    
    @property
    def base_dir(self) -> str:
        """ Директория, в которой расположен репозиторий адресов """
        return self.__m_base_dir
    
    def commit(self) -> None:
        """ Сохранить изменения (вызывать периодически при добавлении больших объёмов,
        а также в конце загрузки) """
        if (not self.__m_modified): 
            return
        if (self.__m_atree is None): 
            return
        nam = pathlib.PurePath(self.__m_base_dir).joinpath("atree.dat")
        with FileStream(nam, "wb") as f: 
            self.__m_atree.save(f)
        self.__m_atree.clear()
        dat = pathlib.Path(nam).read_bytes()
        self.__m_atree.open0_(dat)
        for ot in self.__m_otrees.items(): 
            if (ot[1].modified): 
                dat1 = None
                with MemoryStream() as mem: 
                    ot[1].save(mem)
                    dat1 = mem.toarray()
                self.__m_cobjs.write_key_data(ot[0], dat1)
        self.__m_otrees.clear()
        self.__m_otree_ids.clear()
        self.__m_modified = False
    
    def optimize(self) -> None:
        """ Вызывать в конце длительной загрузки - это займёт некоторое время,
        зато уменьшит размер индекса для оптимизации доступа и поиска. """
        if (self.__m_modified): 
            self.commit()
        if (self.__m_objs is not None): 
            self.__m_objs.optimize(10)
        if (self.__m_chis is not None): 
            self.__m_chis.optimize(10)
        if (self.__m_cobjs is not None): 
            self.__m_cobjs.optimize(10)
    
    def close(self) -> None:
        """ Завершить работу с репозиторием (крайне желательно вызывать в конце) """
        if (self.__m_modified): 
            self.commit()
        if (self.__m_atree is not None): 
            self.__m_atree.clear()
            self.__m_atree = (None)
        for ot in self.__m_otrees.items(): 
            ot[1].clear()
        self.__m_otrees.clear()
        self.__m_otree_ids.clear()
        if (self.__m_chis is not None): 
            self.__m_chis.close()
            self.__m_chis = (None)
        if (self.__m_cobjs is not None): 
            self.__m_cobjs.close()
            self.__m_cobjs = (None)
        if (self.__m_objs is not None): 
            self.__m_objs.close()
            self.__m_objs = (None)
        if (self.__m_typs is not None): 
            self.__m_typs.close()
            self.__m_typs = (None)
    
    def __get_tree(self, id0_ : int) -> 'RepObjTree':
        res = None
        wrapres140 = RefOutArgWrapper(None)
        inoutres141 = Utils.tryGetValue(self.__m_otrees, id0_, wrapres140)
        res = wrapres140.value
        if (inoutres141): 
            if (self.__m_otree_ids[0] != id0_): 
                self.__m_otree_ids.remove(id0_)
                self.__m_otree_ids.insert(0, id0_)
            return res
        if (len(self.__m_otrees) >= 100): 
            id1 = self.__m_otree_ids[len(self.__m_otree_ids) - 1]
            if (self.__m_otrees[id1].modified): 
                dat1 = None
                with MemoryStream() as mem: 
                    self.__m_otrees[id1].save(mem)
                    dat1 = mem.toarray()
                self.__m_cobjs.write_key_data(id1, dat1)
            del self.__m_otrees[id1]
            del self.__m_otree_ids[len(self.__m_otree_ids) - 1]
        res = RepObjTree()
        dat = self.__m_cobjs.read_key_data(id0_, 0)
        if (dat is not None): 
            res.open0_(dat)
        self.__m_otrees[id0_] = res
        self.__m_otree_ids.insert(0, id0_)
        return res
    
    def get_max_id(self) -> int:
        """ Максимальный идентификатор (равен общему количеству элементов)
        
        """
        if (self.__m_objs is None): 
            return 0
        return self.__m_objs.get_max_key()
    
    def get_object(self, id0_ : int) -> 'RepaddrObject':
        """ Получить объект по его идентификатору
        
        Args:
            id0_(int): идентификатор
        
        Returns:
            RepaddrObject: объект или null
        """
        if (self.__m_objs is None): 
            return None
        res = self.__m_objs.get(id0_)
        if (res is None): 
            return None
        res.children = self.__m_chis.get(id0_)
        return res
    
    def get_objects(self, ro : 'RepaddrObject') -> typing.List['RepaddrObject']:
        """ Получить экземпляры дочерних объектов объекта
        
        Args:
            ro(RepaddrObject): родительский объект (если null, то вернёт объекты первого уровня)
        
        Returns:
            typing.List[RepaddrObject]: список дочерних объектов RepaddrObject
        """
        if (ro is None): 
            return None
        res = list()
        if (ro is None): 
            if (self.__m_root is None): 
                return None
            if (self.__m_root.children is not None): 
                for id0_ in self.__m_root.children: 
                    o = self.get_object(id0_)
                    if (o is not None): 
                        res.append(o)
        elif (ro.children is not None): 
            for id0_ in ro.children: 
                o = self.get_object(id0_)
                if (o is not None): 
                    res.append(o)
        AddressRepository.__sort(res)
        return res
    
    @staticmethod
    def __sort(res : typing.List['RepaddrObject']) -> None:
        i = 0
        while i < len(res): 
            ch = False
            j = 0
            while j < (len(res) - 1): 
                if (res[j].compareTo(res[j + 1]) > 0): 
                    r = res[j]
                    res[j] = res[j + 1]
                    res[j + 1] = r
                    ch = True
                j += 1
            if (not ch): 
                break
            i += 1
    
    def add(self, addr : 'TextAddress') -> int:
        """ Добавить адрес (всю иерархию) в репозиторий. У элементов будут
        устанавливаться поля RepObject с информацией о сохранении.
        
        Args:
            addr(TextAddress): адресный элемент нижнего уровня
        
        Returns:
            int: Количество новых добавленных объектов
        """
        if (self.__m_atree is None): 
            return 0
        return self.__search(addr, True)
    
    def search(self, addr : 'TextAddress') -> None:
        """ Без добавления попытаться привязать существующие элементы
        (для кого удалось - устанавливается поле RepObject)
        
        Args:
            addr(TextAddress): адресный элемент нижнего уровня
        """
        if (self.__m_atree is None): 
            return
        self.__search(addr, False)
    def __enter__(self): return self
    def __exit__(self, typ, val, traceback): self.close()