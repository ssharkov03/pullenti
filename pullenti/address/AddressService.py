# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.unisharp.Misc import Stopwatch

from pullenti.address.internal.PullentiAddressInternalResourceHelper import PullentiAddressInternalResourceHelper
from pullenti.address.ImageWrapper import ImageWrapper
from pullenti.ner.fias.FiasAnalyzer import FiasAnalyzer
from pullenti.address.AddressHelper import AddressHelper
from pullenti.address.internal.CorrectionHelper import CorrectionHelper
from pullenti.address.TextAddress import TextAddress
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.address.GarStatistic import GarStatistic
from pullenti.address.internal.ServerHelper import ServerHelper
from pullenti.ner.named.NamedEntityAnalyzer import NamedEntityAnalyzer
from pullenti.ner.date.DateAnalyzer import DateAnalyzer
from pullenti.ner.uri.UriAnalyzer import UriAnalyzer
from pullenti.ner.geo.GeoAnalyzer import GeoAnalyzer
from pullenti.ner.money.MoneyAnalyzer import MoneyAnalyzer
from pullenti.ner.phone.PhoneAnalyzer import PhoneAnalyzer
from pullenti.address.internal.GarHelper import GarHelper
from pullenti.ner.person.PersonAnalyzer import PersonAnalyzer
from pullenti.ner.address.AddressAnalyzer import AddressAnalyzer
from pullenti.address.internal.AddressSearchHelper import AddressSearchHelper
from pullenti.ner.org.OrganizationAnalyzer import OrganizationAnalyzer
from pullenti.address.internal.AnalyzeHelper import AnalyzeHelper

