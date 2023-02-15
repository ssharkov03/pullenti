# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru


class ImageWrapper:
    """ Для иконок ГАР-обектов. Приходится работать через обёртку, так как ориентируемся на все платформы и языки
    Для иконок ГАР-обектов
    """
    
    def __init__(self, id0__ : str, cnt : bytearray) -> None:
        self.id0_ = None;
        self.content = None;
        self.image = None;
        self.id0_ = id0__
        self.content = cnt
    
    def __str__(self) -> str:
        return "{0} ({1} bytes)".format(self.id0_, (0 if self.content is None else len(self.content)))