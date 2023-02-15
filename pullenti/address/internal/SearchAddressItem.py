# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import xml.etree
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Xml import XmlWriter

from pullenti.address.internal.SearchLevel import SearchLevel

class SearchAddressItem(object):
    
    def __init__(self) -> None:
        self.level = SearchLevel.UNDEFINED
        self.id0_ = None;
        self.text = None;
        self.parent = None;
        self.search = False
        self.tag = None;
    
    def __str__(self) -> str:
        return "{0}{1}: {2}".format(("?" if self.search else ""), self.level, self.text)
    
    def serialize(self, xml0_ : XmlWriter) -> None:
        xml0_.write_start_element("item")
        xml0_.write_attribute_string("level", str(self.level))
        if (self.id0_ is not None): 
            xml0_.write_attribute_string("id", self.id0_)
        if (self.text is not None): 
            xml0_.write_attribute_string("text", self.text)
        if (self.search): 
            xml0_.write_attribute_string("search", "true")
        if (self.parent is not None): 
            self.parent.serialize(xml0_)
        xml0_.write_end_element()
    
    def deserialize(self, xml0_ : xml.etree.ElementTree.Element) -> None:
        if (xml0_.attrib is not None): 
            for a in xml0_.attrib.items(): 
                if (Utils.getXmlAttrLocalName(a) == "level"): 
                    self.level = (int(a[1]))
                elif (Utils.getXmlAttrLocalName(a) == "id"): 
                    self.id0_ = a[1]
                elif (Utils.getXmlAttrLocalName(a) == "text"): 
                    self.text = a[1]
                elif (Utils.getXmlAttrLocalName(a) == "search"): 
                    self.search = a[1] == "true"
        for x in xml0_: 
            if (Utils.getXmlLocalName(x) == "item"): 
                self.parent = SearchAddressItem()
                self.parent.deserialize(x)
    
    def compareTo(self, other : 'SearchAddressItem') -> int:
        i = Utils.compareStrings(self.text, other.text, False)
        if (i != 0): 
            return i
        if (self.parent is not None and other.parent is not None): 
            return self.parent.compareTo(other.parent)
        if (self.parent is None and other.parent is not None): 
            return -1
        if (self.parent is not None and other.parent is None): 
            return 1
        return 0
    
    @staticmethod
    def _new78(_arg1 : 'SearchLevel', _arg2 : str) -> 'SearchAddressItem':
        res = SearchAddressItem()
        res.level = _arg1
        res.id0_ = _arg2
        return res
    
    @staticmethod
    def _new79(_arg1 : 'SearchLevel', _arg2 : str) -> 'SearchAddressItem':
        res = SearchAddressItem()
        res.level = _arg1
        res.text = _arg2
        return res
    
    @staticmethod
    def _new86(_arg1 : str, _arg2 : object, _arg3 : 'SearchLevel', _arg4 : 'SearchAddressItem', _arg5 : str) -> 'SearchAddressItem':
        res = SearchAddressItem()
        res.id0_ = _arg1
        res.tag = _arg2
        res.level = _arg3
        res.parent = _arg4
        res.text = _arg5
        return res
    
    @staticmethod
    def _new87(_arg1 : str, _arg2 : object, _arg3 : 'SearchLevel', _arg4 : str) -> 'SearchAddressItem':
        res = SearchAddressItem()
        res.id0_ = _arg1
        res.tag = _arg2
        res.level = _arg3
        res.text = _arg4
        return res
    
    @staticmethod
    def _new89(_arg1 : str, _arg2 : 'SearchLevel', _arg3 : str) -> 'SearchAddressItem':
        res = SearchAddressItem()
        res.id0_ = _arg1
        res.level = _arg2
        res.text = _arg3
        return res
    
    @staticmethod
    def _new90(_arg1 : str) -> 'SearchAddressItem':
        res = SearchAddressItem()
        res.text = _arg1
        return res