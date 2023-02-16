# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils

from pullenti.morph.MorphCase import MorphCase
from pullenti.ner.TextToken import TextToken
from pullenti.ner.Token import Token
from pullenti.ner.core.PrepositionHelper import PrepositionHelper
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr

class NounPhraseHelper:
    """ Выделение именных групп - это существительное с согласованными прилагательными (если они есть).
    
    Хелпер именных групп
    """
    
    @staticmethod
    def try_parse(t : 'Token', attrs : 'NounPhraseParseAttr'=NounPhraseParseAttr.NO, max_char_pos : int=0, noun : 'MetaToken'=None) -> 'NounPhraseToken':
        """ Попробовать создать именную группу с указанного токена
        
        Args:
            t(Token): начальный токен
            attrs(NounPhraseParseAttr): атрибуты (можно битовую маску)
            max_char_pos(int): максимальная позиция в тексте, до которой выделять (если 0, то без ограничений)
            noun(MetaToken): это если нужно выделить только прилагательные для ранее выделенного существительного (из другой группы)
        
        Returns:
            NounPhraseToken: именная группа или null
        """
        from pullenti.ner.core.internal.NounPhraseItem import NounPhraseItem
        from pullenti.ner.core._NounPraseHelperInt import _NounPraseHelperInt
        if (t is None): 
            return None
        if (attrs == NounPhraseParseAttr.NO and (isinstance(t, TextToken))): 
            tt = Utils.asObjectOrNull(t, TextToken)
            if (tt._no_npt): 
                return None
            if (tt._npt is not None): 
                ok = True
                ttt = tt
                while ttt is not None and ttt.begin_char <= tt._npt.end_char: 
                    if (not (isinstance(ttt, TextToken))): 
                        ok = False
                    ttt = ttt.next0_
                if (ok): 
                    return tt._npt.clone()
        res = _NounPraseHelperInt.try_parse(t, attrs, max_char_pos, Utils.asObjectOrNull(noun, NounPhraseItem))
        if (res is not None): 
            if (attrs == NounPhraseParseAttr.NO and (isinstance(t, TextToken))): 
                tt = Utils.asObjectOrNull(t, TextToken)
                tt._no_npt = False
                tt._npt = res
            if ((((attrs) & (NounPhraseParseAttr.PARSEPREPOSITION))) != (NounPhraseParseAttr.NO)): 
                if (res.begin_token == res.end_token and t.morph.class0_.is_preposition): 
                    prep = PrepositionHelper.try_parse(t)
                    if (prep is not None): 
                        res2 = _NounPraseHelperInt.try_parse(t.next0_, attrs, max_char_pos, Utils.asObjectOrNull(noun, NounPhraseItem))
                        if (res2 is not None): 
                            if (not ((prep.next_case) & res2.morph.case_).is_undefined): 
                                res2.morph.remove_items(prep.next_case, False)
                                res2.preposition = prep
                                res2.begin_token = t
                                return res2
            return res
        if ((((attrs) & (NounPhraseParseAttr.PARSEPREPOSITION))) != (NounPhraseParseAttr.NO)): 
            prep = PrepositionHelper.try_parse(t)
            if (prep is not None and (prep.newlines_after_count < 2)): 
                res = _NounPraseHelperInt.try_parse(prep.end_token.next0_, attrs, max_char_pos, Utils.asObjectOrNull(noun, NounPhraseItem))
                if (res is not None): 
                    res.preposition = prep
                    res.begin_token = t
                    if (not ((prep.next_case) & res.morph.case_).is_undefined): 
                        res.morph.remove_items(prep.next_case, False)
                    elif (t.morph.class0_.is_adverb): 
                        return None
                    return res
        if (attrs == NounPhraseParseAttr.NO and (isinstance(t, TextToken))): 
            tt = Utils.asObjectOrNull(t, TextToken)
            tt._no_npt = True
        return None