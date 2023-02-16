# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
from pullenti.unisharp.Utils import Utils

from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.Referent import Referent
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.Termin import Termin
from pullenti.ner.chat.VerbType import VerbType
from pullenti.ner.chat.ChatReferent import ChatReferent
from pullenti.ner.business.internal.PullentiNerBusinessInternalResourceHelper import PullentiNerBusinessInternalResourceHelper
from pullenti.ner.chat.internal.MetaChat import MetaChat
from pullenti.ner.chat.ChatType import ChatType
from pullenti.ner.chat.internal.ChatItemToken import ChatItemToken
from pullenti.ner.Analyzer import Analyzer

class ChatAnalyzer(Analyzer):
    
    ANALYZER_NAME = "CHAT"
    
    @property
    def name(self) -> str:
        return ChatAnalyzer.ANALYZER_NAME
    
    @property
    def caption(self) -> str:
        return "Элемент диалога"
    
    @property
    def description(self) -> str:
        return ""
    
    def clone(self) -> 'Analyzer':
        return ChatAnalyzer()
    
    @property
    def type_system(self) -> typing.List['ReferentClass']:
        return [MetaChat._global_meta]
    
    @property
    def images(self) -> typing.List[tuple]:
        res = dict()
        res[MetaChat.IMAGE_ID] = PullentiNerBusinessInternalResourceHelper.get_bytes("chat.png")
        return res
    
    def create_referent(self, type0_ : str) -> 'Referent':
        if (type0_ == ChatReferent.OBJ_TYPENAME): 
            return ChatReferent()
        return None
    
    @property
    def progress_weight(self) -> int:
        return 1
    
    @property
    def is_specific(self) -> bool:
        return True
    
    def process(self, kit : 'AnalysisKit') -> None:
        ad = kit.get_analyzer_data(self)
        toks = list()
        t = kit.first_token
        first_pass2795 = True
        while True:
            if first_pass2795: first_pass2795 = False
            else: t = t.next0_
            if (not (t is not None)): break
            cit = ChatItemToken.try_parse(t)
            if (cit is None): 
                continue
            toks.append(cit)
            t = cit.end_token
        i = 0
        first_pass2796 = True
        while True:
            if first_pass2796: first_pass2796 = False
            else: i += 1
            if (not (i < (len(toks) - 1))): break
            if (((toks[i].typ == ChatType.ACCEPT or toks[i].typ == ChatType.CANCEL)) and ChatAnalyzer.__can_merge(toks[i], toks[i + 1])): 
                if (toks[i + 1].typ == toks[i].typ): 
                    toks[i].end_token = toks[i + 1].end_token
                    del toks[i + 1]
                    i -= 1
                    continue
                if (toks[i + 1].typ == ChatType.CANCEL or ((toks[i + 1].typ == ChatType.VERB and toks[i + 1].not0_))): 
                    toks[i + 1].begin_token = toks[i].begin_token
                    del toks[i]
                    i -= 1
                    continue
        for cit in toks: 
            cr = ChatReferent._new566(cit.typ)
            if (cit.value is not None): 
                cr.value = cit.value
            if (cit.vtyp != VerbType.UNDEFINED): 
                cr.add_verb_type(cit.vtyp)
            if (cit.not0_): 
                cr.not0_ = True
            cr = (Utils.asObjectOrNull(ad.register_referent(cr), ChatReferent))
            rt = ReferentToken(cr, cit.begin_token, cit.end_token)
            kit.embed_token(rt)
    
    @staticmethod
    def __can_merge(t1 : 'ChatItemToken', t2 : 'ChatItemToken') -> bool:
        t = t1.end_token.next0_
        first_pass2797 = True
        while True:
            if first_pass2797: first_pass2797 = False
            else: t = t.next0_
            if (not (t is not None and (t.end_char < t2.begin_char))): break
            if (not (isinstance(t, TextToken))): 
                return False
            if (t.length_char < 2): 
                continue
            mc = t.get_morph_class_in_dictionary()
            if (((mc.is_adverb or mc.is_preposition or mc.is_pronoun) or mc.is_personal_pronoun or mc.is_misc) or mc.is_conjunction): 
                continue
            return False
        return True
    
    __m_inited = None
    
    @staticmethod
    def initialize() -> None:
        if (ChatAnalyzer.__m_inited): 
            return
        ChatAnalyzer.__m_inited = True
        try: 
            MetaChat.initialize()
            Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = True
            ChatItemToken.initialize()
            Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = False
        except Exception as ex: 
            raise Utils.newException(ex.__str__(), ex)
        ProcessorService.register_analyzer(ChatAnalyzer())