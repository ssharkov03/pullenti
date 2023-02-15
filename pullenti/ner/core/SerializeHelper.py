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

from pullenti.ner.Referent import Referent
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.ProcessorService import ProcessorService

class SerializeHelper:
    """ Сериализация сущностей """
    
    @staticmethod
    def serialize_referents_to_xml_string(refs : typing.List['Referent'], root_tag_name : str="referents", out_occurences : bool=False) -> str:
        """ Сериализация в строку XML списка сущностей. Сущности могут быть взаимосвязаны,
        то есть значениями атрибутов могут выступать другие сущности (то есть сериализуется по сути граф).
        
        Args:
            refs(typing.List[Referent]): список сериализуемых сущностей
            root_tag_name(str): имя корневого узла
            out_occurences(bool): выводить ли вхождения в текст
        
        Returns:
            str: строка с XML
        """
        id0_ = 1
        for r in refs: 
            r.tag = (id0_)
            id0_ += 1
        res = io.StringIO()
        with XmlWriter.create_string(res, None) as xml0_: 
            xml0_.write_start_element(root_tag_name)
            for r in refs: 
                SerializeHelper.serialize_referent_to_xml(r, xml0_, out_occurences, False)
            xml0_.write_end_element()
        SerializeHelper.__corr_xml_file(res)
        for r in refs: 
            r.tag = None
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def serialize_referent_to_xml_string(r : 'Referent', out_occurences : bool=False) -> str:
        """ Прямая сериализация сущности в строку XML.
        
        Args:
            r(Referent): сериализуемая сущность
            out_occurences(bool): выводить ли вхождения в текст
        """
        res = io.StringIO()
        with XmlWriter.create_string(res, None) as xml0_: 
            SerializeHelper.serialize_referent_to_xml(r, xml0_, out_occurences, True)
        SerializeHelper.__corr_xml_file(res)
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def serialize_referent_to_xml(r : 'Referent', xml0_ : XmlWriter, out_occurences : bool=False, convert_slot_refs_to_string : bool=False) -> None:
        """ Прямая сериализация сущности в XML.
        
        Args:
            r(Referent): сериализуемая сущность
            xml0_(XmlWriter): куда сериализовать
            out_occurences(bool): выводить ли вхождения в текст
            convert_slot_refs_to_string(bool): преобразовывать ли ссылки в слотах на сущноси в строковые значения
        """
        xml0_.write_start_element("referent")
        if (isinstance(r.tag, int)): 
            xml0_.write_attribute_string("id", str(r.tag))
        xml0_.write_attribute_string("typ", r.type_name)
        xml0_.write_attribute_string("spel", SerializeHelper.__corr_xml_value(str(r)))
        for s in r.slots: 
            if (s.value is not None): 
                nam = s.type_name
                xml0_.write_start_element("slot")
                xml0_.write_attribute_string("typ", s.type_name)
                if ((isinstance(s.value, Referent)) and (isinstance(s.value.tag, int))): 
                    xml0_.write_attribute_string("ref", str(s.value.tag))
                if (s.value is not None): 
                    xml0_.write_attribute_string("val", SerializeHelper.__corr_xml_value(str(s.value)))
                if (s.count > 0): 
                    xml0_.write_attribute_string("count", str(s.count))
                xml0_.write_end_element()
        if (out_occurences): 
            for o in r.occurrence: 
                xml0_.write_start_element("occ")
                xml0_.write_attribute_string("begin", str(o.begin_char))
                xml0_.write_attribute_string("end", str(o.end_char))
                xml0_.write_attribute_string("text", SerializeHelper.__corr_xml_value(o.get_text()))
                xml0_.write_end_element()
        xml0_.write_end_element()
    
    @staticmethod
    def __corr_xml_file(res : io.StringIO) -> None:
        i = Utils.toStringStringIO(res).find('>')
        if (i > 10 and Utils.getCharAtStringIO(res, 1) == '?'): 
            Utils.removeStringIO(res, 0, i + 1)
        i = 0
        first_pass2830 = True
        while True:
            if first_pass2830: first_pass2830 = False
            else: i += 1
            if (not (i < res.tell())): break
            ch = Utils.getCharAtStringIO(res, i)
            cod = ord(ch)
            if ((cod < 0x80) and cod >= 0x20): 
                continue
            if (LanguageHelper.is_cyrillic_char(ch)): 
                continue
            Utils.removeStringIO(res, i, 1)
            Utils.insertStringIO(res, i, "&#x{0};".format("{:04X}".format(cod)))
    
    @staticmethod
    def __corr_xml_value(txt : str) -> str:
        if (txt is None): 
            return ""
        for c in txt: 
            if ((((ord(c)) < 0x20) and c != '\r' and c != '\n') and c != '\t'): 
                tmp = Utils.newStringIO(txt)
                i = 0
                while i < tmp.tell(): 
                    ch = Utils.getCharAtStringIO(tmp, i)
                    if ((((ord(ch)) < 0x20) and ch != '\r' and ch != '\n') and ch != '\t'): 
                        Utils.setCharAtStringIO(tmp, i, ' ')
                    i += 1
                return Utils.toStringStringIO(tmp)
        return txt
    
    @staticmethod
    def deserialize_referents_from_xml_string(xml_string : str) -> typing.List['Referent']:
        """ Десериализация списка взаимосвязанных сущностей из строки
        
        Args:
            xml_string(str): результат сериализации функцией SerializeReferentsToXmlString()
        
        Returns:
            typing.List[Referent]: Список экземпляров сущностей
        """
        res = list()
        map0_ = dict()
        try: 
            xml0_ = None # new XmlDocument
            xml0_ = Utils.parseXmlFromString(xml_string)
            for x in xml0_.getroot(): 
                if (Utils.getXmlLocalName(x) == "referent"): 
                    r = SerializeHelper.__deserialize_referent(x)
                    if (r is None): 
                        continue
                    res.append(r)
                    if (isinstance(r.tag, int)): 
                        if (not r.tag in map0_): 
                            map0_[r.tag] = r
        except Exception as ex: 
            return None
        # восстанавливаем ссылки
        for r in res: 
            r.tag = None
            for s in r.slots: 
                if (isinstance(s.tag, int)): 
                    rr = None
                    wraprr728 = RefOutArgWrapper(None)
                    Utils.tryGetValue(map0_, s.tag, wraprr728)
                    rr = wraprr728.value
                    if (rr is not None): 
                        s.value = rr
                    s.tag = None
        return res
    
    @staticmethod
    def deserialize_referent_from_xml_string(xml_string : str) -> 'Referent':
        """ Десериализация сущности из строки XML
        
        Args:
            xml_string(str): результат сериализации функцией SerializeReferentToXmlString()
        
        Returns:
            Referent: Экземпляр сущностей
        """
        try: 
            xml0_ = None # new XmlDocument
            xml0_ = Utils.parseXmlFromString(xml_string)
            return SerializeHelper.__deserialize_referent(xml0_.getroot())
        except Exception as ex: 
            pass
        return None
    
    @staticmethod
    def __deserialize_referent(xml0_ : xml.etree.ElementTree.Element) -> 'Referent':
        typ = None
        id0_ = 0
        if (xml0_.attrib is not None): 
            for a in xml0_.attrib.items(): 
                if (Utils.getXmlAttrLocalName(a) == "id"): 
                    id0_ = int(a[1])
                elif (Utils.getXmlAttrLocalName(a) == "typ"): 
                    typ = a[1]
        if (typ is None): 
            return None
        res = ProcessorService.create_referent(typ)
        if (res is None): 
            return None
        res.tag = (id0_)
        for x in xml0_: 
            if (Utils.getXmlLocalName(x) != "slot"): 
                continue
            nam = None
            val = None
            cou = 0
            refid = 0
            if (x.attrib is not None): 
                for a in x.attrib.items(): 
                    if (Utils.getXmlAttrLocalName(a) == "typ"): 
                        nam = a[1]
                    elif (Utils.getXmlAttrLocalName(a) == "count"): 
                        cou = int(a[1])
                    elif (Utils.getXmlAttrLocalName(a) == "ref"): 
                        refid = int(a[1])
                    elif (Utils.getXmlAttrLocalName(a) == "val"): 
                        val = a[1]
            if (nam is None): 
                continue
            slot = res.add_slot(nam, val, False, 0)
            slot.count = cou
            if (refid > 0): 
                slot.tag = refid
        return res
    
    @staticmethod
    def serialize_referents_to_json_string(refs : typing.List['Referent'], out_occurences : bool=False) -> str:
        """ Сериализация в строку JSON списка сущностей. Сущности могут быть взаимосвязаны,
        то есть значениями атрибутов могут выступать другие сущности (то есть сериализуется по сути граф).
        
        Args:
            refs(typing.List[Referent]): список сериализуемых сущностей
            rootTagName: имя корневого узла
            out_occurences(bool): выводить ли вхождения в текст
        
        Returns:
            str: строка с JSON (массив [...])
        """
        id0_ = 1
        for r in refs: 
            r.tag = (id0_)
            id0_ += 1
        res = io.StringIO()
        print("[", end="", file=res)
        for r in refs: 
            json = SerializeHelper.serialize_referent_to_json_string(r, out_occurences)
            print("\r\n", end="", file=res)
            print(json, end="", file=res)
            if (r != refs[len(refs) - 1]): 
                print(", ", end="", file=res)
        print("\r\n]", end="", file=res)
        for r in refs: 
            r.tag = None
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def serialize_referent_to_json_string(r : 'Referent', out_occurences : bool=False) -> str:
        """ Сериализация сущности в JSON (словарь {...}).
        
        Args:
            r(Referent): сериализуемая сущность
            out_occurences(bool): выводить ли вхождения в текст
        
        Returns:
            str: строка со словарём JSON
        """
        res = io.StringIO()
        print("{", end="", file=res)
        if (isinstance(r.tag, int)): 
            print("\r\n  \"id\" : {0},".format(r.tag), end="", file=res, flush=True)
        print("\r\n  \"typ\" : \"{0}\", ".format(r.type_name), end="", file=res, flush=True)
        print("\r\n  \"spel\" : \"", end="", file=res)
        SerializeHelper.__corr_json_value(str(r), res)
        print("\", ", end="", file=res)
        print("\r\n  \"slots\" : [", end="", file=res)
        i = 0
        while i < len(r.slots): 
            s = r.slots[i]
            print("\r\n      {0} \"typ\" : \"{1}\", ".format('{', s.type_name), end="", file=res, flush=True)
            if (isinstance(s.value, Referent)): 
                print("\"ref\" : {0}, ".format(str(s.value.tag)), end="", file=res, flush=True)
            if (s.value is not None): 
                print("\"val\" : \"", end="", file=res)
            SerializeHelper.__corr_json_value(str(s.value), res)
            print("\"", end="", file=res)
            if (s.count > 0): 
                print(", \"count\" : {0}".format(str(s.count)), end="", file=res, flush=True)
            print(" }", end="", file=res)
            if ((i + 1) < len(r.slots)): 
                print(",", end="", file=res)
            i += 1
        print(" ]", end="", file=res)
        if (out_occurences): 
            print(",\r\n  \"occs\" : [", end="", file=res)
            i = 0
            while i < len(r.occurrence): 
                o = r.occurrence[i]
                print("\r\n      {0} \"begin\" : {1}, \"end\" : {2}, \"text\" : \"".format('{', o.begin_char, o.end_char), end="", file=res, flush=True)
                SerializeHelper.__corr_json_value(o.get_text(), res)
                print("\" }", end="", file=res)
                if ((i + 1) < len(r.occurrence)): 
                    print(",", end="", file=res)
                i += 1
            print(" ]", end="", file=res)
        print("\r\n}", end="", file=res)
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def __corr_json_value(txt : str, res : io.StringIO) -> None:
        for ch in txt: 
            if (ch == '"'): 
                print("\\\"", end="", file=res)
            elif (ch == '\\'): 
                print("\\\\", end="", file=res)
            elif (ch == '/'): 
                print("\\/", end="", file=res)
            elif ((ord(ch)) == 0xD): 
                print("\\r", end="", file=res)
            elif ((ord(ch)) == 0xA): 
                print("\\n", end="", file=res)
            elif (ch == '\t'): 
                print("\\t", end="", file=res)
            elif ((ord(ch)) < 0x20): 
                print(' ', end="", file=res)
            else: 
                print(ch, end="", file=res)