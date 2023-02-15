# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import xml.etree
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Xml import XmlWriter

from pullenti.address.GarObject import GarObject
from pullenti.address.SearchParams import SearchParams

class SearchResult:
    """ Результат поискового запроса """
    
    def __init__(self) -> None:
        self.params = None;
        self.total_count = 0
        self.objects = list()
    
    def __str__(self) -> str:
        return "{0} = {1} item(s)".format(("?" if self.params is None else str(self.params)), self.total_count)
    
    def serialize(self, xml0_ : XmlWriter) -> None:
        xml0_.write_start_element("searchresult")
        if (self.params is not None): 
            self.params.serialize(xml0_)
        xml0_.write_element_string("total", str(self.total_count))
        for o in self.objects: 
            o.serialize(xml0_)
        xml0_.write_end_element()
    
    def deserialize(self, xml0_ : xml.etree.ElementTree.Element) -> None:
        for x in xml0_: 
            if (Utils.getXmlLocalName(x) == "seearchparams"): 
                self.params = SearchParams()
                self.params.deserialize(x)
            elif (Utils.getXmlLocalName(x) == "total"): 
                self.total_count = int(Utils.getXmlInnerText(x))
            else: 
                go = GarObject(None)
                go.deserialize(x)
                self.objects.append(go)
    
    @staticmethod
    def _new77(_arg1 : 'SearchParams') -> 'SearchResult':
        res = SearchResult()
        res.params = _arg1
        return res