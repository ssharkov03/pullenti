# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
import io
import xml.etree
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.unisharp.Xml import XmlWriter

from pullenti.address.BaseAttributes import BaseAttributes
from pullenti.address.internal.FiasHelper import FiasHelper
from pullenti.address.RoomAttributes import RoomAttributes
from pullenti.address.HouseAttributes import HouseAttributes
from pullenti.address.AreaAttributes import AreaAttributes
from pullenti.address.AddressHelper import AddressHelper
from pullenti.address.GarParam import GarParam
from pullenti.address.internal.gar.ParamType import ParamType
from pullenti.address.internal.GarHelper import GarHelper

class GarObject(object):
    """ Адресный объект ГАР
    
    """
    
    def __init__(self, attrs_ : 'BaseAttributes') -> None:
        self.attrs = None;
        self.expired = False
        self.guid = None;
        self.id0_ = None;
        self.parent_id = None;
        self.alt_parent_id = None;
        self.tag = None;
        self.children_count = 0
        self.__m_params = None
        self.attrs = attrs_
    
    def get_region_number(self) -> int:
        """ Получить номер региона
        
        Returns:
            int: номер региона или 0
        """
        go = self
        while go is not None: 
            val = go.get_param_value(GarParam.KLADRCODE)
            if (val is not None and len(val) >= 2 and (str.isdigit(val[0]) & str.isdigit(val[1]))): 
                return ((((ord(val[0])) - (ord('0')))) * 10) + (((ord(val[1])) - (ord('0'))))
            go = AddressService.get_object(go.parent_id)
        return 0
    
    def __str__(self) -> str:
        if (self.attrs is None): 
            return "?"
        return str(self.attrs)
    
    def get_param_value(self, ty : 'GarParam') -> str:
        """ Получить значение параметра (код КЛАДР, почтовый индекс и т.п.)
        
        Args:
            ty(GarParam): тип параметра
        
        Returns:
            str: значение или null
        """
        if (ty == GarParam.GUID): 
            return self.guid
        self.__load_params()
        res = None
        wrapres151 = RefOutArgWrapper(None)
        inoutres152 = Utils.tryGetValue(self.__m_params, ty, wrapres151)
        res = wrapres151.value
        if (self.__m_params is not None and inoutres152): 
            return res
        return None
    
    def get_params(self) -> typing.List[tuple]:
        """ Получить все параметры
        
        """
        self.__load_params()
        return self.__m_params
    
    def out_info(self, res : io.StringIO) -> None:
        """ Вывести подробную текстовую информацию об объекте (для отладки)
        
        Args:
            res(io.StringIO): куда выводить
        """
        self.attrs.out_info(res)
        print("\r\nУровень: {0} - {1}\r\n".format(self.attrs.level, AddressHelper.get_level_string(self.attrs.level)), end="", file=res, flush=True)
        if (self.expired): 
            print("Актуальность: НЕТ\r\n".format(), end="", file=res, flush=True)
        print("GUID: {0}\r\n".format(Utils.ifNotNull(self.guid, "?")), end="", file=res, flush=True)
        if (self.__m_params is None): 
            self.__load_params()
        if (self.__m_params is not None): 
            for p in self.__m_params.items(): 
                print("{0}: {1}\r\n".format(Utils.enumToString(p[0]), p[1]), end="", file=res, flush=True)
        print("Полный путь: {0}\r\n".format(self.get_full_path(" ", False)), end="", file=res, flush=True)
    
    def __load_params(self) -> None:
        from pullenti.address.internal.ServerHelper import ServerHelper
        if (self.__m_params is not None): 
            return
        self.__m_params = dict()
        pars = None
        if (ServerHelper.SERVER_URI is not None): 
            pars = ServerHelper.get_object_params(self.id0_)
        else: 
            pars = GarHelper.get_object_params(self.id0_)
        if (pars is not None): 
            for kp in pars.items(): 
                if (kp[0] != ParamType.GUID): 
                    self.__m_params[Utils.valToEnum(kp[0], GarParam)] = kp[1]
    
    def get_full_path(self, delim : str=" ", correct : bool=False) -> str:
        """ Получить полную строку адреса с учётом родителей
        
        Args:
            delim(str): разделитель
        
        Returns:
            str: результат
        """
        path = list()
        o = self
        while o is not None: 
            path.insert(0, o)
            o = AddressService.get_object(o.parent_id)
        tmp = io.StringIO()
        i = 0
        while i < len(path): 
            if (i > 0): 
                print(delim, end="", file=tmp)
            if (correct and (isinstance(path[i].attrs, AreaAttributes))): 
                a = Utils.asObjectOrNull(path[i].attrs, AreaAttributes)
                if (len(a.names) > 0): 
                    print("{0} {1}".format(("?" if len(a.types) > 0 else a.types[0]), FiasHelper.correct_fias_name((a.names[0] if len(a.names) > 0 else "?"))), end="", file=tmp, flush=True)
            else: 
                print(str(path[i].attrs), end="", file=tmp)
            i += 1
        return Utils.toStringStringIO(tmp)
    
    def serialize(self, xml0_ : XmlWriter) -> None:
        xml0_.write_start_element("gar")
        xml0_.write_element_string("id", self.id0_)
        if (self.parent_id is not None): 
            xml0_.write_element_string("parent", self.parent_id)
        if (self.alt_parent_id is not None): 
            xml0_.write_element_string("altparent", self.alt_parent_id)
        xml0_.write_element_string("guid", Utils.ifNotNull(self.guid, ""))
        if (self.expired): 
            xml0_.write_element_string("expired", "true")
        if (self.children_count > 0): 
            xml0_.write_element_string("chcount", str(self.children_count))
        self.attrs.serialize(xml0_)
        xml0_.write_end_element()
    
    def deserialize(self, xml0_ : xml.etree.ElementTree.Element) -> None:
        for x in xml0_: 
            if (Utils.getXmlLocalName(x) == "id"): 
                self.id0_ = Utils.getXmlInnerText(x)
            elif (Utils.getXmlLocalName(x) == "parent"): 
                self.parent_id = Utils.getXmlInnerText(x)
            elif (Utils.getXmlLocalName(x) == "altparent"): 
                self.alt_parent_id = Utils.getXmlInnerText(x)
            elif (Utils.getXmlLocalName(x) == "guid"): 
                self.guid = Utils.getXmlInnerText(x)
            elif (Utils.getXmlLocalName(x) == "expired"): 
                self.expired = Utils.getXmlInnerText(x) == "true"
            elif (Utils.getXmlLocalName(x) == "chcount"): 
                self.children_count = int(Utils.getXmlInnerText(x))
            elif (Utils.getXmlLocalName(x) == "area"): 
                self.attrs = (AreaAttributes())
                self.attrs.deserialize(x)
            elif (Utils.getXmlLocalName(x) == "house"): 
                self.attrs = (HouseAttributes())
                self.attrs.deserialize(x)
            elif (Utils.getXmlLocalName(x) == "room"): 
                self.attrs = (RoomAttributes())
                self.attrs.deserialize(x)
    
    def compareTo(self, other : 'GarObject') -> int:
        if ((self.attrs.level) < (other.attrs.level)): 
            return -1
        if ((self.attrs.level) > (other.attrs.level)): 
            return 1
        aa1 = Utils.asObjectOrNull(self.attrs, AreaAttributes)
        aa2 = Utils.asObjectOrNull(other.attrs, AreaAttributes)
        if (aa1 is not None and aa2 is not None): 
            if (len(aa1.names) > 0 and len(aa2.names) > 0): 
                return Utils.compareStrings(aa1.names[0], aa2.names[0], False)
        return Utils.compareStrings(str(self), str(other), False)