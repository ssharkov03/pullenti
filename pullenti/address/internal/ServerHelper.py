# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import xml.etree
import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import WebClient
from pullenti.unisharp.Xml import XmlWriter

from pullenti.address.internal.gar.ParamType import ParamType
from pullenti.address.GarObject import GarObject
from pullenti.address.SearchResult import SearchResult
from pullenti.address.GarStatistic import GarStatistic
from pullenti.address.TextAddress import TextAddress

class ServerHelper:
    
    @staticmethod
    def get_server_version(address_ : str) -> str:
        if (address_ is None): 
            address_ = ServerHelper.SERVER_URI
        try: 
            web = WebClient()
            res = web.download_data(Utils.ifNotNull(address_, "http://localhost:2222"))
            if (res is None or len(res) == 0): 
                return None
            return res.decode("UTF-8", 'ignore')
        except Exception as ex: 
            return None
    
    SERVER_URI = None
    
    @staticmethod
    def get_gar_statistic() -> 'GarStatistic':
        dat = None
        tmp = io.StringIO()
        with XmlWriter.create_string(tmp, None) as wxml: 
            wxml.write_start_element("GetGarStatistic")
            wxml.write_end_element()
        dat = ServerHelper.__get_dat_from_xml(tmp)
        try: 
            web = WebClient()
            dat1 = web.upload_data(ServerHelper.SERVER_URI, dat)
            if (dat1 is None or len(dat1) == 0): 
                return None
            xml0_ = None # new XmlDocument
            rstr = dat1.decode("UTF-8", 'ignore')
            if (len(rstr) < 10): 
                return None
            xml0_ = Utils.parseXmlFromString(rstr)
            res = GarStatistic()
            res.deserialize(xml0_.getroot())
            return res
        except Exception as ex: 
            return None
    
    @staticmethod
    def __get_dat_from_xml(tmp : io.StringIO) -> bytearray:
        i = 10
        while (i < tmp.tell()) and (i < 100): 
            if (Utils.getCharAtStringIO(tmp, i) == '-' and Utils.getCharAtStringIO(tmp, i + 1) == '1' and Utils.getCharAtStringIO(tmp, i + 2) == '6'): 
                Utils.setCharAtStringIO(tmp, i + 1, '8')
                Utils.removeStringIO(tmp, i + 2, 1)
                break
            i += 1
        return Utils.toStringStringIO(tmp).encode("UTF-8", 'ignore')
    
    @staticmethod
    def process_text(txt : str) -> typing.List['TextAddress']:
        dat = None
        tmp = io.StringIO()
        with XmlWriter.create_string(tmp, None) as wxml: 
            wxml.write_start_element("ProcessText")
            wxml.write_string(Utils.ifNotNull(txt, ""))
            wxml.write_end_element()
        dat = ServerHelper.__get_dat_from_xml(tmp)
        try: 
            web = WebClient()
            dat1 = web.upload_data(ServerHelper.SERVER_URI, dat)
            if (dat1 is None or len(dat1) == 0): 
                return None
            xml0_ = None # new XmlDocument
            rstr = dat1.decode("UTF-8", 'ignore')
            xml0_ = Utils.parseXmlFromString(rstr)
            res = list()
            for x in xml0_.getroot(): 
                if (len(x) == 0): 
                    continue
                to = TextAddress()
                to.deserialize(x)
                res.append(to)
            return res
        except Exception as ex: 
            return None
    
    @staticmethod
    def process_single_address_texts(txts : typing.List[str]) -> typing.List['TextAddress']:
        dat = None
        tmp = io.StringIO()
        with XmlWriter.create_string(tmp, None) as wxml: 
            wxml.write_start_element("ProcessSingleAddressTexts")
            for txt in txts: 
                wxml.write_element_string("text", txt)
            wxml.write_end_element()
        dat = ServerHelper.__get_dat_from_xml(tmp)
        try: 
            web = WebClient()
            dat1 = web.upload_data(ServerHelper.SERVER_URI, dat)
            if (dat1 is None or len(dat1) == 0): 
                return None
            xml0_ = None # new XmlDocument
            rstr = dat1.decode("UTF-8", 'ignore')
            if (len(rstr) < 5): 
                return None
            xml0_ = Utils.parseXmlFromString(rstr)
            res = list()
            for x in xml0_.getroot(): 
                if (len(x) == 0): 
                    continue
                r = TextAddress()
                r.deserialize(x)
                res.append(r)
            if (len(res) != len(txts)): 
                return None
            return res
        except Exception as ex: 
            return None
    
    @staticmethod
    def process_single_address_text(txt : str) -> 'TextAddress':
        dat = None
        tmp = io.StringIO()
        with XmlWriter.create_string(tmp, None) as wxml: 
            wxml.write_start_element("ProcessSingleAddressText")
            wxml.write_string(Utils.ifNotNull(txt, ""))
            wxml.write_end_element()
        dat = ServerHelper.__get_dat_from_xml(tmp)
        try: 
            web = WebClient()
            dat1 = web.upload_data(ServerHelper.SERVER_URI, dat)
            if (dat1 is None or len(dat1) == 0): 
                return None
            xml0_ = None # new XmlDocument
            rstr = dat1.decode("UTF-8", 'ignore')
            if (len(rstr) < 5): 
                return None
            xml0_ = Utils.parseXmlFromString(rstr)
            res = TextAddress()
            res.deserialize(xml0_.getroot())
            return res
        except Exception as ex: 
            return None
    
    @staticmethod
    def search_objects(search_pars : 'SearchParams') -> 'SearchResult':
        dat = None
        tmp = io.StringIO()
        with XmlWriter.create_string(tmp, None) as wxml: 
            wxml.write_start_element("SearchObjects")
            search_pars.serialize(wxml)
            wxml.write_end_element()
        dat = ServerHelper.__get_dat_from_xml(tmp)
        try: 
            web = WebClient()
            dat1 = web.upload_data(ServerHelper.SERVER_URI, dat)
            if (dat1 is None or len(dat1) == 0): 
                return None
            xml0_ = None # new XmlDocument
            rstr = dat1.decode("UTF-8", 'ignore')
            if (len(rstr) < 5): 
                return None
            xml0_ = Utils.parseXmlFromString(rstr)
            res = SearchResult()
            res.deserialize(xml0_.getroot())
            return res
        except Exception as ex: 
            return None
    
    @staticmethod
    def get_children_objects(id0_ : str, ignore_houses : bool=False) -> typing.List['GarObject']:
        dat = None
        tmp = io.StringIO()
        with XmlWriter.create_string(tmp, None) as wxml: 
            wxml.write_start_element("GetObjects")
            if (ignore_houses): 
                wxml.write_attribute_string("ignoreHouses", "true")
            if (id0_ is not None): 
                wxml.write_string(id0_)
            wxml.write_end_element()
        dat = ServerHelper.__get_dat_from_xml(tmp)
        try: 
            web = WebClient()
            dat1 = web.upload_data(ServerHelper.SERVER_URI, dat)
            if (dat1 is None or len(dat1) == 0): 
                return None
            xml0_ = None # new XmlDocument
            rstr = dat1.decode("UTF-8", 'ignore')
            xml0_ = Utils.parseXmlFromString(rstr)
            res = list()
            if (len(rstr) < 10): 
                return res
            for x in xml0_.getroot(): 
                go = GarObject(None)
                go.deserialize(x)
                if (go.attrs is not None): 
                    res.append(go)
            return res
        except Exception as ex: 
            return None
    
    @staticmethod
    def get_object(obj_id : str) -> 'GarObject':
        dat = None
        tmp = io.StringIO()
        with XmlWriter.create_string(tmp, None) as wxml: 
            wxml.write_start_element("GetObject")
            wxml.write_string(obj_id)
            wxml.write_end_element()
        dat = ServerHelper.__get_dat_from_xml(tmp)
        try: 
            web = WebClient()
            dat1 = web.upload_data(ServerHelper.SERVER_URI, dat)
            if (dat1 is None or len(dat1) == 0): 
                return None
            xml0_ = None # new XmlDocument
            rstr = dat1.decode("UTF-8", 'ignore')
            if (len(rstr) < 10): 
                return None
            xml0_ = Utils.parseXmlFromString(rstr)
            res = GarObject(None)
            res.deserialize(xml0_.getroot())
            return res
        except Exception as ex: 
            return None
    
    @staticmethod
    def get_object_params(sid : str) -> typing.List[tuple]:
        dat = None
        tmp = io.StringIO()
        with XmlWriter.create_string(tmp, None) as wxml: 
            wxml.write_start_element("GetObjectParams")
            wxml.write_string(sid)
            wxml.write_end_element()
        dat = ServerHelper.__get_dat_from_xml(tmp)
        try: 
            web = WebClient()
            dat1 = web.upload_data(ServerHelper.SERVER_URI, dat)
            if (dat1 is None or len(dat1) == 0): 
                return None
            xml0_ = None # new XmlDocument
            rstr = dat1.decode("UTF-8", 'ignore')
            if (len(rstr) < 10): 
                return None
            xml0_ = Utils.parseXmlFromString(rstr)
            res = dict()
            for x in xml0_.getroot(): 
                try: 
                    ty = Utils.valToEnum(Utils.getXmlLocalName(x), ParamType)
                    if (ty is not None and ty != ParamType.UNDEFINED): 
                        res[ty] = Utils.getXmlInnerText(x)
                except Exception as ex139: 
                    pass
            return res
        except Exception as ex: 
            return None