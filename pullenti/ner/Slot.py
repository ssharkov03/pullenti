# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

from pullenti.morph.MorphLang import MorphLang
from pullenti.ner.Referent import Referent
from pullenti.ner.TextAnnotation import TextAnnotation
from pullenti.ner.Token import Token

class Slot:
    """ Значение атрибута в конкретном экземпляре сущности
    
    Атрибут сущности
    """
    
    def __init__(self) -> None:
        self.__typename = None;
        self.__owner = None;
        self.__m_value = None;
        self.__count = 0
        self.occurrence = None;
        self.__tag = None;
    
    @property
    def type_name(self) -> str:
        """ Имя атрибута """
        return self.__typename
    @type_name.setter
    def type_name(self, value_) -> str:
        self.__typename = value_
        return self.__typename
    
    @property
    def is_internal(self) -> bool:
        return self.type_name is not None and self.type_name[0] == '@'
    
    @property
    def owner(self) -> 'Referent':
        """ Ссылка на сущность-владельца """
        return self.__owner
    @owner.setter
    def owner(self, value_) -> 'Referent':
        self.__owner = value_
        return self.__owner
    
    @property
    def value(self) -> object:
        """ Значение атрибута """
        return self.__m_value
    @value.setter
    def value(self, value_) -> object:
        self.__m_value = value_
        if (self.__m_value is not None): 
            if (isinstance(self.__m_value, Referent)): 
                pass
            elif (isinstance(self.__m_value, Token)): 
                pass
            elif (isinstance(self.__m_value, str)): 
                pass
            else: 
                self.__m_value = (str(self.__m_value))
        else: 
            pass
        return value_
    
    @property
    def count(self) -> int:
        """ Статистика встречаемости в сущности, когда сущность в нескольких местах текста.
        Используется, например, для имён организаций, чтобы статистически определить
        правильное написание имени. """
        return self.__count
    @count.setter
    def count(self, value_) -> int:
        self.__count = value_
        return self.__count
    
    def add_annotation(self, a : 'MetaToken') -> None:
        if (a is None): 
            return
        if (self.occurrence is None): 
            self.occurrence = list()
        for o in self.occurrence: 
            if (o.begin_char == a.begin_char and o.end_char == a.end_char): 
                return
        self.occurrence.append(TextAnnotation(a.begin_token, a.end_token))
    
    def merge_occurence(self, s : 'Slot') -> None:
        if (s.occurrence is not None): 
            if (self.occurrence is None): 
                self.occurrence = list()
            self.occurrence.extend(s.occurrence)
    
    @property
    def defining_feature(self) -> 'Feature':
        """ Ссылка на атрибут метамодели """
        if (self.owner is None): 
            return None
        if (self.owner.instance_of is None): 
            return None
        return self.owner.instance_of.find_feature(self.type_name)
    
    def __str__(self) -> str:
        return self.to_string_ex(MorphLang.UNKNOWN)
    
    def to_string_ex(self, lang : 'MorphLang') -> str:
        res = io.StringIO()
        attr = self.defining_feature
        if (attr is not None): 
            if (self.count > 0): 
                print("{0} ({1}): ".format(attr.caption, self.count), end="", file=res, flush=True)
            else: 
                print("{0}: ".format(attr.caption), end="", file=res, flush=True)
        else: 
            print("{0}: ".format(self.type_name), end="", file=res, flush=True)
        if (self.value is not None): 
            if (isinstance(self.value, Referent)): 
                print(self.value.to_string_ex(False, lang, 0), end="", file=res)
            elif (attr is None): 
                print(str(self.value), end="", file=res)
            else: 
                print(attr.convert_inner_value_to_outer_value(str(self.value), None), end="", file=res)
        return Utils.toStringStringIO(res)
    
    def convert_value_to_string(self, lang : 'MorphLang') -> str:
        """ Преобразовать внутреннее значение в строку указанного языка
        
        Args:
            lang(MorphLang): язык
        
        Returns:
            str: значение
        """
        if (self.value is None): 
            return None
        attr = self.defining_feature
        if (attr is None): 
            return str(self.value)
        v = attr.convert_inner_value_to_outer_value(str(self.value), lang)
        if (v is None): 
            return None
        if (isinstance(v, str)): 
            return Utils.asObjectOrNull(v, str)
        else: 
            return str(v)
    
    @property
    def tag(self) -> object:
        """ Используется произвольным образом """
        return self.__tag
    @tag.setter
    def tag(self, value_) -> object:
        self.__tag = value_
        return self.__tag
    
    @staticmethod
    def _new2630(_arg1 : str, _arg2 : object, _arg3 : int) -> 'Slot':
        res = Slot()
        res.type_name = _arg1
        res.value = _arg2
        res.count = _arg3
        return res