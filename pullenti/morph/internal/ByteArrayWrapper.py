# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Streams import Stream

class ByteArrayWrapper:
    # Сделан специально для Питона - а то стандартым способом через Memory Stream
    # жутко тормозит, придётся делать самим
    
    def __init__(self, arr : bytearray) -> None:
        self.m_array = None;
        self.__m_len = 0
        self.m_array = arr
        self.__m_len = len(self.m_array)
    
    def iseof(self, pos : int) -> bool:
        return pos >= self.__m_len
    
    def deserialize_byte(self, pos : int) -> int:
        if (pos.value >= self.__m_len): 
            return 0
        retVal2729 = self.m_array[pos.value]
        pos.value += 1
        return retVal2729
    
    def deserialize_short(self, pos : int) -> int:
        if ((pos.value + 1) >= self.__m_len): 
            return 0
        b0 = self.m_array[pos.value]
        pos.value += 1
        b1 = self.m_array[pos.value]
        pos.value += 1
        res = b1
        res <<= 8
        return (res | (b0))
    
    def deserialize_int(self, pos : int) -> int:
        if ((pos.value + 1) >= self.__m_len): 
            return 0
        b0 = self.m_array[pos.value]
        pos.value += 1
        b1 = self.m_array[pos.value]
        pos.value += 1
        b2 = self.m_array[pos.value]
        pos.value += 1
        b3 = self.m_array[pos.value]
        pos.value += 1
        res = b3
        res <<= 8
        res |= (b2)
        res <<= 8
        res |= (b1)
        res <<= 8
        return (res | (b0))
    
    def deserialize_string(self, pos : int) -> str:
        if (pos.value >= self.__m_len): 
            return None
        len0_ = self.m_array[pos.value]
        pos.value += 1
        if (len0_ == (0xFF)): 
            return None
        if (len0_ == (0)): 
            return ""
        if ((pos.value + (len0_)) > self.__m_len): 
            return None
        res = self.m_array[pos.value:pos.value+len0_].decode("UTF-8", 'ignore')
        pos.value += (len0_)
        return res
    
    def deserialize_string_ex(self, pos : int) -> str:
        if (pos.value >= self.__m_len): 
            return None
        len0_ = self.deserialize_short(pos)
        if (len0_ == 0xFFFF or (len0_ < 0)): 
            return None
        if (len0_ == 0): 
            return ""
        if ((pos.value + len0_) > self.__m_len): 
            return None
        res = self.m_array[pos.value:pos.value+len0_].decode("UTF-8", 'ignore')
        pos.value += len0_
        return res