# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import pathlib
import os
import shutil
import datetime
import gc
import typing
import threading
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Streams import FileStream
from pullenti.unisharp.Streams import Stream

class ConsoleHelper:
    """ Запись в лог-файл и на экран """
    
    __m_hide_console_output = None
    
    @staticmethod
    def get_hide_console_output() -> bool:
        return ConsoleHelper.__m_hide_console_output
    @staticmethod
    def set_hide_console_output(value : bool) -> bool:
        ConsoleHelper.__m_hide_console_output = value
        return value
    
    HIDE_LOG_OUTPUT = None
    
    OUT_DATE = True
    
    CLOSE_STREAM_AFTER_EACH_WRITE = False
    
    REMOVE_LOGS_OLDER_THIS_DAYS = 7
    """ Удалять лог-файлы, которые были созданы древнее, чем указанное число дней от текущей даты """
    
    @staticmethod
    def clear(save_log : bool) -> str:
        if (ConsoleHelper.HIDE_LOG_OUTPUT): 
            return None
        try: 
            if (ConsoleHelper.__m_stream is not None): 
                ConsoleHelper.__m_stream.close()
                ConsoleHelper.__m_stream = (None)
        except Exception as ex2703: 
            pass
        ret = None
        try: 
            if (pathlib.Path(ConsoleHelper.get_log_file_name()).is_file()): 
                if (save_log): 
                    fi = pathlib.Path(ConsoleHelper.get_log_file_name())
                    dt = Utils.getDateTimeFromCtime(os.path.getctime(fi.absolute()))
                    ret = ConsoleHelper.__get_dt_file_name(dt)
                    fname = pathlib.PurePath(pathlib.PurePath(ConsoleHelper.get_log_file_name()).parent.absolute()).joinpath(ret)
                    try: 
                        shutil.copy(ConsoleHelper.get_log_file_name(), fname)
                    except Exception as ex2704: 
                        pass
                try: 
                    pathlib.Path(ConsoleHelper.get_log_file_name()).unlink()
                except Exception as ex2705: 
                    pass
                ConsoleHelper.__log_file_length = (0)
            if (ConsoleHelper.REMOVE_LOGS_OLDER_THIS_DAYS > 0): 
                try: 
                    for f in [os.path.abspath(x) for x in os.listdir(os.path.join(pathlib.PurePath(ConsoleHelper.get_log_file_name()).parent.absolute(), ConsoleHelper.get_prefix() + "*.txt")) if os.path.isfile(os.path.join(pathlib.PurePath(ConsoleHelper.get_log_file_name()).parent.absolute(), f))]: 
                        fi = pathlib.Path(f)
                        if ((datetime.datetime.now() - Utils.getDateTimeFromCtime(os.path.getctime(fi.absolute()))).days >= ConsoleHelper.REMOVE_LOGS_OLDER_THIS_DAYS): 
                            fi.unlink()
                except Exception as ex: 
                    pass
        except Exception as ex2706: 
            pass
        return ret
    
    @staticmethod
    def __get_dt_file_name(dt : datetime.datetime) -> str:
        return "{0}{1}{2}{3}{4}{5}.txt".format(ConsoleHelper.__m_prefix, "{:04d}".format(dt.year), "{:02d}".format(dt.month), "{:02d}".format(dt.day), "{:02d}".format(dt.hour), "{:02d}".format(dt.minute))
    
    __m_prefix = "log"
    
    @staticmethod
    def get_prefix() -> str:
        return ConsoleHelper.__m_prefix
    @staticmethod
    def set_prefix(value : str) -> str:
        ConsoleHelper.__m_prefix = value
        ConsoleHelper.__m_log_file_name = (None)
        return value
    
    @staticmethod
    def get_log_file_name() -> str:
        """ Имя файла для лога """
        try: 
            if (ConsoleHelper.__m_log_file_name is None): 
                ConsoleHelper.__m_log_file_name = pathlib.PurePath(ConsoleHelper.get_log_directory()).joinpath(ConsoleHelper.__m_prefix + ".txt")
        except Exception as ex2707: 
            pass
        return ConsoleHelper.__m_log_file_name
    @staticmethod
    def set_log_file_name(value : str) -> str:
        ConsoleHelper.__m_log_file_name = value
        return value
    
    __m_log_file_name = None
    
    M_LOG_DIRECTORY = None
    
    @staticmethod
    def get_log_directory() -> str:
        if (ConsoleHelper.M_LOG_DIRECTORY is not None): 
            return ConsoleHelper.M_LOG_DIRECTORY
        return os.path.dirname(os.path.realpath(__file__))
    @staticmethod
    def set_log_directory(value : str) -> str:
        ConsoleHelper.M_LOG_DIRECTORY = value
        ConsoleHelper.__m_log_file_name = (None)
        return value
    
    __log_file_length = -1
    
    __max_log_file_length = 100000000
    
    MESSAGE_OCCURED = None
    
    @staticmethod
    def write0_(str0_ : str) -> None:
        with ConsoleHelper.__m_lock: 
            ConsoleHelper.__write(str0_)
    
    __m_lock = None
    
    @staticmethod
    def __write(str0_ : str) -> None:
        if (len(ConsoleHelper.MESSAGE_OCCURED) > 0): 
            for iiid in range(len(ConsoleHelper.MESSAGE_OCCURED)): ConsoleHelper.MESSAGE_OCCURED[iiid].call(str0_, None)
        try: 
            if (not ConsoleHelper.get_hide_console_output()): 
                print(str0_, end="", flush=True)
        except Exception as ex2708: 
            pass
        if (ConsoleHelper.HIDE_LOG_OUTPUT): 
            return
        try: 
            if (ConsoleHelper.__log_file_length < (0)): 
                fi = pathlib.Path(ConsoleHelper.get_log_file_name())
                if (not fi.is_file()): 
                    ConsoleHelper.__log_file_length = (0)
                else: 
                    ConsoleHelper.__log_file_length = fi.stat().st_size
            if (ConsoleHelper.__log_file_length > ConsoleHelper.__max_log_file_length): 
                if (not ConsoleHelper.get_hide_console_output()): 
                    print("\r\nLog file too long, it's copied and cleared", end="", flush=True)
                fname = ConsoleHelper.clear(True)
                if (fname is not None): 
                    ConsoleHelper.__write("This log-file is continued, previous part in file {0}\r\n".format(fname))
        except Exception as ex2709: 
            pass
        try: 
            if (ConsoleHelper.__m_stream is None): 
                ConsoleHelper.__m_stream = FileStream(ConsoleHelper.get_log_file_name(), "r+b")
            if (str0_.find('\n') >= 0): 
                dt = datetime.datetime.now()
                date = ""
                if (ConsoleHelper.OUT_DATE): 
                    date = "{0}.{1}.{2} ".format("{:04d}".format(dt.year), "{:02d}".format(dt.month), "{:02d}".format(dt.day))
                time = "\n{0}{1}:{2}:{3} ".format(date, "{:02d}".format(dt.hour), "{:02d}".format(dt.minute), "{:02d}".format(dt.second))
                str0_ = str0_.replace("\n", time)
            dat = str0_.encode("UTF-8", 'ignore')
            ConsoleHelper.__m_stream.position = ConsoleHelper.__m_stream.length
            ConsoleHelper.__m_stream.write(dat, 0, len(dat))
            ConsoleHelper.__m_stream.flush()
            ConsoleHelper.__log_file_length = ConsoleHelper.__m_stream.length
            if (ConsoleHelper.CLOSE_STREAM_AFTER_EACH_WRITE): 
                ConsoleHelper.__m_stream.close()
                ConsoleHelper.__m_stream = (None)
            first = True
            for li in Utils.splitString(str0_, '\n', False): 
                line = li.strip()
                if (Utils.isNullOrEmpty(line)): 
                    first = False
                    continue
                if (first and len(ConsoleHelper.__m_lines) > 0): 
                    ConsoleHelper.__m_lines[len(ConsoleHelper.__m_lines) - 1] += line
                else: 
                    ConsoleHelper.__m_lines.append(line)
                if (len(ConsoleHelper.__m_lines) > ConsoleHelper.__m_max_lines): 
                    del ConsoleHelper.__m_lines[0]
                first = False
        except Exception as ex: 
            pass
    
    __m_stream = None
    
    @staticmethod
    def write_line(str0_ : str) -> None:
        ConsoleHelper.write0_(str0_ + "\r\n")
    
    @staticmethod
    def write_memory(collect : bool=False) -> None:
        if (collect): 
            gc.collect()
    
    __m_lines = None
    
    __m_max_lines = 300
    
    @staticmethod
    def get_last_lines() -> typing.List[str]:
        """ Получить последние строки из лога
        
        """
        with ConsoleHelper.__m_lock: 
            return list(ConsoleHelper.__m_lines)
    
    # static constructor for class ConsoleHelper
    @staticmethod
    def _static_ctor():
        ConsoleHelper.MESSAGE_OCCURED = list()
        ConsoleHelper.__m_lock = threading.Lock()
        ConsoleHelper.__m_lines = list()

ConsoleHelper._static_ctor()