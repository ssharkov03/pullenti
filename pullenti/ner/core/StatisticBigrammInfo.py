# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru


class StatisticBigrammInfo:
    """ Статистическая информация о биграмме - возвращается StatisticCollection.GetBigrammInfo
    Статистика биграмм
    """
    
    def __init__(self) -> None:
        self.first_count = 0
        self.second_count = 0
        self.pair_count = 0
        self.first_has_other_second = False
        self.second_has_other_first = False
    
    @staticmethod
    def _new744(_arg1 : int, _arg2 : int) -> 'StatisticBigrammInfo':
        res = StatisticBigrammInfo()
        res.first_count = _arg1
        res.second_count = _arg2
        return res