class AddressService:
    """ Сервис работы с адресами
    
    """
    
    VERSION = "4.14"
    """ Текущая версия """
    
    VERSION_DATE = "2022.09.01"
    """ Дата создания текущей версии """
    
    @staticmethod
    def initialize() -> None:
        """ Инициализация движка - необходимо вызывать один раз в начале работы. """
        ProcessorService.initialize(None)
        MoneyAnalyzer.initialize()
        UriAnalyzer.initialize()
        PhoneAnalyzer.initialize()
        DateAnalyzer.initialize()
        GeoAnalyzer.initialize()
        AddressAnalyzer.initialize()
        OrganizationAnalyzer.initialize()
        PersonAnalyzer.initialize()
        NamedEntityAnalyzer.initialize()
        FiasAnalyzer.initialize()
        AnalyzeHelper.init()
        GarHelper.init()
        AddressHelper.IMAGES.append(ImageWrapper("region", PullentiAddressInternalResourceHelper.get_bytes("region.png")))
        AddressHelper.IMAGES.append(ImageWrapper("admin", PullentiAddressInternalResourceHelper.get_bytes("admin.png")))
        AddressHelper.IMAGES.append(ImageWrapper("municipal", PullentiAddressInternalResourceHelper.get_bytes("municipal.png")))
        AddressHelper.IMAGES.append(ImageWrapper("settlement", PullentiAddressInternalResourceHelper.get_bytes("settlement.png")))
        AddressHelper.IMAGES.append(ImageWrapper("city", PullentiAddressInternalResourceHelper.get_bytes("city.png")))
        AddressHelper.IMAGES.append(ImageWrapper("locality", PullentiAddressInternalResourceHelper.get_bytes("locality.png")))
        AddressHelper.IMAGES.append(ImageWrapper("area", PullentiAddressInternalResourceHelper.get_bytes("area.png")))
        AddressHelper.IMAGES.append(ImageWrapper("street", PullentiAddressInternalResourceHelper.get_bytes("street.png")))
        AddressHelper.IMAGES.append(ImageWrapper("plot", PullentiAddressInternalResourceHelper.get_bytes("plot.png")))
        AddressHelper.IMAGES.append(ImageWrapper("building", PullentiAddressInternalResourceHelper.get_bytes("building.png")))
        AddressHelper.IMAGES.append(ImageWrapper("room", PullentiAddressInternalResourceHelper.get_bytes("room.png")))
        AddressHelper.IMAGES.append(ImageWrapper("carplace", PullentiAddressInternalResourceHelper.get_bytes("carplace.png")))
    
    __m_default_geo_object = None
    
    @staticmethod
    def get_default_geo_object() -> str:
        """ Географический объект по умолчанию, используется в случае неоднозначности.
        Например, если указана только улица
        без населённого пункта или одноимённых населённых пунктов в регионе несколько. """
        return AddressService.__m_default_geo_object
    @staticmethod
    def set_default_geo_object(value : str) -> str:
        try: 
            AddressService.__m_default_geo_object = value
            AnalyzeHelper.set_default_geo(value)
        except Exception as ex142: 
            pass
        return value
    
    @staticmethod
    def set_gar_index_path(gar_path : str) -> bool:
        """ Указание директории с индексом ГАР (если не задать, то выделяемые объекты привязываться не будут)
        
        Args:
            gar_path(str): папка с индексом ГАР
        
        Returns:
            bool: true, если удача, иначе false (например, папки не существует)
        """
        b = FiasAnalyzer.init_fias(gar_path)
        GarHelper.init()
        if (AddressService.__m_default_geo_object is not None): 
            AnalyzeHelper.set_default_geo(AddressService.__m_default_geo_object)
        CorrectionHelper.initialize(AddressService.get_objects(None, False))
        ServerHelper.SERVER_URI = (None)
        return b
    
    @staticmethod
    def get_gar_index_path() -> str:
        """ Получить папку с используемым ГАР-индексом (если null, то индекс не подгружен)
        
        """
        if (FiasAnalyzer.FIAS_DB is None): 
            return None
        return FiasAnalyzer.FIAS_DB.base_dir
    
    @staticmethod
    def get_gar_statistic() -> 'GarStatistic':
        """ Получить информацию по индексу и его объектам
        
        """
        try: 
            if (ServerHelper.SERVER_URI is not None): 
                return ServerHelper.get_gar_statistic()
            if (FiasAnalyzer.FIAS_DB is None): 
                return None
            res = GarStatistic()
            res.index_path = FiasAnalyzer.FIAS_DB.base_dir
            res.area_count = FiasAnalyzer.FIAS_DB.objects_count
            res.house_count = FiasAnalyzer.FIAS_DB.houses_count
            res.room_count = FiasAnalyzer.FIAS_DB.rooms_count
            return res
        except Exception as ex: 
            return None
    
    @staticmethod
    def set_server_connection(uri : str) -> bool:
        """ Для работы установить связь с сервером и все запросы делать через него
        (используется для ускорения работы для JS и Python)
        
        Args:
            uri(str): например, http://localhost:2222, если null, то связь разрывается
        
        """
        if (uri is None): 
            ServerHelper.SERVER_URI = (None)
            return True
        ver = ServerHelper.get_server_version(uri)
        if (ver is None): 
            ServerHelper.SERVER_URI = (None)
            return False
        else: 
            AddressService.set_gar_index_path(None)
            ServerHelper.SERVER_URI = uri
            return True
    
    @staticmethod
    def get_server_uri() -> str:
        """ Если связь с сервером установлена, то вернёт адрес
        
        """
        return ServerHelper.SERVER_URI
    
    @staticmethod
    def get_server_version(uri : str) -> str:
        """ Получить версию SDK на сервере
        
        Args:
            uri(str): 
        
        Returns:
            str: версия или null при недоступности сервера
        """
        return ServerHelper.get_server_version(uri)
    
    @staticmethod
    def process_text(txt : str) -> typing.List['TextAddress']:
        """ Обработать произвольный текст, в котором есть адреса
        
        Args:
            txt(str): текст
        
        Returns:
            typing.List[TextAddress]: результат - для каждого найденного адреса свой экземпляр
        
        """
        try: 
            if (ServerHelper.SERVER_URI is not None): 
                return ServerHelper.process_text(txt)
            corr = None
            wrapcorr143 = RefOutArgWrapper(None)
            res = AnalyzeHelper.analyze(txt, None, False, wrapcorr143)
            corr = wrapcorr143.value
            return res
        except Exception as ex: 
            return None
    
    @staticmethod
    def process_single_address_text(txt : str) -> 'TextAddress':
        """ Обработать текст с одним адресом (адресное поле)
        
        Args:
            txt(str): исходный текст
        
        Returns:
            TextAddress: результат обработки
        
        """
        try: 
            if (ServerHelper.SERVER_URI is not None): 
                return ServerHelper.process_single_address_text(txt)
            corr = None
            sw = Stopwatch()
            sw.start()
            wrapcorr145 = RefOutArgWrapper(None)
            objs = AnalyzeHelper.analyze(txt, None, True, wrapcorr145)
            corr = wrapcorr145.value
            res = None
            if (objs is None or len(objs) == 0): 
                res = TextAddress._new144("Адрес не выделен", txt)
            else: 
                res = objs[0]
            sw.stop()
            res.milliseconds = (sw.elapsedMilliseconds)
            return res
        except Exception as ex: 
            return None
    
    @staticmethod
    def process_single_address_texts(txts : typing.List[str]) -> typing.List['TextAddress']:
        """ Обработать порцию адресов. Использовать в случае сервера, посылая ему порцию на обработку
        (не более 100-300 за раз), чтобы сократить время на издержки взаимодействия.
        Для обычной работы (не через сервер) это эквивалентно вызову в цикле ProcessSingleAddressText
        и особого смысла не имеет.
        
        Args:
            txts(typing.List[str]): список адресов
        
        Returns:
            typing.List[TextAddress]: результат (количество совпадает с исходным списком), если null, то какая-то ошибка
        """
        try: 
            if (ServerHelper.SERVER_URI is not None): 
                return ServerHelper.process_single_address_texts(txts)
            res = list()
            for txt in txts: 
                res.append(AddressService.process_single_address_text(txt))
            return res
        except Exception as ex: 
            return None
    
    @staticmethod
    def search_objects(search_pars : 'SearchParams') -> 'SearchResult':
        """ Искать объекты (для выпадающих списков)
        
        Args:
            search_pars(SearchParams): параметры запроса
        
        Returns:
            SearchResult: результат
        """
        try: 
            if (search_pars is None): 
                return None
            if (ServerHelper.SERVER_URI is not None): 
                return ServerHelper.search_objects(search_pars)
            else: 
                return AddressSearchHelper.search(search_pars)
        except Exception as ex: 
            return None
    
    @staticmethod
    def get_objects(id0_ : str, ignore_houses : bool=False) -> typing.List['GarObject']:
        """ Получить список дочерних объектов для ГАР-объекта
        
        Args:
            go: идентификатор объект ГАР (если null, то объекты первого уровня - регионы)
            ignore_houses(bool): игнорировать дома и помещения
        
        Returns:
            typing.List[GarObject]: дочерние объекты
        """
        try: 
            if (ServerHelper.SERVER_URI is not None): 
                return ServerHelper.get_children_objects(id0_, ignore_houses)
            else: 
                return GarHelper.get_children_objects(id0_, ignore_houses)
        except Exception as ex146: 
            return None
    
    @staticmethod
    def get_object(obj_id : str) -> 'GarObject':
        """ Получить объект (вместе с родительской иерархией) по идентификатору
        
        Args:
            obj_id(str): внутренний идентификатор
        
        Returns:
            GarObject: объект
        """
        if (Utils.isNullOrEmpty(obj_id)): 
            return None
        try: 
            if (ServerHelper.SERVER_URI is not None): 
                return ServerHelper.get_object(obj_id)
            else: 
                return GarHelper.get_object(obj_id)
        except Exception as ex147: 
            return None