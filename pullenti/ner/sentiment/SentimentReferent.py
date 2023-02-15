# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.core.ReferentsEqualType import ReferentsEqualType
from pullenti.ner.core.IntOntologyItem import IntOntologyItem
from pullenti.ner.core.Termin import Termin
from pullenti.ner.metadata.ReferentClass import ReferentClass
from pullenti.ner.sentiment.internal.MetaSentiment import MetaSentiment
from pullenti.ner.sentiment.SentimentKind import SentimentKind
from pullenti.ner.Referent import Referent

class SentimentReferent(Referent):
    """ Фрагмент, соответсвующий сентиментной оценке """
    
    def __init__(self) -> None:
        super().__init__(SentimentReferent.OBJ_TYPENAME)
        self.instance_of = MetaSentiment._global_meta
    
    OBJ_TYPENAME = "SENTIMENT"
    
    ATTR_KIND = "KIND"
    
    ATTR_COEF = "COEF"
    
    ATTR_REF = "REF"
    
    ATTR_SPELLING = "SPELLING"
    
    def to_string_ex(self, short_variant : bool, lang : 'MorphLang', lev : int=0) -> str:
        res = io.StringIO()
        print(MetaSentiment.FTYP.convert_inner_value_to_outer_value(self.get_string_value(SentimentReferent.ATTR_KIND), lang), end="", file=res)
        print(" {0}".format(Utils.ifNotNull(self.spelling, "")), end="", file=res, flush=True)
        if (self.coef > 0): 
            print(" (coef={0})".format(self.coef), end="", file=res, flush=True)
        r = self.get_slot_value(SentimentReferent.ATTR_REF)
        if (r is not None and not short_variant): 
            print(" -> {0}".format(r), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    @property
    def kind(self) -> 'SentimentKind':
        s = self.get_string_value(SentimentReferent.ATTR_KIND)
        if (s is None): 
            return SentimentKind.UNDEFINED
        try: 
            res = Utils.valToEnum(s, SentimentKind)
            if (isinstance(res, SentimentKind)): 
                return Utils.valToEnum(res, SentimentKind)
        except Exception as ex2433: 
            pass
        return SentimentKind.UNDEFINED
    @kind.setter
    def kind(self, value) -> 'SentimentKind':
        if (value != SentimentKind.UNDEFINED): 
            self.add_slot(SentimentReferent.ATTR_KIND, Utils.enumToString(value), True, 0)
        return value
    
    @property
    def spelling(self) -> str:
        return self.get_string_value(SentimentReferent.ATTR_SPELLING)
    @spelling.setter
    def spelling(self, value) -> str:
        self.add_slot(SentimentReferent.ATTR_SPELLING, value, True, 0)
        return value
    
    @property
    def coef(self) -> int:
        val = self.get_string_value(SentimentReferent.ATTR_COEF)
        if (val is None): 
            return 0
        i = 0
        wrapi2434 = RefOutArgWrapper(0)
        inoutres2435 = Utils.tryParseInt(val, wrapi2434)
        i = wrapi2434.value
        if (not inoutres2435): 
            return 0
        return i
    @coef.setter
    def coef(self, value) -> int:
        self.add_slot(SentimentReferent.ATTR_COEF, str(value), True, 0)
        return value
    
    def can_be_equals(self, obj : 'Referent', typ : 'ReferentsEqualType'=ReferentsEqualType.WITHINONETEXT) -> bool:
        sr = Utils.asObjectOrNull(obj, SentimentReferent)
        if (sr is None): 
            return False
        if (sr.kind != self.kind): 
            return False
        if (sr.spelling != self.spelling): 
            return False
        return True
    
    def can_be_general_for(self, obj : 'Referent') -> bool:
        return False
    
    def create_ontology_item(self) -> 'IntOntologyItem':
        oi = IntOntologyItem(self)
        oi.termins.append(Termin(self.spelling))
        return oi