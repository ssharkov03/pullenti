# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
import threading
from pullenti.unisharp.Utils import Utils

from pullenti.ner.Referent import Referent
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.vacance.VacanceItemType import VacanceItemType
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.vacance.internal.VacanceTokenType import VacanceTokenType
from pullenti.ner.vacance.MetaVacance import MetaVacance
from pullenti.ner.core.internal.PullentiNerCoreInternalResourceHelper import PullentiNerCoreInternalResourceHelper
from pullenti.ner.vacance.VacanceItemReferent import VacanceItemReferent
from pullenti.ner.vacance.internal.VacanceToken import VacanceToken
from pullenti.ner.Analyzer import Analyzer

class VacanceAnalyzer(Analyzer):
    """ Анализатор вакансий (специфический анализатор) """
    
    ANALYZER_NAME = "VACANCE"
    """ Имя анализатора ("VACANCE") """
    
    @property
    def name(self) -> str:
        return VacanceAnalyzer.ANALYZER_NAME
    
    @property
    def caption(self) -> str:
        return "Вакансия"
    
    @property
    def description(self) -> str:
        return "Текст содержит одну вакансию"
    
    def clone(self) -> 'Analyzer':
        return VacanceAnalyzer()
    
    @property
    def is_specific(self) -> bool:
        """ Специфический анализатор """
        return True
    
    @property
    def type_system(self) -> typing.List['ReferentClass']:
        return [MetaVacance.GLOBAL_META]
    
    @property
    def images(self) -> typing.List[tuple]:
        res = dict()
        res[str(MetaVacance.IMAGE_ID)] = PullentiNerCoreInternalResourceHelper.get_bytes("vacance.png")
        return res
    
    def create_referent(self, type0_ : str) -> 'Referent':
        if (type0_ == VacanceItemReferent.OBJ_TYPENAME): 
            return VacanceItemReferent()
        return None
    
    @property
    def progress_weight(self) -> int:
        return 1
    
    def process(self, kit : 'AnalysisKit') -> None:
        ad = kit.get_analyzer_data(self)
        li = VacanceToken.try_parse_list(kit.first_token)
        if (li is None or (len(li) < 1)): 
            return
        is_expired = False
        for v in li: 
            if (v.typ == VacanceTokenType.EXPIRED): 
                is_expired = True
        has_date = False
        has_skills = False
        for v in li: 
            if (v.typ == VacanceTokenType.UNDEFINED or v.typ == VacanceTokenType.DUMMY): 
                continue
            if (Utils.isNullOrEmpty(v.value) and len(v.refs) == 0): 
                continue
            it = VacanceItemReferent()
            if (v.typ == VacanceTokenType.DATE): 
                it.typ = VacanceItemType.DATE
                has_date = True
            elif (v.typ == VacanceTokenType.EXPIERENCE): 
                it.typ = VacanceItemType.EXPERIENCE
            elif (v.typ == VacanceTokenType.MONEY): 
                it.typ = VacanceItemType.MONEY
            elif (v.typ == VacanceTokenType.NAME): 
                it.typ = VacanceItemType.NAME
                if (is_expired): 
                    it.expired = True
            elif (v.typ == VacanceTokenType.EDUCATION): 
                it.typ = VacanceItemType.EDUCATION
            elif (v.typ == VacanceTokenType.LANGUAGE): 
                it.typ = VacanceItemType.LANGUAGE
            elif (v.typ == VacanceTokenType.DRIVING): 
                it.typ = VacanceItemType.DRIVINGLICENSE
            elif (v.typ == VacanceTokenType.LICENSE): 
                it.typ = VacanceItemType.LICENSE
            elif (v.typ == VacanceTokenType.MORAL): 
                it.typ = VacanceItemType.MORAL
            elif (v.typ == VacanceTokenType.PLUS): 
                it.typ = VacanceItemType.PLUS
            elif (v.typ == VacanceTokenType.SKILL): 
                it.typ = VacanceItemType.SKILL
                has_skills = True
            else: 
                continue
            if (v.value is not None): 
                it.value = v.value
            for r in v.refs: 
                it.add_slot(VacanceItemReferent.ATTR_REF, r, False, 0)
            rt = ReferentToken(ad.register_referent(it), v.begin_token, v.end_token)
            kit.embed_token(rt)
    
    __m_initialized = False
    
    __m_lock = None
    
    @staticmethod
    def initialize() -> None:
        with VacanceAnalyzer.__m_lock: 
            if (VacanceAnalyzer.__m_initialized): 
                return
            VacanceAnalyzer.__m_initialized = True
            MetaVacance.initialize()
            VacanceToken.initialize()
            ProcessorService.register_analyzer(VacanceAnalyzer())
    
    # static constructor for class VacanceAnalyzer
    @staticmethod
    def _static_ctor():
        VacanceAnalyzer.__m_lock = threading.Lock()

VacanceAnalyzer._static_ctor()