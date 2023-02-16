# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import xml.etree
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Xml import XmlWriter

from pullenti.address.TextObject import TextObject

class TextAddress:
    """ Полный адрес, выделяемый из текста
    
    """
    
    def __init__(self) -> None:
        self.items = list()
        self.begin_char = 0
        self.end_char = 0
        self.coef = 0
        self.coef_without_house = 0
        self.coef_pure_text = 0
        self.error_message = None;
        self.milliseconds = 0
        self.text = None;
    
    @property
    def last_item(self) -> 'TextObject':
        """ Последний (самый низкоуровневый) элемент адреса """
        if (len(self.items) == 0): 
            return None
        return self.items[0]
    
    @property
    def last_item_with_gar(self) -> 'TextObject':
        """ Самый низкоуровневый объект, который удалось привязать к ГАР """
        for i in range(len(self.items) - 1, -1, -1):
            if (len(self.items[i].gars) > 0): 
                return self.items[i]
        return None
    
    def find_item(self, lev : 'GarLevel') -> 'TextObject':
        """ Найти элемент конкретного уровня
        
        Args:
            lev(GarLevel): 
        
        """
        for it in self.items: 
            if (it.attrs is not None and it.attrs.level == lev): 
                return it
        return None
    
    def __str__(self) -> str:
        res = io.StringIO()
        print("Coef={0}({1}): ".format(self.coef, self.coef_pure_text), end="", file=res, flush=True)
        i = 0
        while i < len(self.items): 
            if (i > 0): 
                print(", ", end="", file=res)
            print(str(self.items[i]), end="", file=res)
            i += 1
        return Utils.toStringStringIO(res)
    
    def get_full_path(self, delim : str=" ") -> str:
        """ Вывести полный путь
        
        Args:
            delim(str): разделитель, пробел по умолчанию
        
        """
        tmp = io.StringIO()
        i = 0
        while i < len(self.items): 
            if (i > 0): 
                print(delim, end="", file=tmp)
            print(str(self.items[i]), end="", file=tmp)
            i += 1
        return Utils.toStringStringIO(tmp)
    
    def out_info(self, res : io.StringIO) -> None:
        """ Вывести подробную текстовую информацию об объекте (для отладки)
        
        Args:
            res(io.StringIO): 
        """
        print("Позиция в тексте: [{0}..{1}]\r\n".format(self.begin_char, self.end_char), end="", file=res, flush=True)
        print("Коэффициент привязки к ГАР: {0}\r\n".format(self.coef), end="", file=res, flush=True)
        print("Коэффициент привязки (без домов): {0}\r\n".format(self.coef_without_house), end="", file=res, flush=True)
        print("Коэффициент без привязки: {0}\r\n".format(self.coef_pure_text), end="", file=res, flush=True)
        if (self.error_message is not None): 
            print("Ошибка: {0}\r\n".format(self.error_message), end="", file=res, flush=True)
        for i in range(len(self.items) - 1, -1, -1):
            print("\r\n", end="", file=res)
            self.items[i].out_info(res)
    
    def serialize(self, xml0_ : XmlWriter, tag : str=None) -> None:
        xml0_.write_start_element("textaddr")
        xml0_.write_element_string("coef", str(self.coef))
        xml0_.write_element_string("coef1", str(self.coef_without_house))
        xml0_.write_element_string("coef2", str(self.coef_pure_text))
        if (self.error_message is not None): 
            xml0_.write_element_string("message", self.error_message)
        xml0_.write_element_string("text", Utils.ifNotNull(self.text, ""))
        xml0_.write_element_string("ms", str(self.milliseconds))
        xml0_.write_element_string("begin", str(self.begin_char))
        xml0_.write_element_string("end", str(self.end_char))
        for o in self.items: 
            o.serialize(xml0_)
        xml0_.write_end_element()
    
    def deserialize(self, xml0_ : xml.etree.ElementTree.Element) -> None:
        for x in xml0_: 
            if (Utils.getXmlLocalName(x) == "coef"): 
                self.coef = int(Utils.getXmlInnerText(x))
            elif (Utils.getXmlLocalName(x) == "coef1"): 
                self.coef_without_house = int(Utils.getXmlInnerText(x))
            elif (Utils.getXmlLocalName(x) == "coef2"): 
                self.coef_pure_text = int(Utils.getXmlInnerText(x))
            elif (Utils.getXmlLocalName(x) == "ms"): 
                self.milliseconds = int(Utils.getXmlInnerText(x))
            elif (Utils.getXmlLocalName(x) == "message"): 
                self.error_message = Utils.getXmlInnerText(x)
            elif (Utils.getXmlLocalName(x) == "text"): 
                self.text = Utils.getXmlInnerText(x)
            elif (Utils.getXmlLocalName(x) == "begin"): 
                self.begin_char = int(Utils.getXmlInnerText(x))
            elif (Utils.getXmlLocalName(x) == "end"): 
                self.end_char = int(Utils.getXmlInnerText(x))
            elif (Utils.getXmlLocalName(x) == "textobj"): 
                to = TextObject(None)
                to.deserialize(x)
                self.items.append(to)
    
    @staticmethod
    def _new144(_arg1 : str, _arg2 : str) -> 'TextAddress':
        res = TextAddress()
        res.error_message = _arg1
        res.text = _arg2
        return res