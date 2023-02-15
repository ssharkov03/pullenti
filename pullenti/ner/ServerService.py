# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Streams import MemoryStream
from pullenti.unisharp.Streams import Stream
from pullenti.unisharp.Misc import WebClient

from pullenti.morph.MorphLang import MorphLang
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.core.internal.SerializerHelper import SerializerHelper
from pullenti.ner.core.AnalysisKit import AnalysisKit
from pullenti.ner.AnalysisResult import AnalysisResult
from pullenti.ner.SourceOfAnalysis import SourceOfAnalysis

class ServerService:
    """ Поддержка проведения анализа текста на внешнем сервере """
    
    @staticmethod
    def get_server_version(address_ : str) -> str:
        """ Проверить работоспособность сервера Pullenti.Server.
        Отправляется GET-запрос на сервер, возвращает ASCII-строку с версией SDK.
        
        Args:
            address_(str): адрес вместе с портом (если null, то это http://localhost:1111)
        
        Returns:
            str: версия SDK на сервере или null, если недоступен
        """
        try: 
            web = WebClient()
            res = web.download_data(Utils.ifNotNull(address_, "http://localhost:1111"))
            if (res is None or len(res) == 0): 
                return None
            return res.decode("UTF-8", 'ignore')
        except Exception as ex: 
            return None
    
    @staticmethod
    def prepare_post_data(proc : 'Processor', text : str, lang : 'MorphLang'=None) -> bytearray:
        """ Подготовить данные для POST-отправки на сервер
        
        Args:
            proc(Processor): процессор, настройки (анализаторы) которого должны быть воспроизведены на сервере (если null, то стандартный)
            text(str): обрабатывамый текст
            lang(MorphLang): язык (если не задан, то будет определён автоматически)
        
        """
        dat = None
        with MemoryStream() as mem1: 
            tmp = io.StringIO()
            print("{0};".format((0 if lang is None else lang.value)), end="", file=tmp, flush=True)
            if (proc is not None): 
                for a in proc.analyzers: 
                    print("{0}{1};".format(("-" if a.ignore_this_analyzer else ""), a.name), end="", file=tmp, flush=True)
            else: 
                print("ALL;", end="", file=tmp)
            SerializerHelper.serialize_int(mem1, 1234)
            SerializerHelper.serialize_string(mem1, Utils.toStringStringIO(tmp))
            SerializerHelper.serialize_string(mem1, text)
            dat = mem1.toarray()
        return dat
    
    @staticmethod
    def create_result(dat : bytearray) -> 'AnalysisResult':
        """ Оформить результат из того, что вернул сервер
        
        Args:
            dat(bytearray): массив байт, возвращённый сервером
        
        Returns:
            AnalysisResult: результат (но может быть Exception, если была на сервере ошибка)
        """
        if (dat is None or (len(dat) < 1)): 
            raise Utils.newException("Empty result", None)
        res = AnalysisResult()
        kit = AnalysisKit(None)
        with MemoryStream(dat) as mem2: 
            if ((chr(dat[0])) == 'E' and (chr(dat[1])) == 'R'): 
                err = SerializerHelper.deserialize_string(mem2)
                raise Utils.newException(err, None)
            kit.deserialize(mem2)
            res.entities.extend(kit.entities)
            res.first_token = kit.first_token
            res.sofa = kit.sofa
            i = SerializerHelper.deserialize_int(mem2)
            res.base_language = MorphLang._new215(i)
            i = SerializerHelper.deserialize_int(mem2)
            while i > 0: 
                res.log0_.append(SerializerHelper.deserialize_string(mem2))
                i -= 1
        return res
    
    @staticmethod
    def process_on_server(address_ : str, proc : 'Processor', text : str, lang : 'MorphLang'=None) -> 'AnalysisResult':
        """ Обработать текст на сервере (если он запущен).
        Функция фактически оформляет данные для отправки на сервер через PreparePostData(...),
        затем делает POST-запрос по http, полученный массив байт через CreateResult(...) оформляет как результат.
        Внимание! Внешняя онтология не поддерживается, в отличие от локальной обработки через Process.
        
        Args:
            address_(str): адрес вместе с портом (если null, то это http://localhost:1111)
            proc(Processor): процессор, настройки (анализаторы) которого должны быть воспроизведены на сервере (если null, то стандартный)
            text(str): обрабатывамый текст
            lang(MorphLang): язык (если не задан, то будет определён автоматически)
        
        Returns:
            AnalysisResult: аналитический контейнер с результатом
        Обработать текст на сервере
        """
        dat = ServerService.prepare_post_data(proc, text, lang)
        web = WebClient()
        res = web.upload_data(Utils.ifNotNull(address_, "http://localhost:1111"), dat)
        return ServerService.create_result(res)
    
    @staticmethod
    def internal_proc(stream : Stream) -> bytearray:
        # Для внутреннего использования
        tag = SerializerHelper.deserialize_int(stream)
        if (tag != 1234): 
            return None
        attrs = SerializerHelper.deserialize_string(stream)
        if (Utils.isNullOrEmpty(attrs)): 
            return None
        parts = Utils.splitString(attrs, ';', False)
        if (len(parts) < 1): 
            return None
        lang = None
        if (parts[0] != "0"): 
            lang = MorphLang._new215(int(parts[0]))
        with ProcessorService.create_empty_processor() as proc: 
            i = 1
            first_pass3071 = True
            while True:
                if first_pass3071: first_pass3071 = False
                else: i += 1
                if (not (i < len(parts))): break
                nam = parts[i]
                if (len(nam) == 0): 
                    continue
                ign = False
                if (nam[0] == '-'): 
                    ign = True
                    nam = nam[1:]
                for a in ProcessorService.get_analyzers(): 
                    if (a.name == nam or ((nam == "ALL" and not a.is_specific))): 
                        aa = a.clone()
                        if (ign): 
                            a.ignore_this_analyzer = True
                        proc.add_analyzer(a)
            txt = SerializerHelper.deserialize_string(stream)
            ar = proc.process(SourceOfAnalysis(txt), None, lang)
            res = None
            if (ar is not None and (isinstance(ar.tag, AnalysisKit))): 
                with MemoryStream() as mem: 
                    kit = Utils.asObjectOrNull(ar.tag, AnalysisKit)
                    kit.entities.clear()
                    kit.entities.extend(ar.entities)
                    kit.serialize(mem, True)
                    SerializerHelper.serialize_int(mem, (0 if ar.base_language is None else ar.base_language.value))
                    SerializerHelper.serialize_int(mem, len(ar.log0_))
                    for s in ar.log0_: 
                        SerializerHelper.serialize_string(mem, s)
                    res = mem.toarray()
            return res