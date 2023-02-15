# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils

from pullenti.ner.metadata.ReferentClass import ReferentClass
from pullenti.ner.business.FundsKind import FundsKind

class FundsMeta(ReferentClass):
    
    def __init__(self) -> None:
        super().__init__()
        self.kind_feature = None;
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.business.FundsReferent import FundsReferent
        FundsMeta.GLOBAL_META = FundsMeta()
        f = FundsMeta.GLOBAL_META.add_feature(FundsReferent.ATTR_KIND, "Класс", 0, 1)
        FundsMeta.GLOBAL_META.kind_feature = f
        f.add_value(Utils.enumToString(FundsKind.STOCK), "Акция", None, None)
        f.add_value(Utils.enumToString(FundsKind.CAPITAL), "Уставной капитал", None, None)
        FundsMeta.GLOBAL_META.add_feature(FundsReferent.ATTR_TYPE, "Тип", 0, 1)
        FundsMeta.GLOBAL_META.add_feature(FundsReferent.ATTR_SOURCE, "Эмитент", 0, 1)
        FundsMeta.GLOBAL_META.add_feature(FundsReferent.ATTR_PERCENT, "Процент", 0, 1)
        FundsMeta.GLOBAL_META.add_feature(FundsReferent.ATTR_COUNT, "Количество", 0, 1)
        FundsMeta.GLOBAL_META.add_feature(FundsReferent.ATTR_PRICE, "Номинал", 0, 1)
        FundsMeta.GLOBAL_META.add_feature(FundsReferent.ATTR_SUM, "Денежная сумма", 0, 1)
    
    @property
    def name(self) -> str:
        from pullenti.ner.business.FundsReferent import FundsReferent
        return FundsReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Ценная бумага"
    
    IMAGE_ID = "funds"
    
    def get_image_id(self, obj : 'Referent'=None) -> str:
        return FundsMeta.IMAGE_ID
    
    GLOBAL_META = None