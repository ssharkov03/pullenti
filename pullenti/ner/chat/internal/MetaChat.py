# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru


from pullenti.ner.metadata.ReferentClass import ReferentClass

class MetaChat(ReferentClass):
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.chat.ChatReferent import ChatReferent
        MetaChat._global_meta = MetaChat()
        MetaChat._global_meta.add_feature(ChatReferent.ATTR_TYPE, "Тип", 1, 1)
        MetaChat._global_meta.add_feature(ChatReferent.ATTR_VALUE, "Значение", 0, 1)
        MetaChat._global_meta.add_feature(ChatReferent.ATTR_NOT, "Отрицание", 0, 1)
        MetaChat._global_meta.add_feature(ChatReferent.ATTR_VERBTYPE, "Тип глагола", 0, 0)
    
    @property
    def name(self) -> str:
        from pullenti.ner.chat.ChatReferent import ChatReferent
        return ChatReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Элемент диалога"
    
    IMAGE_ID = "chat"
    
    def get_image_id(self, obj : 'Referent'=None) -> str:
        return MetaChat.IMAGE_ID
    
    _global_meta = None