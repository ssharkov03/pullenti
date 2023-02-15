# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import typing
from pullenti.unisharp.Utils import Utils

from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.address.AreaAttributes import AreaAttributes
from pullenti.address.internal.AbbrTreeNode import AbbrTreeNode

class CorrectionHelper:
    
    @staticmethod
    def correct(txt : str) -> str:
        ii = txt.find("областьг")
        if (ii > 0): 
            tmp = Utils.newStringIO(txt)
            Utils.insertStringIO(tmp, ii + 7, ' ')
            txt = Utils.toStringStringIO(tmp)
        if ("снт Тверь" in txt): 
            txt = txt.replace("снт Тверь", "г.Тверь")
        if (CorrectionHelper.__m_root is None): 
            return txt
        i = 0
        while i < (len(txt) - 5): 
            if (txt[i] == 'у' and txt[i + 1] == 'л' and str.isupper(txt[i + 2])): 
                txt = "{0}.{1}".format(txt[0:0+i + 2], txt[i + 2:])
                break
            i += 1
        i = 10
        while i < (len(txt) - 5): 
            if (txt[i - 1] == ' ' or txt[i - 1] == ','): 
                if ((CorrectionHelper.__is_start_of(txt, i, "паспорт") or CorrectionHelper.__is_start_of(txt, i, "выдан") or CorrectionHelper.__is_start_of(txt, i, "Выдан")) or CorrectionHelper.__is_start_of(txt, i, "серия") or CorrectionHelper.__is_start_of(txt, i, "док:")): 
                    txt = Utils.trimEndString(txt[0:0+i])
                    break
                elif (CorrectionHelper.__is_start_of(txt, i, "ОВД") or CorrectionHelper.__is_start_of(txt, i, "УВД") or CorrectionHelper.__is_start_of(txt, i, "РОВД")): 
                    j = i - 2
                    sp = 0
                    while j > 0: 
                        if (txt[j] == ' ' and txt[j - 1] != ' '): 
                            sp += 1
                            if (sp >= 4): 
                                break
                        j -= 1
                    if (j > 10 and sp == 4): 
                        txt = Utils.trimEndString(txt[0:0+j])
                        break
            i += 1
        txt0 = txt.upper()
        i = 0
        first_pass2722 = True
        while True:
            if first_pass2722: first_pass2722 = False
            else: i += 1
            if (not (i < len(txt0))): break
            if (not str.isalpha(txt0[i])): 
                continue
            if (i == 0 or txt[i - 1] == ',' or txt[i - 1] == ' '): 
                pass
            else: 
                continue
            tn = CorrectionHelper.__m_root.find(txt0, i)
            if (tn is None): 
                continue
            j = i + tn.len0_
            ok = False
            while j < len(txt0): 
                if (txt0[j] == '.' or txt0[j] == ' '): 
                    ok = True
                else: 
                    break
                j += 1
            if (j >= len(txt0) or not ok or tn.corrs is None): 
                continue
            for kp in tn.corrs.items(): 
                if (not CorrectionHelper.__is_start_of(txt0, j, kp[0])): 
                    continue
                tmp = Utils.newStringIO(txt)
                Utils.removeStringIO(tmp, i, tn.len0_)
                if (Utils.getCharAtStringIO(tmp, i) == '.'): 
                    Utils.removeStringIO(tmp, i, 1)
                Utils.insertStringIO(tmp, i, kp[1] + " ")
                txt = Utils.toStringStringIO(tmp)
                txt0 = txt.upper()
                break
        return txt
    
    @staticmethod
    def __is_start_of(txt : str, i : int, sub : str) -> bool:
        j = 0
        while j < len(sub): 
            if ((i + j) >= len(txt)): 
                return False
            elif (sub[j] != txt[i + j]): 
                return False
            j += 1
        return True
    
    @staticmethod
    def initialize(roots : typing.List['GarObject']) -> None:
        CorrectionHelper.__m_root = AbbrTreeNode()
        if (roots is not None): 
            for r in roots: 
                a = Utils.asObjectOrNull(r.attrs, AreaAttributes)
                if (a is None): 
                    continue
                if (len(a.types) == 0): 
                    continue
                if (len(a.names) == 0): 
                    continue
                if (a.types[0] == "республика"): 
                    CorrectionHelper.__add(a.names[0], "респ")
                elif (a.types[0] == "край"): 
                    CorrectionHelper.__add(a.names[0], "кр")
                    if (a.names[0].endswith("ий")): 
                        CorrectionHelper.__add(a.names[0][0:0+len(a.names[0]) - 2] + "ая", "об")
                elif (a.types[0] == "область"): 
                    CorrectionHelper.__add(a.names[0], "об")
                    if (a.names[0].endswith("ая")): 
                        CorrectionHelper.__add(a.names[0][0:0+len(a.names[0]) - 2] + "ий", "р")
                elif (a.types[0] == "автономная область"): 
                    CorrectionHelper.__add(a.names[0], "об")
                    CorrectionHelper.__add(a.names[0], "ао")
                elif (a.types[0] == "автономный округ"): 
                    CorrectionHelper.__add(a.names[0], "ок")
                    CorrectionHelper.__add(a.names[0], "ао")
                elif (a.types[0] == "город"): 
                    CorrectionHelper.__add(a.names[0], "г")
                else: 
                    pass
    
    __m_root = None
    
    @staticmethod
    def __add(corr : str, typ : str) -> None:
        typ = typ.upper()
        i = 2
        while i < (len(corr) - 2): 
            if (not LanguageHelper.is_cyrillic_vowel(corr[i])): 
                CorrectionHelper.__m_root.add(corr[0:0+i + 1].upper(), 0, corr, typ)
            i += 1