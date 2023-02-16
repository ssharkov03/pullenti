# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing

class ITranslator:
    # Интерфейс переводчика
    
    @property
    def enabled(self) -> bool:
        return None
    
    def translate_word(self, word : str, lang_from : str, lang_to : str, ignore_new_words : bool=False) -> object:
        return None
    
    def translate_words(self, words : typing.List[str], lang_from : str, lang_to : str, ignore_new_words : bool=False) -> typing.List[object]:
        return None
    
    def commit(self) -> None:
        pass