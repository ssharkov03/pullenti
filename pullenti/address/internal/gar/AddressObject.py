# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

from pullenti.address.internal.NameAnalyzer import NameAnalyzer
from pullenti.address.internal.gar.HouseObject import HouseObject
from pullenti.address.internal.gar.AddressObjectStatus import AddressObjectStatus

class AddressObject(object):
    """ Адресный объект ГАР ФИАС """
    
    def __init__(self) -> None:
        self.id0_ = 0
        self.parents_id = list()
        self.alt_parent_id = 0
        self.typ = None;
        self.names = list()
        self.old_typ = None;
        self.unom = 0
        self.level = 0
        self.actual = False
        self.has_sec_object = False
        self.region = 0
        self.guid = None;
        self.status = AddressObjectStatus.OK
        self.children_ids = list()
        self.tag = None;
        self._parent = None;
    
    HOUSEMASK = 0x80000000
    
    ROOMMASK = 0xC0000000
    
    def __str__(self) -> str:
        res = io.StringIO()
        if (self.id0_ > 0): 
            print("{0}: ".format(self.id0_), end="", file=res, flush=True)
        if (not self.actual): 
            print("(*) ", end="", file=res)
        if (self.has_sec_object): 
            print("(+) ", end="", file=res)
        print("[{0}] ".format(self.level), end="", file=res, flush=True)
        if (self.typ is not None): 
            print("{0} ".format(self.typ.name), end="", file=res, flush=True)
        if (self.old_typ is not None): 
            print("(уст. {0}) ".format(self.old_typ.name), end="", file=res, flush=True)
        i = 0
        while i < len(self.names): 
            print("{0}{1}".format(("/" if i > 0 else ""), self.names[i]), end="", file=res, flush=True)
            i += 1
        return Utils.toStringStringIO(res)
    
    def _merge_with(self, ao : 'AddressObject') -> None:
        if (ao.actual == self.actual or ((self.actual and not ao.actual))): 
            for n in ao.names: 
                if (not n in self.names): 
                    self.names.append(n)
            if (ao.old_typ is not None and self.old_typ is None): 
                self.old_typ = ao.old_typ
            elif (self.typ is not None and ao.typ != self.typ and self.old_typ is None): 
                self.old_typ = ao.typ
            if (ao.level > (0) and self.level == (0)): 
                self.level = ao.level
        elif (not self.actual and ao.actual): 
            self.actual = True
            nams = list(ao.names)
            for n in self.names: 
                if (not n in nams): 
                    nams.append(n)
            self.names = nams
            if (self.typ != ao.typ): 
                self.old_typ = self.typ
                self.typ = ao.typ
            self.level = ao.level
        else: 
            pass
    
    def compareTo(self, other : 'AddressObject') -> int:
        if (self.level < other.level): 
            return -1
        if (self.level > other.level): 
            return 1
        if (len(self.names) > 0 and len(other.names) > 0): 
            i = HouseObject._comp_nums(self.names[0], other.names[0])
            if (i != 0): 
                return i
        return 0
    
    def out_info(self, tmp : io.StringIO, db : 'FiasDatabase'=None) -> None:
        print("Id: {0}\r\nLevel: {1}".format((str(self.unom) if self.unom > 0 else str(self.id0_)), self.level), end="", file=tmp, flush=True)
        if (not self.actual): 
            print("\r\nActual: no", end="", file=tmp)
        if (self.typ is not None): 
            print("\r\nTyp: {0} ".format(self.typ.name), end="", file=tmp, flush=True)
            if (self.old_typ is not None): 
                print(" (ранее: {0})".format(self.old_typ.name), end="", file=tmp, flush=True)
        print("\r\nName: ".format(), end="", file=tmp, flush=True)
        i = 0
        while i < len(self.names): 
            print("{0}\"{1}\"".format((" | " if i > 0 else ""), self.names[i]), end="", file=tmp, flush=True)
            i += 1
        if (db is not None): 
            pars = db.getaoparams(self.id0_)
            if (pars is not None): 
                for kp in pars.items(): 
                    print("\r\n{0}: {1} ".format(Utils.enumToString(kp[0]), kp[1]), end="", file=tmp, flush=True)
        print("\r\n\r\n", end="", file=tmp)
        self.out_analyze_info(tmp)
    
    def out_analyze_info(self, tmp : io.StringIO) -> None:
        print("Анализ => ".format(), end="", file=tmp, flush=True)
        if (self.typ is None): 
            print("нет типа", end="", file=tmp)
            return
        are = NameAnalyzer()
        are.process(self.names, self.typ.name, None)
        if (are is None or are.res == AddressObjectStatus.ERROR): 
            print("ошибка", end="", file=tmp)
        else: 
            if (are.typ is not None): 
                print("{0} ".format(are.typ), end="", file=tmp, flush=True)
            if (are.entry_strings is not None and len(are.entry_strings) > 0): 
                print("<", end="", file=tmp)
                i = 0
                while i < len(are.entry_strings): 
                    print("{0}{1}".format((", " if i > 0 else ""), are.entry_strings[i]), end="", file=tmp, flush=True)
                    i += 1
                print(">", end="", file=tmp)
            if (are.sec is not None): 
                print(" + {0} <".format(Utils.ifNotNull(are.sec.typ, "?")), end="", file=tmp, flush=True)
                i = 0
                while i < len(are.sec.entry_strings): 
                    print("{0}{1}".format((", " if i > 0 else ""), are.sec.entry_strings[i]), end="", file=tmp, flush=True)
                    i += 1
                print(">", end="", file=tmp)
            if (are.res == AddressObjectStatus.WARNING): 
                print(" (неточность)", end="", file=tmp)
            else: 
                print(" (ОК)", end="", file=tmp)
    
    @staticmethod
    def _new45(_arg1 : int) -> 'AddressObject':
        res = AddressObject()
        res.id0_ = _arg1
        return res